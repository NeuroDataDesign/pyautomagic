import pytest

@pytest.mark.usefixture('eegts')
class TestDummy():
    def test_dummy(self, eegts):
        """
        Auto-pass a pytest unit test.

        :param eegts:
        :type eegts:
        :return:
        :rtype:
        """
        assert True