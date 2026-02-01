# verify_mod_output.ps1 - Vérifie la présence et le contenu des fichiers de sortie du mod Living Narrator

# 1. Définir le chemin du dossier de sortie (avec OneDrive)
$DocsDir = [Environment]::GetFolderPath('MyDocuments')
$NarratorPath = Join-Path $DocsDir "Civ6Narrator"

Write-Host "Vérification des fichiers de sortie du mod Living Narrator..." -ForegroundColor Cyan
Write-Host "Chemin attendu: $NarratorPath"

# 2. Vérifier si le fichier des événements existe
if (Test-Path "$NarratorPath\events.jsonl") {
    Write-Host "`n✅ Fichier 'events.jsonl' trouvé ! Voici les 5 dernières lignes :" -ForegroundColor Green
    Get-Content "$NarratorPath\events.jsonl" -Tail 5
} else {
    Write-Error "`n❌ Fichier 'events.jsonl' non trouvé dans '$NarratorPath'."
    Write-Host "Assurez-vous que Civ 6 a bien été lancé avec le mod activé et qu'une partie a commencé."
}

# 3. Vérifier si le fichier d'état du jeu existe
if (Test-Path "$NarratorPath\game_state.json") {
    Write-Host "`n✅ Fichier 'game_state.json' trouvé ! Vérification du contenu..." -ForegroundColor Green
    try {
        # On essaie de lire le JSON pour confirmer qu'il est valide
        Get-Content "$NarratorPath\game_state.json" | ConvertFrom-Json | Out-Null
        Write-Host "Le fichier 'game_state.json' est un JSON valide." -ForegroundColor Green
        Write-Host "Voici le début du contenu pour vérification :"
        (Get-Content "$NarratorPath\game_state.json" | ConvertFrom-Json) | Format-List -Depth 2
    }
    catch {
        Write-Error "Le fichier 'game_state.json' semble corrompu ou n'est pas un JSON valide : $($_.Exception.Message)"
        Write-Host "Voici le début du contenu brut pour inspection :"
        Get-Content "$NarratorPath\game_state.json" -First 10
    }
} else {
    Write-Error "`n❌ Fichier 'game_state.json' non trouvé dans '$NarratorPath'."
    Write-Host "Assurez-vous que Civ 6 a bien été lancé avec le mod activé et qu'une partie a commencé."
}

Write-Host "`n--- Vérification terminée ---" -ForegroundColor Cyan
