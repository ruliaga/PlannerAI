from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QFrame, QGridLayout)
from PySide6.QtCore import Qt
from ui.charts import GanttChart, UtilChart, OutputChart


class KpiTile(QFrame):
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("kpiTile")
        self.setFrameShape(QFrame.StyledPanel)
        lay = QVBoxLayout(self); lay.setContentsMargins(10, 6, 10, 6)
        self.v = QLabel("—"); self.v.setObjectName("kpiValue")
        self.l = QLabel(title); self.l.setObjectName("kpiLabel")
        lay.addWidget(self.v); lay.addWidget(self.l)

    def set(self, value):
        self.v.setText(str(value))


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        root = QVBoxLayout(self); root.setContentsMargins(12, 12, 12, 12)

        # KPI-плашки
        self.kpi_box = QHBoxLayout()
        self.tiles = {
            "on_time": KpiTile("Готовность"),
            "late":    KpiTile("Опозданий"),
            "jobs":    KpiTile("Заказов"),
            "makespan":KpiTile("Makespan, дн"),
            "tard":    KpiTile("Сумм. опоздание, ч"),
        }
        for t in self.tiles.values():
            self.kpi_box.addWidget(t)
        root.addLayout(self.kpi_box)

        # Графики: Gantt сверху, под ним — 2 в ряд
        self.gantt = GanttChart()
        self.gantt.setMinimumHeight(360)
        root.addWidget(self._card("Загрузка рабочих центров (Gantt)", self.gantt), 3)

        bottom = QGridLayout()
        self.util = UtilChart(); self.util.setMinimumHeight(260)
        self.out = OutputChart(); self.out.setMinimumHeight(260)
        bottom.addWidget(self._card("Узкие места, %", self.util), 0, 0)
        bottom.addWidget(self._card("Выпуск по неделям", self.out), 0, 1)
        root.addLayout(bottom, 2)

    def _card(self, title: str, chart: QWidget) -> QFrame:
        f = QFrame(); f.setObjectName("card")
        lay = QVBoxLayout(f); lay.setContentsMargins(10, 8, 10, 8)
        head = QLabel(title); head.setObjectName("cardTitle")
        lay.addWidget(head); lay.addWidget(chart)
        return f

    def apply_charts(self, charts: list[dict]):
        for c in charts:
            t = c.get("type")
            if t == "gantt":        self.gantt.render(c)
            elif t == "utilization": self.util.render(c)
            elif t == "output":     self.out.render(c)

    def apply_kpi(self, kpi: dict | None):
        if not kpi:
            return
        self.tiles["on_time"].set(f"{kpi.get('on_time_pct', '—')} %")
        self.tiles["late"].set(kpi.get("late_jobs", "—"))
        self.tiles["jobs"].set(kpi.get("jobs", "—"))
        self.tiles["makespan"].set(kpi.get("makespan_days", "—"))
        self.tiles["tard"].set(kpi.get("total_tardiness_h", "—"))