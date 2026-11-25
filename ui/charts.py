from __future__ import annotations
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from datetime import datetime

pg.setConfigOptions(antialias=True, background="w", foreground="k")

# Палитра для операций
OP_COLORS = {
    "Резка": "#60a5fa", "ТО": "#f97316", "УЗК": "#a855f7",
    "Мех.обработка": "#10b981", "Наплавка": "#ef4444",
    "Полимер": "#eab308", "Сборка": "#06b6d4", "ОТК": "#6b7280",
}


class GanttChart(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = pg.PlotWidget()
        self.plot.setLabel("bottom", "Время")
        self.plot.showGrid(x=True, y=False, alpha=0.2)
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.addWidget(self.plot)

    def render(self, payload: dict):
        self.plot.clear()
        rows = payload.get("data") or []
        if not rows:
            return
        # уникальные метки заказов → ось Y
        labels = list(dict.fromkeys(r["label"] for r in rows))
        y_index = {lab: i for i, lab in enumerate(labels)}

        for r in rows:
            start = datetime.fromisoformat(r["start"]).timestamp()
            end = datetime.fromisoformat(r["end"]).timestamp()
            y = y_index[r["label"]]
            color = OP_COLORS.get(r["operation"], "#94a3b8")
            item = pg.BarGraphItem(
                x0=start, y0=y - 0.4, width=end - start, height=0.8,
                brush=color, pen=pg.mkPen(None))
            self.plot.addItem(item)

        # ось Y — метки
        ax = self.plot.getAxis("left")
        ticks = [(i, lab[:45]) for lab, i in y_index.items()]
        ax.setTicks([ticks])
        ax.setWidth(240)

        # ось X — даты
        self.plot.getAxis("bottom").setLabel("Время")


class UtilChart(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = pg.PlotWidget()
        self.plot.setLabel("left", "Загрузка, %")
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.addWidget(self.plot)

    def render(self, payload: dict):
        self.plot.clear()
        rows = payload.get("data") or []
        if not rows:
            return
        ops = [r["operation"] for r in rows]
        vals = [r["utilization_pct"] for r in rows]
        x = list(range(len(ops)))
        brushes = [pg.mkBrush("#ef4444" if v > 90 else "#f59e0b" if v > 70 else "#10b981") for v in vals]
        bars = pg.BarGraphItem(x=x, height=vals, width=0.6, brushes=brushes)
        self.plot.addItem(bars)
        ax = self.plot.getAxis("bottom")
        ax.setTicks([[(i, op) for i, op in enumerate(ops)]])
        self.plot.setYRange(0, 110)


class OutputChart(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = pg.PlotWidget()
        self.plot.setLabel("left", "шт")
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.addWidget(self.plot)

    def render(self, payload: dict):
        self.plot.clear()
        rows = payload.get("data") or []
        if not rows:
            return
        weeks = [r["week"] for r in rows]
        qty = [r["qty"] for r in rows]
        jobs = [r["jobs"] for r in rows]
        x = list(range(len(weeks)))
        self.plot.addItem(pg.BarGraphItem(x=x, height=qty, width=0.6,
                                          brush=pg.mkBrush("#3b82f6")))
        self.plot.plot(x, jobs, pen=pg.mkPen("#ef4444", width=2),
                       symbol="o", symbolBrush="#ef4444", name="заказов")
        ax = self.plot.getAxis("bottom")
        ax.setTicks([[(i, w) for i, w in enumerate(weeks)]])