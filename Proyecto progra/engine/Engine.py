import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JSON = BASE_DIR / "Data" / "materias.json"
DATA_DZN = BASE_DIR / "Data" / "Malla_Curri.dzn"
SALIDA_DZN = BASE_DIR / "Data" / "salida.dzn"
EXTEND_FILE = BASE_DIR / "Data" / "agent_extend_semestres.json"

if not DATA_JSON.exists():
    raise FileNotFoundError(f"No se encontró {DATA_JSON}")
if not DATA_DZN.exists():
    raise FileNotFoundError(f"No se encontró {DATA_DZN}")

with open(DATA_JSON, "r", encoding="utf-8") as f:
    materias_data = json.load(f)

text = DATA_DZN.read_text(encoding="utf-8")
match = re.search(r"creditos\s*=\s*\[(.*?)\];", text, re.S)
if not match:
    raise ValueError("No se pudo leer la lista de créditos desde Malla_Curri.dzn")

creditos = [
    int(token.strip())
    for token in re.sub(r"%.*", "", match.group(1)).split(",")
    if token.strip()
]

total_creditos = sum(creditos)
print(f"\n📊 Total de créditos en la malla: {total_creditos}")

materias = list(materias_data.keys())
idx = {materia: i for i, materia in enumerate(materias)}
n = len(materias)

# =========================
# 2. VALIDAR REFERENCIAS
# =========================
print("🔍 Validando referencias del JSON...")
errores = []
for materia, info in materias_data.items():
    for pre in info.get("prereq", []):
        if pre not in materias_data:
            errores.append(f"  - '{pre}' referenciado en prereq de '{materia}' no existe")
    for co in info.get("coreq", []):
        if co not in materias_data:
            errores.append(f"  - '{co}' referenciado en coreq de '{materia}' no existe")

if errores:
    print("⚠️ Referencias inválidas encontradas:")
    for error in errores:
        print(error)
    raise ValueError("Corrige las referencias antes de continuar.")

if len(creditos) != n:
    raise ValueError("El número de créditos en Malla_Curri.dzn no coincide con la cantidad de materias")

print("✅ Validación completada")

prereq = [[False] * n for _ in range(n)]
coreq = [[False] * n for _ in range(n)]
for materia, info in materias_data.items():
    i = idx[materia]
    for pre in info.get("prereq", []):
        prereq[idx[pre]][i] = True
    for co in info.get("coreq", []):
        j = idx[co]
        coreq[i][j] = True
        coreq[j][i] = True

num_semestres = 12
if EXTEND_FILE.exists():
    try:
        with open(EXTEND_FILE, encoding="utf-8") as f_ext:
            extension = json.load(f_ext)
        if extension.get("agent") == "extend_semestres":
            num_semestres = int(extension.get("num_semestres", num_semestres))
            print(f"🔧 Usando num_semestres={num_semestres} desde agente extend_semestres")
    except Exception as e:
        raise ValueError(f"Error leyendo {EXTEND_FILE}: {e}") from e

with open(SALIDA_DZN, "w", encoding="utf-8") as f:
    f.write("% Generado automáticamente desde materias.json y Malla_Curri.dzn\n\n")
    f.write(f"n = {n};\n")
    f.write(f"num_semestres = {num_semestres};\n\n")
    f.write("creditos = [\n")
    for credito in creditos:
        f.write(f"  {credito},\n")
    f.write("];\n\n")

    flat_prereq = [valor for fila in prereq for valor in fila]
    f.write("prereq_flat = [\n")
    for valor in flat_prereq:
        f.write(f"  {'true' if valor else 'false'},\n")
    f.write("];\n\n")

    flat_coreq = [valor for fila in coreq for valor in fila]
    f.write("coreq_flat = [\n")
    for valor in flat_coreq:
        f.write(f"  {'true' if valor else 'false'},\n")
    f.write("];\n")

print(f"\n📦 salida.dzn generado: {SALIDA_DZN}")
print(f"   • {n} materias")
print(f"   • {sum(sum(1 for x in fila if x) for fila in prereq)} prerrequisitos")
print(f"   • {sum(sum(1 for x in fila if x) for fila in coreq) // 2} pares de correquisitos")
print("\n✅ Todo listo.")

