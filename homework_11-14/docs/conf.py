import os
import sys

sys.path.append(os.path.abspath(".."))

project = "Contacts REST API"
copyright = "2023, Matajur"
author = "Matajur"
release = "0.1.0"

extensions = ["sphinx.ext.autodoc"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "nature"
html_static_path = ["_static"]
