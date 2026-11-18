"""Carga de los datos del BAF."""
import numpy as np
import pandas as pd

from src.config import resolve_path

# Partición temporal fija del proyecto (ver CLAUDE.md)
TRAIN_MONTHS = [0, 1, 2, 3, 4]
VAL_MONTHS = [5]
TEST_MONTHS = [6, 7]

# Variables cuyos ausentes vienen codificados como -1 (ver docs/datos.md)
MISSING_AS_MINUS_ONE = [
    "prev_address_months_count",
    "current_address_months_count",
    "bank_months_count",
    "session_length_in_minutes",
    "device_distinct_emails_8w",
]

# Variables en las que cualquier valor negativo es ausente (ver docs/datos.md)
MISSING_AS_NEGATIVE = ["intended_balcon_amount"]


def load_data(config, filename="Base.csv"):
    """Carga un CSV del BAF y lo devuelve como DataFrame."""
    path = resolve_path(config["data_dir"]) / filename
    df = pd.read_csv(path)
    return df


def missing_to_nan(df):
    """Devuelve una copia de df con los ausentes documentados convertidos a NaN."""
    df = df.copy()
    df[MISSING_AS_MINUS_ONE] = df[MISSING_AS_MINUS_ONE].replace(-1, np.nan)
    df[MISSING_AS_NEGATIVE] = df[MISSING_AS_NEGATIVE].where(df[MISSING_AS_NEGATIVE] >= 0)
    return df


def split_by_month(df):
    """Divide df en train, val y test según la columna `month`."""
    train = df[df["month"].isin(TRAIN_MONTHS)]
    val = df[df["month"].isin(VAL_MONTHS)]
    test = df[df["month"].isin(TEST_MONTHS)]
    assert len(train) + len(val) + len(test) == len(df), "Hay filas sin partición o en dos a la vez"
    return train, val, test
