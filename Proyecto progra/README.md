# Programacion III — Planificador de Malla

Este repositorio contiene scripts para validar una malla curricular, generar un `.dzn` para MiniZinc y resolver una instancia.

Requisitos
- Python 3.8+
- MiniZinc con un solver instalado (p. ej. `gecode`).

Instalación rápida (Windows PowerShell):

```powershell
# Activar entorno virtual si existe
& .venv\Scripts\Activate.ps1
# Instalar dependencias Python
pip install -r requirements.txt
```

Uso

- Validar estructura y generar resúmenes:

```powershell
python PlanGlobal.py --verbose
```

- Generar `.dzn` desde la malla y archivos JSON (script del motor):

```powershell
python engine\Engine.py
# Esto genera Data/salida.dzn
```

- Resolver la instancia con MiniZinc:

```powershell
python Archivo_Instancia.py
```

Notas
- `engine/Engine.py` ahora usa rutas robustas y lee `Data/materias.json`.
- Recordar de que MiniZinc y el solver (`gecode`) estén instalados y accesibles en PATH.
- Para integración futura considera convertir `engine/Engine.py` en un módulo con funciones reutilizables.
