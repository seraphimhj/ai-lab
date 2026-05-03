#!/usr/bin/env bash
# Clone every repo listed in repos.txt into ./repos/.
# Idempotent: skips repos that are already cloned.
# Usage: bash scripts/bootstrap.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIST="$ROOT/repos.txt"
DEST="$ROOT/repos"

if [[ ! -f "$LIST" ]]; then
  echo "error: $LIST not found" >&2
  exit 1
fi

mkdir -p "$DEST"
cd "$DEST"

while IFS= read -r line || [[ -n "$line" ]]; do
  # strip comments and whitespace
  url="${line%%#*}"
  url="$(echo "$url" | xargs || true)"
  [[ -z "$url" ]] && continue

  name="$(basename "$url" .git)"
  if [[ -d "$name/.git" ]]; then
    echo "✓ $name already cloned"
  else
    echo "→ cloning $url"
    git clone "$url"
  fi
done < "$LIST"

echo "Done. Repos live in: $DEST"
