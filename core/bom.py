from __future__ import annotations
import pandas as pd

# Из Разузловки: для каждой готовой номенклатуры ищем компоненты (заготовки),
# количество которых берётся из "Количество" (кг или мм — зависит от uom).
# Прототип: сопоставляем по префиксу кода в Номенклатуре.
# В проде — по "Ресурсная спецификация" (связь изделие -> ресурс).

def explode(plan_row: pd.Series, bom: pd.DataFrame) -> list[dict]:
    """Возвращает список потребностей по заготовкам для одной позиции плана."""
    item = str(plan_row["item"])
    qty = int(plan_row["qty"])

    # Поиск компонентов: берём все строки BOM, где spec/материал указывает
    # на заготовку, а код готового изделия НЕ совпадает с кодом (чтобы не ловить сам себя).
    # Здесь — эвристика: ищем упоминание типоразмера изделия в полях BOM.
    # Пример: "Труба ТБТ-К1-133-102-57/З-108" -> ищем "133-102" или "133х102".
    key = _key_from_item(item)
    comps = bom[bom["spec"].str.contains(key, na=False, regex=False)] if key else bom.iloc[0:0]

    result = []
    for _, c in comps.iterrows():
        # Норма расхода: qty компонента в BOM * количество готовых
        # (в реальности — делить на вес/длину; здесь — как есть)
        result.append({
            "component_code": c["code"],
            "component_item": c["item"],
            "component_qty":  float(c["qty"]) * qty,
            "uom": c["uom"],
        })
    return result


def _key_from_item(item: str) -> str | None:
    """Вытащить типоразмер из наименования: '133-102' из 'ТБТ-К1-133-102-...'."""
    import re
    m = re.search(r"(\d{3})[-x](\d{2,3})", item)
    return f"{m.group(1)}-{m.group(2)}" if m else None