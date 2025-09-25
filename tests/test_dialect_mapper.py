import pytest

from dialect_mapper import DialectMapper


def test_map_snowflake_types():
    type_info = {
        "amount": {
            "inferred_type": "integer",
            "parameters": {"precision": 5, "scale": 0}
        }
    }

    mapper = DialectMapper("snowflake")
    mapped = mapper.map_column_types(type_info)

    assert mapped["amount"] == "NUMBER(5, 0)"


def test_map_sqlite_types():
    type_info = {
        "description": {
            "inferred_type": "string",
            "parameters": {"max_length": 50}
        }
    }

    mapper = DialectMapper("sqlite")
    mapped = mapper.map_column_types(type_info)

    assert mapped["description"] == "TEXT"


def test_map_postgres_integer():
    type_info = {
        "order_id": {
            "inferred_type": "integer",
            "parameters": {"precision": 12, "scale": 0}
        }
    }

    mapper = DialectMapper("postgres")
    mapped = mapper.map_column_types(type_info)

    assert mapped["order_id"] == "BIGINT"


def test_map_mysql_string_to_text():
    type_info = {
        "notes": {
            "inferred_type": "string",
            "parameters": {"max_length": 70000}
        }
    }

    mapper = DialectMapper("mysql")
    mapped = mapper.map_column_types(type_info)

    assert mapped["notes"] == "TEXT"


def test_map_oracle_string_to_clob():
    type_info = {
        "payload": {
            "inferred_type": "string",
            "parameters": {"max_length": 8000}
        }
    }

    mapper = DialectMapper("oracle")
    mapped = mapper.map_column_types(type_info)

    assert mapped["payload"] == "CLOB"


def test_map_oracle_float_precision_cap():
    type_info = {
        "amount": {
            "inferred_type": "float",
            "parameters": {"precision": 45, "scale": 6}
        }
    }

    mapper = DialectMapper("oracle")
    mapped = mapper.map_column_types(type_info)

    assert mapped["amount"] == "NUMBER"


def test_map_sqlserver_float_to_decimal():
    type_info = {
        "ratio": {
            "inferred_type": "float",
            "parameters": {"precision": 20, "scale": 8}
        }
    }

    mapper = DialectMapper("sqlserver")
    mapped = mapper.map_column_types(type_info)

    assert mapped["ratio"] == "DECIMAL(20, 8)"


def test_map_sqlserver_string_to_nvarchar_max():
    type_info = {
        "comment": {
            "inferred_type": "string",
            "parameters": {"max_length": 6000}
        }
    }

    mapper = DialectMapper("sqlserver")
    mapped = mapper.map_column_types(type_info)

    assert mapped["comment"] == "NVARCHAR(MAX)"


def test_map_databricks_integer_large_precision():
    type_info = {
        "identifier": {
            "inferred_type": "integer",
            "parameters": {"precision": 25, "scale": 0}
        }
    }

    mapper = DialectMapper("databricks")
    mapped = mapper.map_column_types(type_info)

    assert mapped["identifier"] == "DECIMAL(25, 0)"


def test_map_databricks_string_overflow_to_string():
    type_info = {
        "payload": {
            "inferred_type": "string",
            "parameters": {"max_length": 100000}
        }
    }

    mapper = DialectMapper("databricks")
    mapped = mapper.map_column_types(type_info)

    assert mapped["payload"] == "STRING"


def test_unsupported_dialect_raises():
    with pytest.raises(ValueError):
        DialectMapper("teradata")
