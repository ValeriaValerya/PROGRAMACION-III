import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "Data"
OUTPUT_JSON = DATA_DIR / "agent_minimizar.json"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

resultado = {
    "agent": "minimizar",
    "weights": {
        "w_low": 10,   
        "w_no_vacios": 5, 
        "w_balance": 20
    },
    "target_creditos": 15,
    "note": "Minimiza desviación global de carga entre semestres."
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Agente minimizar (soft) ejecutado.")
print(f"Guardado en: {OUTPUT_JSON}")
