#!/usr/bin/env python3
"""Main orquestador: valida workspace, permite seleccionar hasta 5 agentes,
genera .dzn con el engine y resuelve la instancia con MiniZinc.
"""

import argparse
import importlib.util
import json
import subprocess
import sys
import time
import itertools
import threading
from pathlib import Path

from PlanGlobal import PlanGlobal

BASE = Path(__file__).parent


# ──────────────────────────────────────────────
#  Animación de actividad del agente
# ──────────────────────────────────────────────

def mostrar_actividad_agente(nombre_agente: str, tarea: str, duracion: float = 2.5):
    """Muestra una animación de spinner indicando que el agente está activo."""
    spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    fin = time.time() + duracion
    print()
    while time.time() < fin:
        frame = next(spinner)
        print(f"\r  {frame}  [{nombre_agente}] {tarea}...", end="", flush=True)
        time.sleep(0.08)
    print(f"\r  ✓  [{nombre_agente}] {tarea} — listo.          ")
    print()


def spinner_en_hilo(nombre_agente: str, tarea: str, evento_fin: threading.Event):
    """Spinner que corre en un hilo paralelo hasta que evento_fin se active."""
    spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    print()
    while not evento_fin.is_set():
        frame = next(spinner)
        print(f"\r  {frame}  [{nombre_agente}] {tarea}...", end="", flush=True)
        time.sleep(0.08)
    print(f"\r  ✓  [{nombre_agente}] {tarea} — completado.     ")
    print()


# ──────────────────────────────────────────────

def choose_agents(available, requested):
    available_set = set(available)
    if requested:
        sel = [r for r in requested if r in available_set]
        missing = [r for r in requested if r not in available_set]
        return sel[:5], missing

    print("Agentes disponibles:")
    for i, name in enumerate(sorted(available), start=1):
        print(f"  {i}. {name}")
    s = input("Ingresa nombres de agentes separados por comas (máx 5), o ENTER para ninguno: ").strip()
    if not s:
        return [], []
    names = [x.strip() for x in s.split(",") if x.strip()]
    sel = [n for n in names if n in available_set]
    missing = [n for n in names if n not in available_set]
    return sel[:5], missing


def run_script(path: Path, nombre_agente: str = "Agente"):
    """Ejecuta un script mostrando actividad del agente en tiempo real."""
    evento_fin = threading.Event()
    tarea = f"Procesando {path.name}"

    hilo = threading.Thread(
        target=spinner_en_hilo,
        args=(nombre_agente, tarea, evento_fin),
        daemon=True,
    )
    hilo.start()

    try:
        subprocess.run([sys.executable, str(path)], check=True)
    except subprocess.CalledProcessError as e:
        evento_fin.set()
        hilo.join()
        print(f"Error ejecutando {path}:", e)
        raise
    finally:
        evento_fin.set()
        hilo.join()


def is_module_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def main():
    parser = argparse.ArgumentParser(description="Main orquestador del proyecto")
    parser.add_argument("--agents", nargs="*", help="Nombres de agentes a incluir (máx 5)")
    parser.add_argument("--no-engine", action="store_true", help="No ejecutar engine/generar .dzn")
    parser.add_argument("--no-solve", action="store_true", help="No ejecutar la resolución MiniZinc")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mensajes verbosos")
    args = parser.parse_args()

    if not args.no_solve and not is_module_available("minizinc"):
        print("Error: el paquete Python 'minizinc' no está instalado.")
        print("Instala con: pip install minizinc")
        sys.exit(1)

    plan = PlanGlobal(verbose=args.verbose)
    if not plan.validar():
        print("Validación fallida — revisa la estructura del proyecto.")
        cont = input("Continuar de todas formas? [y/N]: ").strip().lower()
        if cont != "y":
            sys.exit(1)

    plan.cargar_agentes()
    available = sorted(plan.datos.get("agentes", {}).keys())

    selected, missing = choose_agents(available, args.agents or [])
    if missing:
        print("Agentes no encontrados:", ", ".join(missing))

    print("Agentes seleccionados:", selected)

    # Mostrar que cada agente seleccionado está inicializándose
    for agente in selected:
        mostrar_actividad_agente(agente, "Inicializando", duracion=1.2)

    sel_path = BASE / "Data" / "selected_agents.json"
    sel_path.parent.mkdir(parents=True, exist_ok=True)
    sel_path.write_text(json.dumps(selected, indent=2), encoding="utf-8")
    print(f"Selección guardada en: {sel_path}")

    # Ejecutar agentes seleccionados antes de engine
    for agente in selected:
        agente_path = plan.datos.get("agentes", {}).get(agente)
        if agente_path:
            print(f"Ejecutando agente seleccionado: {agente}")
            try:
                mostrar_actividad_agente(agente, "Ejecutando acción", duracion=1.0)
                run_script(agente_path, nombre_agente=agente)
            except Exception:
                print(f"Fallo al ejecutar agente {agente}. Abortando.")
                sys.exit(1)

    # Ejecutar engine (genera .dzn)
    if not args.no_engine:
        engine_path = BASE / "engine" / "Engine.py"
        nombre_engine = selected[0] if selected else "Engine"
        print(f"Ejecutando engine para generar .dzn...")
        mostrar_actividad_agente(nombre_engine, "Analizando datos y preparando el modelo", duracion=1.8)
        try:
            run_script(engine_path, nombre_agente=nombre_engine)
        except Exception:
            print("Fallo al ejecutar engine. Abortando.")
            sys.exit(1)

    # Ejecutar MiniZinc
    if not args.no_solve:
        instancia_path = BASE / "Archivo_Instancia.py"
        nombre_solver = selected[-1] if selected else "Solver"
        print("Ejecutando Archivo_Instancia.py (resolver MiniZinc)...")
        mostrar_actividad_agente(nombre_solver, "Construyendo la malla de restricciones", duracion=1.8)
        try:
            run_script(instancia_path, nombre_agente=nombre_solver)
        except Exception:
            print("Fallo al resolver la instancia.")
            sys.exit(1)

    print("\n✅ Ejecución finalizada.")


if __name__ == "__main__":
    main()