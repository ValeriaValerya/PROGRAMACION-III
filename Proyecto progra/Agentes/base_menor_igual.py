import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "Data"
OUTPUT_JSON = DATA_DIR / "agent_base_le.json"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

resultado = {
    "agent": "base_menor_igual",
    "weights": {
        "w_low": 5,   
        "w_no_vacios": 0, 
        "w_balance": 30
    },
    "target_creditos": 10,
    "note": "Sesgo hacia semestres más livianos.",
    "Filosofy": "Vida liviana"
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Agente base_menor_igual (soft) ejecutado.")
print(f"Guardado en: {OUTPUT_JSON}")
