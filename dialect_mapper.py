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


class PostgresDialect(Dialect):
    """PostgreSQL SQL dialect mapper."""

    SMALLINT_PRECISION = 4
    INTEGER_PRECISION = 9
    BIGINT_PRECISION = 18

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'DATE'
        if inferred_type == 'integer':
            precision = params.get('precision', 10)
            if precision <= self.SMALLINT_PRECISION:
                return 'SMALLINT'
            if precision <= self.INTEGER_PRECISION:
                return 'INTEGER'
            if precision <= self.BIGINT_PRECISION:
                return 'BIGINT'
            return f'NUMERIC({precision}, 0)'
        if inferred_type == 'float':
            precision = params.get('precision', 18)
            scale = params.get('scale', 6)
            precision = max(scale + 1, min(precision, 1000))
            scale = min(scale, precision - 1)
            return f'NUMERIC({precision}, {scale})'
        if inferred_type == 'string':
            max_length = params.get('max_length', 255)
            if max_length > 10485760:  # 10 MB upper bound for practical varchar sizing
                return 'TEXT'
            return f'VARCHAR({max_length})'
        return 'TEXT'


class MySQLDialect(Dialect):
    """MySQL SQL dialect mapper."""

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'DATE'
        if inferred_type == 'integer':
            precision = params.get('precision', 10)
            if precision <= 3:
                return 'TINYINT'
            if precision <= 5:
                return 'SMALLINT'
            if precision <= 7:
                return 'MEDIUMINT'
            if precision <= 10:
                return 'INT'
            if precision <= 19:
                return 'BIGINT'
            return f'DECIMAL({precision}, 0)'
        if inferred_type == 'float':
            precision = params.get('precision', 18)
            scale = params.get('scale', 6)
            precision = max(scale + 1, min(precision, 65))
            scale = min(scale, 30)
            if scale >= precision:
                precision = scale + 1
            return f'DECIMAL({precision}, {scale})'
        if inferred_type == 'string':
            max_length = params.get('max_length', 255)
            if max_length > 65535:
                return 'TEXT'
            return f'VARCHAR({max_length})'
        return 'TEXT'


class OracleDialect(Dialect):
    """Oracle SQL dialect mapper."""

    MAX_NUMERIC_PRECISION = 38
    MAX_VARCHAR_LENGTH = 4000

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'DATE'
        if inferred_type == 'integer':
            precision = max(1, params.get('precision', 10))
            if precision > self.MAX_NUMERIC_PRECISION:
                return 'NUMBER'
            return f'NUMBER({precision}, 0)'
        if inferred_type == 'float':
            requested_precision = max(1, params.get('precision', 18))
            scale = max(0, params.get('scale', 6))
            precision = max(scale + 1, min(requested_precision, self.MAX_NUMERIC_PRECISION))
            scale = min(scale, precision - 1)
            if requested_precision > self.MAX_NUMERIC_PRECISION:
                return 'NUMBER'
            return f'NUMBER({precision}, {scale})'
        if inferred_type == 'string':
            max_length = max(1, params.get('max_length', 255))
            if max_length > self.MAX_VARCHAR_LENGTH:
                return 'CLOB'
            return f'VARCHAR2({max_length})'
        return 'VARCHAR2(255)'


class SQLServerDialect(Dialect):
    """SQL Server dialect mapper."""

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'DATE'
        if inferred_type == 'integer':
            precision = max(1, params.get('precision', 10))
            if precision <= 3:
                return 'TINYINT'
            if precision <= 5:
                return 'SMALLINT'
            if precision <= 10:
                return 'INT'
            if precision <= 19:
                return 'BIGINT'
            return f'DECIMAL({min(precision, 38)}, 0)'
        if inferred_type == 'float':
            precision = max(1, params.get('precision', 18))
            scale = max(0, params.get('scale', 6))
            precision = max(scale + 1, min(precision, 38))
            scale = min(scale, precision - 1)
            return f'DECIMAL({precision}, {scale})'
        if inferred_type == 'string':
            max_length = max(1, params.get('max_length', 255))
            if max_length > 4000:
                return 'NVARCHAR(MAX)'
            return f'NVARCHAR({max_length})'
        return 'NVARCHAR(MAX)'


class DatabricksDialect(Dialect):
    """Databricks (Spark SQL) dialect mapper."""

    def map_type(self, inferred_type: str, params: Dict[str, Any]) -> str:
        if inferred_type == 'date':
            return 'DATE'
        if inferred_type == 'integer':
            precision = max(1, params.get('precision', 10))
            if precision <= 3:
                return 'TINYINT'
            if precision <= 5:
                return 'SMALLINT'
            if precision <= 9:
                return 'INT'
            if precision <= 18:
                return 'BIGINT'
            return f'DECIMAL({min(precision, 38)}, 0)'
        if inferred_type == 'float':
            precision = max(1, params.get('precision', 18))
            scale = max(0, params.get('scale', 6))
            precision = max(scale + 1, min(precision, 38))
            scale = min(scale, precision - 1)
            return f'DECIMAL({precision}, {scale})'
        if inferred_type == 'string':
            max_length = max(1, params.get('max_length', 255))
            if max_length > 65535:
                return 'STRING'
            return f'VARCHAR({max_length})'
        return 'STRING'


class DialectMapper:
    """Maps inferred types to SQL dialect types."""

    DIALECTS = {
        'snowflake': SnowflakeDialect,
        'sqlite': SQLiteDialect,
        'postgres': PostgresDialect,
        'mysql': MySQLDialect,
        'oracle': OracleDialect,
        'sqlserver': SQLServerDialect,
        'databricks': DatabricksDialect,
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
