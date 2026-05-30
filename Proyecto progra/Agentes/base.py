import json
from pathlib import Path

# Intentamos importar minizinc, si no está instalado, mostramos un mensaje de error y salimos.
BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "Data"                    # Directorio para almacenar los archivos de datos y resultados
OUTPUT_JSON = DATA_DIR / "agent_base.json"

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

resultado = {
    "agent": "base",
    "weights": {
        "w_low":      20,
        "w_no_vacios": 15,
        "w_balance":   25 
    },
    "target_creditos": 15,
    "note": "Sesgo hacia semestres con mayor carga (evita semestres débiles).",
    "Filosofy": "estructura intensa."
     }
# Guardamos el resultado en un archivo JSON para su posterior análisis o uso.
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False)

print("Agente base (soft) ejecutado.")
print(f"Guardado en: {OUTPUT_JSON}")
