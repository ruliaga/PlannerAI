# core/service.py
from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from .loader import load_plan, load_bom
from .routing import Routing, load_cfg
from .scheduler import ORToolsScheduler
from .analytics import utilization, output_by_week, kpi

class PlanningService:
    def __init__(self, cfg_path="config.yaml"):
        self.cfg = load_cfg(cfg_path)
        self.routing = Routing(self.cfg)
        self.plan: pd.DataFrame | None = None
        self.bom: pd.DataFrame | None = None
        self.sched: pd.DataFrame | None = None
        self.info: dict | None = None

    def load_data(self) -> dict:
        self.plan = load_plan(self.cfg["files"]["plan"])
        self.bom = load_bom(self.cfg["files"]["bom"])
        return {
            "plan_rows": len(self.plan),
            "plan_qty": int(self.plan["qty"].sum()),
            "bom_rows": len(self.bom),
            "date_min": str(self.plan["due"].min().date()),
            "date_max": str(self.plan["due"].max().date()),
        }

    def plan_schedule(self, time_limit_s: int = 30, tardiness_weight: float = 10.0) -> dict:
        if self.plan is None:
            self.load_data()
        h = self.cfg["horizon"]
        
        # --- ИЗМЕНЕНИЕ: Планируем с текущей даты ---
        t0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        horizon_min = h["days"] * h["minutes_per_shift"] * h["shifts_per_day"]
        sch = ORToolsScheduler(self.routing, t0, horizon_min,
                               tardiness_weight=tardiness_weight)
        self.sched, self.info = sch.solve(self.plan, time_limit_s=time_limit_s)
        return {"status": self.info["status"], **kpi(self.sched, self.info)}

    # ... остальные методы остаются без изменений ...