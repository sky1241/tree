#!/usr/bin/env python3
"""
WINTER TREE — Hook universel pour n'importe quel repo.
S'installe via: python hooks/install_all_hooks.py (depuis le repo tree)

Avant chaque commit, met à jour un fichier .winter-tree-stats.json
avec les stats du repo (lignes, fichiers, langages, phase).
Léger, rapide, pas de dépendances.
"""
import json
import os
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent.parent  # .git/hooks/ → repo root
STATS_FILE = ROOT / ".winter-tree-stats.json"

# Extensions code → langage
EXT_LANG = {
    ".py": "Python", ".dart": "Dart", ".js": "JavaScript", ".ts": "TypeScript",
    ".jsx": "React", ".tsx": "React", ".vue": "Vue",
    ".swift": "Swift", ".kt": "Kotlin", ".java": "Java",
    ".rs": "Rust", ".go": "Go", ".rb": "Ruby", ".php": "PHP",
    ".c": "C", ".cpp": "C++", ".h": "C/C++", ".cs": "C#",
    ".sh": "Shell", ".ps1": "PowerShell", ".html": "HTML", ".css": "CSS",
}

IGNORE = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".idea", ".vscode", ".DS_Store", "build", "dist", ".next",
    ".dart_tool", ".pub-cache", ".flutter-plugins", "Pods", ".gradle", "target",
}

def count_lines(filepath):
    try:
        return sum(1 for _ in open(filepath, "r", encoding="utf-8", errors="ignore"))
    except:
        return 0

def scan():
    lang_count = {}
    total_files = 0
    total_code_lines = 0
    biggest = {"path": "", "lines": 0, "lang": ""}

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE]
        for f in files:
            fpath = Path(root) / f
            ext = fpath.suffix.lower()
            total_files += 1

            if ext in EXT_LANG:
                lines = count_lines(fpath)
                lang = EXT_LANG[ext]
                lang_count[lang] = lang_count.get(lang, 0) + lines
                total_code_lines += lines
                if lines > biggest["lines"]:
                    biggest = {"path": str(fpath.relative_to(ROOT)), "lines": lines, "lang": lang}

    # Phase
    if total_code_lines < 500:
        phase = "GRAINE"
    elif total_code_lines < 2000:
        phase = "GERMINATION"
    elif total_code_lines < 10000:
        phase = "CROISSANCE"
    else:
        phase = "CANOPÉE"

    return {
        "repo": ROOT.name,
        "date": datetime.now().isoformat(),
        "phase": phase,
        "total_files": total_files,
        "total_code_lines": total_code_lines,
        "languages": lang_count,
        "biggest_file": biggest,
    }

def main():
    stats = scan()

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # Git add the stats file
    os.system(f'git add "{STATS_FILE}"')

    print(f"[winter-tree] ✅ {stats['repo']}: {stats['total_code_lines']:,}L, phase {stats['phase']}")

if __name__ == "__main__":
    main()
