import pandas as pd


def utilization(sched: pd.DataFrame, horizon_start, horizon_end) -> pd.DataFrame:
    """Загрузка РЦ: суммарные минуты операций / доступный фонд."""
    total = (horizon_end - horizon_start).total_seconds() / 60
    g = sched.groupby("operation")["duration_min"].sum().rename("busy_min").reset_index()
    g["available_min"] = total
    g["utilization_pct"] = (g["busy_min"] / g["available_min"] * 100).round(1)
    return g.sort_values("utilization_pct", ascending=False)


def output_by_week(sched: pd.DataFrame) -> pd.DataFrame:
    """Выпуск по неделям (по завершению последней операции job'а)."""
    last = sched.sort_values("seq").groupby("job_idx").tail(1).copy()
    last["week"] = last["end"].dt.to_period("W").astype(str)
    return last.groupby("week").agg(
        jobs=("job_idx", "nunique"),
        qty=("qty", "sum"),
    ).reset_index()


def kpi(sched: pd.DataFrame, info: dict) -> dict:
    last = sched.sort_values("seq").groupby("job_idx").tail(1)
    late = last[last["end"] > last["due"]]
    return {
        "makespan_days": round(info["makespan_min"] / (60 * 8), 1),
        "jobs": int(last.shape[0]),
        "late_jobs": int(late.shape[0]),
        "on_time_pct": round(100 * (1 - late.shape[0] / max(1, last.shape[0])), 1),
        "total_tardiness_h": round(info["total_tardiness_min"] / 60, 1),
        "objective": round(info["objective"], 1),
    }