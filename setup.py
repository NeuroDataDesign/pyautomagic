import os
import sys

from setuptools import find_packages, setup

"""
To re-setup: 

    python setup.py sdist bdist_wheel

    pip install -r requirements.txt --process-dependency-links

To test on test pypi:
    
    twine upload --repository testpypi dist/*
    
    # test upload
    pip install -i https://test.pypi.org/simple/ --no-deps pyautomagic

    twine upload dist/* 
"""
PACKAGE_NAME = "pyautomagic"
# get the version
version = None
with open(os.path.join("pyautomagic", '__init__.py'), 'r') as fid:
    for line in (line.strip() for line in fid):
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('\'').strip('"')
            break
if version is None:
    raise RuntimeError('Could not determine version')

MAINTAINER = 'Adam Li'
MAINTAINER_EMAIL = 'adam2392@gmail.com'
DESCRIPTION = "A Python3 package for eeg (pre)processing from Automagic."
URL = 'https://github.com/NeuroDataDesign/pyautomagic'
MINIMUM_PYTHON_VERSION = 3, 6  # Minimum of Python 3.6
REQUIRED_PACKAGES = [
    "numpy>=1.14.5",
    "scipy>=1.1.0",
    "scikit-learn>=0.19.2",
    "pandas>=0.23.4",
    "mne>=0.19.2",
    "mne-bids>=0.3",
]
CLASSIFICATION_OF_PACKAGE = [
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Medical Science Apps.',
    'Topic :: Scientific/Engineering',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation',

    'Natural Language :: English',
]


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))


setup(
    name=PACKAGE_NAME,
    version=version,
    description=DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=find_packages(exclude=["tests"]),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url=URL,
    author='NDD19',
    license='MIT',
    keywords="EEG, research tools, automated processing",
    dependency_links=[
        'git+https://github.com/NeuroDataDesign/pyautomagic#egg=pyautomagic',
    ],
    project_urls={
        "Documentation": "https://github.com/NeuroDataDesign/pyautomagic/docs/",
        "Source": URL,
        "Tracker": "https://github.com/NeuroDataDesign/pyautomagic/issues",
    },
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    classifiers=CLASSIFICATION_OF_PACKAGE,
    zip_ok=False,
)
