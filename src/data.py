"""Carga de los datos del BAF."""
import pandas as pd

from src.config import resolve_path


def load_data(config, filename="Base.csv"):
    """Carga un CSV del BAF y lo devuelve como DataFrame."""
    path = resolve_path(config["data_dir"]) / filename
    df = pd.read_csv(path)
    return df





    
