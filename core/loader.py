# core/loader.py
from __future__ import annotations
import pandas as pd
from pathlib import Path

# Определяем корень проекта (папка, где лежит run.py и config.yaml)
ROOT_DIR = Path(__file__).resolve().parent.parent

def _find_file(filename: str | Path) -> Path:
    """Ищет файл в текущей директории или в корне проекта."""
    p = Path(filename)
    if p.exists():
        return p
    # Если не нашли, пробуем найти в корне проекта
    p_root = ROOT_DIR / p
    if p_root.exists():
        return p_root
    
    raise FileNotFoundError(
        f"Файл '{filename}' не найден!\n"
        f"Искали по путям:\n  - {p.absolute()}\n  - {p_root.absolute()}\n"
        f"Пожалуйста, положите файлы Excel в папку проекта: {ROOT_DIR}"
    )


def load_plan(path: str | Path) -> pd.DataFrame:
    """Лист 'План производства' -> нормализованный DataFrame."""
    file_path = _find_file(path)
    df = pd.read_excel(file_path, sheet_name=0)
    df = df.rename(columns={
        "N": "n", "Номенклатура": "item", "Группа": "group",
        "Количество": "qty", "Назначение": "purpose", "Дата выпуска": "due",
    })
    df["due"] = pd.to_datetime(df["due"], dayfirst=True, errors="coerce")
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0).astype(int)
    # вытащим заказчика и номер заказа
    df["customer"] = df["purpose"].str.split(",").str[0].str.strip()
    df["order_no"] = df["purpose"].str.extract(r"(ПКЦБ-\d+)")
    return df


def load_bom(path: str | Path) -> pd.DataFrame:
    """Лист 'Разузловка' -> DataFrame с колонками code, item, spec, material, uom, qty."""
    file_path = _find_file(path)
    df = pd.read_excel(file_path, sheet_name=0)
    df = df.rename(columns={
        "Код": "code", "Номенклатура": "item",
        "Ресурсная спецификация": "spec", "Материал": "material",
        "Ед.изм.": "uom", "Количество": "qty",
    })
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0)
    return df.dropna(subset=["code"])