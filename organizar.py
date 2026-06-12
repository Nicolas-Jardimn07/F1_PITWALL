"""
Execute este script UMA VEZ dentro da pasta f1_pitwall/ para mover
os arquivos para as subpastas corretas:

    cd ~/f1_pitwall
    python organizar.py
"""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Mapa: arquivo → subpasta destino
MOVER = {
    "theme.py":        "utils",
    "constants.py":    "utils",
    "helpers.py":      "utils",
    "home.py":         "pages",
    "historical.py":   "pages",
    "live_mode.py":    "pages",
    "english_study.py":"pages",
    "charts.py":       "components",
    "f1_data.py":      "data",
    "season_data.py":  "data",
    "content.py":      "data",
}
# news.py existe em pages/ E em data/ — o da raiz vai para data/
# (o pages/news.py já deve ter sido copiado antes)

for filename, subpasta in MOVER.items():
    src  = ROOT / filename
    dest_dir = ROOT / subpasta
    dest = dest_dir / filename

    dest_dir.mkdir(exist_ok=True)

    # Cria __init__.py se não existir
    init = dest_dir / "__init__.py"
    if not init.exists():
        init.touch()

    if src.exists():
        shutil.move(str(src), str(dest))
        print(f"  ✅  {filename} → {subpasta}/")
    elif dest.exists():
        print(f"  ✓   {subpasta}/{filename} já está no lugar")
    else:
        print(f"  ❌  {filename} não encontrado!")

# news.py: se ainda estiver na raiz, vai para data/
# se já tiver um pages/news.py, copia para data/news.py também
news_root = ROOT / "news.py"
news_data = ROOT / "data" / "news.py"
news_pages = ROOT / "pages" / "news.py"

if news_root.exists() and not news_data.exists():
    shutil.copy(str(news_root), str(news_data))
    print(f"  ✅  news.py → data/news.py (copiado)")
    if not news_pages.exists():
        shutil.move(str(news_root), str(news_pages))
        print(f"  ✅  news.py → pages/news.py (movido)")
    else:
        news_root.unlink()
elif news_root.exists():
    # Determina destino pelo conteúdo
    content = news_root.read_text()
    if "fetch_f1_news" in content and "def render" not in content:
        dest = news_data
        label = "data/news.py"
    else:
        dest = news_pages
        label = "pages/news.py"
    if not dest.exists():
        shutil.move(str(news_root), str(dest))
        print(f"  ✅  news.py → {label}")
    else:
        news_root.unlink()
        print(f"  ✓   news.py removido da raiz (já existe no destino)")

print("\n✅  Pronto! Rode: streamlit run app.py")
