# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'myapp'
copyright = '2025, Deivid Palacios'
author = 'Deivid Palacios'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode', 'sphinx.ext.napoleon']

templates_path = ['_templates']
exclude_patterns = [
    'venv/**', #Excluir los archivos del entorno virtual
    'venv/Lib/site-packages/**', #Excluir paquetes instalados
    '**/LICENSE.rst', #Excluir todos los archivos LICENSE.rst
    '**/templates/**', #Excluir plantillas
]

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys
import django
sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
