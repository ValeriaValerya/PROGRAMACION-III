#!/usr/bin/env python3

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "Data"
OUTPUT_JSON = DATA_DIR / "agente_no_vacios.json"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

resultado = {
    "agent": "no_vacios",
    "weights": {
        "w_no_vacios": 40
    },
    "note": "Evita semestres completamente vacíos."
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Agente no_vacios (soft) ejecutado.")
print(f"Guardado en: {OUTPUT_JSON}")