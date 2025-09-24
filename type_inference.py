import logging
import pandas as pd
from dateutil.parser import parse as date_parse
from typing import Dict, Any


logger = logging.getLogger(__name__)


class TypeInferrer:
    """Engine for inferring data types from DataFrame columns."""

    DATE_FORMATS = [
        '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d',
        '%d-%m-%Y', '%m-%d-%Y', '%Y%m%d', '%d/%m/%y'
    ]

    def __init__(self, date_formats: list = None):
        self.date_formats = date_formats or self.DATE_FORMATS

    def infer_types(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Infer types for all columns in DataFrame.

        Returns:
            Dict with column names as keys and type info as values
        """
        results = {}
        logger.debug("Inferring types for %s columns", len(df.columns))
        for col in df.columns:
            logger.debug("Analyzing column '%s'", col)
            inferred = self._infer_column_type(df[col])
            logger.debug("Column '%s' inferred as %s", col, inferred['snowflake_type'])
            results[col] = inferred
        return results

    def _infer_column_type(self, series: pd.Series) -> Dict[str, Any]:
        """Infer type for a single column."""
        # Remove nulls for analysis
        non_null = series.dropna()

        if len(non_null) == 0:
            # All nulls - default to string
            logger.debug("Column empty after dropping nulls; defaulting to VARCHAR(1)")
            return {
                'inferred_type': 'string',
                'snowflake_type': 'VARCHAR(1)',
                'parameters': {'max_length': 1},
                'confidence': 0.5
            }

        # Check for boolean-like values
        if self._is_boolean_column(non_null):
            logger.debug("Column detected as boolean-like; treating as VARCHAR(5)")
            return {
                'inferred_type': 'string',  # Treat as string for compatibility
                'snowflake_type': 'VARCHAR(5)',
                'parameters': {'max_length': 5},
                'confidence': 0.9
            }

        # First, try numeric detection (most restrictive)
        numeric_info = self._analyze_numeric(non_null)
        if numeric_info:
            return numeric_info

        # Then try date detection
        if self._is_date_column(non_null):
            logger.debug("Column detected as date")
            return {
                'inferred_type': 'date',
                'snowflake_type': 'DATE',
                'parameters': {},
                'confidence': 0.9
            }

        # Default to string
        string_info = self._analyze_string(non_null)
        return string_info

    def _is_date_column(self, series: pd.Series) -> bool:
        """Check if column contains dates."""
        sample_size = min(100, len(series))  # Sample up to 100 values
        sample = series.sample(sample_size) if len(series) > sample_size else series

        date_count = 0
        for value in sample:
            if self._is_date_value(str(value)):
                date_count += 1

        # Consider it a date column if >80% of sampled values are dates
        return date_count / len(sample) > 0.8

    def _is_date_value(self, value: str) -> bool:
        """Check if a single value is a date."""
        try:
            # Try parsing with dateutil
            date_parse(value, fuzzy=False)
            return True
        except (ValueError, TypeError):
            return False

    def _is_boolean_column(self, series: pd.Series) -> bool:
        """Check if column contains boolean values."""
        # Convert to string and check for boolean representations
        str_series = series.astype(str).str.lower()
        boolean_values = {'true', 'false', '1', '0', 'yes', 'no', 'y', 'n'}

        # Check if all non-null values are boolean-like
        non_null_str = str_series.dropna()
        if len(non_null_str) == 0:
            return False

        boolean_count = 0
        for value in non_null_str:
            if value in boolean_values:
                boolean_count += 1

        # Consider boolean if >90% are boolean-like
        return boolean_count / len(non_null_str) > 0.9

    def _analyze_numeric(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze if column is numeric and determine precision/scale."""
        # Try to convert to numeric
        try:
            numeric_series = pd.to_numeric(series, errors='coerce')
            numeric_series = numeric_series.dropna()

            if len(numeric_series) / len(series) < 0.8:
                # Less than 80% numeric - not a numeric column
                logger.debug("Column rejected for numeric inference (<80%% numeric)")
                return None

            # Check if integers or floats
            is_integer = all(numeric_series == numeric_series.astype(int))

            if is_integer:
                # Integer column
                max_val = int(numeric_series.max())
                min_val = int(numeric_series.min())

                # Calculate precision (digits needed)
                precision = max(len(str(abs(max_val))), len(str(abs(min_val))))
                if min_val < 0:
                    precision += 1  # For negative sign

                logger.debug(
                    "Detected integer column with bounds (%s, %s) and precision %s",
                    min_val,
                    max_val,
                    precision
                )
                return {
                    'inferred_type': 'integer',
                    'snowflake_type': f'NUMBER({precision}, 0)',
                    'parameters': {'precision': precision, 'scale': 0},
                    'confidence': 0.95
                }
            else:
                # Float column
                # Calculate precision and scale
                str_values = [str(abs(x)) for x in numeric_series]
                max_digits_before = 0
                max_digits_after = 0

                for val_str in str_values:
                    if '.' in val_str:
                        before, after = val_str.split('.')
                        max_digits_before = max(max_digits_before, len(before))
                        max_digits_after = max(max_digits_after, len(after))
                    else:
                        max_digits_before = max(max_digits_before, len(val_str))

                precision = max_digits_before + max_digits_after
                scale = max_digits_after

                # Add padding
                precision = min(precision + 2, 38)  # Snowflake max precision
                scale = min(scale + 1, 37)

                logger.debug(
                    "Detected float column with precision %s and scale %s",
                    precision,
                    scale
                )
                return {
                    'inferred_type': 'float',
                    'snowflake_type': f'NUMBER({precision}, {scale})',
                    'parameters': {'precision': precision, 'scale': scale},
                    'confidence': 0.95
                }

        except (ValueError, TypeError):
            return None

    def _analyze_string(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze string column and determine max length."""
        str_series = series.astype(str)
        max_length = str_series.str.len().max()

        # Add padding for future growth (20% or at least 10 chars)
        padded_length = int(max_length * 1.2) + 10
        logger.debug(
            "Detected string column with max length %s -> padded length %s",
            max_length,
            padded_length
        )

        return {
            'inferred_type': 'string',
            'snowflake_type': f'VARCHAR({padded_length})',
            'parameters': {'max_length': padded_length},
            'confidence': 0.9
        }
