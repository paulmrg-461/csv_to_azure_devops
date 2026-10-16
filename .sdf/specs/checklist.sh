#!/usr/bin/env bash
# checklist.sh — INTERPRETE_VERSION: 1
# Verificación MECÁNICA del cierre SDF (capa 1). Toda la lógica vive en
# checklist.rules — este script solo la interpreta; no dupliques un check aquí
# sin agregarlo también allá (misma decisión que generar-proyecciones/proyecciones.rules).
#
#   bash .sdf/specs/checklist.sh <id-documento>   # checklist de un cambio
#   bash .sdf/specs/checklist.sh --pendientes     # ¿algo en curso? (para hooks: exit 2 si sí)
#
# Verifica lo estructural en ~2 segundos y ~0 tokens. Las FALLAs se corrigen antes de cerrar.
set -u
AQUI="$(cd "$(dirname "$0")" && pwd)"
REGLAS="$AQUI/checklist.rules"
[ -f "$REGLAS" ] || { echo "error: falta $REGLAS" >&2; exit 2; }

# ── --pendientes: ¿hay algún cambio con Estado: en curso? ─────────────────────
if [ "${1-}" = "--pendientes" ]; then
  n=0
  while IFS= read -r p; do
    [ -z "$p" ] && continue
    if grep -q 'Estado: *en curso' "$p" 2>/dev/null; then
      echo "PENDIENTE  $p"
      n=$((n + 1))
    fi
  done <<EOF
$(find .sdf/docs -type f -name proposal.md 2>/dev/null)
EOF
  if [ "$n" -eq 0 ]; then
    echo "sin cambios en curso"
    exit 0
  else
    echo "$n cambio(s) en curso"
    exit 2
  fi
fi

id="${1-}"
[ -z "$id" ] && { echo "Uso: bash .sdf/specs/checklist.sh <id-documento> | --pendientes"; exit 2; }

ULTIMO=$(ls -d ".sdf/docs/$id/changes"/*/ 2>/dev/null | sort | tail -1 | sed 's#/*$##')
ULTIMO=$(basename "${ULTIMO:-_ninguno_}" 2>/dev/null)

resolver() { printf '%s' "$1" | sed "s/{id}/$id/g; s/{ultimo}/$ULTIMO/g"; }

fail=0
pasa() { echo "PASA  $1"; }
falla() { echo "FALLA $1"; fail=1; }

# ── parseo de checklist.rules: un registro por bloque separado por '---' ──────
declare -A R=()
vaciar() { R=(); }

evaluar() {
  local tipo="${R[tipo]:-}" desc ruta patron patron_b max excl ci
  desc=$(resolver "${R[descripcion]:-}")
  ruta=$(resolver "${R[ruta]:-}")
  patron=$(resolver "${R[patron]:-}")
  patron_b=$(resolver "${R[patron_b]:-}")
  max="${R[max]:-}"
  excl="${R[excluir]:-}"
  ci=""; [ "${R[sin_distincion_mayusculas]:-}" = "true" ] && ci="i"
  local exclarg=() nombre
  if [ -n "$excl" ]; then
    local IFS=,; for nombre in $excl; do exclarg+=(--exclude="$nombre"); done
  fi

  case "$tipo" in
    archivo_existe) [ -f "$ruta" ] && pasa "$desc" || falla "$desc" ;;
    carpeta_existe) [ -d "$ruta" ] && pasa "$desc" || falla "$desc" ;;
    glob_existe) ls -d $ruta >/dev/null 2>&1 && pasa "$desc" || falla "$desc" ;;
    grep_existe)
      grep -q$ci -- "$patron" "$ruta" 2>/dev/null && pasa "$desc" || falla "$desc" ;;
    grep_ausente)
      grep -rq$ci "${exclarg[@]}" -- "$patron" "$ruta" 2>/dev/null && falla "$desc" || pasa "$desc" ;;
    conteo_lineas_max)
      [ -f "$ruta" ] && [ "$(wc -l < "$ruta")" -le "$max" ] && pasa "$desc" || falla "$desc" ;;
    contiene_fecha_hoy)
      grep -q "$(date +%F)" "$ruta" 2>/dev/null && pasa "$desc" || falla "$desc" ;;
    sin_subcarpetas)
      ! ls -d "$ruta"/*/ >/dev/null 2>&1 && pasa "$desc" || falla "$desc" ;;
    grep_todas_cumplen)
      if grep -rh$ci "${exclarg[@]}" -- "$patron" "$ruta" 2>/dev/null | grep -qv -- "$patron_b"; then
        falla "$desc"
      else
        pasa "$desc"
      fi ;;
    presupuesto_no_excedido)
      if [ ! -f "$ruta" ]; then falla "$desc (sin proposal que leer)"; return; fi
      local pl tl pn tn
      pl=$(grep -m1 'Presupuesto:' "$ruta" 2>/dev/null)
      tl=$(grep -m1 'Tokens:' "$ruta" 2>/dev/null)
      pn=$(printf '%s' "$pl" | grep -oE '[0-9]+ ?k' | head -1 | grep -oE '[0-9]+')
      tn=$(printf '%s' "$tl" | grep -oE '~ ?[0-9]+' | head -1 | grep -oE '[0-9]+')
      if [ -z "$pn" ] || [ -z "$tn" ]; then
        pasa "$desc (sin cifras numéricas que comparar todavía)"
      elif [ "$tn" -le $((pn * 1000)) ]; then
        pasa "$desc"
      else
        falla "$desc ($tn > ${pn}k)"
      fi ;;
    *) falla "tipo de check desconocido: $tipo ($desc)" ;;
  esac
}

while IFS= read -r linea || [ -n "$linea" ]; do
  case "$linea" in
    '#'*) continue ;;
    '---') [ ${#R[@]} -gt 0 ] && evaluar; vaciar; continue ;;
    *:*)
      clave="${linea%%:*}"; valor="${linea#*: }"; [ "$valor" = "$linea" ] && valor=""
      R["$clave"]="$valor"
      ;;
  esac
done < "$REGLAS"
[ ${#R[@]} -gt 0 ] && evaluar

# Informativo: la cola de revisión NO bloquea el cierre, solo se reporta.
if [ -f .sdf/REVIEW.md ]; then
  REV=$(grep -c '^- \*\*Estado:\*\* pendiente' .sdf/REVIEW.md 2>/dev/null || echo 0)
  echo "INFO  cola de revisión: $REV entrada(s) pendiente(s) en .sdf/REVIEW.md (no bloquea)"
fi

[ $fail -eq 0 ] && echo "== MECÁNICA: TODO PASA ==" || echo "== MECÁNICA: HAY FALLAS — corregir antes de cerrar =="
exit $fail
