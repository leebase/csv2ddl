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


def test_unsupported_dialect_raises():
    with pytest.raises(ValueError):
        DialectMapper("postgres")
