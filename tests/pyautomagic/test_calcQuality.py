import numpy as np
import pytest

from pyautomagic.src.calcQuality import calcQuality

"""

"""


def test_basic_input():
    time = np.arange(0.001, 0.1, 0.001)
    eeg = np.stack((100 * np.sin(50 * time), 10 * np.cos(40 * time)))
    bad_chans = [2]
    expected_quality = {
        "overall_high_amp": 0,
        "times_high_var": 0.7475,
        "ratio_bad_chans": 0.5,
        "chan_high_var": 1,
        "mean_abs_volt": 30.6472,
        "overallThresh": 50,
        "timeThresh": 25,
        "chanThresh": 25,
        "apply_common_avg": True,
    }
    calculated_quality = calcQuality(eeg, bad_chans)
    assert expected_quality["overall_high_amp"] == pytest.approx(
        calculated_quality["overall_high_amp"], 0.001
    )
    assert expected_quality["times_high_var"] == pytest.approx(
        calculated_quality["times_high_var"], 0.001
    )
    assert expected_quality["ratio_bad_chans"] == pytest.approx(
        calculated_quality["ratio_bad_chans"], 0.001
    )
    assert expected_quality["chan_high_var"] == pytest.approx(
        calculated_quality["chan_high_var"], 0.001
    )
    assert expected_quality["mean_abs_volt"] == pytest.approx(
        calculated_quality["mean_abs_volt"], 0.001
    )


def test_not_enough_inputs():
    with pytest.raises(TypeError):
        calculated_quality = calcQuality()


def test_parameters():
    overallThresh = 20
    chanThresh = 20
    timeThresh = 20
    avg_ref = False
    time = np.arange(0.001, 0.1, 0.001)
    eeg = np.stack((100 * np.sin(50 * time), 10 * np.cos(40 * time)))
    bad_chans = [2]
    expected_quality = {
        "overall_high_amp": 0.4394,
        "times_high_var": 0.8081,
        "ratio_bad_chans": 0.5,
        "chan_high_var": 0.5,
        "mean_abs_volt": 36.3618,
        "overallThresh": 20,
        "timeThresh": 20,
        "chanThresh": 20,
        "apply_common_avg": False,
    }
    calculated_quality = calcQuality(
        eeg, bad_chans, overallThresh, timeThresh, chanThresh, avg_ref
    )
    assert expected_quality["overall_high_amp"] == pytest.approx(
        calculated_quality["overall_high_amp"], 0.001
    )
    assert expected_quality["times_high_var"] == pytest.approx(
        calculated_quality["times_high_var"], 0.001
    )
    assert expected_quality["ratio_bad_chans"] == pytest.approx(
        calculated_quality["ratio_bad_chans"], 0.001
    )
    assert expected_quality["chan_high_var"] == pytest.approx(
        calculated_quality["chan_high_var"], 0.001
    )
    assert expected_quality["mean_abs_volt"] == pytest.approx(
        calculated_quality["mean_abs_volt"], 0.001
    )
