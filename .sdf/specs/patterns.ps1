# patterns.ps1 -- armazon de la 6.0 para el detector de patrones de la 6.2.
# Interfaz que consumira esa entrega (no cambiar sin actualizar patterns.sh igual):
#
#   powershell -File .sdf\specs\patterns.ps1 [--umbral N]
#
#   Salida esperada (cuando la 6.2 lo implemente): una lista de patrones detectados
#   en .sdf\LOG.md y en .sdf\docs\*\changes\*\ que se repiten >= N veces (por
#   defecto 3), cada uno con sus ocurrencias y una propuesta de receta reutilizable
#   para que el usuario apruebe o descarte. Sin argumentos: modo reporte, no toca
#   archivos. Con receta aprobada: escribe en un destino que la 6.2 todavia define.
#
# Por ahora, este script SOLO existe para que la ruta este instalada de antemano
# (task 6.6) -- no ejecuta deteccion real todavia.
Write-Host "patterns.ps1: el detector de patrones se construye en el bloque 6.2 del plan v6."
Write-Host "Esta es la interfaz reservada, sin logica todavia -- no es un error."
exit 0
