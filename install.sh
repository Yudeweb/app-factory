#!/usr/bin/env bash
# Installs the App Factory skill and agents into your Claude configuration
# (~/.claude by default). Existing files with the same names are moved to a
# dated backup folder first. Safe to run again to update.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
BACKUP="$DEST/backups/app-factory-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$DEST/skills" "$DEST/agents"

if [ -e "$DEST/skills/app-factory" ]; then
  mkdir -p "$BACKUP/skills"
  mv "$DEST/skills/app-factory" "$BACKUP/skills/app-factory"
  echo "Backed up existing skill to $BACKUP/skills/app-factory"
fi
cp -R "$SRC/skills/app-factory" "$DEST/skills/app-factory"
chmod +x "$DEST/skills/app-factory/scripts/factory.py"
echo "Installed skill: $DEST/skills/app-factory"

for f in "$SRC"/agents/*.md; do
  name="$(basename "$f")"
  if [ -e "$DEST/agents/$name" ] && ! cmp -s "$f" "$DEST/agents/$name"; then
    mkdir -p "$BACKUP/agents"
    mv "$DEST/agents/$name" "$BACKUP/agents/$name"
    echo "Backed up existing agent $name"
  fi
  cp "$f" "$DEST/agents/$name"
  echo "Installed agent: $name"
done

echo "Done. Open a new Claude session in an empty folder and run: /app-factory <your idea>"
