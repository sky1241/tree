#!/usr/bin/env python3
# SETUP.PY - Configuration automatique complete du Winter Tree.
# Usage: python setup.py
# Fait TOUT en une seule commande: detecte les repos, installe les hooks, sync.

import json
import os
import sys
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
REPOS_JSON = ROOT / "repos.json"
HOOK_TEMPLATE = ROOT / "hooks" / "repo-hook-template.py"
TREE_HOOK = ROOT / "hooks" / "pre-commit"

# Extensions code
EXT_LANG = {
    ".py": "Python", ".dart": "Dart", ".js": "JavaScript", ".ts": "TypeScript",
    ".jsx": "React", ".tsx": "React", ".vue": "Vue",
    ".swift": "Swift", ".kt": "Kotlin", ".java": "Java",
    ".rs": "Rust", ".go": "Go", ".rb": "Ruby", ".php": "PHP",
    ".c": "C", ".cpp": "C++", ".h": "C/C++", ".cs": "C#",
    ".sh": "Shell", ".ps1": "PowerShell", ".html": "HTML", ".css": "CSS",
}

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".idea", ".vscode", ".DS_Store", "build", "dist", ".next",
    ".dart_tool", ".pub-cache", ".flutter-plugins", "Pods",
    ".gradle", "target", "AppData", "Application Data",
    "Windows", "Program Files", "ProgramData", ".cache", ".npm",
}


