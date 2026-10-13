"""Carga de la configuración del proyecto desde archivos YAML."""

import yaml


def load_config(path):
    """Lee un archivo YAML y devuelve su contenido como diccionario."""
    with open(path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config