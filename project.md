This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.
The content has been processed where content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: **/__pycache__/**, **/*.pyc, **/.venv/**, **/*.db, **/*.sqlite, **/*.png, **/*.jpg, **/*.xlsx, **/*.csv, **/node_modules/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
agent/
  __init__.py
  llm.py
  tools.py
  worker.py
core/
  __init__.py
  analytics.py
  bom.py
  loader.py
  routing.py
  scheduler.py
  service.py
storage/
  __init__.py
  db.py
ui/
  __init__.py
  charts.py
  chat_panel.py
  dashboard.py
  main_window.py
  style.css
.gitignore
виды рц.txt
Структура.txt
build.spec
config.yaml
requirements.txt
run.py
russian-trusted-cacert.pem
```

# Files

## File: виды рц.txt
```
Выбор
	Когда (СтрНайти([Операция.Наименование], "токарная") > 0 Или СтрНайти([Операция.Наименование], "трубонарезная") > 0) И (СтрНайти([Операция.Наименование], "ЧПУ") > 0 Или СтрНайти([Операция.Наименование], "ПУ") > 0) Или ((СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПКНГ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "PKNM") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "РЦО") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "internal") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "РЦО") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "КОГИС") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПК ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПК ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПКС") > 0) И СтрНайти([Операция.Наименование], "Токарная") > 0 И СтрНайти([Операция.Наименование], "ПУ") > 0 Или СтрНайти([Ссылка.Рабочий центр.Наименование], "Токарные ЧПУ (Те") > 0)
		Тогда "УСсЧПУ // Токарная с ЧПУ"
	Когда (СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПКНГ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "PKNM") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "РЦО") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "internal") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "РЦО") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "КОГИС") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПК ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПКС") > 0) И СтрНайти([Операция.Наименование], "Токарная") > 0 И (Не СтрНайти([Ссылка.Исполнитель], "Урыту") > 0)
		Тогда "УСсЧПУ // Токарная (НП и Телеметрия)"
	Когда СтрНайти([Операция.Наименование], "Ленточно-отре") > 0
		Тогда "Заготовительный участок // Отрезная"
	Когда (СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "стбт") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "УБТ.1589.000 СБ Труба УБТ-КСТ-105-82-51/Z-86-2  (9 300) // до полимера") > 0) И (СтрНайти([Операция.Наименование], "узк") > 0 Или СтрНайти([Операция.Наименование], "мпд") > 0)
		Тогда "ЛНК // Контроль сварных швов"
	Когда СтрНайти([Операция.Наименование], "УЗК") > 0 И (Не СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Вид номенклатуры.Наименование], "Замки") > 0)
		Тогда "ЛНК // УЗК"
	Когда СтрНайти([Операция.Наименование], "МПД") > 0 И (СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Вид номенклатуры.Наименование], "Замки") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Вид номенклатуры.Наименование], "Переводники") > 0)
		Тогда "ЛНК // МПД"
	Когда (СтрНайти([Операция.Наименование], "Термообработка") > 0 Или СтрНайти([Операция.Наименование], "накал") > 0) И СтрНайти(Строка([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Единица хранения]), "шт") > 0 И (Не СтрНайти(Строка([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование]), "СТБТ") > 0) И (Не СтрНайти(Строка([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование]), "тело") > 0) И (Не СтрНайти(Строка([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование]), "СВБТ") > 0) И (Не СтрНайти(Строка([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование]), "УБТ.") > 0)
		Тогда "Участок Термообработки // Накал"
	Когда (СтрНайти([Операция.Наименование], "Термообработка") > 0 Или СтрНайти([Операция.Наименование], "накал") > 0) И СтрНайти(Строка([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Единица хранения]), "мм") > 0
		Тогда "Участок Термообработки // ИНТ"
	Когда СтрНайти([Операция.Наименование], "Азот") > 0
		Тогда "Участок Термообработки // Азотирование"
	Когда (СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "стбт") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "УБТ.1589.000 СБ Труба УБТ-КСТ-105-82-51/Z-86-2  (9 300) // до полимера") > 0) И СтрНайти([Операция.Наименование], "ПКНВ-648") > 0 И (Не СтрНайти([Операция.Наименование], "упак") > 0) И (Не СтрНайти([Операция.Наименование], "пакет") > 0)
		Тогда "Участок сварки трением // Все ВРЦ"
	Когда СтрНайти([Операция.Наименование], "правка") > 0 Или СтрНайти([Операция.Наименование], "Расконсервация ПКНВ-324") > 0 Или СтрНайти([Операция.Наименование], "Маркирование ПКНВ-392") > 0
		Тогда "УУС // Правка"
	Когда СтрНайти([Ссылка.Рабочий центр.Наименование], "286") > 0 Или СтрНайти([Ссылка.Рабочий центр.Наименование], "1H65") > 0
		Тогда "УУС // 286"
	Когда СтрНайти([Операция.Наименование], "Сверл") > 0 Или СтрНайти([Операция.Наименование], "расточн") > 0 Или СтрНайти([Операция.Наименование], "Раскат") > 0
		Тогда "УУС // Сверление и Расточка"
	Когда СтрНайти([Операция.Наименование], "токарная") > 0 Или СтрНайти([Операция.Наименование], "Трубонарез") > 0 И (Не СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "стбт") > 0) И (Не СтрНайти([Вид рабочего центра.Наименование], "ЧПУ") > 0) И СтрНайти([Операция.Наименование], "Разметочн") > 0
		Тогда "УУС // Токарная"
	Когда СтрНайти([Операция.Наименование], "хон") > 0
		Тогда "УУС // Хонингование"
	Когда СтрНайти([Операция.Наименование], "фрезерная") > 0
		Тогда "УСсЧПУ // Фрезерная ЧПУ"
	Когда (СтрНайти([Операция.Наименование], "приработка") > 0 Или СтрНайти([Операция.Наименование], "фосфат") > 0 Или СтрНайти([Операция.Наименование], "марк") > 0 Или СтрНайти([Операция.Наименование], "диффу") > 0 Или СтрНайти([Операция.Наименование], "покры") > 0 Или СтрНайти([Операция.Наименование], "слеса") > 0 Или СтрНайти([Операция.Наименование], "свинч") > 0 Или СтрНайти([Операция.Наименование], "обкат") > 0 Или СтрНайти([Операция.Наименование], "дробестру") > 0 Или СтрНайти([Операция.Наименование], "комплектов") > 0 Или СтрНайти([Операция.Наименование], "консерв") > 0 Или СтрНайти([Операция.Наименование], "абразивн") > 0 Или СтрНайти([Операция.Наименование], "упаков") > 0 Или СтрНайти([Операция.Наименование], "пакет") > 0) И (Не((СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПКНГ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "PKNM") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "РЦО") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "пульсат") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "screw") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "internal") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "РЦО") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "КОГИС") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПК ") > 0 Или СтрНайти([Этап.Изделия по рассчитываемой стоимости.Номенклатура.Наименование], "ПКС") > 0) И (СтрНайти([Операция.Наименование], "марк") > 0 Или СтрНайти([Операция.Наименование], "слеса") > 0 Или СтрНайти([Операция.Наименование], "сбор") > 0 Или СтрНайти([Операция.Наименование], "песко") > 0 Или СтрНайти([Операция.Наименование], "магни") > 0 Или СтрНайти([Операция.Наименование], "дефект") > 0 Или СтрНайти([Операция.Наименование], "гидро") > 0 Или СтрНайти([Операция.Наименование], "старен") > 0 Или СтрНайти([Операция.Наименование], "вакуум") > 0 Или СтрНайти([Операция.Наименование], "упак") > 0)))
		Тогда "Сдача // Все ВРЦ"
	Иначе ""
