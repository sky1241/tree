#!/bin/bash
# WINTER TREE — Install git hooks (Linux/Mac)
HOOK_SRC="$(dirname "$0")/pre-commit"
HOOK_DST="$(git rev-parse --git-dir)/hooks/pre-commit"
cp "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_DST"
echo "[winter-tree] ✅ Hook installé: $HOOK_DST"
