import yaml
import psycopg2

def load_config():
    with open("etl/config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
db_cfg = config["database"]

def get_connection():
    conn = psycopg2.connect(
        host=db_cfg["host"],
        port=db_cfg["port"],
        user=db_cfg["user"],
        password=db_cfg["password"],
        database=db_cfg["name"]
    )
    return conn

def get_cursor():
    conn = get_connection()
    return conn.cursor()
