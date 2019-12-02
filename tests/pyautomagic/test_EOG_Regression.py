import numpy as np
from performEOGRegression import perform_EOG_regression
import pytest

def test_EOG_Regression():
    """Test for EOG Regression in EEG data"""

    # making a random signal with no noise
    pure = np.array(np.linspace(-1, 1, 100))
    noise = np.array(np.random.normal(0, 1, pure.shape))
    # adding noise to the signal
    signal = pure + noise
    clean = perform_EOG_regression(signal, noise)
    # checking if the clean signal is similar to the pure signal
    assert np.sqrt(np.mean((clean - pure) ** 2)) < 0.1


