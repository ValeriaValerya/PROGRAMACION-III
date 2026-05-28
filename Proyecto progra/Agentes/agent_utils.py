import os
import ast
import json
from typing import Dict, Any


def verify_agents(path: str = "Agentes") -> Dict[str, Dict[str, Any]]:
    """Verifica archivos en el directorio de agentes.

    Para cada archivo devuelve información básica:
    - tipo de archivo
    - tamaño en bytes
    - si es .py, si contiene clases o una asignación 'agent_name'/'name'
    - si es .json, si es válido
    - cualquier error de parseo
    """
    results: Dict[str, Dict[str, Any]] = {}
    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directorio no encontrado: {path}")

    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if not os.path.isfile(full):
            continue

        info: Dict[str, Any] = {
            "size": os.path.getsize(full),
            "type": os.path.splitext(name)[1],
            "parse_error": None,
        }

        try:
            with open(full, "r", encoding="utf-8") as f:
                src = f.read()

            if name.endswith(".py"):
                info.update({"has_class": False, "has_agent_name": False})
                try:
                    tree = ast.parse(src)
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef):
                            info["has_class"] = True
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id.lower() in ("agent_name", "name", "agent"):
                                    info["has_agent_name"] = True
                except Exception as e:
                    info["parse_error"] = str(e)

            elif name.endswith(".json"):
                try:
                    json.loads(src)
                    info["json_valid"] = True
                except Exception as e:
                    info["json_valid"] = False
                    info["parse_error"] = str(e)

            else:
                info["preview"] = src[:200]

        except Exception as e:
            info["parse_error"] = str(e)

        results[name] = info

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verificar archivos de Agentes")
    parser.add_argument("--path", "-p", default="Agentes", help="Directorio de agentes")
    args = parser.parse_args()
    res = verify_agents(args.path)
    print(json.dumps(res, indent=2, ensure_ascii=False))
