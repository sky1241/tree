#!/usr/bin/env python3
# DETECT REPOS - Trouve automatiquement tous les repos git sur le PC.
# Usage: python scripts/detect_repos.py
# Scanne le disque pour trouver les repos sky1241 et remplit repos.json.

import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOS_JSON = ROOT / "repos.json"


def find_git_repos(search_dirs, max_depth=4):
    """Trouve tous les dossiers contenant un .git dans les chemins donnés."""
    found = {}  # name → path

    for base in search_dirs:
        base = Path(base)
        if not base.exists():
            continue

        print(f"  🔍 Scan: {base}")

        for depth in range(max_depth):
            # Walk only to max_depth
            for root, dirs, files in os.walk(base):
                # Calculate current depth
                rel = Path(root).relative_to(base)
                current_depth = len(rel.parts)
                if current_depth > max_depth:
                    dirs.clear()
                    continue

                # Skip heavy dirs
                skip = {
                    "node_modules", ".venv", "venv", "__pycache__",
                    ".git", "AppData", "Application Data",
                    "Windows", "Program Files", "ProgramData",
                    ".cache", ".npm", ".pub-cache", "Android",
                }
                dirs[:] = [d for d in dirs if d not in skip]

                # Check if this is a git repo
                git_dir = Path(root) / ".git"
                if git_dir.is_dir():
                    repo_name = Path(root).name
                    repo_path = str(Path(root).resolve())

                    # Check if it has a remote matching sky1241
                    try:
                        result = subprocess.run(
                            ["git", "remote", "-v"],
                            capture_output=True, text=True,
                            cwd=root, timeout=5
                        )
                        if "sky1241" in result.stdout:
                            found[repo_name] = repo_path
                    except:
                        # If git command fails, still record it
                        found[repo_name] = repo_path

                    # Don't recurse into git repos
                    dirs.clear()
            break  # os.walk already handles recursion

    return found


def main():
    print("\n  🌲 DETECT REPOS — Recherche automatique")
    print(f"  {'─' * 50}")

    if not REPOS_JSON.exists():
        print("  ❌ repos.json introuvable")
        return

    # Charger repos.json
    with open(REPOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    repo_names = {r["name"] for r in data["repos"]}

    # Déterminer les dossiers à scanner
    home = Path.home()
    tree_parent = ROOT.parent

    search_dirs = [
        tree_parent,
        home,
        home / "Desktop",
        home / "Bureau",
        home / "Documents",
        home / "OneDrive",
        home / "OneDrive" / "Bureau",
        home / "OneDrive" / "Desktop",
        home / "repos",
        home / "projects",
        home / "dev",
        home / "git",
        home / "AppData" / "Local" / "Temp",
    ]

    # Aussi D:\ et E:\ si existent
    for drive in ["D:/", "E:/"]:
        d = Path(drive)
        if d.exists():
            search_dirs.append(d)

    # Supprimer les doublons et les chemins inexistants
    search_dirs = list(dict.fromkeys(str(d) for d in search_dirs if Path(d).exists()))
    search_dirs = [Path(d) for d in search_dirs]

    print(f"  Dossiers à scanner: {len(search_dirs)}")
    for d in search_dirs:
        print(f"    📂 {d}")
    print()

    # Scanner
    found = find_git_repos(search_dirs)

    print(f"\n  {'─' * 50}")
    print(f"  Repos sky1241 trouvés: {len(found)}")

    # Matcher avec repos.json
    updated = 0
    not_found = []

    for repo in data["repos"]:
        name = repo["name"]
        if name in found:
            old_path = repo.get("local_path", "")
            new_path = found[name]
            if old_path != new_path:
                repo["local_path"] = new_path
                print(f"  ✅ {name}: {new_path}")
                updated += 1
            else:
                print(f"  ✓  {name}: déjà correct")
        else:
            not_found.append(name)
            print(f"  ❌ {name}: pas trouvé sur le disque")

    # Repos trouvés mais pas dans repos.json
    unknown = set(found.keys()) - repo_names
    for name in unknown:
        print(f"  ❓ {name}: trouvé ({found[name]}) mais pas dans repos.json")

    # Sauvegarder
    if updated > 0:
        with open(REPOS_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"\n  💾 repos.json mis à jour ({updated} chemins)")
    else:
        print(f"\n  Rien à mettre à jour")

    if not_found:
        print(f"\n  ⚠️  Repos non trouvés: {', '.join(not_found)}")
        print(f"     → Soit pas clonés, soit dans un dossier non scanné")
        print(f"     → Ajouter le chemin manuellement ou 'tree-sync --github'")


if __name__ == "__main__":
    main()
