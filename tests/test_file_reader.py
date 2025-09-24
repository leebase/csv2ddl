import pandas as pd

from file_reader import FileReader


def test_read_csv(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("id,name\n1,Alpha\n", encoding="utf-8")

    df = FileReader.read_file(str(csv_path))

    assert list(df.columns) == ["id", "name"]
    assert df.iloc[0]["name"] == "Alpha"


def test_read_excel(tmp_path):
    df_in = pd.DataFrame({"id": [1, 2], "value": ["A", "B"]})
    xlsx_path = tmp_path / "sample.xlsx"
    df_in.to_excel(xlsx_path, index=False)

    df = FileReader.read_file(str(xlsx_path))

    assert list(df.columns) == ["id", "value"]
    assert df.iloc[1]["value"] == "B"


def test_read_csv_with_encoding_detection(tmp_path):
    csv_path = tmp_path / "latin.csv"
    csv_path.write_text("id;name\n1;José\n", encoding="latin-1")

    df = FileReader.read_file(str(csv_path), delimiter=";")

    assert df.iloc[0]["name"] == "José"
