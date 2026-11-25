# ui/charts.py
from __future__ import annotations
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from datetime import datetime

pg.setConfigOptions(antialias=True, background="w", foreground="k")

OP_COLORS = {
    "Резка": "#60a5fa", "ТО": "#f97316", "УЗК": "#a855f7",
    "Мех.обработка": "#10b981", "Наплавка": "#ef4444",
    "Полимер": "#eab308", "Сборка": "#06b6d4", "ОТК": "#6b7280",
}

class GanttChart(QWidget):
    def __init__(self):
        super().__init__()
        axis_x = pg.DateAxisItem(orientation='bottom')
        self.plot = pg.PlotWidget(axisItems={'bottom': axis_x})
        
        self.plot.showGrid(x=True, y=False, alpha=0.3)
        
        # --- ИЗМЕНЕНИЕ: Настройка оси Y ---
        ax_y = self.plot.getAxis("left")
        # Увеличиваем ширину оси, чтобы влезали названия заказов
        ax_y.setWidth(320) 
        # Задаем шрифт для подписей
        ax_y.setStyle(tickFont=QFont("Arial", 9))
        
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plot)

    def render(self, payload: dict):
        self.plot.clear()
        rows = payload.get("data") or []
        if not rows:
            return

        # Формируем уникальные подписи
        labels = list(dict.fromkeys(r["label"] for r in rows))
        y_index = {lab: i for i, lab in enumerate(labels)}

        for r in rows:
            start_ts = datetime.fromisoformat(r["start"]).timestamp()
            end_ts = datetime.fromisoformat(r["end"]).timestamp()
            duration = end_ts - start_ts
            
            if duration <= 0:
                continue
                
            y = y_index[r["label"]]
            color = OP_COLORS.get(r["operation"], "#94a3b8")

            # Рисуем полосу
            item = pg.BarGraphItem(
                x0=start_ts, y0=y - 0.35, width=duration, height=0.7,
                brush=color, pen=pg.mkPen(None),
                tooltip=f"Заказ: {r['label']}\nОперация: {r['operation']}\nДо: {r['due']}"
            )
            self.plot.addItem(item)

        # --- ИЗМЕНЕНИЕ: Принудительно задаем тики для оси Y ---
        ax_y = self.plot.getAxis("left")
        # Обрезаем строку, если она слишком длинная, чтобы не ломать график
        ticks = [(i, str(lab)[:45]) for lab, i in y_index.items()]
        ax_y.setTicks([ticks])

        self.plot.setYRange(-1, len(labels))
        self.plot.invertY(True)

        # Рассчитываем границы X
        min_time = min(datetime.fromisoformat(r["start"]).timestamp() for r in rows)
        max_time = max(datetime.fromisoformat(r["end"]).timestamp() for r in rows)
        
        # Отступ по 2 дня с каждой стороны, чтобы график не "прилипал" к краям
        self.plot.setXRange(min_time - 172800, max_time + 172800)


# Остальные классы (UtilChart и OutputChart) оставляем без изменений
class UtilChart(QWidget):
    def __init__(self):
        super().__init__()
        self.plot = pg.PlotWidget()
        self.plot.setLabel("left", "Загрузка, %")
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.addWidget(self.plot)

    def render(self, payload: dict):
        self.plot.clear()
        rows = payload.get("data") or []
        if not rows: return
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
        if not rows: return
        weeks = [r["week"] for r in rows]
        qty = [r["qty"] for r in rows]
        jobs = [r["jobs"] for r in rows]
        x = list(range(len(weeks)))
        
        self.plot.addItem(pg.BarGraphItem(x=x, height=qty, width=0.6, brush=pg.mkBrush("#3b82f6")))
        self.plot.plot(x, jobs, pen=pg.mkPen("#ef4444", width=2), symbol="o", symbolBrush="#ef4444")
        ax = self.plot.getAxis("bottom")
        ax.setTicks([[(i, w) for i, w in enumerate(weeks)]])