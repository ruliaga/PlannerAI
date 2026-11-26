from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser,
                               QLineEdit, QPushButton, QLabel, QFrame)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from agent.worker import AgentWorker
from storage import db


class ChatPanel(QWidget):
    charts_ready = Signal(list)
    kpi_ready    = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setObjectName("chatPanel")
        self.worker: AgentWorker | None = None

        root = QVBoxLayout(self); root.setContentsMargins(10, 10, 10, 10)

        head = QHBoxLayout()
        title = QLabel("ИИ-ассистент"); title.setObjectName("chatTitle")
        self.status = QLabel("готов"); self.status.setObjectName("chatStatus")
        head.addWidget(title); head.addStretch(); head.addWidget(self.status)
        root.addLayout(head)

        # быстрые кнопки
        quick = QHBoxLayout()
        for text, prompt in [
            ("Построить план", "Загрузи данные и построй план"),
            ("Загрузка РЦ",    "Покажи загрузку рабочих центров"),
            ("Опоздания",      "Что опаздывает?"),
            ("Выпуск",         "Покажи выпуск по неделям"),
            ("Экспорт",        "Экспортируй расписание в Excel"),
        ]:
            b = QPushButton(text); b.setObjectName("quickBtn")
            b.clicked.connect(lambda _, p=prompt: self.send(p))
            quick.addWidget(b)
        root.addLayout(quick)

        # лог
        self.log = QTextBrowser(); self.log.setObjectName("chatLog")
        self.log.setOpenExternalLinks(False)
        self.log.setFont(QFont("Segoe UI", 10))
        root.addWidget(self.log, 1)

        # ввод
        inp = QHBoxLayout()
        self.input = QLineEdit(); self.input.setPlaceholderText(
            "Например: подними приоритет ПКЦБ-328 и покажи Gantt")
        self.input.returnPressed.connect(lambda: self.send(self.input.text()))
        self.send_btn = QPushButton("→"); self.send_btn.clicked.connect(
            lambda: self.send(self.input.text()))
        inp.addWidget(self.input, 1); inp.addWidget(self.send_btn)
        root.addLayout(inp)

        self._restore_history()

    # --------- отправка ----------

    def send(self, text: str):
        text = (text or "").strip()
        if not text or self.worker is not None:
            return
        db.add_msg("user", text)
        self._append("user", text)
        self.input.clear()
        self._busy(True)

        hist = db.history(limit=20)
        self.worker = AgentWorker(text, hist)
        self.worker.finished.connect(self._on_done)
        self.worker.failed.connect(self._on_fail)
        self.worker.start()

    def _on_done(self, res: dict):
        self._busy(False)
        db.add_msg("assistant", res.get("text", ""))
        db.add_msg("assistant", res.get("text", ""))
        self._append("assistant", res.get("text", ""))
        if res.get("charts"):
            for c in res["charts"]:
                db.save_snapshot(c["type"], c)
            self.charts_ready.emit(res["charts"])
        if res.get("kpi"):
            self.kpi_ready.emit(res["kpi"])
        self.worker = None

    def _on_fail(self, err: str):
        self._busy(False)
        self._append("assistant", f"⚠ Ошибка: {err}")
        self.worker = None

    def _busy(self, b: bool):
        self.send_btn.setEnabled(not b)
        self.input.setEnabled(not b)
        self.status.setText("печатает…" if b else "готов")
        self.status.setProperty("busy", b)
        self.status.style().polish(self.status)

    # ---------- лог ----------
    def _append(self, role: str, text: str):
        color = "#2563eb" if role == "user" else "#374151"
        who = "Вы" if role == "user" else "Ассистент"
        safe = (text or "").replace("\n", "<br>")
        self.log.append(
            f'<div style="margin:6px 0"><b style="color:{color}">{who}:</b><br>{safe}</div>')
        db.add_msg(role, text)
        self.log.verticalScrollBar().setValue(self.log.verticalScrollBar().maximum())

    def _restore_history(self):
        for m in db.history(limit=30):
            color = "#2563eb" if m["role"] == "user" else "#374151"
            who = "Вы" if m["role"] == "user" else "Ассистент"
            self.log.append(
                f'<div style="margin:6px 0"><b style="color:{color}">{who}:</b><br>'
                f'{m["content"].replace(chr(10), "<br>")}</div>')
