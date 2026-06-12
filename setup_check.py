"""
Rode este script UMA VEZ para verificar se todos os arquivos estão no lugar:
    python setup_check.py
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "app.py",
    "utils/__init__.py",
    "utils/constants.py",
    "utils/helpers.py",
    "utils/theme.py",
    "data/__init__.py",
    "data/f1_data.py",
    "data/season_data.py",
    "data/news.py",
    "data/content.py",
    "pages/__init__.py",
    "pages/home.py",
    "pages/historical.py",
    "pages/live_mode.py",
    "pages/news.py",
    "pages/english_study.py",
    "components/__init__.py",
    "components/charts.py",
]

print(f"\n📁 Verificando arquivos em: {ROOT}\n")

missing = []
for f in REQUIRED_FILES:
    path = ROOT / f
    if path.exists():
        print(f"  ✅  {f}")
    else:
        print(f"  ❌  {f}  ← FALTANDO")
        missing.append(f)

print()
if missing:
    print(f"⚠️  {len(missing)} arquivo(s) faltando. Copie-os para a pasta correta.")
    print("\nEstrutura esperada:")
    print("  f1_pitwall/")
    print("  ├── app.py")
    print("  ├── utils/        (constants.py, helpers.py, theme.py, __init__.py)")
    print("  ├── data/         (f1_data.py, season_data.py, news.py, content.py, __init__.py)")
    print("  ├── pages/        (home.py, historical.py, live_mode.py, news.py, english_study.py, __init__.py)")
    print("  └── components/   (charts.py, __init__.py)")
    sys.exit(1)
else:
    print("✅  Todos os arquivos encontrados! Rode: streamlit run app.py")
