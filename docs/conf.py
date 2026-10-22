"""Sphinx configuration for the MACR documentation."""

import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))

project = "MACR"
copyright = "2026, MACR Developers"
author = "MACR Developers"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

html_theme = "pydata_sphinx_theme"
html_title = "MACR"
html_theme_options = {
    "github_url": "https://github.com/cda24/MACR",
    "use_edit_page_button": True,
    "show_nav_level": 2,
    "show_toc_level": 2,
    "navigation_with_keys": True,
    "navbar_align": "left",
    "secondary_sidebar_items": ["page-toc", "sourcelink"],
}

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}
autodoc_typehints = "description"
