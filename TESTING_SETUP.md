# Guide to setup Testing Environment

Run tests and also autoformatting of your code. Install black, pylint, pytest, and pytest-coverage.
    
    conda install sphinx black pytest pytest-cov coverage 
    pip install pydocstyle check_manifest
    pip install coverage-badge
    black pyautomagic/*
    pylint ./pyautomagic/

Use sphinx to generate documentation:

    sphinx-quickstart

# Testing Scipts

    pytest --cov-config=.coveragerc --cov=./pyautomagic/ tests/
    coverage-badge -f -o coverage.svg


# Updating Packages

    conda update --all
    pip freeze > requirements.txt
    conda env export > environment.yaml


# Documentation Setup Guidelines

Steps to create documentation for this package

1. Install and setup sphinx from terminal and run through the options, defaults are okay when available
    
    ```
    pip install sphinx sphinx_bootstrap_theme sphinx_gallery numpydoc
    mkdir docs
    cd docs
    sphinx-quickstart
    ```
   
2. Edit the `conf.py` file. 

    conf.py is adapted from mne-bids file. The most important additions to make are:
    
    - Append the path with documented code using sys.path.append
    - Include the extensions autodoc, intersphinx, viewcode, autosummary, numpydoc,
      githubpages, and gen\_gallery
    - Make sure the master\_doc field is correct. 
    - Change the theme to 'bootstrap', which must be installed and linked with the
      path 
    
    html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
    
    To create the jupyter notebooks from example documents, use
    
    ```
    sphinx_gallery_conf = {
        'example_dirs': '../examples',
        'gallery_dirs': 'auto_examples',
        'filename_pattern': '^((?!sgskip).)*$',
        'backreferences_dir': 'generated',
        'binder': {
            'org' : 'Org name',
            'repo': 'repo name'
            'branch': 'branch name',
            'binder_url': 'https://mybinder.org',
            'dependencies': [
                '..environment.yml'
            ],
         }
     }
    ```
   
3. Update the `Makefile`, directly borrowed from mne-bids.

4. Create the automodule document, `funcref.rst` with the following format:
    
    ```
    .. contents:: Table of Contents

    module_one_name
    ======================
    .. automodule:: path.to.module.one.file
        :members:

    module_two_name
    ======================
    .. automodule:: path.to.module.two.file
        :members:
   ```
   
    And so on for every module to be documented.

5. Create the `index.rst` file.
    
    We use html containers to link to each of the modules. The reference to the module has the following format:
    
    ```
    <a href="path/to/funcref.html#module-path.to.module.file">Button Name</a>
    ```