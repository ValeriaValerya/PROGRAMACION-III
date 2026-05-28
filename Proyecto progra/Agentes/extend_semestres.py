#!/usr/bin/env python3
"""Agente que extiende el horizonte de semestres.

Este agente genera un archivo JSON que indica al engine cuántos
semestres usar en la generación de la instancia MiniZinc.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE / "Data" / "agent_extend_semestres.json"
NUM_SEMESTRES = 12


def main() -> None:
    resultado = {
        "agent": "extend_semestres",
        "activated": True,
        "note": "Extiende el número de semestres para administrar mejor la carga del agente base.",
        "num_semestres": NUM_SEMESTRES,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print("Agente extend_semestres ejecutado.")
    print(f"Resultado guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
