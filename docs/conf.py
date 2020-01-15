# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
import pyautomagic

import sphinx_gallery  # noqa: F401
from sphinx_gallery.sorting import ExampleTitleSortKey
import sphinx_bootstrap_theme

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../pyautomagic/src'))
sys.path.insert(0, os.path.abspath('../pyautomagic/preprocessing'))

# -- Project information -----------------------------------------------------

project = u'pyautoomagic'
td = datetime.date.today()
copyright = '2019, C. Zurn, R. Bechtold, A. Lawrence, L. Xiang, S. Meza, D. Soni'
author = 'C. Zurn, R. Bechtold, A. Lawrence, L. Xiang, S. Meza, D. Soni'

version = pyautomagic.__version__
# The full version, including alpha/beta/rc tags
release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.napoleon','sphinx.ext.autodoc'
]

napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# HTML options (e.g., theme)
# see: https://sphinx-bootstrap-theme.readthedocs.io/en/latest/README.html
# Clean up sidebar: Do not show "Source" link
html_show_sourcelink = False

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'navbar_title': 'PyAutomagic',
    'bootswatch_theme': "flatly",
    'navbar_sidebarrel': False,  # no "previous / next" navigation
    'navbar_pagenav': False,  # no "Page" navigation in sidebar
    'bootstrap_version': "3",
    'navbar_links': [
        ("Examples", "auto_examples/index"),
        ("API", "api"),
        ("What's new", "whats_new"),
        ("Github", "https://github.com/neurodatadesign/pyautomagic", True),
    ]}

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'mne': ('https://mne.tools/stable/', None),
    'mne-bids': ('http://mne.tools/mne-bids/', None),
    'numpy': ('https://www.numpy.org/devdocs', None),
    'scipy': ('https://scipy.github.io/devdocs', None),
    'matplotlib': ('https://matplotlib.org', None),
}

sphinx_gallery_conf = {
    'examples_dirs': '../examples',
    'within_subsection_order': ExampleTitleSortKey,
    'gallery_dirs': 'auto_examples',
    'filename_pattern': '^((?!sgskip).)*$',
    'backreferences_dir': 'generated',
    'binder': {
        # Required keys
        'org': 'neurodatadesign',
        'repo': 'pyautomagic',
        'branch': 'gh-pages',  # noqa: E501 Can be any branch, tag, or commit hash. Use a branch that hosts your docs.
        'binderhub_url': 'https://mybinder.org',  # noqa: E501 Any URL of a binderhub deployment. Must be full URL (e.g. https://mybinder.org).
        'dependencies': [
            './environment.yml'
        ],
    }
}

# -- Options for LaTeX output -------------------------------------------------

latex_elements = {
  'extraclassoptions': 'openany,oneside'
}
