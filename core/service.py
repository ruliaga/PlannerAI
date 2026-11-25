from __future__ import annotations
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

from .loader import load_plan, load_bom
from .routing import Routing, load_cfg
from .scheduler import ORToolsScheduler
from .analytics import utilization, output_by_week, kpi



class PlanningService:
    """Единая точка входа. Все методы возвращают JSON-сериализуемые dict."""

    def __init__(self, cfg_path="config.yaml"):
        self.cfg = load_cfg(cfg_path)
        self.routing = Routing(self.cfg)
        self.plan: pd.DataFrame | None = None
        self.bom: pd.DataFrame | None = None
        self.sched: pd.DataFrame | None = None
        self.info: dict | None = None

    # --- tools для ИИ ---
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
        t0 = datetime.fromisoformat(h["start"])
        horizon_min = h["days"] * h["minutes_per_shift"] * h["shifts_per_day"]
        sch = ORToolsScheduler(self.routing, t0, horizon_min,
                               tardiness_weight=tardiness_weight)
        self.sched, self.info = sch.solve(self.plan, time_limit_s=time_limit_s)
        return {"status": self.info["status"], **kpi(self.sched, self.info)}

    def get_kpi(self) -> dict:
        if self.sched is None:
            return {"error": "Сначала вызовите plan_schedule"}
        return kpi(self.sched, self.info)

    def get_utilization(self) -> list[dict]:
        if self.sched is None:
            return []
        h = self.cfg["horizon"]
        t0 = datetime.fromisoformat(h["start"])
        t1 = t0 + timedelta(days=h["days"])
        return utilization(self.sched, t0, t1).to_dict(orient="records")

    def get_output(self) -> list[dict]:
        if self.sched is None:
            return []
        return output_by_week(self.sched).to_dict(orient="records")

    def get_late_jobs(self, top: int = 10) -> list[dict]:
        if self.sched is None:
            return []
        last = self.sched.sort_values("seq").groupby("job_idx").tail(1)
        late = last[last["end"] > last["due"]].sort_values("end")
        return late[["order_no", "item", "qty", "due", "end"]].head(top).to_dict("records")

    def change_priority(self, order_no: str, weight: float = 3.0) -> dict:
        """Пересчёт с приоритетом: приближаем дедлайн для указанного заказа."""
        if self.plan is None:
            return {"error": "Нет данных"}
        mask = self.plan["order_no"] == order_no
        if not mask.any():
            return {"error": f"Заказ {order_no} не найден"}
        # ускоряем дедлайн — планировщик штрафует опоздание сильнее
        self.plan.loc[mask, "due"] = self.plan.loc[mask, "due"] - pd.Timedelta(days=3)
        return {"changed": int(mask.sum()), "new_due": str(self.plan.loc[mask, "due"].iloc[0])}

    def export_schedule(self, path: str = "schedule.xlsx") -> dict:
        if self.sched is None:
            return {"error": "Нет расписания"}
        self.sched.to_excel(path, index=False)
        return {"file": path, "rows": len(self.sched)}

   