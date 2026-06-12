"""
Corrige o menu duplo do Streamlit.

O Streamlit detecta automaticamente arquivos .py dentro de uma pasta
chamada exatamente "pages/" e cria um menu de navegação extra.

Este script renomeia pages/ → _pages/ (e as outras subpastas por consistência)
e atualiza todos os imports automaticamente.

Execute UMA VEZ:
    cd ~/f1_pitwall
    python corrigir_menu.py
"""
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ── 1. Renomear pastas
RENOMEAR = {
    "pages":      "_pages",
    "data":       "_data",
    "utils":      "_utils",
    "components": "_components",
}

print("1. Renomeando pastas...")
for antigo, novo in RENOMEAR.items():
    src  = ROOT / antigo
    dest = ROOT / novo
    if src.exists() and not dest.exists():
        shutil.copytree(str(src), str(dest))
        shutil.rmtree(str(src))
        print(f"   ✅  {antigo}/ → {novo}/")
    elif dest.exists():
        print(f"   ✓   {novo}/ já existe, pulando")
    else:
        print(f"   ⚠️  {antigo}/ não encontrado")

# ── 2. Atualizar imports em todos os .py do projeto
print("\n2. Atualizando imports...")

SUBSTITUICOES = [
    ("from pages.",      "from _pages."),
    ("import pages.",    "import _pages."),
    ("from data.",       "from _data."),
    ("import data.",     "import _data."),
    ("from utils.",      "from _utils."),
    ("import utils.",    "import _utils."),
    ("from components.", "from _components."),
    ("import components.","import _components."),
]

py_files = list(ROOT.rglob("*.py"))
for py_file in py_files:
    if py_file.name in ("corrigir_menu.py", "organizar.py", "organizar_v2.py", "setup_check.py"):
        continue
    try:
        original = py_file.read_text(encoding="utf-8")
        novo_conteudo = original
        for velho, novo in SUBSTITUICOES:
            novo_conteudo = novo_conteudo.replace(velho, novo)
        if novo_conteudo != original:
            py_file.write_text(novo_conteudo, encoding="utf-8")
            print(f"   ✅  {py_file.relative_to(ROOT)}")
    except Exception as e:
        print(f"   ⚠️  Erro em {py_file.name}: {e}")

print("\n✅  Pronto! O menu duplo foi corrigido.")
print("    Rode: streamlit run app.py")
