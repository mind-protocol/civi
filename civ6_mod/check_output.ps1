# check_output.ps1 - Vérifie les fichiers de sortie du mod

$OutputDir = "$env:USERPROFILE\Documents\Civ6Narrator"
$EventsFile = "$OutputDir\events.jsonl"
$StateFile = "$OutputDir\game_state.json"

Write-Host "=== Living Narrator - Vérification ===" -ForegroundColor Cyan
Write-Host ""

# Check output directory
if (Test-Path $OutputDir) {
    Write-Host "[OK] Dossier de sortie existe: $OutputDir" -ForegroundColor Green
} else {
    Write-Host "[FAIL] Dossier de sortie manquant!" -ForegroundColor Red
    Write-Host "Le mod n'a pas été lancé ou n'a pas pu créer le dossier."
    exit 1
}

Write-Host ""

# Check events.jsonl
if (Test-Path $EventsFile) {
    $lineCount = (Get-Content $EventsFile | Measure-Object -Line).Lines
    $fileSize = (Get-Item $EventsFile).Length
    Write-Host "[OK] events.jsonl existe ($lineCount lignes, $fileSize bytes)" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Derniers events:" -ForegroundColor Yellow
    Get-Content $EventsFile -Tail 5 | ForEach-Object {
        $json = $_ | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($json) {
            Write-Host "  - $($json.event_type) (turn $($json.turn))"
        }
    }
} else {
    Write-Host "[FAIL] events.jsonl manquant!" -ForegroundColor Red
}

Write-Host ""

# Check game_state.json
if (Test-Path $StateFile) {
    $fileSize = (Get-Item $StateFile).Length
    Write-Host "[OK] game_state.json existe ($fileSize bytes)" -ForegroundColor Green
    
    try {
        $state = Get-Content $StateFile -Raw | ConvertFrom-Json
        Write-Host ""
        Write-Host "État du jeu:" -ForegroundColor Yellow
        Write-Host "  Turn: $($state.turn)"
        Write-Host "  Game ID: $($state.game_id)"
        Write-Host "  Players: $($state.players.Count)"
        
        foreach ($player in $state.players) {
            $humanTag = if ($player.is_human) { "[HUMAN]" } else { "[AI]" }
            Write-Host ""
            Write-Host "  $humanTag $($player.civ) ($($player.leader))" -ForegroundColor $(if ($player.is_human) { "Cyan" } else { "Gray" })
            Write-Host "    Cities: $($player.cities.Count)"
            Write-Host "    Units: $($player.units.Count)"
            if ($player.gold) { Write-Host "    Gold: $($player.gold)" }
        }
    } catch {
        Write-Host "[WARN] Impossible de parser game_state.json" -ForegroundColor Yellow
    }
} else {
    Write-Host "[FAIL] game_state.json manquant!" -ForegroundColor Red
}

Write-Host ""

# Check Lua logs
$LogFile = "$env:USERPROFILE\Documents\My Games\Sid Meier's Civilization VI\Logs\Lua.log"
if (Test-Path $LogFile) {
    Write-Host "=== Logs Lua (LivingNarrator) ===" -ForegroundColor Cyan
    Get-Content $LogFile | Select-String "LivingNarrator" | Select-Object -Last 20 | ForEach-Object {
        Write-Host $_.Line -ForegroundColor Gray
    }
} else {
    Write-Host "[INFO] Lua.log non trouvé (normal si Civ pas encore lancé)" -ForegroundColor Yellow
}
