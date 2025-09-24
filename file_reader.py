import os
import pandas as pd
from typing import Optional
import chardet


MAX_SAMPLE_ROWS = 50000
DEFAULT_MAX_COLUMNS = 512


class FileReader:
    """Main class for reading CSV and Excel files with automatic type detection."""

    @staticmethod
    def detect_file_type(file_path: str) -> str:
        """Detect file type based on extension."""
        _, ext = os.path.splitext(file_path.lower())
        if ext == '.csv':
            return 'csv'
        elif ext == '.xlsx':
            return 'excel'
        else:
            raise ValueError(f"Unsupported file type: {ext}. Supported: .csv, .xlsx")

    @staticmethod
    def read_file(file_path: str,
                  delimiter: str = ',',
                  encoding: Optional[str] = None,
                  sheet_name: Optional[str] = None,
                  sample_size: Optional[int] = None,
                  max_columns: Optional[int] = None) -> pd.DataFrame:
        """
        Read CSV or Excel file and return DataFrame.

        Args:
            file_path: Path to the file
            delimiter: CSV delimiter (ignored for Excel)
            encoding: File encoding (auto-detected for CSV if None)
            sheet_name: Excel sheet name (uses first sheet if None)
            sample_size: Number of rows to read (None for all)

        Returns:
            pandas DataFrame with the file data
        """
        file_type = FileReader.detect_file_type(file_path)

        bounded_sample = FileReader._sanitize_sample_size(sample_size)

        if file_type == 'csv':
            df = FileReader._read_csv(file_path, delimiter, encoding, bounded_sample)
        elif file_type == 'excel':
            df = FileReader._read_excel(file_path, sheet_name, bounded_sample)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        FileReader._validate_column_count(df, max_columns)
        return df

    @staticmethod
    def _read_csv(file_path: str,
                  delimiter: str = ',',
                  encoding: Optional[str] = None,
                  sample_size: Optional[int] = None) -> pd.DataFrame:
        """Read CSV file with encoding detection."""
        if encoding is None:
            # Auto-detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)  # Read first 10KB for detection
                detected = chardet.detect(raw_data)
                encoding = detected.get('encoding', 'utf-8')

        # Read CSV
        nrows = sample_size if sample_size else None
        df = pd.read_csv(file_path,
                        delimiter=delimiter,
                        encoding=encoding,
                        nrows=nrows)
        return df

    @staticmethod
    def _read_excel(file_path: str,
                    sheet_name: Optional[str] = None,
                    sample_size: Optional[int] = None) -> pd.DataFrame:
        """Read Excel file."""
        # Read Excel
        nrows = sample_size if sample_size else None

        if sheet_name is None:
            # Read first sheet
            df = pd.read_excel(file_path, nrows=nrows)
        else:
            df = pd.read_excel(file_path,
                              sheet_name=sheet_name,
                              nrows=nrows)
        return df

    @staticmethod
    def _sanitize_sample_size(sample_size: Optional[int]) -> Optional[int]:
        """Clamp requested sample size to prevent excessive memory usage."""
        if sample_size is None:
            return None

        if sample_size <= 0:
            raise ValueError("sample_size must be positive when provided")

        return min(sample_size, MAX_SAMPLE_ROWS)

    @staticmethod
    def _validate_column_count(df: pd.DataFrame, max_columns: Optional[int]) -> None:
        """Ensure the dataframe does not exceed the allowed column count."""
        limit = max_columns if max_columns is not None else DEFAULT_MAX_COLUMNS
        column_count = len(df.columns)
        if column_count > limit:
            raise ValueError(
                f"File contains {column_count} columns which exceeds the allowed maximum of {limit}."
            )
