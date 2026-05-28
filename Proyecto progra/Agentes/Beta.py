import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "Data"
OUTPUT_JSON = DATA_DIR / "agent_balance_master.json"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

resultado = {
    "agent": "stability",
    "weights": {
        "w_stability": 25,   # fuerza principal de equilibrio
        "w_balance": 10      # suaviza contra target
    },
     "target_creditos": 15,
    "note": "Agente que minimiza la variación entre semestres."
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Agente stability ejecutado.")
print(f"Guardado en: {OUTPUT_JSON}")