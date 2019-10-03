import numpy as np
import pytest
import performRPCA
"""
Basic unit Testing for performRPCA
Tests basic input, erorr on no input, and changing the parameters.
"""
def test_basic_input():
    EEG = np.array([[1,2],[3,4]])
    expected_A = np.array([[1.00000027, 1.62530315],[2.58654179, 3.99999973]])
    expected_E = np.array([[-0.,0.37469685],[ 0.41345821, 0.]])
    A,E = performRPCA.performRPCA(EEG);
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))

def test_no_input():
    with pytest.raises(TypeError):
        A,E = performRPCA.performRPCA();

def test_params():
    EEG = np.array([[1,2,3],[4,5,6],[7,8,9]])
    lam = .7
    tol = 1e-8
    maxIter = 20
    expected_A = np.array([[1., 2., 3.],[4., 5., 6.],[7.,8.,9.]])
    expected_E = np.array([[-0.,0,0],[0,0,0],[0,0,0]])
    A,E = performRPCA.performRPCA(EEG,lam,tol,maxIter);
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
