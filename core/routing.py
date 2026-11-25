# core/routing.py
from __future__ import annotations
import yaml
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.yaml"

class Routing:
    def __init__(self, cfg: dict):
        self.cfg = cfg

    def operations(self, group: str) -> list[str]:
        """Возвращает список операций (маршрут). Понимает любые названия групп."""
        group_lower = str(group).lower()
        
        # Если группа содержит "полимер" (но не "не полимер"), берем маршрут для полимера
        if "полимер" in group_lower and "не" not in group_lower:
            ops = self.cfg.get("routing_polymer", [])
        else:
            ops = self.cfg.get("routing_non_polymer", [])
            
        # ЗАЩИТА: Если список пустой, возвращаем дефолтный маршрут
        if not ops:
            ops = ["Резка", "ТО", "УЗК", "Мех.обработка", "Наплавка", "Сборка", "ОТК"]
            
        return ops

    def op_time_min(self, op: str) -> int:
        times = self.cfg.get("operation_times", {})
        return int(times.get(op, 60))

    def wc(self, op: str) -> dict:
        centers = self.cfg.get("work_centers", {})
        count = centers.get(op, 1)
        # Если count пришел как словарь (старый формат), достаем из него
        if isinstance(count, dict):
            count = count.get("count", 1)
        return {"count": int(count), "capacity_per_shift": 1}

def load_cfg(path: str | Path = None) -> dict:
    if path is None:
        cfg_path = DEFAULT_CONFIG_PATH
    else:
        cfg_path = Path(path)
        if not cfg_path.is_absolute() and not cfg_path.exists():
            cfg_path = ROOT_DIR / cfg_path

    if not cfg_path.exists():
        raise FileNotFoundError(f"Файл конфигурации не найден: {cfg_path}")

    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)