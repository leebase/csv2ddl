from typing import Dict
import re


COMMON_RESERVED_WORDS = {
    'add', 'all', 'alter', 'and', 'any', 'as', 'asc', 'between', 'by',
    'case', 'check', 'column', 'create', 'current', 'default',
    'delete', 'desc', 'distinct', 'drop', 'else', 'exists', 'from',
    'group', 'having', 'in', 'index', 'insert', 'into', 'join', 'like',
    'not', 'null', 'on', 'or', 'order', 'primary', 'select', 'table',
    'then', 'union', 'unique', 'update', 'using', 'values', 'view', 'when',
    'where'
}

DIALECT_RESERVED_WORDS = {
    'snowflake': COMMON_RESERVED_WORDS | {'date', 'timestamp', 'variant'},
    'sqlite': COMMON_RESERVED_WORDS | {
        'abort', 'after', 'analyze', 'attach', 'before', 'begin', 'commit',
        'conflict', 'detach', 'each', 'exclusive', 'explain', 'fail', 'for',
        'if', 'ignore', 'immediate', 'indexed', 'instead', 'isnull', 'limit',
        'offset', 'plan', 'pragma', 'raise', 'regexp', 'reindex', 'release',
        'replace', 'restrict', 'rollback', 'rowid', 'vacuum'
    }
}


class DDLGenerator:
    """Generates CREATE TABLE DDL statements for different SQL dialects."""

    def __init__(self, dialect: str = 'snowflake'):
        self.dialect = dialect.lower()
        self.reserved_words = DIALECT_RESERVED_WORDS.get(
            self.dialect,
            COMMON_RESERVED_WORDS
        )

    def generate_ddl(self,
                    table_name: str,
                    column_types: Dict[str, str],
                    if_not_exists: bool = True) -> str:
        """
        Generate CREATE TABLE DDL statement.

        Args:
            table_name: Name of the table
            column_types: Dict of column_name -> sql_type
            if_not_exists: Whether to include IF NOT EXISTS clause

        Returns:
            Complete CREATE TABLE statement
        """
        # Sanitize table name
        table_name = self._sanitize_identifier(table_name)

        # Build column definitions
        columns = []
        used_names = set()
        used_normalized = set()
        for col_name, col_type in column_types.items():
            sanitized_name = self._sanitize_identifier(col_name)
            sanitized_name = self._avoid_reserved_word(sanitized_name)
            unique_name = self._make_unique_identifier(sanitized_name, used_names, used_normalized)
            used_names.add(unique_name)
            used_normalized.add(self._normalize_identifier(unique_name))
            columns.append(f"    {unique_name} {col_type}")

        columns_str = ",\n".join(columns)

        # Build DDL
        if_not_exists_clause = "IF NOT EXISTS " if if_not_exists else ""
        ddl = f"CREATE TABLE {if_not_exists_clause}{table_name} (\n{columns_str}\n);"

        return ddl

    def _sanitize_identifier(self, identifier: str) -> str:
        """Sanitize column/table names for SQL."""
        # Remove invalid characters, replace with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', identifier)

        # Remove trailing underscores introduced by replacement
        sanitized = sanitized.rstrip('_')

        # Ensure starts with letter or underscore
        if sanitized and sanitized[0].isdigit():
            sanitized = f"col_{sanitized}"

        # Ensure not empty
        if not sanitized:
            sanitized = "column"

        return sanitized

    def _avoid_reserved_word(self, identifier: str) -> str:
        """Adjust identifier if it matches a reserved SQL keyword."""
        lower = identifier.lower()
        if lower in self.reserved_words:
            if lower == 'date':
                return f"{identifier}_dt"
            return f"{identifier}_col"
        return identifier

    def _make_unique_identifier(self, base_name: str, existing: set, existing_normalized: set) -> str:
        """Ensure identifier is unique within the current statement."""
        normalized = self._normalize_identifier(base_name)
        if base_name not in existing and normalized not in existing_normalized:
            return base_name

        suffix = 1
        candidate = f"{base_name}_{suffix}"
        normalized_candidate = self._normalize_identifier(candidate)
        while candidate in existing or normalized_candidate in existing_normalized:
            suffix += 1
            candidate = f"{base_name}_{suffix}"
            normalized_candidate = self._normalize_identifier(candidate)

        return candidate

    @staticmethod
    def _normalize_identifier(identifier: str) -> str:
        """Return a case-insensitive canonical form for uniqueness checks."""
        return identifier.lower()
