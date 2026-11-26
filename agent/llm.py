# agent/llm.py
from __future__ import annotations
import json
import os
from openai import OpenAI
from agent.tools import TOOLS, IMPL
from core.routing import load_cfg

_cfg_full = load_cfg()
_cfg = _cfg_full.get("llm", {})

provider = _cfg.get("provider", "ollama")
model_name = _cfg.get("model", "yandexgpt-5-pro/latest")
temperature = _cfg.get("temperature", 0.2)
max_steps = _cfg.get("max_steps", 8)

client = None

if provider == "openai":
    client = OpenAI()
elif provider == "ollama":
    client = OpenAI(base_url=_cfg.get("base_url", "http://localhost:11434/v1"), api_key="ollama")
elif provider == "yandexgpt":
    api_key = os.environ.get("YANDEX_API_KEY") or _cfg.get("yc_api_key")
    folder_id = os.environ.get("YANDEX_FOLDER_ID") or _cfg.get("yc_folder_id")
    
    if not api_key or not folder_id:
        raise ValueError("Для YandexGPT не заданы ключи!")
        
    client = OpenAI(
        base_url="https://ai.api.cloud.yandex.net/v1",
        api_key=api_key,
        default_headers={"x-folder-id": folder_id},
    )

SYSTEM = """Ты — ИИ-ассистент планировщика производства труб (участок ТБТ).
У тебя есть инструменты (функции), которые ты ОБЯЗАН вызывать для выполнения команд.

Инструменты: load_data, plan_schedule, get_kpi, get_utilization, get_output,
get_late_jobs, change_priority, export_schedule, chart_gantt, chart_utilization, chart_output.

ПРАВИЛА:
1. «План/расписание» → вызови load_data, затем plan_schedule, затем chart_gantt + chart_utilization.
2. «Загрузка/узкие места» → вызови chart_utilization + get_utilization.
3. «Что опаздывает» → вызови get_late_jobs.
4. «Подними приоритет X» → вызови change_priority(order_no=X), plan_schedule, get_kpi, chart_gantt.
5. КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО просить пользователя ввести данные вручную. Ты должен САМ вызвать функцию.
6. Отвечай по-русски, кратко, с цифрами и единицами.
ПРАВИЛА РАСЧЁТА МЕТАЛЛА (обязательно через инструмент calc_metal, не считай сам):
- Тело: на 1 трубу — 1 ЦЕЛАЯ палка металла, кг берётся из РС проката.
- Замки: на комплект «муфта+ниппель» — 1500 мм (обычные) или 1800 мм (удлинённые).
- По умолчанию: Газпром — удлинённые (long), остальные заказчики — обычные (regular).
- С палки выходит floor(длина палки / мм на комплект) комплектов; остаток — отход.
- Вопросы «сколько металла на N труб …», «сколько круга, если замки укороченные» —
  всегда через calc_metal с указанием lock_type, если пользователь задал тип замков.
- Переключить тип замков по умолчанию — set_lock_type (сборка, заказчик или глобально).
- Список сборок — list_assemblies. Портфель целиком — calc_metal_portfolio.

"""

def _prepare_messages_for_yandex(msgs: list[dict]) -> list[dict]:
    """
    Специальная очистка для YandexGPT.
    Убирает content, если есть tool_calls, и удаляет пустые сообщения.
    """
    cleaned = []
    for m in msgs:
        new_m = {"role": m["role"]}
        
        # Если есть tool_calls, YandexGPT не хочет видеть content вообще
        if m.get("tool_calls"):
            new_m["tool_calls"] = m["tool_calls"]
        elif "content" in m and m["content"] is not None:
            # Для обычных сообщений оставляем content, если он не пустой
            content_str = str(m["content"]).strip()
            if content_str:
                new_m["content"] = m["content"]
            else:
                # Если текст пустой, лучше пропустить сообщение, чтобы не вызвать ошибку
                continue
        
        # Копируем остальные системные поля
        for k in ("tool_call_id", "name"):
            if k in m:
                new_m[k] = m[k]
                
        cleaned.append(new_m)
    return cleaned

def run_agent(user_msg: str, history: list[dict] | None = None) -> dict:
    charts: list[dict] = []
    kpi_data: dict | None = None
    return _run_openai_compatible(user_msg, history, charts, kpi_data)

def _run_openai_compatible(user_msg, history, charts, kpi_data):
    # Формируем историю
    msgs = [{"role": "system", "content": SYSTEM}] + (history or []) + \
           [{"role": "user", "content": user_msg}]

    for _ in range(max_steps):
        # Применяем очистку для YandexGPT
        safe_msgs = _prepare_messages_for_yandex(msgs)
        
        try:
            resp = client.chat.completions.create(
                model=model_name, 
                messages=safe_msgs, 
                tools=TOOLS,
                tool_choice="auto", 
                temperature=temperature
            )
            m = resp.choices[0].message
        except Exception as e:
            return {"text": f"⚠ Ошибка API: {e}", "charts": charts, "kpi": kpi_data}

        if not m.tool_calls:
            # Если модель вернула обычный текст
            final_text = m.content if m.content and str(m.content).strip() else "Готово."
            return {"text": final_text, "charts": charts, "kpi": kpi_data}

        # === КРИТИЧЕСКИЙ МОМЕНТ: Формируем сообщение ассистента ===
        # Для YandexGPT мы НЕ добавляем поле "content", если есть tool_calls.
        assistant_msg = {
            "role": "assistant",
            "tool_calls": [tc.model_dump() for tc in m.tool_calls]
        }
        # Добавляем content ТОЛЬКО если это реальный текст (не пустой)
        if m.content and str(m.content).strip():
            assistant_msg["content"] = m.content
        
        msgs.append(assistant_msg)

        # Выполняем инструменты
        for tc in m.tool_calls:
            name = tc.function.name
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            
            try:
                result = IMPL[name](**args)
            except Exception as e:
                result = {"error": f"{type(e).__name__}: {e}"}

            if name == "get_kpi" and isinstance(result, dict):
                kpi_data = result
            if name.startswith("chart_") and isinstance(result, dict):
                charts.append(result)
                tool_content = {"ok": True, "chart_type": result["type"]}
            else:
                tool_content = result

            # Результат инструмента отправляем обратно
            msgs.append({
                "role": "tool", 
                "tool_call_id": tc.id,
                "content": json.dumps(tool_content, ensure_ascii=False, default=str)[:20000]
            })
            
    return {"text": "Не удалось завершить за отведённые шаги.", "charts": charts, "kpi": kpi_data}
