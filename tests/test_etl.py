from etl.utils import RAW_FILE

def test_raw_file_exists():
    assert RAW_FILE.exists()
