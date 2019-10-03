import numpy as np
import pytest
from pyautomagic.preprocessing.rpca import performRPCA


def test_basic_input():
    EEG = np.array([[1,2],[3,4]])
    expected_A = np.array([[1.00000014,1.47051825],[1.47569674,2.17003868]])
    expected_E = np.array([[0.,0.52948166],[1.52430317,1.82996138]])
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
    expected_A = np.array([[1.21416342,1.99964425,2.79453087],[3.99964063,5.00068211,5.94182001],[6.75789278,7.94410702,9.00016552]])
    expected_E = np.array([[-0.21397595,0.,0.20564244],[0.,0.,0.05784774],[ 0.24228631,0.05555309,0.]])
    A,E = performRPCA.performRPCA(EEG,lam,tol,maxIter);
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
