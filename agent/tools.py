# agent/tools.py
"""Инструменты агента: графики, заказы и расчёт металла по правилам core.rules."""
from __future__ import annotations

from core import rules
from core.analytics import output_by_week, utilization
from core.bom import assembly_key, parse_blank
from core.service import PlanningService
from storage import db

_service: PlanningService | None = None


def get_service() -> PlanningService:
    """Ленивый singleton: инициализация только при первом обращении."""
    global _service
    if _service is None:
        _service = PlanningService("config.yaml")
    return _service


# ---------- графики (как раньше) ----------
def _payload_gantt():
    return get_service().sched_payload()

def _payload_util():
    svc = get_service()
    t0, t1 = svc.horizon_window()
    return {"type": "utilization",
            "data": utilization(svc.sched, t0, t1).to_dict("records")}

def _payload_output():
    return {"type": "output",
            "data": output_by_week(get_service().sched).to_dict("records")}

def _payload_orders():
    p = get_service().plan
    cols = [c for c in ("order_no", "customer", "item", "qty", "due") if c in p.columns]
    return {"type": "orders", "data": p[cols].to_dict("records")}


# ---------- РАСЧЁТ МЕТАЛЛА ----------
def calc_metal(assembly: str, qty: int, lock_type: str | None = None) -> dict:
    """Сколько заготовок и металла нужно на qty труб сборки.
    lock_type='regular'/'long' — явный выбор; None — по правилам (заказчик)."""
    svc = get_service()
    asm = assembly_key(assembly)
    sub = svc.rs[svc.rs["assembly"] == asm]
    if sub.empty:
        return {"error": f"РС для {asm} не найдена",
                "available": sorted(set(svc.rs["assembly"]))}
    qty = int(qty)
    if qty <= 0:
        return {"error": "qty должен быть больше 0"}
    customer = str(sub["customer"].iloc[0])
    lt = lock_type if lock_type in rules.LOCK_SET_MM else \
        rules.resolve_lock_type(customer=customer, assembly=asm)

    body = sub[sub["role_n"] == "заготовка под тела"].iloc[0]
    locks = sub[sub["role_n"] == "заготовка под замки"].iloc[0]
    bb, lb = parse_blank(body["item"]), parse_blank(locks["item"])

    mb = rules.metal_for_bodies(qty, bb["kg_per_m"], bb["l_to"])
    ml = rules.metal_for_locks([(lt, qty)], lb["kg_per_m"], lb["l_to"])
    mb_rec = svc.metal.find(body["item"], bb) if svc.metal else None
    ml_rec = svc.metal.find(locks["item"], lb) if svc.metal else None

    return {
        "assembly": asm, "qty": qty,
        "lock_type": lt, "lock_label": rules.LOCK_LABELS[lt],
        "customer": customer or "не задан",
        "тела": {"заготовка": body["item"], "шт": qty,
                 "мм": qty * (bb["l_from"] or 0), "палок": mb["pallets"], "кг": mb["kg"],
                 "прокат": (mb_rec or {}).get("material", "норма расчётная (нет в РС проката)"),
                 "note": (mb_rec or {}).get("note", "")},
        "замки": {"заготовка": locks["item"], "комплектов": qty,
                  "мм_на_комплект": ml["set_mm"], "мм_всего": ml["total_mm"],
                  "комплектов_с_палки": ml["per_pallet"], "палок": ml["pallets"],
                  "кг": ml["kg"],
                  "прокат": (ml_rec or {}).get("material", "норма расчётная (нет в РС проката)"),
                  "note": (ml_rec or {}).get("note", "")},
        "итого_палок": mb["pallets"] + ml["pallets"],
        "итого_кг": round(mb["kg"] + ml["kg"], 1),
    }


def calc_metal_portfolio(lock_type: str | None = None) -> dict:
    """Потребность в заготовках и металле по всему портфелю заказов.
    lock_type='regular'/'long' — пересчитать все замки заданным типом."""
    svc = get_service()
    req = svc.metal_requirements()
    if lock_type in rules.LOCK_SET_MM:
        req = req.copy()
        req.loc[req["role"] == "заготовка под замки", "lock_type"] = lock_type
        req["set_mm"] = req["lock_type"].map(rules.lock_set_mm)
    prok = svc.metal_procurement()
    if lock_type in rules.LOCK_SET_MM:      # пересчитать палки замков
        import pandas as pd
        rows = []
        for _, r in prok.iterrows():
            if r["role"] == "замки":
                g = req[req["blank_name"] == r["blank"]]
                groups = [(lt, int(s)) for lt, s in g.groupby("lock_type")["qty"].sum().items()]
                m = rules.metal_for_locks(groups, float(g["kg_per_m"].iloc[0]),
                                          int(g["pallet_len_mm"].iloc[0]))
                r = {**r, "pallets": m["pallets"], "kg": m["kg"], "cut": m["cut"]}
            rows.append(r)
        prok = pd.DataFrame(rows)
    return {"type": "procurement", "data": prok.to_dict("records"),
            "total_kg": round(float(prok["kg"].sum()), 1)}


