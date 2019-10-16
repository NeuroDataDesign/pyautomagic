import numpy as np
import pytest
import performRPCA


def test_basic_input1():
    EEG = np.array([[1,2],[3,4]])
    expected_A = np.array([[1.00000014,1.47051825],[1.47569674,2.17003868]])
    expected_E = np.array([[0.,0.52948166],[1.52430317,1.82996138]])
    A,E = performRPCA.performRPCA(EEG);
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
    print('test_basic_input1 Pass')
    
def test_basic_input2():
    EEG = np.array([[1,2,3],[4,5,6],[7,8,9]])
    expected_A = np.array([[1.5999989,1.99999912,2.3999982],\
                           [3.99999961,5.00000076,5.99999904],\
                           [5.13368148,6.41710344,7.70052173]])
    expected_E = np.array([[-5.99998725e-01,4.82951146e-07,6.00002018e-01],\
                           [0.00000000e+00,-0.00000000e+00,5.78509154e-07],\
                           [1.86631877e+00,1.58289609e+00,1.29947849e+00]])
    A,E = performRPCA.performRPCA(EEG);
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
    print('test_basic_input2 Pass')

def test_basic_input3():
    EEG = np.array([[1,2,3,4,5,6,7],[10,2,-30,6,15,39,92]])
    expected_A = np.array([[0.99999674,2.00000276,0.34522968,4.00000449,5.00000174,5.9999975,6.99999895],\
                           [10.00000152,1.99999938,-29.50244429,5.99999916,15.00000048,35.50896724,36.46037802]])
    expected_E = np.array([[0,0,2.65476565,0,0,0,0],\
                           [0,0,-0.49755573,0,0,3.49103264,55.5396215]])
    A,E = performRPCA.performRPCA(EEG);
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
    print('test_basic_input3 Pass')    

def test_no_input():
    with pytest.raises(TypeError):
        A,E = performRPCA.performRPCA()
    assert(True)
    print('test_no_input Pass')
    
def test_incorrect_input():
    with pytest.raises(AttributeError):
        A,E = performRPCA.performRPCA("Wrong input Type")
    assert(True)
    print('test_incorrect_input Pass')

def test_params1():
    EEG = np.array([[1,2,3],[4,5,6],[7,8,9]])
    lam = .7
    tol = 1e-8
    maxIter = 20
    expected_A = np.array([[1.21416342,1.99964425,2.79453087],\
                           [3.99964063,5.00068211,5.94182001],\
                           [6.75789278,7.94410702,9.00016552]])
    expected_E = np.array([[-0.21397595,0.,0.20564244],\
                           [0.,0.,0.05784774],\
                           [ 0.24228631,0.05555309,0.]])
    A,E = performRPCA.performRPCA(EEG,lam,tol,maxIter)
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
    print('test_params1 Pass')
    
def test_params2():
    EEG = np.array([[1,2,3],[4,5,6],[7,8,9]])
    lam = .2
    tol = 1e-3
    maxIter = 100
    expected_A = np.array([[0,0,0],[0,0,0],[0,0,0]])
    expected_E = np.array([[1,2,3],[4,5,6],[7,8,9]])
    A,E = performRPCA.performRPCA(EEG,lam,tol,maxIter)
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
    print('test_params2 Pass')
    

def test_params3():
    EEG = np.array([[1,2,3],[4,5,6],[7,8,9]])
    lam = .5
    tol = 1e-10
    maxIter = 1000
    expected_A = np.array([[1.45445617,2,2.14299791],\
                           [3.30885118,4.54994966,4.8752663],\
                           [3.31508751,4.55852514,4.88445492]])
    expected_E = np.array([[-0.45445617,0,0.85700209],\
                           [0.69114882,0.45005034,1.1247337],\
                           [3.68491249,3.44147486,4.11554508]])
    A,E = performRPCA.performRPCA(EEG,lam,tol,maxIter)
    assert(np.allclose(A,expected_A))
    assert(np.allclose(E,expected_E))
    print('test_params3 Pass')
    