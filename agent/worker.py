from PySide6.QtCore import QThread, Signal
from agent.llm import run_agent


class AgentWorker(QThread):
    finished = Signal(dict)       # {'text', 'charts', 'kpi'}
    failed = Signal(str)

    def __init__(self, message: str, history: list[dict]):
        super().__init__()
        self.message = message
        self.history = history

    def run(self):
        try:
            self.finished.emit(run_agent(self.message, self.history))
        except Exception as e:
            self.failed.emit(f"{type(e).__name__}: {e}")