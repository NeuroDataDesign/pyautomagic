import numpy as np
from sklearn.decomposition import TruncatedSVD


"""
    Cian Scannell - Oct-2017 (https://github.com/cianmscannell/RPCA)
    Computes rpca separation of M into L(low rank) and S(Sparse) using the parameter lam
    this uses the alternating directions augmented method of multipliers
    as described in my blog
"""
def rpca(M,lam,tol,maxIter):

    """ Perform Robust Principle Component Analysis:
    -Input = [M,lam,tol,maxIter]
           EEG = EEG Data (must include)
           lam = Lamda paramter for RPCA (default = 1/(sqrt(# of Colunms))
           tol = Tolerance (defalut = 1e-7) RPCA param
           maxIter = Maximum Iterations (deafult = 1000)

    -Output = [L, S]
            L = Corrected Data (Low rank matrix)
            S = Noise removed from the data (Sparse Matrix)
            M = L + S        
    
    -Summary = Performs a Robust Principal Component Analysis on the EEG data with
            the specified parameters: Lamda, Tolerance, and Maximum number of Iterations.
            The function outputs the EEG data with the noise removed as well as the nosie
            that was removed.
"""

    Nr = M.shape[0]
    Nc = M.shape[1]
    norm_2 = np.linalg.norm(M,2)
    norm_inf = np.linalg.norm(M,np.inf) / lam
    dual_norm = np.maximum(norm_2, norm_inf)
    Y = M / dual_norm

    mu = 1.25 / norm_2
    mu_bar = mu * 1e7
    rho = 1.5

    L = np.zeros((Nr,Nc))
    S = np.zeros((Nr,Nc))    
    
    error = 10
    count = 0
    isRunning = True;
    while (isRunning and error > tol):
        temp_t = M-L+(Y/mu)
        S = soft_thres(temp_t, lam/mu)
        U,sig,V = np.linalg.svd(M-S+(Y/mu), full_matrices=False)
        L = np.dot(U, np.dot(np.diag(soft_thres(sig, 1/mu)), V))
        Y = Y + mu*(M-L-S)
        mu = np.minimum(mu*rho,mu_bar)
        error = np.linalg.norm(M-L-S,'fro')/np.linalg.norm(M,'fro')
        count += 1 
        if (count >= maxIter):
            isRunning = False;
            
            
    L = L.reshape(Nr,Nc)
    S = S.reshape(Nr,Nc)

    return L,S

def soft_thres(x,eps):
    """
    Cian Scannell - Oct-2017  
    Soft thresholds a matrix x at the eps level
    i.e ST(x,eps)_ij = sgn(x_ij) max(|x_ij| - eps, 0)
    """
    a = np.sign(x)
    b = np.maximum((np.fabs(x) - eps), 0)
    return np.multiply(a,b)
