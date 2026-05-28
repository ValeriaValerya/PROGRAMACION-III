import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "Data"
OUTPUT_JSON = DATA_DIR / "agent_low.json"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

resultado = {
    "agent": "low",
    "weights": {
        "w_low": 8,    # penaliza semestres con baja carga (< 10)
        "w_no_vacios": 20,    # casi no penaliza exceder carga
        "w_balance": 25   # penaliza semestres vacíos, pero poco
    },
    "target_creditos": 12,
    "note": "Sesgo hacia evitar semestres con baja carga (low credits bias)."
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Agente low ejecutado.")
print(f"Guardado en: {OUTPUT_JSON}")