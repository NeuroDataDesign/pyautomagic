# INSTALLATION GUIDE

pyautomagic relies on the following libraries to work:

    numpy
    scipy
    scikit-learn
    pandas
    mne
    matplotlib
    seaborn
    mne-bids
    
Setup virtual environment via Conda inside your Unix-friendly terminal (aka Mac, or Linux) is recommended (see https://docs.anaconda.com/anaconda/install/):

    conda create -n pyautomagic # creates conda env
    conda activate pyautomagic  # activates the environment
    conda config --add channels conda-forge # add extra channels necessary
    conda install numpy pandas mne mne-bids scikit-learn scipy seaborn matplotlib
    
## Install from Github
To install, run this command in your repo:

    pip install -e git+https://github.com/NeuroDataDesign/pyautomagic#egg=pyautomagic
