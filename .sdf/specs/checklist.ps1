# checklist.ps1 -- INTERPRETE_VERSION: 1
# Verificacion MECANICA del cierre SDF (capa 1). Misma logica que checklist.sh:
# toda la logica vive en checklist.rules -- este script solo la interpreta.
#
#   powershell -File .sdf\specs\checklist.ps1 <id-documento>
#   powershell -File .sdf\specs\checklist.ps1 --pendientes
#
# Verifica lo estructural en segundos y ~0 tokens. Las FALLAs se corrigen antes de cerrar.

# Deliberadamente SIN bloque param(): con param(), PowerShell trata cualquier
# argumento que empiece con "-" como un intento de parametro nombrado (fallaria
# al pasar literalmente "--pendientes"). Sin param(), todo llega crudo en $args.
$Id = if ($args.Count -gt 0) { [string]$args[0] } else { '' }

$ErrorActionPreference = 'Stop'
$Aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$Reglas = Join-Path $Aqui 'checklist.rules'

if (-not (Test-Path $Reglas)) { Write-Error "falta $Reglas"; exit 2 }

# -- --pendientes: hay algun cambio con Estado: en curso? ----------------------
if ($Id -eq '--pendientes') {
    $n = 0
    if (Test-Path '.sdf/docs') {
        $proposals = Get-ChildItem -Recurse -File -Filter 'proposal.md' '.sdf/docs' -ErrorAction SilentlyContinue
        foreach ($p in $proposals) {
            if (Select-String -Path $p.FullName -Pattern 'Estado: *en curso' -Quiet -ErrorAction SilentlyContinue) {
                Write-Host "PENDIENTE  $($p.FullName)"
                $n++
            }
        }
    }
    if ($n -eq 0) { Write-Host 'sin cambios en curso'; exit 0 }
    else { Write-Host "$n cambio(s) en curso"; exit 2 }
}

if (-not $Id) { Write-Host 'Uso: powershell -File .sdf\specs\checklist.ps1 <id-documento> | --pendientes'; exit 2 }

$carpetaCambios = ".sdf/docs/$Id/changes"
$ultimo = ''
if (Test-Path $carpetaCambios) {
    $c = Get-ChildItem -Directory $carpetaCambios -ErrorAction SilentlyContinue | Sort-Object Name | Select-Object -Last 1
    if ($c) { $ultimo = $c.Name }
}

function Resolver([string]$Texto) {
    if ([string]::IsNullOrEmpty($Texto)) { return $Texto }
    $Texto.Replace('{id}', $Id).Replace('{ultimo}', $ultimo)
}

$Script:Fallas = 0
function Pasa([string]$Desc) { Write-Host "PASA  $Desc" }
function Falla([string]$Desc) { Write-Host "FALLA $Desc"; $Script:Fallas++ }

function Buscar-Archivos([string]$Ruta, [string]$Excluir) {
    $dir = Get-ChildItem -Recurse -File $Ruta -ErrorAction SilentlyContinue
    if ($Excluir) {
        $nombres = $Excluir -split ','
        $dir = $dir | Where-Object { $nombres -notcontains $_.Name }
    }
    return $dir
}

