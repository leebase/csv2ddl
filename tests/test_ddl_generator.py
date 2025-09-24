from ddl_generator import DDLGenerator


def test_generate_ddl_sanitizes_and_uniquifies_columns():
    generator = DDLGenerator("snowflake")
    column_types = {
        "Order Date": "DATE",
        "order date": "DATE",
        "Select": "VARCHAR(10)"
    }

    ddl = generator.generate_ddl("Orders", column_types)

    assert "Order_Date DATE" in ddl
    assert "order_date_1 DATE" in ddl
    assert "Select_col VARCHAR(10)" in ddl
    assert "__" not in ddl
