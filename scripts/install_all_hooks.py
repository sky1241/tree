#!/usr/bin/env python3
"""
INSTALL ALL HOOKS — Installe le hook Winter Tree dans tous les repos.
============================================================

Usage (depuis le repo tree):
  python scripts/install_all_hooks.py

Lit repos.json, copie hooks/repo-hook-template.py dans chaque repo/.git/hooks/pre-commit
Installe aussi le hook du repo tree lui-même.
"""

import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS_JSON = ROOT / "repos.json"
HOOK_TEMPLATE = ROOT / "hooks" / "repo-hook-template.py"
TREE_HOOK = ROOT / "hooks" / "pre-commit"


def main():
    print("\n  🌲 INSTALL ALL HOOKS")
    print(f"  {'─' * 50}")

    if not REPOS_JSON.exists():
        print("  ❌ repos.json introuvable")
        return

    if not HOOK_TEMPLATE.exists():
        print("  ❌ hooks/repo-hook-template.py introuvable")
        return

    with open(REPOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    repos = [r for r in data.get("repos", []) if r.get("active", True)]
    installed = 0
    skipped = 0
    failed = 0

    for repo in repos:
        name = repo["name"]
        local_path = repo.get("local_path", "")

        if not local_path:
            print(f"  ⚠️  {name}: pas de chemin local → skip")
            skipped += 1
            continue

        repo_dir = Path(local_path)
        if not repo_dir.is_dir():
            print(f"  ⚠️  {name}: {local_path} n'existe pas → skip")
            skipped += 1
            continue

        git_hooks = repo_dir / ".git" / "hooks"
        if not git_hooks.exists():
            print(f"  ⚠️  {name}: pas de .git/hooks/ → skip")
            skipped += 1
            continue

        target = git_hooks / "pre-commit"

        # Le repo tree utilise son propre hook (pas le template)
        if name == "tree":
            try:
                shutil.copy2(TREE_HOOK, target)
                # Make executable
                os.chmod(target, 0o755)
                print(f"  ✅ {name}: hook tree installé")
                installed += 1
            except Exception as e:
                print(f"  ❌ {name}: {e}")
                failed += 1
            continue

        # Tous les autres repos: hook template
        try:
            shutil.copy2(HOOK_TEMPLATE, target)
            os.chmod(target, 0o755)
            print(f"  ✅ {name}: hook installé")
            installed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1

    print(f"\n  {'─' * 50}")
    print(f"  ✅ {installed} installés | ⚠️ {skipped} skippés | ❌ {failed} échoués")

    # Rappel
    print(f"\n  💡 Pense à mettre les vrais chemins dans repos.json!")
    print(f"     Cherche 'C:\\\\Users\\\\Sky\\\\path\\\\to\\\\' et remplace.")


if __name__ == "__main__":
    main()
