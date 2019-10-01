import pytest
import numpy as np
from pyautomagic.preprocessing.performEOGRegression import performEOGRegression 

def test_performEOGRegression():
    eeg=np.array([[1, 2, 4, 0.8], [0.1, 0.2, 0.4, 0.9]])
    eog=np.array([[9, 10, 11, 12], [10, 12, 3, 4]])
    assert np.array_equal(np.round(performEOGRegression(eeg, eog), 2), 
                          np.round(np.array([[-0.42197603, 0.47275097, 1.71501431, -1.64957357],
                                             [-0.07695577, 0.04392939, -0.2369535, 0.23831638]]),2))