Конец
```

## File: Структура.txt
```
prod_planner_desktop/
├── requirements.txt
├── config.yaml
├── run.py                        # точка входа
├── build.spec                    # PyInstaller
├── core/                         # ядро планирования (без изменений)
│   ├── loader.py
│   ├── bom.py
│   ├── routing.py
│   ├── scheduler.py
│   ├── analytics.py
│   └── service.py
├── agent/
│   ├── tools.py                  # tool-схемы + диспетчер
│   ├── llm.py                    # клиент OpenAI / Ollama
│   └── worker.py                 # QThread-обёртка для агента
├── ui/
│   ├── main_window.py            # QMainWindow: сплиттер дашборд/чат
│   ├── dashboard.py              # 3 карточки с графиками
│   ├── chat_panel.py             # чат-панель
│   ├── charts.py                 # рендер Gantt/Util/Output
│   └── style.qss                 # тёмная/светлая тема
└── storage/
    └── db.py                     # SQLite: история чата, снимки
```

## File: agent/__init__.py
```python

```

## File: agent/llm.py
```python
# agent/llm.py
⋮----
_cfg_full = load_cfg()
_cfg = _cfg_full.get("llm", {})
⋮----
provider = _cfg.get("provider", "ollama")
model_name = _cfg.get("model", "yandexgpt-5-pro/latest")
temperature = _cfg.get("temperature", 0.2)
max_steps = _cfg.get("max_steps", 8)
⋮----
client = None
⋮----
client = OpenAI()
⋮----
client = OpenAI(base_url=_cfg.get("base_url", "http://localhost:11434/v1"), api_key="ollama")
⋮----
api_key = os.environ.get("YANDEX_API_KEY") or _cfg.get("yc_api_key")
folder_id = os.environ.get("YANDEX_FOLDER_ID") or _cfg.get("yc_folder_id")
⋮----
client = OpenAI(
⋮----
SYSTEM = """Ты — ИИ-ассистент планировщика производства труб (участок ТБТ).
⋮----
def _prepare_messages_for_yandex(msgs: list[dict]) -> list[dict]
⋮----
"""
    Специальная очистка для YandexGPT.
    Убирает content, если есть tool_calls, и удаляет пустые сообщения.
    """
cleaned = []
⋮----
new_m = {"role": m["role"]}
⋮----
# Если есть tool_calls, YandexGPT не хочет видеть content вообще
⋮----
# Для обычных сообщений оставляем content, если он не пустой
content_str = str(m["content"]).strip()
⋮----
# Если текст пустой, лучше пропустить сообщение, чтобы не вызвать ошибку
⋮----
# Копируем остальные системные поля
⋮----
def run_agent(user_msg: str, history: list[dict] | None = None) -> dict
⋮----
charts: list[dict] = []
kpi_data: dict | None = None
⋮----
def _run_openai_compatible(user_msg, history, charts, kpi_data)
⋮----
# Формируем историю
msgs = [{"role": "system", "content": SYSTEM}] + (history or []) + \
⋮----
# Применяем очистку для YandexGPT
safe_msgs = _prepare_messages_for_yandex(msgs)
⋮----
resp = client.chat.completions.create(
m = resp.choices[0].message
⋮----
# Если модель вернула обычный текст
final_text = m.content if m.content and str(m.content).strip() else "Готово."
⋮----
# === КРИТИЧЕСКИЙ МОМЕНТ: Формируем сообщение ассистента ===
# Для YandexGPT мы НЕ добавляем поле "content", если есть tool_calls.
assistant_msg = {
# Добавляем content ТОЛЬКО если это реальный текст (не пустой)
⋮----
# Выполняем инструменты
⋮----
name = tc.function.name
⋮----
args = json.loads(tc.function.arguments or "{}")
⋮----
args = {}
⋮----
result = IMPL[name](**args)
⋮----
result = {"error": f"{type(e).__name__}: {e}"}
⋮----
kpi_data = result
⋮----
tool_content = {"ok": True, "chart_type": result["type"]}
⋮----
tool_content = result
⋮----
# Результат инструмента отправляем обратно
```

## File: agent/tools.py
```python
_svc = PlanningService("config.yaml")
⋮----
TOOLS = [
⋮----
def _payload_gantt()
⋮----
def _payload_util()
⋮----
h = _svc.cfg["horizon"]; t0 = datetime.fromisoformat(h["start"])
u = utilization(_svc.sched, t0, t0 + timedelta(days=h["days"]))
⋮----
def _payload_output()
⋮----
IMPL = {
```

## File: agent/worker.py
```python
class AgentWorker(QThread)
⋮----
finished = Signal(dict)       # {'text', 'charts', 'kpi'}
failed = Signal(str)
⋮----
def __init__(self, message: str, history: list[dict])
⋮----
def run(self)
```

## File: core/__init__.py
```python

```

## File: core/analytics.py
```python
def utilization(sched: pd.DataFrame, horizon_start, horizon_end) -> pd.DataFrame
⋮----
"""Загрузка РЦ: суммарные минуты операций / доступный фонд."""
total = (horizon_end - horizon_start).total_seconds() / 60
g = sched.groupby("operation")["duration_min"].sum().rename("busy_min").reset_index()
⋮----
def output_by_week(sched: pd.DataFrame) -> pd.DataFrame
⋮----
"""Выпуск по неделям (по завершению последней операции job'а)."""
last = sched.sort_values("seq").groupby("job_idx").tail(1).copy()
⋮----
def kpi(sched: pd.DataFrame, info: dict) -> dict
⋮----
last = sched.sort_values("seq").groupby("job_idx").tail(1)
late = last[last["end"] > last["due"]]
```

## File: core/bom.py
```python
# Из Разузловки: для каждой готовой номенклатуры ищем компоненты (заготовки),
# количество которых берётся из "Количество" (кг или мм — зависит от uom).
# Прототип: сопоставляем по префиксу кода в Номенклатуре.
# В проде — по "Ресурсная спецификация" (связь изделие -> ресурс).
⋮----
def explode(plan_row: pd.Series, bom: pd.DataFrame) -> list[dict]
⋮----
"""Возвращает список потребностей по заготовкам для одной позиции плана."""
item = str(plan_row["item"])
qty = int(plan_row["qty"])
⋮----
# Поиск компонентов: берём все строки BOM, где spec/материал указывает
# на заготовку, а код готового изделия НЕ совпадает с кодом (чтобы не ловить сам себя).
# Здесь — эвристика: ищем упоминание типоразмера изделия в полях BOM.
# Пример: "Труба ТБТ-К1-133-102-57/З-108" -> ищем "133-102" или "133х102".
key = _key_from_item(item)
comps = bom[bom["spec"].str.contains(key, na=False, regex=False)] if key else bom.iloc[0:0]
⋮----
result = []
⋮----
# Норма расхода: qty компонента в BOM * количество готовых
# (в реальности — делить на вес/длину; здесь — как есть)
⋮----
def _key_from_item(item: str) -> str | None
⋮----
"""Вытащить типоразмер из наименования: '133-102' из 'ТБТ-К1-133-102-...'."""
⋮----
m = re.search(r"(\d{3})[-x](\d{2,3})", item)
```

## File: core/loader.py
```python
# core/loader.py
⋮----
# Определяем корень проекта (папка, где лежит run.py и config.yaml)
ROOT_DIR = Path(__file__).resolve().parent.parent
⋮----
def _find_file(filename: str | Path) -> Path
⋮----
"""Ищет файл в текущей директории или в корне проекта."""
p = Path(filename)
⋮----
# Если не нашли, пробуем найти в корне проекта
p_root = ROOT_DIR / p
⋮----
def load_plan(path: str | Path) -> pd.DataFrame
⋮----
"""Лист 'План производства' -> нормализованный DataFrame."""
file_path = _find_file(path)
df = pd.read_excel(file_path, sheet_name=0)
df = df.rename(columns={
⋮----
# вытащим заказчика и номер заказа
⋮----
def load_bom(path: str | Path) -> pd.DataFrame
⋮----
"""Лист 'Разузловка' -> DataFrame с колонками code, item, spec, material, uom, qty."""
```

## File: core/routing.py
```python
# core/routing.py
⋮----
ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.yaml"
⋮----
class Routing
⋮----
def __init__(self, cfg: dict)
⋮----
def operations(self, group: str) -> list[str]
⋮----
"""Возвращает список операций (маршрут). Понимает любые названия групп."""
group_lower = str(group).lower()
⋮----
# Если группа содержит "полимер" (но не "не полимер"), берем маршрут для полимера
⋮----
ops = self.cfg.get("routing_polymer", [])
⋮----
ops = self.cfg.get("routing_non_polymer", [])
⋮----
# ЗАЩИТА: Если список пустой, возвращаем дефолтный маршрут
⋮----
ops = ["Резка", "ТО", "УЗК", "Мех.обработка", "Наплавка", "Сборка", "ОТК"]
⋮----
def op_time_min(self, op: str) -> int
⋮----
times = self.cfg.get("operation_times", {})
⋮----
def wc(self, op: str) -> dict
⋮----
centers = self.cfg.get("work_centers", {})
count = centers.get(op, 1)
# Если count пришел как словарь (старый формат), достаем из него
⋮----
count = count.get("count", 1)
⋮----
def load_cfg(path: str | Path = None) -> dict
⋮----
cfg_path = DEFAULT_CONFIG_PATH
⋮----
cfg_path = Path(path)
⋮----
cfg_path = ROOT_DIR / cfg_path
```

## File: core/scheduler.py
```python
# core/scheduler.py
⋮----
@dataclass
class Job
⋮----
idx: int
item: str
group: str
qty: int
due: datetime
customer: str
order_no: str
⋮----
@dataclass
class Op
⋮----
job_idx: int
op_name: str
duration_min: int
wc_slots: int          # сколько машин параллельно
seq_in_job: int
⋮----
class ORToolsScheduler
⋮----
"""CP-SAT планировщик Job-Shop с параллельными машинами и дедлайнами."""
⋮----
# ---------- построение модели ----------
def build(self, plan: pd.DataFrame) -> dict
⋮----
# 1. Проверка на наличие обязательных колонок в DataFrame
required_cols = ["item", "group", "qty", "due", "customer", "order_no"]
⋮----
# 2. Сборка списка задач (Jobs)
jobs: list[Job] = []
⋮----
# Безопасно обрабатываем дату (если NaT, ставим дефолтную)
due_date = r["due"]
⋮----
due_date = self.t0 + timedelta(days=self.horizon_min // 1440)
⋮----
# 3. Сборка списка операций (Ops)
ops: list[Op] = []
⋮----
seq = self.routing.operations(j.group)
⋮----
per_unit = self.routing.op_time_min(op_name)
# длительность = норма * кол-во, но не меньше 1 мин
dur = max(1, per_unit * j.qty // 10)  # /10 — условная "партия", калибруется
wc = self.routing.wc(op_name)
⋮----
# 4. Защитная проверка: если операций нет, выдаем понятную ошибку
⋮----
m = cp_model.CpModel()
H = self.horizon_min
⋮----
# start/end для каждой операции
⋮----
k = (o.job_idx, o.op_name, o.seq_in_job)
s = m.NewIntVar(0, H, f"s_{k}")
e = m.NewIntVar(0, H, f"e_{k}")
⋮----
# 1) последовательность внутри job
by_job: dict[int, list[Op]] = {}
⋮----
ka = (a.job_idx, a.op_name, a.seq_in_job)
kb = (b.job_idx, b.op_name, b.seq_in_job)
⋮----
# 2) мощность РЦ: на каждую операцию — пул из wc_slots машин
⋮----
pool = [o for o in ops if o.op_name == op_name]
slots = max(o.wc_slots for o in pool)
machine_intervals: list[list] = [[] for _ in range(slots)]
⋮----
presences = []
⋮----
b = m.NewBoolVar(f"pres_{k}_{slot}")
iv = m.NewOptionalIntervalVar(
⋮----
# 3) дедлайны и целевая функция
tardiness_vars = []
⋮----
last = max((o for o in ops if o.job_idx == j.idx), key=lambda x: x.seq_in_job)
k = (last.job_idx, last.op_name, last.seq_in_job)
due_min = int((j.due - self.t0).total_seconds() // 60)
t = m.NewIntVar(0, H + 100000, f"tard_{j.idx}")
⋮----
makespan = m.NewIntVar(0, H, "makespan")
⋮----
# ---------- решение ----------
def solve(self, plan: pd.DataFrame, time_limit_s: int = 30, workers: int = 8)
⋮----
data = self.build(plan)
solver = cp_model.CpSolver()
⋮----
status = solver.Solve(data["model"])
⋮----
rows = []
⋮----
s_min = solver.Value(data["starts"][k])
e_min = solver.Value(data["ends"][k])
j = data["jobs"][o.job_idx]
⋮----
sched = pd.DataFrame(rows).sort_values(["job_idx", "seq"]).reset_index(drop=True)
info = {
```

## File: storage/__init__.py
```python

```

## File: storage/db.py
```python
APP_DIR = Path(os.getenv("APPDATA") or Path.home() / ".planner") / "Planner"
⋮----
DB = APP_DIR / "planner.db"
⋮----
def _conn()
⋮----
c = sqlite3.connect(DB)
⋮----
def init()
⋮----
def add_msg(role: str, content: str)
⋮----
def history(limit: int = 40) -> list[dict]
⋮----
rows = c.execute("SELECT role, content FROM chat ORDER BY id DESC LIMIT ?",
⋮----
def save_snapshot(name: str, payload: dict)
⋮----
def last_snapshot(name: str) -> dict | None
⋮----
r = c.execute("SELECT payload FROM snapshots WHERE name=? ORDER BY id DESC LIMIT 1",
```

## File: ui/__init__.py
```python

```

## File: ui/chat_panel.py
```python
class ChatPanel(QWidget)
⋮----
charts_ready = Signal(list)
kpi_ready    = Signal(dict)
⋮----
def __init__(self)
⋮----
root = QVBoxLayout(self); root.setContentsMargins(10, 10, 10, 10)
⋮----
head = QHBoxLayout()
title = QLabel("ИИ-ассистент"); title.setObjectName("chatTitle")
⋮----
# быстрые кнопки
quick = QHBoxLayout()
⋮----
b = QPushButton(text); b.setObjectName("quickBtn")
⋮----
# лог
⋮----
# ввод
inp = QHBoxLayout()
⋮----
# ---------- отправка ----------
def send(self, text: str)
⋮----
text = (text or "").strip()
⋮----
hist = db.history(limit=20)
⋮----
def _on_done(self, res: dict)
⋮----
db.add_msg("user", self.input.text())  # уже добавлено в send — пропустим
⋮----
def _on_fail(self, err: str)
⋮----
def _busy(self, b: bool)
⋮----
# ---------- лог ----------
def _append(self, role: str, text: str)
⋮----
color = "#2563eb" if role == "user" else "#374151"
who = "Вы" if role == "user" else "Ассистент"
safe = (text or "").replace("\n", "<br>")
⋮----
def _restore_history(self)
⋮----
color = "#2563eb" if m["role"] == "user" else "#374151"
who = "Вы" if m["role"] == "user" else "Ассистент"
```

## File: ui/dashboard.py
```python
class KpiTile(QFrame)
⋮----
def __init__(self, title: str)
⋮----
lay = QVBoxLayout(self); lay.setContentsMargins(10, 6, 10, 6)
⋮----
def set(self, value)
⋮----
class Dashboard(QWidget)
⋮----
def __init__(self)
⋮----
root = QVBoxLayout(self); root.setContentsMargins(12, 12, 12, 12)
⋮----
# KPI-плашки
⋮----
# Графики: Gantt сверху, под ним — 2 в ряд
⋮----
bottom = QGridLayout()
⋮----
def _card(self, title: str, chart: QWidget) -> QFrame
⋮----
f = QFrame(); f.setObjectName("card")
lay = QVBoxLayout(f); lay.setContentsMargins(10, 8, 10, 8)
head = QLabel(title); head.setObjectName("cardTitle")
⋮----
def apply_charts(self, charts: list[dict])
⋮----
t = c.get("type")
⋮----
def apply_kpi(self, kpi: dict | None)
```

## File: ui/main_window.py
```python
class MainWindow(QMainWindow)
⋮----
def __init__(self)
⋮----
split = QSplitter(Qt.Horizontal)
⋮----
# сигналы чат → дашборд
⋮----
# восстановление последних графиков
⋮----
snap = db.last_snapshot(name)
⋮----
# восстановление KPI
```

## File: ui/style.css
```css
QMainWindow, QWidget { background: #f3f4f6; color: #1f2937;
⋮----
#card { background: #ffffff; border-radius: 10px; }
#cardTitle { font-size: 14px; font-weight: 600; color: #111827; }
⋮----
#kpiTile { background: #ffffff; border-radius: 10px; border: 1px solid #e5e7eb; }
#kpiValue { font-size: 18px; font-weight: 700; color: #111827; }
#kpiLabel { font-size: 11px; color: #6b7280; text-transform: uppercase; }
⋮----
#chatPanel { background: #ffffff; border-left: 1px solid #e5e7eb; }
#chatTitle { font-size: 15px; font-weight: 600; }
#chatStatus { font-size: 11px; color: #6b7280; }
#chatStatus[busy="true"] { color: #2563eb; }
⋮----
#quickBtn { font-size: 11px; padding: 5px 10px; border-radius: 14px;
#quickBtn:hover { background: #eef2ff; border-color: #c7d2fe; }
⋮----
#chatLog { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;
⋮----
QLineEdit { border: 1px solid #d1d5db; border-radius: 8px; padding: 7px 10px;
QLineEdit:focus { border-color: #2563eb; }
QPushButton { border: none; border-radius: 8px; padding: 7px 12px;
QPushButton:disabled { background: #93c5fd; }
QPushButton#quickBtn { background: #f9fafb; color: #1f2937; font-weight: 400; }
```

## File: build.spec
```
# build.spec
a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.yaml', '.'),
        ('ui/style.qss', 'ui'),
        ('План производства.xlsx', '.'),
        ('Разузловка.xlsx', '.'),
    ],
    hiddenimports=['ortools', 'pyqtgraph', 'openai'],
    hookspath=[], runtime_hooks=[],
    excludes=['tkinter', 'matplotlib'],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [],
          name='Planner',
          debug=False, strip=False, upx=True, console=False)
```

## File: requirements.txt
```
PySide6>=6.6
pyqtgraph>=0.13
pandas>=2.0
openpyxl>=3.1
ortools>=9.8
pydantic>=2.5
pyyaml>=6.0
openai>=1.30
httpx>=0.27
pyinstaller>=6.3          # только для сборки exe
```

## File: russian-trusted-cacert.pem
```
-----BEGIN CERTIFICATE-----
MIIHQjCCBSqgAwIBAgICEAIwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx
PzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu
ZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg
Q0EwHhcNMjIwMzAyMTEyNTE5WhcNMjcwMzA2MTEyNTE5WjBvMQswCQYDVQQGEwJS
VTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg
YW5kIENvbW11bmljYXRpb25zMR8wHQYDVQQDDBZSdXNzaWFuIFRydXN0ZWQgU3Vi
IENBMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA9YPqBKOk19NFymrE
wehzrhBEgT2atLezpduB24mQ7CiOa/HVpFCDRZzdxqlh8drku408/tTmWzlNH/br
HuQhZ/miWKOf35lpKzjyBd6TPM23uAfJvEOQ2/dnKGGJbsUo1/udKSvxQwVHpVv3
S80OlluKfhWPDEXQpgyFqIzPoxIQTLZ0deirZwMVHarZ5u8HqHetRuAtmO2ZDGQn
vVOJYAjls+Hiueq7Lj7Oce7CQsTwVZeP+XQx28PAaEZ3y6sQEt6rL06ddpSdoTMp
BnCqTbxW+eWMyjkIn6t9GBtUV45yB1EkHNnj2Ex4GwCiN9T84QQjKSr+8f0psGrZ
vPbCbQAwNFJjisLixnjlGPLKa5vOmNwIh/LAyUW5DjpkCx004LPDuqPpFsKXNKpa
L2Dm6uc0x4Jo5m+gUTVORB6hOSzWnWDj2GWfomLzzyjG81DRGFBpco/O93zecsIN
3SL2Ysjpq1zdoS01CMYxie//9zWvYwzI25/OZigtnpCIrcd2j1Y6dMUFQAzAtHE+
qsXflSL8HIS+IJEFIQobLlYhHkoE3avgNx5jlu+OLYe0dF0Ykx1PGNjbwqvTX37R
Cn32NMjlotW2QcGEZhDKj+3urZizp5xdTPZitA+aEjZM/Ni71VOdiOP0igbw6asZ
2fxdozZ1TnSSYNYvNATwthNmZysCAwEAAaOCAeUwggHhMBIGA1UdEwEB/wQIMAYB
Af8CAQAwDgYDVR0PAQH/BAQDAgGGMB0GA1UdDgQWBBTR4XENCy2BTm6KSo9MI7NM
XqtpCzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qwshzCBxwYIKwYBBQUH
AQEEgbowgbcwOwYIKwYBBQUHMAKGL2h0dHA6Ly9yb3N0ZWxlY29tLnJ1L2NkcC9y
b290Y2Ffc3NsX3JzYTIwMjIuY3J0MDsGCCsGAQUFBzAChi9odHRwOi8vY29tcGFu
eS5ydC5ydS9jZHAvcm9vdGNhX3NzbF9yc2EyMDIyLmNydDA7BggrBgEFBQcwAoYv
aHR0cDovL3JlZXN0ci1wa2kucnUvY2RwL3Jvb3RjYV9zc2xfcnNhMjAyMi5jcnQw
gbAGA1UdHwSBqDCBpTA1oDOgMYYvaHR0cDovL3Jvc3RlbGVjb20ucnUvY2RwL3Jv
b3RjYV9zc2xfcnNhMjAyMi5jcmwwNaAzoDGGL2h0dHA6Ly9jb21wYW55LnJ0LnJ1
L2NkcC9yb290Y2Ffc3NsX3JzYTIwMjIuY3JsMDWgM6Axhi9odHRwOi8vcmVlc3Ry
LXBraS5ydS9jZHAvcm9vdGNhX3NzbF9yc2EyMDIyLmNybDANBgkqhkiG9w0BAQsF
AAOCAgEARBVzZls79AdiSCpar15dA5Hr/rrT4WbrOfzlpI+xrLeRPrUG6eUWIW4v
Sui1yx3iqGLCjPcKb+HOTwoRMbI6ytP/ndp3TlYua2advYBEhSvjs+4vDZNwXr/D
anbwIWdurZmViQRBDFebpkvnIvru/RpWud/5r624Wp8voZMRtj/cm6aI9LtvBfT9
cfzhOaexI/99c14dyiuk1+6QhdwKaCRTc1mdfNQmnfWNRbfWhWBlK3h4GGE9JK33
Gk8ZS8DMrkdAh0xby4xAQ/mSWAfWrBmfzlOqGyoB1U47WTOeqNbWkkoAP2ys94+s
Jg4NTkiDVtXRF6nr6fYi0bSOvOFg0IQrMXO2Y8gyg9ARdPJwKtvWX8VPADCYMiWH
h4n8bZokIrImVKLDQKHY4jCsND2HHdJfnrdL2YJw1qFskNO4cSNmZydw0Wkgjv9k
F+KxqrDKlB8MZu2Hclph6v/CZ0fQ9YuE8/lsHZ0Qc2HyiSMnvjgK5fDc3TD4fa8F
E8gMNurM+kV8PT8LNIM+4Zs+LKEV8nqRWBaxkIVJGekkVKO8xDBOG/aN62AZKHOe
GcyIdu7yNMMRihGVZCYr8rYiJoKiOzDqOkPkLOPdhtVlgnhowzHDxMHND/E2WA5p
ZHuNM/m0TXt2wTTPL7JH2YC0gPz/BvvSzjksgzU5rLbRyUKQkgU=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIFwjCCA6qgAwIBAgICEAAwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx
PzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu
ZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg
Q0EwHhcNMjIwMzAxMjEwNDE1WhcNMzIwMjI3MjEwNDE1WjBwMQswCQYDVQQGEwJS
VTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg
YW5kIENvbW11bmljYXRpb25zMSAwHgYDVQQDDBdSdXNzaWFuIFRydXN0ZWQgUm9v
dCBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMfFOZ8pUAL3+r2n
qqE0Zp52selXsKGFYoG0GM5bwz1bSFtCt+AZQMhkWQheI3poZAToYJu69pHLKS6Q
XBiwBC1cvzYmUYKMYZC7jE5YhEU2bSL0mX7NaMxMDmH2/NwuOVRj8OImVa5s1F4U
zn4Kv3PFlDBjjSjXKVY9kmjUBsXQrIHeaqmUIsPIlNWUnimXS0I0abExqkbdrXbX
YwCOXhOO2pDUx3ckmJlCMUGacUTnylyQW2VsJIyIGA8V0xzdaeUXg0VZ6ZmNUr5Y
Ber/EAOLPb8NYpsAhJe2mXjMB/J9HNsoFMBFJ0lLOT/+dQvjbdRZoOT8eqJpWnVD
U+QL/qEZnz57N88OWM3rabJkRNdU/Z7x5SFIM9FrqtN8xewsiBWBI0K6XFuOBOTD
4V08o4TzJ8+Ccq5XlCUW2L48pZNCYuBDfBh7FxkB7qDgGDiaftEkZZfApRg2E+M9
G8wkNKTPLDc4wH0FDTijhgxR3Y4PiS1HL2Zhw7bD3CbslmEGgfnnZojNkJtcLeBH
BLa52/dSwNU4WWLubaYSiAmA9IUMX1/RpfpxOxd4Ykmhz97oFbUaDJFipIggx5sX
ePAlkTdWnv+RWBxlJwMQ25oEHmRguNYf4Zr/Rxr9cS93Y+mdXIZaBEE0KS2iLRqa
OiWBki9IMQU4phqPOBAaG7A+eP8PAgMBAAGjZjBkMB0GA1UdDgQWBBTh0YHlzlpf
BKrS6badZrHF+qwshzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qwshzAS
BgNVHRMBAf8ECDAGAQH/AgEEMA4GA1UdDwEB/wQEAwIBhjANBgkqhkiG9w0BAQsF
AAOCAgEAALIY1wkilt/urfEVM5vKzr6utOeDWCUczmWX/RX4ljpRdgF+5fAIS4vH
tmXkqpSCOVeWUrJV9QvZn6L227ZwuE15cWi8DCDal3Ue90WgAJJZMfTshN4OI8cq
W9E4EG9wglbEtMnObHlms8F3CHmrw3k6KmUkWGoa+/ENmcVl68u/cMRl1JbW2bM+
/3A+SAg2c6iPDlehczKx2oa95QW0SkPPWGuNA/CE8CpyANIhu9XFrj3RQ3EqeRcS
AQQod1RNuHpfETLU/A2gMmvn/w/sx7TB3W5BPs6rprOA37tutPq9u6FTZOcG1Oqj
C/B7yTqgI7rbyvox7DEXoX7rIiEqyNNUguTk/u3SZ4VXE2kmxdmSh3TQvybfbnXV
4JbCZVaqiZraqc7oZMnRoWrXRG3ztbnbes/9qhRGI7PqXqeKJBztxRTEVj8ONs1d
WN5szTwaPIvhkhO3CO5ErU2rVdUr89wKpNXbBODFKRtgxUT70YpmJ46VVaqdAhOZ
D9EUUn4YaeLaS8AjSF/h7UkjOibNc4qVDiPP+rkehFWM66PVnP1Msh93tc+taIfC
EYVMxjh8zNbFuoc7fzvvrFILLe7ifvEIUqSVIC/AzplM/Jxw7buXFeGP1qVCBEHq
391d/9RAfaZ12zkwFsl+IKwE/OZxW8AHa9i1p4GO0YSNuczzEm4=
-----END CERTIFICATE-----
```

## File: core/service.py
```python
# core/service.py
⋮----
class PlanningService
⋮----
def __init__(self, cfg_path="config.yaml")
⋮----
def load_data(self) -> dict
⋮----
def plan_schedule(self, time_limit_s: int = 30, tardiness_weight: float = 10.0) -> dict
⋮----
h = self.cfg["horizon"]
⋮----
# --- ИЗМЕНЕНИЕ: Планируем с текущей даты ---
t0 = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
⋮----
horizon_min = h["days"] * h["minutes_per_shift"] * h["shifts_per_day"]
sch = ORToolsScheduler(self.routing, t0, horizon_min,
⋮----
# ... остальные методы остаются без изменений ...
```

## File: ui/charts.py
```python
# ui/charts.py
⋮----
OP_COLORS = {
⋮----
class GanttChart(QWidget)
⋮----
def __init__(self)
⋮----
axis_x = pg.DateAxisItem(orientation='bottom')
⋮----
# --- ИЗМЕНЕНИЕ: Настройка оси Y ---
ax_y = self.plot.getAxis("left")
# Увеличиваем ширину оси, чтобы влезали названия заказов
⋮----
# Задаем шрифт для подписей
⋮----
lay = QVBoxLayout(self)
⋮----
def render(self, payload: dict)
⋮----
rows = payload.get("data") or []
⋮----
# Формируем уникальные подписи
labels = list(dict.fromkeys(r["label"] for r in rows))
y_index = {lab: i for i, lab in enumerate(labels)}
⋮----
start_ts = datetime.fromisoformat(r["start"]).timestamp()
end_ts = datetime.fromisoformat(r["end"]).timestamp()
duration = end_ts - start_ts
⋮----
y = y_index[r["label"]]
color = OP_COLORS.get(r["operation"], "#94a3b8")
⋮----
# Рисуем полосу
item = pg.BarGraphItem(
⋮----
# --- ИЗМЕНЕНИЕ: Принудительно задаем тики для оси Y ---
⋮----
# Обрезаем строку, если она слишком длинная, чтобы не ломать график
ticks = [(i, str(lab)[:45]) for lab, i in y_index.items()]
⋮----
# Рассчитываем границы X
min_time = min(datetime.fromisoformat(r["start"]).timestamp() for r in rows)
max_time = max(datetime.fromisoformat(r["end"]).timestamp() for r in rows)
⋮----
# Отступ по 2 дня с каждой стороны, чтобы график не "прилипал" к краям
⋮----
# Остальные классы (UtilChart и OutputChart) оставляем без изменений
class UtilChart(QWidget)
⋮----
lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.addWidget(self.plot)
⋮----
ops = [r["operation"] for r in rows]
vals = [r["utilization_pct"] for r in rows]
x = list(range(len(ops)))
⋮----
brushes = [pg.mkBrush("#ef4444" if v > 90 else "#f59e0b" if v > 70 else "#10b981") for v in vals]
bars = pg.BarGraphItem(x=x, height=vals, width=0.6, brushes=brushes)
⋮----
ax = self.plot.getAxis("bottom")
⋮----
class OutputChart(QWidget)
⋮----
weeks = [r["week"] for r in rows]
qty = [r["qty"] for r in rows]
jobs = [r["jobs"] for r in rows]
x = list(range(len(weeks)))
```

## File: .gitignore
```
# Виртуальное окружение
venv/
.venv/
env/

# Кэш Python
__pycache__/
*.py[cod]
*.egg-info/
build/
dist/

__pycache__/
*.pyc


# Файлы IDE
.vscode/
.idea/

# Секреты и настройки окружения
.env
.env.*

# Логи и временные файлы
*.log
*.tmp

# Файлы выгрузки (результаты работы программы)
exports/
output/
out/
results/
reports/
*.csv
*.xlsx
*.xls
*.json.gz
*.parquet
*.sqlite
*.db

# Системные файлы
.DS_Store
Thumbs.db
__pycache__/
*.pyc
```

## File: config.yaml
```yaml
files:
  plan: "План производства.xlsx"
  bom: "Разузловка.xlsx"

horizon:
  start: "2026-04-01"
  days: 260
  minutes_per_shift: 480
  shifts_per_day: 2

llm:
  provider: "yandexgpt"
  model: "gpt://b1g445gcc12vkbeu2iqv/yandexgpt-5-pro/latest"  # Замените <ВАШ_FOLDER_ID>
  temperature: 0.2
  max_steps: 8
  
 

routing_polymer:
  - "Резка"
  - "ТО"
  - "УЗК"
  - "Мех.обработка"
  - "Наплавка"
  - "Полимер"
  - "Сборка"
  - "ОТК"

routing_non_polymer:
  - "Резка"
  - "ТО"
  - "УЗК"
  - "Мех.обработка"
  - "Наплавка"
  - "Сборка"
  - "ОТК"

operation_times:
  "Резка": 6
  "ТО": 180
  "УЗК": 25
  "Мех.обработка": 90
  "Наплавка": 120
  "Полимер": 60
  "Сборка": 45
  "ОТК": 30

work_centers:
  "Резка": 2
  "ТО": 1
  "УЗК": 1
  "Мех.обработка": 3
  "Наплавка": 2
  "Полимер": 1
  "Сборка": 2
  "ОТК": 1
```

## File: run.py
```python
def main()
⋮----
app = QApplication(sys.argv)
⋮----
qss = Path(__file__).parent / "ui" / "style.qss"
⋮----
w = MainWindow()
```