function Evaluar([hashtable]$Reg) {
    $tipo = $Reg['tipo']; $desc = Resolver ($Reg['descripcion'])
    $ruta = Resolver ($Reg['ruta'])
    $patron = Resolver ($Reg['patron']); $patronB = Resolver ($Reg['patron_b'])
    $maxLineas = $Reg['max']; $excluir = $Reg['excluir']
    $ci = ($Reg['sin_distincion_mayusculas'] -eq 'true')

    switch ($tipo) {
        'archivo_existe' {
            if (Test-Path $ruta -PathType Leaf) { Pasa $desc } else { Falla $desc }
        }
        'carpeta_existe' {
            if (Test-Path $ruta -PathType Container) { Pasa $desc } else { Falla $desc }
        }
        'glob_existe' {
            $m = Get-ChildItem $ruta -ErrorAction SilentlyContinue
            if ($m) { Pasa $desc } else { Falla $desc }
        }
        'grep_existe' {
            if (-not (Test-Path $ruta)) { Falla $desc; return }
            $r = Select-String -Path $ruta -Pattern $patron -CaseSensitive:(!$ci) -Quiet -ErrorAction SilentlyContinue
            if ($r) { Pasa $desc } else { Falla $desc }
        }
        'grep_ausente' {
            $archivos = Buscar-Archivos $ruta $excluir
            $encontrado = $false
            foreach ($a in $archivos) {
                if (Select-String -Path $a.FullName -Pattern $patron -CaseSensitive:(!$ci) -Quiet -ErrorAction SilentlyContinue) { $encontrado = $true; break }
            }
            if ($encontrado) { Falla $desc } else { Pasa $desc }
        }
        'conteo_lineas_max' {
            if (-not (Test-Path $ruta)) { Falla $desc; return }
            $n = (Get-Content $ruta | Measure-Object -Line).Lines
            if ($n -le [int]$maxLineas) { Pasa $desc } else { Falla $desc }
        }
        'contiene_fecha_hoy' {
            $hoy = Get-Date -Format 'yyyy-MM-dd'
            if ((Test-Path $ruta) -and (Select-String -Path $ruta -Pattern ([regex]::Escape($hoy)) -Quiet -ErrorAction SilentlyContinue)) { Pasa $desc } else { Falla $desc }
        }
        'sin_subcarpetas' {
            $sub = Get-ChildItem -Directory $ruta -ErrorAction SilentlyContinue
            if (-not $sub) { Pasa $desc } else { Falla $desc }
        }
        'grep_todas_cumplen' {
            $archivos = Buscar-Archivos $ruta $excluir
            $malas = 0
            foreach ($a in $archivos) {
                $lineasMatch = Select-String -Path $a.FullName -Pattern $patron -CaseSensitive:(!$ci) -ErrorAction SilentlyContinue
                foreach ($l in $lineasMatch) {
                    if ($l.Line -notmatch [regex]::Escape($patronB)) { $malas++ }
                }
            }
            if ($malas -eq 0) { Pasa $desc } else { Falla "$desc ($malas linea(s) sin cumplir)" }
        }
        'presupuesto_no_excedido' {
            if (-not (Test-Path $ruta)) { Falla "$desc (sin proposal que leer)"; return }
            $pl = (Select-String -Path $ruta -Pattern 'Presupuesto:' | Select-Object -First 1).Line
            $tl = (Select-String -Path $ruta -Pattern 'Tokens:' | Select-Object -First 1).Line
            $pn = $null; $tn = $null
            if ($pl -match '(\d+) ?k') { $pn = [int]$Matches[1] }
            if ($tl -match '~ ?(\d+)') { $tn = [int]$Matches[1] }
            if ($null -eq $pn -or $null -eq $tn) { Pasa "$desc (sin cifras numericas que comparar todavia)" }
            elseif ($tn -le ($pn * 1000)) { Pasa $desc }
            else { Falla "$desc ($tn > ${pn}k)" }
        }
        default { Falla "tipo de check desconocido: $tipo ($desc)" }
    }
}

# -- parseo de checklist.rules: un registro por bloque separado por '---' -----
$Reg = @{}
function Vaciar-Registro { $script:Reg = @{} }

foreach ($linea in (Get-Content $Reglas -Encoding UTF8)) {
    if ($linea.StartsWith('#')) { continue }
    if ($linea -eq '---') {
        if ($Reg.Count -gt 0) { Evaluar $Reg }
        Vaciar-Registro
        continue
    }
    $idx = $linea.IndexOf(':')
    if ($idx -lt 0) { continue }
    $clave = $linea.Substring(0, $idx)
    $valor = if ($linea.Length -gt $idx + 2) { $linea.Substring($idx + 2) } else { '' }
    $Reg[$clave] = $valor
}
if ($Reg.Count -gt 0) { Evaluar $Reg }

# Informativo: la cola de revision NO bloquea el cierre, solo se reporta.
if (Test-Path '.sdf/REVIEW.md') {
    $rev = (Select-String -Path '.sdf/REVIEW.md' -Pattern '^- \*\*Estado:\*\* pendiente' -ErrorAction SilentlyContinue).Count
    Write-Host "INFO  cola de revision: $rev entrada(s) pendiente(s) en .sdf/REVIEW.md (no bloquea)"
}

if ($Script:Fallas -eq 0) { Write-Host '== MECANICA: TODO PASA =='; exit 0 }
else { Write-Host '== MECANICA: HAY FALLAS -- corregir antes de cerrar =='; exit 1 }
