#!/usr/bin/env python3
"""
SYNC ALL — Re-scanne tous les repos et met à jour scans/
============================================================

Usage:
  python scripts/sync_all.py              # scan tous les repos locaux
  python scripts/sync_all.py --github     # scan via GitHub API (pas besoin de cloner)
  python scripts/sync_all.py --one <nom>  # scan un seul repo
  python scripts/sync_all.py --clean      # supprime les scans orphelins/doublons

Lit repos.json pour trouver les chemins locaux.
Si le chemin local n'existe pas, tente via GitHub API.
"""

import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime

# Ajouter scripts/ au path pour importer engine
SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from engine import (
    scan_repo, scan_github_repo, save_tree_json,
    calculate_scale, FAMILIES, _update_phase
)


def load_repos_json():
    """Charge le registre repos.json."""
    rpath = ROOT / "repos.json"
    if not rpath.exists():
        print("  ❌ repos.json introuvable à la racine du repo tree")
        return []
    with open(rpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [r for r in data.get("repos", []) if r.get("active", True)]


def load_github_token():
    """Cherche le token GitHub."""
    # 1. Variable d'environnement
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    # 2. Fichier dans scripts/
    token_file = SCRIPT_DIR / "CLEGITJAMAISTOUCHER.txt"
    if token_file.exists():
        return token_file.read_text().strip()
    # 3. Fichier à la racine
    token_file2 = ROOT / "CLEGITJAMAISTOUCHER.txt"
    if token_file2.exists():
        return token_file2.read_text().strip()
    return None


def scan_one_repo(repo_info, token=None, force_github=False):
    """Scanne un repo — local si possible, GitHub sinon."""
    name = repo_info["name"]
    local_path = repo_info.get("local_path", "")
    github = repo_info.get("github", "")

    # Essayer le scan local d'abord
    if not force_github and local_path and Path(local_path).is_dir():
        print(f"  📂 {name} (local: {local_path})")
        tree = scan_repo(local_path)
        if tree:
            tree["scanned_from"] = local_path
            tree["scan_method"] = "local"
            return tree

    # Fallback: GitHub API
    if github:
        owner, repo_name = github.split("/", 1)
        print(f"  🌐 {name} (GitHub: {github})")
        tree = scan_github_repo(owner, repo_name, token)
        if tree:
            tree["scan_method"] = "github_api"
            return tree

    print(f"  ⚠️  {name} — ni chemin local valide ni GitHub")
    return None


def save_scan(tree, name):
    """Sauvegarde un scan dans scans/."""
    scans_dir = ROOT / "scans"
    scans_dir.mkdir(exist_ok=True)
    filepath = scans_dir / f"{name}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)
    return filepath


def clean_duplicates():
    """Supprime les scans orphelins et doublons."""
    scans_dir = ROOT / "scans"
    repos = load_repos_json()
    repo_names = {r["name"] for r in repos}

    # Scans connus
    known_files = {f"{name}.json" for name in repo_names}
    # Aussi garder les _tree.md et TEMPLATE
    keep_patterns = ["TEMPLATE", "_demo_"]

    removed = []
    kept = []

    for f in sorted(scans_dir.glob("*.json")):
        fname = f.name
        base = fname.replace(".json", "")

        # Garder si c'est un repo connu
        if fname in known_files:
            kept.append(fname)
            continue

        # Garder les demos et templates
        if any(p in fname for p in keep_patterns):
            kept.append(fname)
            continue

        # Doublon? Vérifier si c'est un scan alternatif d'un repo connu
        # Ex: "scanned--yggdrasil-engine.json" → "yggdrasil-engine.json" existe
        is_dupe = False
        for rn in repo_names:
            if rn in base and fname != f"{rn}.json":
                is_dupe = True
                break

        # Anciens noms: shazam-piano-scan, hsbc-algo, winter-tree
        old_names = {
            "shazam-piano-scan": "shazam-piano",
            "hsbc-algo": "HSBC-algo-genetic",
            "winter-tree": "tree",
            "scanned--yggdrasil-engine": "yggdrasil-engine",
        }
        if base in old_names:
            is_dupe = True

        if is_dupe:
            print(f"  🗑️  Doublon: {fname}")
            f.unlink()
            removed.append(fname)
        else:
            # Repo pas dans repos.json — orphelin
            print(f"  ❓ Orphelin (pas dans repos.json): {fname}")
            kept.append(fname)

    # Aussi nettoyer les _tree.md orphelins
    for f in sorted(scans_dir.glob("*_tree.md")):
        base = f.name.replace("_tree.md", "")
        if not (scans_dir / f"{base}.json").exists():
            print(f"  🗑️  MD orphelin: {f.name}")
            f.unlink()
            removed.append(f.name)

    return removed, kept


def print_forest_summary(scans_dir):
    """Affiche un résumé de la forêt après sync."""
    trees = []
    for f in sorted(scans_dir.glob("*.json")):
        if f.name.startswith("_demo") or f.name == "TEMPLATE_v2.md":
            continue
        try:
            with open(f, "r", encoding="utf-8") as fh:
                t = json.load(fh)
            trees.append((f.name, t))
        except:
            continue

    if not trees:
        print("  Aucun scan trouvé.")
        return

    total_lines = 0
    total_files = 0

    print(f"\n  {'═' * 65}")
    print(f"  🌲 LA FORÊT — {len(trees)} arbres")
    print(f"  {'═' * 65}")
    print(f"  {'Repo':<30s} {'Famille':<10s} {'Lignes':>8s} {'Fichiers':>8s}  {'Date':<12s}")
    print(f"  {'─' * 65}")

    for fname, t in sorted(trees, key=lambda x: x[1].get("stats", {}).get("total_code_lines", 0), reverse=True):
        name = fname.replace(".json", "")
        emoji = t.get("family_emoji", "?")
        fam = t.get("family_name", "?")[:8]
        stats = t.get("stats", {})
        lines = stats.get("total_code_lines", 0)
        files = stats.get("total_files", 0)
        date = t.get("date", "?")[:10]
        method = t.get("scan_method", "")
        marker = "📂" if method == "local" else "🌐" if method == "github_api" else "  "

        total_lines += lines
        total_files += files

        print(f"  {marker} {name:<28s} {emoji}{fam:<9s} {lines:>8,}  {files:>8}  {date}")

    print(f"  {'─' * 65}")
    print(f"  {'TOTAL':<30s} {'':10s} {total_lines:>8,}  {total_files:>8}")
    print(f"  {'═' * 65}")


def sync_all(force_github=False, target=None):
    """Synchronise tous les repos."""
    repos = load_repos_json()
    token = load_github_token()
    scans_dir = ROOT / "scans"

    if not repos:
        print("  ❌ Aucun repo dans repos.json")
        return

    # Filtrer si --one
    if target:
        repos = [r for r in repos if r["name"] == target]
        if not repos:
            print(f"  ❌ Repo '{target}' pas trouvé dans repos.json")
            return

    print(f"\n  🌲 SYNC ALL — {len(repos)} repos")
    print(f"  {'─' * 50}")

    updated = 0
    failed = 0
    skipped = 0

    for repo in repos:
        name = repo["name"]
        tree = scan_one_repo(repo, token, force_github)

        if tree:
            # Sauvegarder
            save_scan(tree, name)
            lines = tree.get("stats", {}).get("total_code_lines", 0)
            emoji = tree.get("family_emoji", "🌳")
            print(f"    {emoji} {name}: {lines:,}L ✅")
            updated += 1
        else:
            # Garder l'ancien scan s'il existe
            old_scan = scans_dir / f"{name}.json"
            if old_scan.exists():
                print(f"    ⚠️  {name}: scan échoué, ancien scan conservé")
                skipped += 1
            else:
                print(f"    ❌ {name}: pas de scan")
                failed += 1

    print(f"\n  {'─' * 50}")
    print(f"  ✅ {updated} mis à jour | ⚠️ {skipped} conservés | ❌ {failed} échoués")

    # Résumé
    print_forest_summary(scans_dir)


def main():
    args = sys.argv[1:]

    if "--clean" in args:
        print("\n  🧹 NETTOYAGE DES SCANS")
        print(f"  {'─' * 40}")
        removed, kept = clean_duplicates()
        print(f"\n  Supprimés: {len(removed)} | Conservés: {len(kept)}")
        return

    force_github = "--github" in args
    target = None
    if "--one" in args:
        idx = args.index("--one")
        if idx + 1 < len(args):
            target = args[idx + 1]
        else:
            print("Usage: sync_all.py --one <nom_repo>")
            return

    sync_all(force_github=force_github, target=target)


if __name__ == "__main__":
    main()
