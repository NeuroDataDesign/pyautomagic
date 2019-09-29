import numpy as np
import preProcessRPCA as preprocess

""" Perform Robust Principle Component Analysis:
    -Input = [EEG,params]
           EEG = EEG Data (must include)
           lam = Lamda paramter for RPCA (default = 1/(sqrt(# of Colunms))
           tol = Tolerance (defalut = 1e-7) RPCA param
           maxIter = Maximum Iterations (deafult = 1000)
    
    -Output = [Data, Noise]
            Data = Corrected Data
            Noise = Noise removed from the data
            Original EEG = Data + Noise        
    
    -Summary = Performs a Robust Principal Component Analysis on the EEG data with
            the specified parameters: Lamda, Tolerance, and Maximum number of Iterations.
            The function outputs the EEG data with the noise removed as well as the nosie
            that was removed.
"""

def performRPCA(EEG, lam=[], tol=1e-7, maxIter=1000):
    #Find lamda if not provided using the Automagic algorithim
    col = EEG.shape;
    if (len(lam) == 0): #if no input lamda, calculate its value
        lam = 1 / np.sqrt(col);
        
    #Perform Robust Principal Component Analysis
    data, error = preprocess.rpca(EEG,lam,tol,maxIter);
    return data, error;
