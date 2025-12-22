# install_mod.ps1 - Copie le mod dans le dossier Civ 6
# Exécuter depuis le dossier civ6_mod/

# UTF-8 propre (évite le "trouvÃ©")
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()

$ModName = "LivingNarrator"
$SourceDir = $PSScriptRoot

$DocsDir = [Environment]::GetFolderPath('MyDocuments')
$Civ6ModsDir = Join-Path $DocsDir "My Games\Sid Meier's Civilization VI\Mods"
$DestDir = "$Civ6ModsDir\$ModName"
$OutputDir = Join-Path $DocsDir "Civ6Narrator"

Write-Host "=== Living Narrator - Installation ===" -ForegroundColor Cyan
Write-Host ""

# Vérifier que le dossier Civ 6 existe
if (-not (Test-Path $Civ6ModsDir)) {
    Write-Error "ERREUR: Dossier Civ 6 Mods non trouvé!`nAttendu: $Civ6ModsDir"
    exit 1
}

# Supprimer l'ancienne version si elle existe
if (Test-Path $DestDir) {
    Write-Host "Suppression de l'ancienne version..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $DestDir
}

# Copier les fichiers
Write-Host "Copie du mod vers $DestDir ..."
New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
New-Item -ItemType Directory -Path "$DestDir\Scripts" -Force | Out-Null

Copy-Item "$SourceDir\LivingNarrator.modinfo" $DestDir
Copy-Item "$SourceDir\Scripts\*.lua" "$DestDir\Scripts\"

Write-Host "OK - Mod copié!" -ForegroundColor Green
Write-Host ""

# Créer le dossier de sortie
Write-Host "Création du dossier de sortie..."
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "OK - Créé: $OutputDir" -ForegroundColor Green
} else {
    Write-Host "OK - Existe déjà: $OutputDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Installation terminée ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prochaines étapes:"
Write-Host "1. Lancer Civ 6"
Write-Host "2. Aller dans Additional Content"
Write-Host "3. Activer 'Living Narrator - Event Exporter'"
Write-Host "4. Créer une partie"
Write-Host ""
Write-Host "Vérifier après un tour:"
Write-Host "  Get-Content '$OutputDir\events.jsonl' -Tail 5"
Write-Host "  Get-Content '$OutputDir\game_state.json'"
