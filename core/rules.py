# core/rules.py
"""Технологические правила расчёта заготовок и металла (участок ТБТ).

Единственный источник правил для core.bom, core.service, agent.tools и UI.

Правила:
  1. Тело: на 1 тело трубы уходит 1 ЦЕЛАЯ палка металла (без распила).
  2. Замки: на один комплект «муфта + ниппель» уходит 1500 мм палки (обычные
     замки) или 1800 мм (удлинённые). С палки выходит
     floor(длина_палки / мм_на_комплект) комплектов, остаток — отход.
  3. По умолчанию удлинённые замки — у заказчиков из customers_long (Газпром),
     у остальных — обычные.

Приоритет типа замков:
  override по сборке > override по заказчику > глобальный override >
  заказчик (customers_long) > default.
"""
from __future__ import annotations

import math
from functools import lru_cache
from typing import Optional

LOCK_SET_MM = {"regular": 1500, "long": 1800}
LOCK_LABELS = {"regular": "обычные (1500 мм на комплект)",
               "long": "удлинённые (1800 мм на комплект)"}
BODY_PALLETS_PER_UNIT = 1                      # под тело — целая палка на 1 тело
DEFAULT_CUSTOMERS_LONG = ("Газпром",)

try:
    from core.routing import load_cfg
    _locks_cfg = (load_cfg() or {}).get("rules", {}).get("locks", {})
except Exception:
    _locks_cfg = {}

CUSTOMERS_LONG = tuple(_locks_cfg.get("customers_long", DEFAULT_CUSTOMERS_LONG))
DEFAULT_LOCK_TYPE = _locks_cfg.get("default", "regular")


def lock_set_mm(lock_type: str) -> int:
    """мм палки на один комплект замков."""
    return int(LOCK_SET_MM.get(lock_type, LOCK_SET_MM["regular"]))


def _db():
    try:
        from storage import db
        return db
    except Exception:
        return None


def override_for(assembly: str = "", customer: str = "") -> Optional[str]:
    """Сохранённый override типа замков, если он есть."""
    d = _db()
    if d is None:
        return None
    keys = [f"lock_override:{str(assembly).strip().lower()}"] if assembly else []
    if customer:
        keys.append(f"lock_override:customer:{str(customer).strip().lower()}")
    keys.append("lock_global_override")
    for key in keys:
        v = d.get_setting(key)
        if v in LOCK_SET_MM:
            return v
    return None


def set_override(assembly: str = "", customer: str = "", value: Optional[str] = None):
    """Сохранить override в БД (value=None — снять)."""
    d = _db()
    if d is None:
        raise RuntimeError("storage.db недоступен")
    key = (f"lock_override:{assembly.strip().lower()}" if assembly
           else f"lock_override:customer:{customer.strip().lower()}")
    if value is None:
        d.del_setting(key)
    else:
        if value not in LOCK_SET_MM:
            raise ValueError("lock_type должен быть 'regular' или 'long'")
        d.set_setting(key, value)


def resolve_lock_type(customer: str = "", assembly: str = "") -> str:
    """Итоговый тип замков: override (БД) -> заказчик -> default."""
    o = override_for(assembly=assembly, customer=customer)
    if o:
        return o
    c = (customer or "").lower()
    if any(k.lower() in c for k in CUSTOMERS_LONG):
        return "long"
    return DEFAULT_LOCK_TYPE


def metal_for_bodies(qty: int, kg_per_m: float, pallet_len_mm: int) -> dict:
    """Тело: 1 труба = 1 целая палка металла, без распила."""
    qty = int(qty)
    return {"units": qty, "pallets": qty,
            "kg": round(qty * kg_per_m * pallet_len_mm / 1000.0, 1)}


def _fill_pallets_exact(n_long: int, n_reg: int, L: int) -> list[dict]:
    """Минимальное число палок для набора комплектов 1800 и 1500 мм.
    Палка заполняется комбинациями (a длинных, b обычных):
    a*1800 + b*1500 <= L. Точный перебор с мемоизацией — размеры малы."""
    lp, rp = L // LOCK_SET_MM["long"], L // LOCK_SET_MM["regular"]
    if lp <= 0 and rp <= 0:
        raise ValueError("палка короче комплекта замков")
    if lp <= 0:   # палка не вмещает удлинённый комплект — по 1 в палку
        out = [{"regular": rp} for _ in range(math.ceil(n_reg / rp))]
        out += [{"long": 1} for _ in range(n_long)]
        return out

    pairs = [(a, (L - a * LOCK_SET_MM["long"]) // LOCK_SET_MM["regular"])
             for a in range(lp + 1)]

    @lru_cache(maxsize=None)
    def f(nl: int, nr: int) -> int:
        if nl <= 0 and nr <= 0:
            return 0
        if nl <= 0:
            return math.ceil(nr / rp)
        if nr <= 0:
            return math.ceil(nl / lp)
        best = None
        for a, bmax in pairs:
            a2, b2 = min(a, nl), min(bmax, nr)
            if a2 == 0 and b2 == 0:
                continue
            v = 1 + f(nl - a2, nr - b2)
            if best is None or v < best:
                best = v
        return best

    n = f(n_long, n_reg)
    cut, nl, nr, remaining = [], n_long, n_reg, n
    while remaining > 0:
        if nl == 0:
            full = nr // rp
            if full:
                cut += [{"regular": rp}] * full
                nr -= full * rp
                remaining -= full
                if nr == 0:
                    break
            cut.append({"regular": nr}); nr = 0; remaining -= 1
            continue
        if nr == 0:
            full = nl // lp
            if full:
                cut += [{"long": lp}] * full
                nl -= full * lp
                remaining -= full
                if nl == 0:
                    break
            cut.append({"long": nl}); nl = 0; remaining -= 1
            continue
        for a, bmax in pairs:                      # восстановление распределения
            a2, b2 = min(a, nl), min(bmax, nr)
            if a2 == 0 and b2 == 0:
                continue
            if 1 + f(nl - a2, nr - b2) == remaining:
                cut.append({"long": a2, "regular": b2} if b2 else {"long": a2})
                nl -= a2; nr -= b2; remaining -= 1
                break
    return cut


def metal_for_locks(groups, kg_per_m: float, pallet_len_mm: int) -> dict:
    """Замки: комплекты режутся из целых палок по правилу 1500/1800 мм.
    groups: [(lock_type, комплектов), ...] — можно по нескольким сборкам,
    использующим один и тот же прокат: раскрой считается суммарно."""
    by_type = {"long": 0, "regular": 0}
    for lt, s in groups:
        if lt not in LOCK_SET_MM:
            raise ValueError(f"неизвестный тип замков: {lt}")
        by_type[lt] += int(s)
    total = by_type["long"] + by_type["regular"]
    if total == 0:
        return {"sets": 0, "by_type": by_type, "per_pallet": None,
                "pallets": 0, "cut": [], "kg": 0.0}
    cut = _fill_pallets_exact(by_type["long"], by_type["regular"], int(pallet_len_mm))
    single = [lt for lt in ("long", "regular") if by_type[lt] > 0]
    per_pallet = (max(1, int(pallet_len_mm) // LOCK_SET_MM[single[0]])
                  if len(single) == 1 else None)      # при смешанном раскрое — см. cut
    return {"sets": total, "by_type": by_type, "per_pallet": per_pallet,
            "pallets": len(cut), "cut": cut,
            "kg": round(len(cut) * kg_per_m * int(pallet_len_mm) / 1000.0, 1)}
