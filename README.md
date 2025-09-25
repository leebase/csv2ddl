# CSV to SQL DDL Converter

![CI](https://github.com/leebase/csv2ddl/actions/workflows/ci.yml/badge.svg)

A Python tool that analyzes CSV files and generates optimized DDL statements for creating tables in various SQL databases. Currently supports Snowflake, SQLite, Postgres, and MySQL dialects, with an extensible architecture for adding more databases.

## Features

- **Multiple File Formats**: Supports CSV and Excel files (.csv, .xlsx)
- **Automatic Type Inference**: Intelligently detects dates, numbers, and strings from data
- **Optimal Sizing**: Calculates appropriate column sizes based on actual data content
- **Multiple SQL Dialects**: Generate DDL for Snowflake, SQLite, Postgres, and MySQL, and easily add more
- **Safe Identifiers**: Sanitizes table and column names, handling spaces, special characters, and reserved keywords (e.g., `date` → `Date_dt`) automatically while guaranteeing uniqueness.
- **Configurable Sampling**: Analyze large files efficiently without loading everything into memory
- **Command-Line Interface**: Simple to use from the terminal
- **Snowflake Stored Procedure Ready**: Designed for easy integration with Snowflake Python UDFs

## Installation

### From source (editable)
```bash
git clone <repository-url>
cd csv2ddl
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Install as a package
```bash
pip install .               # from the project root
# include developer tooling (pytest, ruff)
pip install .[dev]
```

After installation you can invoke the CLI with the `csv2ddl` command instead of `python csv2ddl.py`.

## Usage

### Basic Usage
```bash
csv2ddl path/to/your/file.csv
csv2ddl path/to/your/file.xlsx
```

### Specify SQL Dialect
```bash
csv2ddl --dialect snowflake path/to/file.csv
csv2ddl --dialect sqlite path/to/file.csv
csv2ddl --dialect postgres path/to/file.csv
csv2ddl --dialect mysql path/to/file.csv
```

### Advanced Options
```bash
csv2ddl \
  --dialect snowflake \
  --sample-size 5000 \
  --output ddl.sql \
  --max-columns 256 \
  --table-name my_custom_table \
  path/to/file.csv
```

### Options
- `--dialect`: SQL dialect (snowflake, sqlite, postgres, mysql) - default: snowflake
- `--sample-size`: Number of rows to sample for type inference - default: 1000
- `--output`: Output file path (optional, prints to stdout if not specified)
- `--table-name`: Custom table name (optional, uses filename if not specified)
- `--delimiter`: CSV delimiter - default: ','
- `--encoding`: File encoding - default: auto-detect
- `--sheet-name`: Excel sheet name to read (optional, uses first sheet if not specified)
- `--max-columns`: Maximum allowed column count before aborting (default: 512)
- `--allow-outside-output`: Permit writing files outside the working directory (requires explicit opt-in)

> `--sample-size` is internally capped at 50,000 rows to keep memory usage predictable.

## Testing

Install developer tooling and run the suite:

```bash
pip install ".[dev]"
pytest
```

The tests cover file loading, type inference for common and mixed data, dialect mappings, and identifier sanitization edge cases.

## Examples

### Quick workflow

```bash
csv2ddl sample_data.csv --dialect snowflake --output sample_snowflake.sql
csv2ddl sample_data.csv --dialect sqlite --output sample_sqlite.sql
csv2ddl sample_data.csv --dialect postgres --output sample_postgres.sql
csv2ddl sample_data.csv --dialect mysql --output sample_mysql.sql
cat sample_snowflake.sql
cat sample_sqlite.sql
cat sample_postgres.sql
cat sample_mysql.sql
```

### Input CSV (sample_data.csv)
```csv
id,name,created_date,revenue,active
1,John Doe,2023-01-15,1234.56,true
2,Jane Smith,2023-02-20,5678.90,false
3,Bob Johnson,2023-03-10,999.99,true
```

### Generated Snowflake DDL
```sql
CREATE TABLE sample_data (
    id NUMBER(1, 0),
    name VARCHAR(11),
    created_date DATE,
    revenue NUMBER(6, 2),
    active VARCHAR(5)
);
```

### Generated SQLite DDL
```sql
CREATE TABLE sample_data (
    id INTEGER,
    name TEXT,
    created_date TEXT,
    revenue REAL,
    active TEXT
);
```

## Type Inference Rules

### Date Recognition
- Recognizes common formats: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY
- Falls back to string if date parsing fails

### Numeric Types
- **Integers**: Whole numbers → NUMBER(precision, 0) or INTEGER
- **Floats**: Decimal numbers → NUMBER(precision, scale) or REAL
- Precision and scale calculated from actual data range

### String Types
- **Snowflake**: VARCHAR(max_length) with padding for future growth
- **SQLite**: TEXT for all strings

### Null Handling
- Columns with NULL values are still typed based on non-null values
- Mixed types default to string representation

## Architecture

The tool consists of several key components:

1. **CSV Reader**: Handles file reading with encoding detection
2. **Type Inference Engine**: Analyzes sampled data to determine optimal types
3. **Dialect Mapper**: Maps inferred types to SQL dialect-specific syntax
4. **DDL Generator**: Constructs the final CREATE TABLE statement

See [architecture.md](architecture.md) for detailed technical documentation.

## Adding New SQL Dialects

To add support for a new database:

1. Create a new dialect class (either alongside the existing ones in `dialect_mapper.py` or in a new module).
2. Implement the `Dialect` interface with type mappings tailored to your database.
3. Register the dialect name and class in `DialectMapper.DIALECTS` so the CLI can discover it.
4. Add tests that exercise the new dialect's mappings.

Example dialect implementation:
```python
class MyDatabaseDialect(Dialect):
    def map_type(self, inferred_type, params):
        # Your type mapping logic here
        pass
```

## Snowflake Stored Procedure Usage

The tool is designed to be easily integrated into Snowflake Python stored procedures:

```python
import csv2ddl

def generate_ddl(file_path: str, dialect: str = 'snowflake') -> str:
    # Implementation using the csv2ddl modules
    pass
```

## Limitations

- Assumes CSV has headers in the first row
- Sampling-based inference may miss edge cases in very large files
- No support for complex data types (arrays, objects, etc.)
- Limited to basic CREATE TABLE statements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For issues and questions, please [create an issue](link-to-issues) or contact the maintainers.
