# core/scheduler.py
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
import math
from ortools.sat.python import cp_model
import pandas as pd

from .routing import Routing

@dataclass
class Job:
    idx: int
    item: str
    group: str
    qty: int
    due: datetime
    customer: str
    order_no: str

@dataclass
class Op:
    job_idx: int
    op_name: str
    duration_min: int
    wc_slots: int          # сколько машин параллельно
    seq_in_job: int

class ORToolsScheduler:
    """CP-SAT планировщик Job-Shop с параллельными машинами и дедлайнами."""

    def __init__(self, routing: Routing, horizon_start: datetime, horizon_minutes: int,
                 makespan_weight: float = 1.0, tardiness_weight: float = 10.0):
        self.routing = routing
        self.t0 = horizon_start
        self.horizon_min = horizon_minutes
        self.w_makespan = makespan_weight
        self.w_tardiness = tardiness_weight

    # ---------- построение модели ----------
    def build(self, plan: pd.DataFrame) -> dict:
        # 1. Проверка на наличие обязательных колонок в DataFrame
        required_cols = ["item", "group", "qty", "due", "customer", "order_no"]
        for col in required_cols:
            if col not in plan.columns:
                raise ValueError(f"В данных отсутствует обязательная колонка: '{col}'. Проверьте файл Excel.")

        # 2. Сборка списка задач (Jobs)
        jobs: list[Job] = []
        for i, r in plan.reset_index(drop=True).iterrows():
            # Безопасно обрабатываем дату (если NaT, ставим дефолтную)
            due_date = r["due"]
            if pd.isna(due_date):
                due_date = self.t0 + timedelta(days=self.horizon_min // 1440)
            
            jobs.append(Job(
                idx=i, 
                item=str(r["item"]), 
                group=str(r["group"]), 
                qty=int(r["qty"]),
                due=due_date.to_pydatetime() if hasattr(due_date, 'to_pydatetime') else due_date,
                customer=str(r.get("customer", "")), 
                order_no=str(r.get("order_no", ""))
            ))

        # 3. Сборка списка операций (Ops)
        ops: list[Op] = []
        for j in jobs:
            seq = self.routing.operations(j.group)
            for s, op_name in enumerate(seq):
                per_unit = self.routing.op_time_min(op_name)
                # длительность = норма * кол-во, но не меньше 1 мин
                dur = max(1, per_unit * j.qty // 10)  # /10 — условная "партия", калибруется
                wc = self.routing.wc(op_name)
                ops.append(Op(j.idx, op_name, dur, int(wc["count"]), s))

        # 4. Защитная проверка: если операций нет, выдаем понятную ошибку
        if not ops:
            raise ValueError(
                "Список операций пуст. Это означает, что ни для одной детали из плана "
                "не нашлось маршрута в config.yaml. Проверьте, что в Excel заполнена "
                "колонка 'Группа' и для неё настроен routing_polymer или routing_non_polymer."
            )

        m = cp_model.CpModel()
        H = self.horizon_min

        # start/end для каждой операции
        starts, ends, intervals = {}, {}, {}
        for o in ops:
            k = (o.job_idx, o.op_name, o.seq_in_job)
            s = m.NewIntVar(0, H, f"s_{k}")
            e = m.NewIntVar(0, H, f"e_{k}")
            m.Add(e == s + o.duration_min)
            starts[k] = s
            ends[k] = e
            intervals[k] = m.NewIntervalVar(s, o.duration_min, e, f"i_{k}")

        # 1) последовательность внутри job
        by_job: dict[int, list[Op]] = {}
        for o in ops:
            by_job.setdefault(o.job_idx, []).append(o)
        for jidx, jops in by_job.items():
            jops.sort(key=lambda x: x.seq_in_job)
            for a, b in zip(jops, jops[1:]):
                ka = (a.job_idx, a.op_name, a.seq_in_job)
                kb = (b.job_idx, b.op_name, b.seq_in_job)
                m.Add(starts[kb] >= ends[ka])

        # 2) мощность РЦ: на каждую операцию — пул из wc_slots машин
        for op_name in {o.op_name for o in ops}:
            pool = [o for o in ops if o.op_name == op_name]
            slots = max(o.wc_slots for o in pool)
            machine_intervals: list[list] = [[] for _ in range(slots)]
            for o in pool:
                k = (o.job_idx, o.op_name, o.seq_in_job)
                presences = []
                for slot in range(slots):
                    b = m.NewBoolVar(f"pres_{k}_{slot}")
                    iv = m.NewOptionalIntervalVar(
                        starts[k], o.duration_min, ends[k], b, f"oiv_{k}_{slot}")
                    machine_intervals[slot].append(iv)
                    presences.append(b)
                m.AddExactlyOne(presences)
            for slot in range(slots):
                m.AddNoOverlap(machine_intervals[slot])

        # 3) дедлайны и целевая функция
        tardiness_vars = []
        for j in jobs:
            last = max((o for o in ops if o.job_idx == j.idx), key=lambda x: x.seq_in_job)
            k = (last.job_idx, last.op_name, last.seq_in_job)
            due_min = int((j.due - self.t0).total_seconds() // 60)
            t = m.NewIntVar(0, H + 100000, f"tard_{j.idx}")
            m.Add(t >= ends[k] - due_min)
            tardiness_vars.append(t)

        makespan = m.NewIntVar(0, H, "makespan")
        m.AddMaxEquality(makespan, [ends[(o.job_idx, o.op_name, o.seq_in_job)] for o in ops])

        m.Minimize(self.w_makespan * makespan + self.w_tardiness * sum(tardiness_vars))

        return {"model": m, "starts": starts, "ends": ends, "ops": ops,
                "jobs": jobs, "makespan": makespan, "tardiness": tardiness_vars}

    # ---------- решение ----------
    def solve(self, plan: pd.DataFrame, time_limit_s: int = 30, workers: int = 8):
        data = self.build(plan)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_s
        solver.parameters.num_search_workers = workers
        status = solver.Solve(data["model"])
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError(f"Нет решения: {solver.StatusName(status)}")

        rows = []
        for o in data["ops"]:
            k = (o.job_idx, o.op_name, o.seq_in_job)
            s_min = solver.Value(data["starts"][k])
            e_min = solver.Value(data["ends"][k])
            j = data["jobs"][o.job_idx]
            rows.append({
                "job_idx": j.idx, "item": j.item, "group": j.group, "qty": j.qty,
                "customer": j.customer, "order_no": j.order_no, "due": j.due,
                "operation": o.op_name, "seq": o.seq_in_job,
                "start": self.t0 + timedelta(minutes=s_min),
                "end":   self.t0 + timedelta(minutes=e_min),
                "duration_min": o.duration_min,
            })
        sched = pd.DataFrame(rows).sort_values(["job_idx", "seq"]).reset_index(drop=True)
        info = {
            "status": solver.StatusName(status),
            "makespan_min": solver.Value(data["makespan"]),
            "total_tardiness_min": int(sum(solver.Value(t) for t in data["tardiness"])),
            "objective": solver.ObjectiveValue(),
        }
        return sched, info