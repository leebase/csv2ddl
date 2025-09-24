import pandas as pd

from type_inference import TypeInferrer


def test_infer_integer_column():
    df = pd.DataFrame({"amount": [1, 2, 3]})

    result = TypeInferrer().infer_types(df)

    assert result["amount"]["inferred_type"] == "integer"
    assert "NUMBER" in result["amount"]["snowflake_type"]


def test_infer_string_for_mixed_values():
    df = pd.DataFrame({"notes": ["1", "two", None]})

    result = TypeInferrer().infer_types(df)

    assert result["notes"]["inferred_type"] == "string"
    assert "VARCHAR" in result["notes"]["snowflake_type"]


def test_infer_date_column():
    df = pd.DataFrame({"created": ["2024-01-01", "2024-02-01", "2024-03-01"]})

    result = TypeInferrer().infer_types(df)

    assert result["created"]["inferred_type"] == "date"
    assert result["created"]["snowflake_type"] == "DATE"
