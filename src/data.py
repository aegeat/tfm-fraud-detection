"""Carga de los datos del BAF."""
import pandas as pd

from src.config import resolve_path


MISSING_AS_MINUS_ONE = [
    "prev_address_months_count",
    "current_address_months_count",
    "bank_months_count",
    "session_length_in_minutes",
    "device_distinct_emails_8w",
]
    

def load_data(config, filename="Base.csv"):
    """Carga un CSV del BAF y lo devuelve como DataFrame."""
    path = resolve_path(config["data_dir"]) / filename
    df = pd.read_csv(path)
    return df




