# ============================================================
# PLAN DE MEJORA — SISTEMA DE AGENTES + MINIZINC
# ============================================================
#
# OBJETIVO:
# Separar correctamente:
#
#   - Energías (MiniZinc)
#   - Preferencias/Pesos (Agentes)
#   - Configuración (Engine)
#
# Para volver el sistema:
#
#   ✓ modular
#   ✓ extensible
#   ✓ configurable
#   ✓ interpretable
#   ✓ multiobjetivo
#
# 1. PROBLEMA ACTUAL
#
# Actualmente existen valores hardcodeados:
#
#   if carga[s] < 10 then (10 - carga[s]) * 10
#
# Problemas:
#
#   ✗ pesos duplicados
#   ✗ poca flexibilidad
#   ✗ difícil experimentar
#   ✗ agentes menos reutilizables
#
# 2. OBJETIVO DE ARQUITECTURA
#
# MiniZinc:
#   - SOLO calcula energías
#
# Agentes:
#   - definen pesos
#   - definen preferencias
#   - definen configuraciones
#
# Engine:
#   - fusiona configuración
#   - genera .dzn
#
# Solver:
#   - optimiza
#
# 3. CAMBIOS RECOMENDADOS EN MINIZINC
#
# 3.1 AGREGAR CONFIGURACIONES DINÁMICAS
#
# Agregar:
#
# int: min_load;
#
# Para evitar valores hardcodeados.
#
# 3.2 ENERGÍAS PURAS (SIN PESOS INTERNOS)
#
# REEMPLAZAR:
#
# energia_low =
#   sum(s in SEMESTRES)(
#     if carga[s] < 10 then (10 - carga[s]) * 10 else 0 endif
#   );
#
# POR:
#
# energia_low =
#   sum(s in SEMESTRES)(
#     if carga[s] < min_load
#     then (min_load - carga[s])
#     else 0
#     endif
#   );
#
# IMPORTANTE:
#
# La energía NO debe tener pesos internos.
#
# La energía solo mide "qué tan malo es".
#
# 3.3 TODOS LOS PESOS EN solve
#
# RECOMENDADO:
#
# solve minimize (
#   w_base * energia_base +
#   w_base_le * energia_base_le +
#   w_no_vacios * energia_no_vacios +
#   w_balance * energia_balance +
#   w_low * energia_low
# );
#
# BENEFICIO:
#
#   ✓ matemática más limpia
#   ✓ tuning más fácil
#   ✓ agentes reutilizables
#
# 4. NUEVO FORMATO RECOMENDADO DE AGENTES
#
# RECOMENDADO:
#
# resultado = {
#     "agent": "low",
#
#     "weights": {
#         "w_low": 12,
#         "w_base_le": 2,
#         "w_no_vacios": 5
#     },
#
#     "config": {
#         "min_load": 10
#     },
#
#     "note": (
#         "Sesgo hacia evitar semestres con baja carga."
#     )
# }
#
# 5. CAMBIOS NECESARIOS EN EL ENGINE
#
# El engine debe:
#
#   ✓ leer TODOS los agentes
#   ✓ fusionar weights
#   ✓ fusionar config
#   ✓ generar salida.dzn
#
# 6. FORMATO ESPERADO EN salida.dzn
#
# w_low = 12;
# w_base_le = 2;
# w_no_vacios = 5;
#
# min_load = 10;
#
# 7. NUEVAS ENERGÍAS FUTURAS (IDEAS)
#
# 7.1 DISPERSIÓN ENTRE SEMESTRES
#
# Penalizar cambios bruscos:
#
# abs(carga[s] - carga[s+1])
#
# Evita:
#
#   27 -> 4 -> 26
#
# 7.2 COMPACTACIÓN
#
# Reducir cantidad total de semestres usados.
#
# 7.3 PRERREQUISITOS TARDÍOS
#
# Penalizar materias importantes muy tarde.
#
# ============================================================