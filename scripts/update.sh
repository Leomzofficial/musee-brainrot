#!/bin/bash
# Mise à jour hebdomadaire du musée Brainrot
# Récupère les nouvelles images + descriptions depuis steal-a-brainrot.org

set -e
REPO="/Users/michaelmougin/Documents/Brainrots"
LOG="$REPO/scripts/update.log"

echo "=== $(date '+%Y-%m-%d %H:%M') ===" >> "$LOG"

cd "$REPO"

# Lancer le script Python
python3 "$REPO/scripts/fetch_site.py" >> "$LOG" 2>&1

# Committer si des fichiers ont changé
if ! git diff --quiet || ! git diff --cached --quiet; then
    git add photos/ index.html
    git commit -m "Mise à jour auto brainrots $(date '+%Y-%m-%d')" >> "$LOG" 2>&1
    git push >> "$LOG" 2>&1
    echo "✅ Mis à jour et poussé" >> "$LOG"
else
    echo "— Aucun changement" >> "$LOG"
fi

echo "" >> "$LOG"
