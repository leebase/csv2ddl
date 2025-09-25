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


def test_unsupported_dialect_raises():
    with pytest.raises(ValueError):
        DialectMapper("oracle")
