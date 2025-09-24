from typing import Dict, Any
from abc import ABC, abstractmethod


class Dialect(ABC):
    """Abstract base class for SQL dialects."""

    @abstractmethod
    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        """Map inferred type to dialect-specific SQL type."""
        pass


class SnowflakeDialect(Dialect):
    """Snowflake SQL dialect mapper."""

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'DATE'
        elif inferred_type == 'integer':
            precision = params.get('precision', 10)
            return f'NUMBER({precision}, 0)'
        elif inferred_type == 'float':
            precision = params.get('precision', 10)
            scale = params.get('scale', 2)
            return f'NUMBER({precision}, {scale})'
        elif inferred_type == 'string':
            max_length = params.get('max_length', 255)
            return f'VARCHAR({max_length})'
        else:
            # Default fallback
            return 'VARCHAR(255)'


class SQLiteDialect(Dialect):
    """SQLite SQL dialect mapper."""

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'TEXT'  # SQLite stores dates as TEXT
        elif inferred_type == 'integer':
            return 'INTEGER'
        elif inferred_type == 'float':
            return 'REAL'
        elif inferred_type == 'string':
            return 'TEXT'
        else:
            # Default fallback
            return 'TEXT'


class DialectMapper:
    """Maps inferred types to SQL dialect types."""

    DIALECTS = {
        'snowflake': SnowflakeDialect,
        'sqlite': SQLiteDialect
    }

    def __init__(self, dialect_name: str = 'snowflake'):
        if dialect_name not in self.DIALECTS:
            raise ValueError(f"Unsupported dialect: {dialect_name}. Supported: {list(self.DIALECTS.keys())}")

        self.dialect = self.DIALECTS[dialect_name]()

    def map_column_types(self, type_info: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Map all columns to dialect-specific types.

        Args:
            type_info: Dict from TypeInferrer.infer_types()

        Returns:
            Dict with column names as keys and SQL types as values
        """
        mapped = {}
        for col_name, info in type_info.items():
            inferred_type = info['inferred_type']
            params = info.get('parameters', {})
            mapped[col_name] = self.dialect.map_type(inferred_type, params)
        return mapped

    @staticmethod
    def get_supported_dialects() -> list:
        """Get list of supported dialect names."""
        return list(DialectMapper.DIALECTS.keys())