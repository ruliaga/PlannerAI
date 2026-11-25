from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from ui.dashboard import Dashboard
from ui.chat_panel import ChatPanel
from storage import db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Планировщик производства ТБТ — ИИ-ассистент")
        self.resize(1500, 900)

        split = QSplitter(Qt.Horizontal)

        self.dash = Dashboard()
        self.chat = ChatPanel()

        split.addWidget(self.dash)
        split.addWidget(self.chat)
        split.setStretchFactor(0, 3)
        split.setStretchFactor(1, 2)
        split.setSizes([950, 550])

        self.setCentralWidget(split)

        # сигналы чат → дашборд
        self.chat.charts_ready.connect(self.dash.apply_charts)
        self.chat.kpi_ready.connect(self.dash.apply_kpi)

        # восстановление последних графиков
        for name in ("gantt", "utilization", "output"):
            snap = db.last_snapshot(name)
            if snap:
                self.dash.apply_charts([snap])

        # восстановление KPI
        from agent.tools import _svc
        if _svc.sched is not None:
            from core.analytics import kpi
            self.dash.apply_kpi(kpi(_svc.sched, _svc.info))