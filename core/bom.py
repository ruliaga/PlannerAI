# core/bom.py
"""Разузловка сборок ТБТ до заготовок и металла по правилам core.rules.

Источники:
  - РС сборок (лист «Ресусные сп.» файла files.bom): сборка -> Муфта, Ниппель,
    Тело, Заготовка под тела, Заготовка под замки (все по 1 шт на трубу).
  - РС проката (files.metal_rs): код заготовки -> материал и норма кг на 1 заготовку.

Важно: «вес N» в наименовании заготовки — это КГ НА МЕТР
(норма РС = вес/м × длина: 85 кг/м × 8,3 м = 705,5 кг — сходится с РС).
"""
from __future__ import annotations

import re
from typing import Optional

import pandas as pd

from core import rules
from core.loader import _find_file

_ROLE_MAP = (("труба (сборка)", "сборка"), ("муфта", "муфта"),
             ("ниппель", "ниппель"), ("тело", "тело"),
             ("заготовка под замки", "заготовка под замки"),
             ("заготовка под тела", "заготовка под тела"))

def normalize_role(raw: str) -> str:
    s = str(raw).strip().lower()
    for pat, role in _ROLE_MAP:
        if s.startswith(pat):
            return role
    return s

def assembly_key(item: str) -> str:
    """'СТБТ.К1.168.127.76.133.812.000-01 Труба ...' -> 'СТБТ.812-01';
    'СТБТ.1506.000-01 ...' -> 'СТБТ.1506-01'; 'СТБТ.1742.000 ...' -> 'СТБТ.1742'."""
    s = str(item).strip()
    if not s.upper().startswith("СТБТ"):
        return s
    body = s.split()[0]
    m = re.search(r"\.000(-\d+)?", body)
    suffix = m.group(1) if (m and m.group(1)) else ""
    body = re.sub(r"\.000(-\d+)?$", "", body)
    nums = re.findall(r"\d+", body)
    return f"СТБТ.{nums[-1]}{suffix}" if nums else s


def _num(m) -> Optional[float]:
    return float(m.group(1).replace(",", ".").replace(" ", "")) if m else None


def parse_blank(name: str) -> dict:
    """Разбор наименования заготовки. 'вес N' = кг/м."""
    s, low = str(name), str(name).lower()
    rng = re.search(r"L\s*=\s*(\d+)(?:\s*[-–—]\s*(\d+))?", s, re.I)
    return {"kind": "круг" if "круг" in low else "труба",
            "d_in": _num(re.search(r"D\s*вн\s*=\s*(\d+(?:[.,]\d+)?)", s, re.I)),
            "d_out": _num(re.search(r"D\s*нар\s*=\s*(\d+(?:[.,]\d+)?)", s, re.I)),
            "l_from": int(rng.group(1)) if rng else None,
            "l_to": int(rng.group(2)) if (rng and rng.group(2)) else (int(rng.group(1)) if rng else None),
            "kg_per_m": _num(re.search(r"вес\s*(\d+(?:[.,]\d+)?)", low)),
            "for_locks": "под замки" in low, "for_bodies": "под тела" in low}


def parse_material(material: str) -> dict:
    """'Круг 129х9600 40ХГМА ТС ...' -> {desc, d, pallet_len_mm, steel}."""
    s = str(material)
    m = re.search(r"круг\s*(\d+(?:[.,]\d+)?)\s*[xх×]\s*(\d+)", s.lower())
    if m:
        return {"desc": f"Круг {m.group(1)}×{m.group(2)}", "d": float(m.group(1).replace(",", ".")),
                "pallet_len_mm": int(m.group(2)), "steel": s.split("/")[-1].strip() if "/" in s else None}
    m = re.search(r"труба\s*(\d+(?:[.,]\d+)?)\s*[xх×]\s*(\d+(?:[.,]\d+)?)(?:\s*[xх×]\s*(\d+))?", s.lower())
    if m:
        length = int(m.group(3)) if m.group(3) else None
        desc = (f"Труба {m.group(1)}×{m.group(2)}×{m.group(3)}" if length
                else f"Труба {m.group(1)}×{m.group(2)}")
        return {"desc": desc, "d": float(m.group(1).replace(",", ".")),
                "pallet_len_mm": length, "steel": s.split("/")[-1].strip() if "/" in s else None}
    return {"desc": s.split("/")[0].strip(), "d": None, "pallet_len_mm": None,
            "steel": s.split("/")[-1].strip() if "/" in s else None}


def _norm_name(s: str) -> str:
    return re.sub(r"\s+", " ", str(s)).strip().lower()


class MetalRS:
    """Индекс РС проката: поиск по наименованию заготовки, затем по (Dнар, кг/м)."""

    def __init__(self, df: pd.DataFrame):
        self.by_name: dict[str, dict] = {}
        self.by_dim: dict[tuple, dict] = {}
        for _, r in df.iterrows():
            b = parse_blank(r["item"])
            mat = parse_material(r.get("material", ""))
            rec = {"code": r.get("code"), "item": r["item"], "material": r.get("material", ""),
                   "kg_norm": float(r["qty"]), "kg_per_m": b["kg_per_m"],
                   "pallet_len_mm": mat["pallet_len_mm"] or b["l_to"],
                   "steel": mat["steel"], "desc": mat["desc"]}
            self.by_name[_norm_name(r["item"])] = rec
            if b["d_out"] is not None and b["kg_per_m"] is not None:
                self.by_dim.setdefault((b["d_out"], b["kg_per_m"]), rec)

    def find(self, blank_name: str, blank_info: dict) -> Optional[dict]:
        rec = self.by_name.get(_norm_name(blank_name))
        if rec:
            return rec
        rec = self.by_dim.get((blank_info["d_out"], blank_info["kg_per_m"]))
        return dict(rec, note="норма по совпадению Dнар и кг/м") if rec else None


