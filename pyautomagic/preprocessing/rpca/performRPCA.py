import numpy as np
import preProcessRPCA as preprocess

def performRPCA(EEG, lam=-1, tol=1e-7, maxIter=1000):

    """ Perform Robust Principle Component Analysis:

    Performs a Robust Principal Component Analysis on the EEG data with
    the specified parameters: Lamda, Tolerance, and Maximum number of Iterations.
    The function outputs the EEG data with the noise removed as well as the nosie
    that was removed.
    
    Parameters
    ----------
    EEG : double numpy array
        First Parameter, EEG Data (must include)
    lam : double (default = 1/(sqrt(# of Colunms))
        Second Parameter, lamda paramter for RPCA (input -1 for default calculation)
    tol : double (defalut = 1e-7)
        Third Parameter, tolerance RPCA parameter
    maxIter : int
        Fourth Parameter, Maximum Iterations (deafult = 1000)
    
    Returns
    -------
    Data : double numpy array
        Corrected Data
    Noise : double numpy array
        Noise removed from the data, Original EEG = Data + Noise        
    
    """
    #Find lamda if not provided using the Automagic algorithim
    col = EEG.shape;
    if (lam == -1): #if no input lamda, calculate its value
        lam = 1 / np.sqrt(col[0]);
        
    #Perform Robust Principal Component Analysis
    data, error = preprocess.rpca(EEG,lam,tol,maxIter);
    return data, error;
