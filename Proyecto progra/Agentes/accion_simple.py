#!/usr/bin/env python3
"""Agente simple de acción condicional.

Este agente verifica si en la malla existe al menos una materia con
3 o más prerrequisitos.
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_FILE = BASE / "Data" / "materias.json"
OUTPUT_FILE = BASE / "Data" / "agent_condicion_simple.json"


def main() -> None:
    if not DATA_FILE.exists():
        print("No se encontró Data/materias.json. No se puede evaluar la condición.")
        raise SystemExit(1)

    with open(DATA_FILE, encoding="utf-8") as f:
        materias = json.load(f)

    materias_con_prerreq = [
        nombre
        for nombre, info in materias.items()
        if len(info.get("prereq", [])) >= 3
    ]

    condicion = len(materias_con_prerreq) > 0
    if condicion:
        print("✅ Condición cumplida: existe al menos una materia con 3 o más prerrequisitos.")
        print("Materias encontradas:")
        for nombre in materias_con_prerreq:
            print(f"  - {nombre}")
    else:
        print("⚠️ Condición no cumplida: ninguna materia tiene 3 o más prerrequisitos.")

    resultado = {
        "agent": "accion_simple",
        "condition": "materia_con_3_o_mas_prerrequisitos",
        "result": condicion,
        "matches": materias_con_prerreq,
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    print(f"Resultado guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