def load_assembly_rs(path) -> pd.DataFrame:
    """Читает лист «Ресусные сп.»: секции
    'СТБТ.1742      РН-БУРЕНИЕ' + строки 'Роль | Номенклатура | Код РС'."""
    xl = pd.read_excel(_find_file(path), sheet_name=None, header=None)
    sheet = next((n for n in xl if "есусн" in n.lower() or "есурсн" in n.lower()), next(iter(xl)))
    raw = xl[sheet].fillna("")
    rows, current = [], None
    for _, r in raw.iterrows():
        a, b, c3 = (str(r.iloc[0]).strip(), str(r.iloc[1]).strip(), str(r.iloc[2]).strip())
        if re.match(r"^СТБТ", a, re.I) and b == "" and c3 == "":
            m = re.match(r"^(СТБТ[\w.\-]*)\s+(.+)$", a)
            current = (m.group(1).strip(), m.group(2).strip()) if m else None
            continue
        if current and a and not a.lower().startswith("разузловка"):
            role = normalize_role(a)
            if role != str(a).strip().lower():      # строка распознана как роль
                rows.append({"assembly": assembly_key(current[0]), "customer": current[1],
                             "role": a, "role_n": role, "item": b, "code": c3})
    return pd.DataFrame(rows)


def explode_plan(plan: pd.DataFrame, rs: pd.DataFrame,
                 metal: Optional[MetalRS]) -> pd.DataFrame:
    """Потребность по всем позициям плана: сборка -> комплектующие -> заготовки -> металл."""
    out = []
    for _, p in plan.iterrows():
        asm, qty, cust = assembly_key(p["item"]), int(p["qty"]), str(p.get("customer", ""))
        lt = rules.resolve_lock_type(customer=cust, assembly=asm)
        set_mm = rules.lock_set_mm(lt)
        sub = rs[rs["assembly"] == asm]
        if sub.empty:
            out.append({"order_no": p.get("order_no"), "customer": cust, "assembly": asm,
                        "qty": qty, "role": "-", "component": f"РС не найдена: {asm}",
                        "code": "", "note": "нет РС"})
            continue
        for _, c in sub.iterrows():
            role, base = c["role_n"], {"order_no": p.get("order_no"), "customer": cust,
                                       "assembly": asm, "qty": qty, "role": role,
                                       "component": c["item"], "code": c["code"],
                                       "per_unit": 1, "total": qty, "note": ""}
            if role in ("муфта", "ниппель", "тело"):
                out.append({**base, "blank_code": "", "blank_name": "", "kg_per_m": None,
                            "pallet_len_mm": None, "lock_type": lt, "set_mm": set_mm if role != "тело" else None,
                            "total_mm": None, "pallets": None, "kg": None})
            elif role == "заготовка под тела":
                b = parse_blank(c["item"])
                kg = (metal.find(c["item"], b) or {}).get("kg_norm") if metal else None
                if kg is None and b["kg_per_m"]:
                    kg = b["kg_per_m"] * b["l_to"] / 1000.0
                out.append({**base, "blank_code": c["code"], "blank_name": c["item"],
                            "kg_per_m": b["kg_per_m"], "pallet_len_mm": b["l_to"],
                            "lock_type": lt, "set_mm": None,
                            "total_mm": qty * (b["l_from"] or 0), "pallets": qty, "kg": kg})
            elif role == "заготовка под замки":
                b = parse_blank(c["item"])
                pallet_len = b["l_to"] or 9600
                m = rules.metal_for_locks([(lt, qty)], b["kg_per_m"] or 0, pallet_len)
                out.append({**base, "blank_code": c["code"], "blank_name": c["item"],
                            "kg_per_m": b["kg_per_m"], "pallet_len_mm": pallet_len,
                            "lock_type": lt, "set_mm": set_mm, "total_mm": m["total_mm"],
                            "pallets": m["pallets"], "kg": m["kg"]})
    return pd.DataFrame(out)


def procurement(req: pd.DataFrame) -> pd.DataFrame:
    """Сводная закупка металла. Для замков — смешанный раскрой между сборками,
    использующими один прокат (правила rules.metal_for_locks)."""
    out = []
    locks = req[req["role"] == "заготовка под замки"]
    for name, g in locks.groupby("blank_name"):
        groups = [(lt, int(s)) for lt, s in g.groupby("lock_type")["qty"].sum().items()]
        m = rules.metal_for_locks(groups, g["kg_per_m"].iloc[0], g["pallet_len_mm"].iloc[0])
        out.append({"blank": name, "role": "замки", "pallets": m["pallets"], "kg": m["kg"],
                    "cut": m["cut"], "by_type": m["by_type"]})
    bodies = req[req["role"] == "заготовка под тела"]
    for name, g in bodies.groupby("blank_name"):
        out.append({"blank": name, "role": "тела", "pallets": int(g["pallets"].sum()),
                    "kg": round(float(g["kg"].sum()), 1), "cut": None, "by_type": None})
    return pd.DataFrame(out).sort_values("kg", ascending=False).reset_index(drop=True)
