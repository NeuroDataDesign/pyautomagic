import numpy as np
import pytest

from pyautomagic.preprocessing.perform_EOG_regression import perform_EOG_regression


def test_EOG_egression():
    """Test for EOG Regression in EEG data"""

    # making a random signal with no noise
    np.random.seed(0)
    pure = np.array(np.linspace(-1, 1, 100))
    noise = np.array(np.random.normal(0, 1, pure.shape))
    # adding noise to the signal
    signal = pure + noise
    clean = perform_EOG_regression(signal, noise)
    # checking if the clean signal is similar to the pure signal
    assert np.sqrt(np.mean((clean - pure) ** 2)) < 0.1


