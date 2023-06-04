# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PyWikipedia2LaTeX'
copyright = '2023, L.E.Charles'
author = 'L.E.Charles'
release = '1.0.0'

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'

html_static_path = ['_static']
pygments_style = "sphinx"
pygments_dark_style = "monokai"


html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "black",
        "color-brand-content": "black"
    },
    "dark_css_variables": {
        "color-brand-primary": "white",
        "color-brand-content": "white"
    },
    "light_logo": "logo_light.png",
    "dark_logo": "logo_dark.png",
    "sidebar_hide_name":True,
}

