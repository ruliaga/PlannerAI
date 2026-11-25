from __future__ import annotations
from datetime import datetime, timedelta
from core.service import PlanningService
from core.analytics import utilization, output_by_week, kpi

_svc = PlanningService("config.yaml")

TOOLS = [
    {"type": "function", "function": {
        "name": "load_data",
        "description": "Загрузить выгрузки 1С (План + Разузловка).",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "plan_schedule",
        "description": "Построить расписание CP-SAT.",
        "parameters": {"type": "object", "properties": {
            "time_limit_s": {"type": "integer", "default": 30},
            "tardiness_weight": {"type": "number", "default": 10.0}}}}},
    {"type": "function", "function": {
        "name": "get_kpi", "description": "KPI расписания.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_utilization", "description": "Загрузка РЦ, %.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_output", "description": "Выпуск по неделям.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_late_jobs", "description": "Топ опоздавших.",
        "parameters": {"type": "object", "properties": {
            "top": {"type": "integer", "default": 10}}}}},
    {"type": "function", "function": {
        "name": "change_priority",
        "description": "Поднять приоритет заказа.",
        "parameters": {"type": "object", "properties": {
            "order_no": {"type": "string"},
            "weight": {"type": "number", "default": 3.0}}, "required": ["order_no"]}}},
    {"type": "function", "function": {
        "name": "export_schedule",
        "description": "Сохранить расписание в Excel.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "default": "schedule.xlsx"}}}}},
    {"type": "function", "function": {
        "name": "chart_gantt", "description": "Показать Gantt на дашборде.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "chart_utilization", "description": "Показать загрузку РЦ.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "chart_output", "description": "Показать выпуск по неделям.",
        "parameters": {"type": "object", "properties": {}}}},
]


def _payload_gantt():
    return {"type": "gantt", "data": [
        {"label": f"{r.order_no or ''} | {r.item[:40]}",
         "operation": r.operation, "start": r.start.isoformat(),
         "end": r.end.isoformat(), "qty": int(r.qty),
         "customer": r.customer, "due": r.due.date().isoformat()}
        for r in _svc.sched.itertuples()]}


def _payload_util():
    h = _svc.cfg["horizon"]; t0 = datetime.fromisoformat(h["start"])
    u = utilization(_svc.sched, t0, t0 + timedelta(days=h["days"]))
    return {"type": "utilization", "data": u.to_dict(orient="records")}


def _payload_output():
    return {"type": "output", "data": output_by_week(_svc.sched).to_dict(orient="records")}


IMPL = {
    "load_data":        lambda **_: _svc.load_data(),
    "plan_schedule":    lambda **kw: _svc.plan_schedule(**kw),
    "get_kpi":          lambda **_: _svc.get_kpi(),
    "get_utilization":  lambda **_: _svc.get_utilization(),
    "get_output":       lambda **_: _svc.get_output(),
    "get_late_jobs":    lambda **kw: _svc.get_late_jobs(**kw),
    "change_priority":  lambda **kw: _svc.change_priority(**kw),
    "export_schedule":  lambda **kw: _svc.export_schedule(**kw),
    "chart_gantt":       lambda **_: _payload_gantt(),
    "chart_utilization": lambda **_: _payload_util(),
    "chart_output":      lambda **_: _payload_output(),
}