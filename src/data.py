"""Carga de los datos del BAF."""
import pandas as pd

from src.config import resolve_path


def load_data(config, filename="Base.csv"):
    """Carga un CSV del BAF y lo devuelve como DataFrame."""
    path = resolve_path(config["data_dir"]) / filename
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    from src.config import load_config

    config = load_config("configs/local.yaml")
    df = load_data(config)

    # 1. Filas y columnas
    print(df.shape)
    # 2. Porcentaje de fraude
    print(f"{df['fraud_bool'].mean()}")
    # 3. Filas por mes
    print(df["month"].value_counts().sort_index())
