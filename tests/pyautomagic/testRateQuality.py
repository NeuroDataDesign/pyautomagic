import pytest
from pyautomagic.src.rateQuality import rateQuality


def test_basic_input():
    quality_metrics = {'overall_high_amp': 0.15, 'times_high_var': 0.19, 'ratio_bad_chans': 0.27, 'chan_high_var': 0.2}
    expected_rating = {'dataset_qualification': 50}
    calculated_rating = rateQuality(quality_metrics)

    assert (expected_rating['dataset_qualification'] == pytest.approx(calculated_rating['dataset_qualification'], .001))