def run(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return r.stdout.strip()


def step(msg):
    print(f"\n  {'=' * 60}")
    print(f"  {msg}")
    print(f"  {'=' * 60}")


# ─────────────────────────────────────────────────────────────
# STEP 1: DETECT ALL REPOS
# ─────────────────────────────────────────────────────────────
def detect_repos():
    step("1/4  DETECTION DES REPOS")

    with open(REPOS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    repo_names = {r["name"] for r in data["repos"]}
    home = Path.home()

    search_dirs = []
    for d in [
        ROOT.parent,
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
        home / "AndroidStudioProjects",
    ]:
        if d.exists() and d not in search_dirs:
            search_dirs.append(d)

    for drive in ["D:/", "E:/"]:
        d = Path(drive)
        if d.exists():
            search_dirs.append(d)

    found = {}
    for base in search_dirs:
        for root_dir, dirs, files in os.walk(base):
            rel = Path(root_dir).relative_to(base)
            if len(rel.parts) > 4:
                dirs.clear()
                continue
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

            git_dir = Path(root_dir) / ".git"
            if git_dir.is_dir():
                try:
                    result = subprocess.run(
                        ["git", "remote", "-v"],
                        capture_output=True, text=True,
                        cwd=root_dir, timeout=5
                    )
                    if "sky1241" in result.stdout:
                        repo_name = Path(root_dir).name
                        found[repo_name] = str(Path(root_dir).resolve())
                except:
                    pass
                dirs.clear()

    # Mapper les noms alternatifs
    alt_names = {
        ".infernal_wheel": "infernal-wheel",
        "infernal_wheel": "infernal-wheel",
    }

    updated = 0
    for repo in data["repos"]:
        name = repo["name"]
        # Direct match
        if name in found:
            repo["local_path"] = found[name]
            print(f"  OK {name}: {found[name]}")
            updated += 1
        else:
            # Try alternative names
            for alt, real in alt_names.items():
                if real == name and alt in found:
                    repo["local_path"] = found[alt]
                    print(f"  OK {name}: {found[alt]}")
                    updated += 1
                    break
            else:
                lp = repo.get("local_path", "")
                if lp and Path(lp).is_dir():
                    print(f"  OK {name}: {lp} (deja configure)")
                else:
                    print(f"  -- {name}: pas sur le disque (GitHub API only)")

    with open(REPOS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n  {updated} repos detectes sur le disque")
    return data


# ─────────────────────────────────────────────────────────────
# STEP 2: INSTALL HOOKS
# ─────────────────────────────────────────────────────────────
def install_hooks(data):
    step("2/4  INSTALLATION DES HOOKS")

    installed = 0
    for repo in data["repos"]:
        if not repo.get("active", True):
            continue

        name = repo["name"]
        local_path = repo.get("local_path", "")

        if not local_path or not Path(local_path).is_dir():
            continue

        git_hooks = Path(local_path) / ".git" / "hooks"
        if not git_hooks.exists():
            continue

        target = git_hooks / "pre-commit"
        src = TREE_HOOK if name == "tree" else HOOK_TEMPLATE

        if not src.exists():
            continue

        try:
            shutil.copy2(src, target)
            os.chmod(target, 0o755)
            print(f"  OK {name}")
            installed += 1
        except Exception as e:
            print(f"  !! {name}: {e}")

    print(f"\n  {installed} hooks installes")


# ─────────────────────────────────────────────────────────────
# STEP 3: SYNC VIA GITHUB API
# ─────────────────────────────────────────────────────────────
def sync_github(data):
    step("3/4  SYNC VIA GITHUB API")

    # Charger le token
    token = os.environ.get("GITHUB_TOKEN")
    for token_file in [SCRIPTS / "CLEGITJAMAISTOUCHER.txt", ROOT / "CLEGITJAMAISTOUCHER.txt"]:
        if not token and token_file.exists():
            token = token_file.read_text().strip()

    if not token:
        print("  !! Pas de token GitHub, skip sync")
        print("  -> Mettre le token dans scripts/CLEGITJAMAISTOUCHER.txt")
        return

    sys.path.insert(0, str(SCRIPTS))
    try:
        from engine import scan_github_repo
    except ImportError:
        print("  !! engine.py introuvable, skip sync")
        return

    scans_dir = ROOT / "scans"
    scans_dir.mkdir(exist_ok=True)

    total_lines = 0
    synced = 0

    for repo in data["repos"]:
        if not repo.get("active", True):
            continue

        name = repo["name"]
        github = repo.get("github", "")
        if not github:
            continue

        owner, repo_name = github.split("/", 1)
        try:
            tree = scan_github_repo(owner, repo_name, token)
            if tree:
                tree["scan_method"] = "github_api"
                scan_file = scans_dir / f"{name}.json"
                with open(scan_file, "w", encoding="utf-8") as f:
                    json.dump(tree, f, indent=2, ensure_ascii=False)
                lines = tree.get("stats", {}).get("total_code_lines", 0)
                emoji = tree.get("family_emoji", "?")
                print(f"  {emoji} {name}: {lines:,}L")
                total_lines += lines
                synced += 1
        except Exception as e:
            print(f"  !! {name}: {e}")

    print(f"\n  {synced} repos scannes, {total_lines:,} lignes totales")


# ─────────────────────────────────────────────────────────────
# STEP 4: POWERSHELL SHORTCUT
# ─────────────────────────────────────────────────────────────
def setup_shortcut():
    step("4/4  RACCOURCI POWERSHELL")

    tree_path = str(ROOT).replace("\\", "\\\\")
    sync_cmd = f'function tree-sync {{ python "{tree_path}\\\\scripts\\\\sync_all.py" @args }}'
    setup_cmd = f'function tree-setup {{ python "{tree_path}\\\\setup.py" @args }}'

    print(f"  Pour avoir 'tree-sync' et 'tree-setup' partout,")
    print(f"  colle ceci dans ton profil PowerShell ($PROFILE):")
    print()
    print(f'  function tree-sync {{ python "{ROOT}\\scripts\\sync_all.py" @args }}')
    print(f'  function tree-setup {{ python "{ROOT}\\setup.py" @args }}')
    print()
    print(f"  Apres: tree-sync         = re-scanne tout")
    print(f"         tree-sync --github = via GitHub API")
    print(f"         tree-setup        = reinstalle tout")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    print()
    print("  " + "#" * 60)
    print("  #  WINTER TREE — SETUP AUTOMATIQUE                      #")
    print("  " + "#" * 60)

    # 1. Detect
    data = detect_repos()

    # 2. Hooks
    install_hooks(data)

    # 3. Sync
    sync_github(data)

    # 4. Shortcut
    setup_shortcut()

    print()
    print("  " + "#" * 60)
    print("  #  SETUP TERMINE                                        #")
    print("  " + "#" * 60)
    print()


if __name__ == "__main__":
    main()
