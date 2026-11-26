# core/service.py
"""Сервис планирования: загрузка данных, CP-SAT-планирование, разузловка до металла."""
from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd

from core.routing import Routing, load_cfg
from core.loader import load_plan, load_bom, load_metal_rs
from core.scheduler import ORToolsScheduler
from core.analytics import kpi as analytics_kpi
from core.bom import MetalRS, explode_plan, load_assembly_rs, procurement


class PlanningService:
    def __init__(self, cfg_path: str = "config.yaml"):
        self.cfg = load_cfg(cfg_path)
        self.routing = Routing(self.cfg)
        self.plan: pd.DataFrame = pd.DataFrame()
        self.bom: pd.DataFrame = pd.DataFrame()
        self.rs: pd.DataFrame = pd.DataFrame()      # РС сборок (разузловка)
        self.metal: MetalRS | None = None           # РС проката: нормы металла
        self.sched: pd.DataFrame = pd.DataFrame()
        self.info: dict = {}
        self._t0: datetime | None = None
        self.load_data()

    # ---------- данные ----------
    def load_data(self) -> dict:
        files = self.cfg.get("files", {})
        self.plan = load_plan(files["plan"])
        self.bom = load_bom(files["bom"])

        # РС сборок из листа «Ресусные сп.» + нормы проката
        self.rs = load_assembly_rs(files["bom"])
        self.metal = None
        try:
            self.metal = MetalRS(load_metal_rs(files.get("metal_rs", files["bom"])))
        except FileNotFoundError:
            # нет файла РС проката — нормы считаются расчётно из наименования
            self.metal = None
        return {"plan": len(self.plan), "bom": len(self.bom), "rs": len(self.rs)}

    # ---------- планирование ----------
    def plan_schedule(self, time_limit_s: int = 30, tardiness_weight: float = 10.0) -> dict:
        h = self.cfg["horizon"]
        # --- планирование от текущей даты ---
        t0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self._t0 = t0                                # единое окно для графиков и аналитики
        horizon_min = h["days"] * h["minutes_per_shift"] * h["shifts_per_day"]

        sch = ORToolsScheduler(self.routing, t0, horizon_min,
                               tardiness_weight=tardiness_weight)
        result = sch.solve(self.plan, time_limit_s=time_limit_s)
        # solve может вернуть (sched, info) или {"sched":..., "info":...} — поддержим оба
        if isinstance(result, tuple) and len(result) == 2:
            self.sched, self.info = result
        else:
            self.sched = (result or {}).get("sched", pd.DataFrame())
            self.info = (result or {}).get("info", {})
        return {"rows": len(self.sched), "info": self.info}

    # ---------- payloads для UI/агента ----------
    @staticmethod
    def _iso(v) -> str:
        return v if isinstance(v, str) else v.isoformat()

    def sched_payload(self) -> dict:
        """Данные диаграммы Ганта."""
        if self.sched is None or self.sched.empty:
            return {"type": "gantt", "data": []}
        rows = []
        for _, r in self.sched.iterrows():
            label = " ".join(str(r.get(c, "") or "") for c in
                             ("order_no", "customer", "item")).strip()
            rows.append({"label": label, "operation": r["operation"],
                         "start": self._iso(r["start"]), "end": self._iso(r["end"])})
        return {"type": "gantt", "data": rows}

    def horizon_window(self) -> tuple[datetime, datetime]:
        """Актуальное окно горизонта: от фактического старта планирования."""
        h = self.cfg["horizon"]
        t0 = self._t0 or datetime.fromisoformat(str(h["start"]))
        return t0, t0 + timedelta(days=h["days"])

    def kpi_payload(self) -> dict:
        if self.sched is None or self.sched.empty:
            return {}
        t0, t1 = self.horizon_window()
        return analytics_kpi(self.sched, {**(self.info or {}), "t0": t0, "t1": t1})

    # ---------- разузловка до металла ----------
    def metal_requirements(self) -> pd.DataFrame:
        """Потребность по всем позициям плана: сборка -> комплектующие ->
        заготовки -> металл (по правилам core.rules)."""
        return explode_plan(self.plan, self.rs, self.metal)

    def metal_procurement(self) -> pd.DataFrame:
        """Сводная закупка металла: палки и кг, замки — со смешанным раскроем."""
        return procurement(self.metal_requirements())