def set_lock_type(target: str, lock_type: str) -> dict:
    """Переключить тип замков: target — сборка ('СТБТ.1801') или заказчик ('Газпром')."""
    if lock_type not in rules.LOCK_SET_MM:
        return {"error": "lock_type должен быть 'regular' или 'long'"}
    t = (target or "").strip()
    if not t:
        db.set_setting("lock_global_override", lock_type)
        return {"ok": True, "message": f"Глобально замки переключены: {rules.LOCK_LABELS[lock_type]}"}
    if t.lower().startswith("стбт"):
        rules.set_override(assembly=t, value=lock_type)
    else:
        rules.set_override(customer=t, value=lock_type)
    return {"ok": True, "target": t, "lock_type": lock_type,
            "message": f"«{t}»: {rules.LOCK_LABELS[lock_type]}. Пересчёт выполняется автоматически."}


def list_assemblies() -> dict:
    """Все сборки РС: заказчик, тип замков, заготовки."""
    svc = get_service()
    out = []
    for asm, g in svc.rs.groupby("assembly"):
        out.append({"assembly": asm, "customer": g["customer"].iloc[0],
                    "lock_type": rules.resolve_lock_type(customer=g["customer"].iloc[0], assembly=asm),
                    "заготовка_под_тела": g[g["role_n"] == "заготовка под тела"]["item"].iloc[0],
                    "заготовка_под_замки": g[g["role_n"] == "заготовка под замки"]["item"].iloc[0]})
    return {"assemblies": out}


TOOLS = [
    {"type": "function", "function": {"name": "get_gantt", "description": "Диаграмма Ганта текущего плана", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_utilization", "description": "Загрузка рабочих центров, %", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_output", "description": "Выпуск по неделям", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_orders", "description": "Портфель заказов из плана производства", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "calc_metal",
        "description": "Рассчитать заготовки и металл для N труб сборки СТБТ. Правила: тело = 1 целая палка на трубу; замки = 1500 мм (обычные) или 1800 мм (удлинённые) на комплект муфта+ниппель.",
        "parameters": {"type": "object", "properties": {
            "assembly": {"type": "string", "description": "Сборка, напр. СТБТ.1800"},
            "qty": {"type": "integer", "description": "Количество труб"},
            "lock_type": {"type": "string", "enum": ["regular", "long"],
                          "description": "Тип замков; если не указан — по правилам (Газпром=long, остальные=regular)"}},
            "required": ["assembly", "qty"]}}},
    {"type": "function", "function": {
        "name": "calc_metal_portfolio",
        "description": "Потребность в заготовках и металле по всему портфелю, со смешанным раскроем замков",
        "parameters": {"type": "object", "properties": {
            "lock_type": {"type": "string", "enum": ["regular", "long"],
                          "description": "Пересчитать все замки заданным типом"}}}}},
    {"type": "function", "function": {
        "name": "set_lock_type",
        "description": "Переключить тип замков (пересчёт сохраняется в настройках)",
        "parameters": {"type": "object", "properties": {
            "target": {"type": "string", "description": "Сборка (СТБТ.1801) или заказчик (Газпром); пусто — глобально"},
            "lock_type": {"type": "string", "enum": ["regular", "long"]}},
            "required": ["lock_type"]}}},
    {"type": "function", "function": {"name": "list_assemblies", "description": "Список сборок РС с заказчиками и типами замков", "parameters": {"type": "object", "properties": {}}}},
]

IMPL = {"get_gantt": _payload_gantt, "get_utilization": _payload_util,
        "get_output": _payload_output, "get_orders": _payload_orders,
        "calc_metal": calc_metal, "calc_metal_portfolio": calc_metal_portfolio,
        "set_lock_type": set_lock_type, "list_assemblies": list_assemblies}
