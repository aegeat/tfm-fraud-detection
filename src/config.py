"""Carga de la configuración del proyecto desde archivos YAML."""

from pathlib import Path

import yaml

# Raíz del repositorio: la carpeta que contiene src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def resolve_path(path):
    """Convierte una ruta del config en absoluta, tomando la raíz del repo como base."""
    return PROJECT_ROOT / path


def load_config(path):
    """Lee un archivo YAML y devuelve su contenido como diccionario."""
    with open(path, encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config