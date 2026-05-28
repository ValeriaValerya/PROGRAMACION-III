import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
 
 
BASE = Path(__file__).parent
 
DIRECTORIOS = {
    "agentes": BASE / "Agentes",
    "models":  BASE / "Models",
    "data":    BASE / "Data",
    "engine":  BASE / "engine",
}
 
ARCHIVOS = {
    "modelo":  BASE / "Models" / "Modelo_Solution.mzn",
    "malla":   BASE / "Data"   / "Malla_Curri.dzn",
    "materias": BASE / "Data"  / "materias.json",
}
 
 
_verbose = False
 
def log(msg: str) -> None:
    if _verbose:
        print(msg)
 
 
class PlanGlobal:
 
    def __init__(self, verbose: bool = False):
        global _verbose
        _verbose = verbose
        self.status: Dict[str, str] = {}
        self.datos:  Dict[str, Any] = {}
 
    # ---------- validación ----------
 
    def _check_dirs(self) -> bool:
        ok = True
        for nombre, ruta in DIRECTORIOS.items():
            if ruta.exists():
                self.status[nombre] = "ok"
                log(f"  dir  {nombre}")
            else:
                self.status[nombre] = "missing"
                log(f"  dir  {nombre}  [no encontrado]")
                ok = False
        return ok
 
    def _check_files(self) -> bool:
        ok = True
        for nombre, ruta in ARCHIVOS.items():
            if ruta.exists():
                self.status[nombre] = "ok"
                log(f"  file {nombre}")
            else:
                self.status[nombre] = "missing"
                log(f"  file {nombre}  [no encontrado]")
                ok = False
        return ok
 
    def validar(self) -> bool:
        log("[validar]")
        dirs_ok  = self._check_dirs()
        files_ok = self._check_files()
        return dirs_ok and files_ok

    def cargar_datos(self) -> Optional[Dict]:
        log("[datos]")
        try:
            with open(ARCHIVOS["materias"], encoding="utf-8") as f:
                self.datos["materias"] = json.load(f)
            log(f"  materias: {len(self.datos['materias'])} entradas")
            return self.datos["materias"]
        except FileNotFoundError:
            log("  materias.json no encontrado")
        except Exception as e:
            log(f"  error: {e}")
        return None
 
    def cargar_modelo(self) -> Optional[Any]:
        log("[modelo]")
        try:
            from minizinc import Model
            modelo = Model(str(ARCHIVOS["modelo"]))
            self.datos["modelo"] = modelo
            log("  modelo cargado")
            return modelo
        except ImportError:
            log("  minizinc no instalado")
        except Exception as e:
            log(f"  error: {e}")
        return None
 
    def cargar_agentes(self) -> Dict[str, Path]:
        log("[agentes]")
        agentes = {}
        ruta = DIRECTORIOS["agentes"]
        excluded = {"agent_utils.py", "__init__.py"}
        if ruta.exists():
            for f in ruta.glob("*.py"):
                if f.name in excluded or f.name.startswith("_"):
                    continue
                agentes[f.stem] = f
                log(f"  {f.stem}")
        else:
            log("  directorio no encontrado")
        self.datos["agentes"] = agentes
        return agentes
 
    def inicializar_engine(self) -> bool:
        log("[engine]")
        ok = DIRECTORIOS["engine"].exists()
        self.status["engine"] = "ok" if ok else "missing"
        log(f"  {'listo' if ok else 'no encontrado'}")
        return ok
 
    # ---------- reporte ----------
 
    def resumen(self) -> str:
        lines = ["status:"]
        for k, v in self.status.items():
            marca = "+" if v == "ok" else "-"
            lines.append(f"  [{marca}] {k}")
        lines.append(f"agentes : {len(self.datos.get('agentes', {}))}")
        lines.append(f"materias: {len(self.datos.get('materias', []))}")
        return "\n".join(lines)
 
    def guardar_reporte(self, destino: Optional[Path] = None) -> Path:
        destino = destino or BASE / "salida.txt"
        destino.write_text(self.resumen(), encoding="utf-8")
        log(f"  reporte -> {destino}")
        return destino
 
    def run(self) -> bool:
        log("=== PlanGlobal ===")
 
        if not self.validar():
            print("validacion fallida — revisa la estructura")
            return False
 
        self.cargar_datos()
        self.cargar_modelo()
        self.cargar_agentes()
        self.inicializar_engine()
 
        self.guardar_reporte()
 
        if _verbose:
            print(self.resumen())
 
        return True
 
 
# ==================== ENTRADA ====================
 
if __name__ == "__main__":
    # --verbose  activa los mensajes de progreso
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
 
    plan = PlanGlobal(verbose=verbose)
    ok   = plan.run()
 
    sys.exit(0 if ok else 1)
 
