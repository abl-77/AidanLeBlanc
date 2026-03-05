import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from OnlineAlgorithm import OnlineAlgorithm
import numpy as np
from util import get_data
from numpy.linalg import norm
import torch
from numpy_da import DynamicArray
np.random.seed(1)

class CRFRExtension(OnlineAlgorithm):
    def __init__(self, num_features, num_outputs, transform_size, transform_method, sigma, error, lam, **kwargs):
        
        self.x = np.empty((num_features, 0))
        self.y = np.empty((num_outputs, 0))
        self.num_features = num_features
        self.num_outputs = num_outputs
        self.transform_size = transform_size
        if transform_method == "fourier":
            self.transform_method = self._fourier_transform
            self.transform_init = self._fourier_init(sigma)
            
        if transform_method == "random":
            self.transform_method = self._random_transform
            self.transform_init = self._random_init()
            
        if transform_method == "hadamard":
            self.transform_method = self._hadamard_transform
            self.transform_init = self._hadamard_init()
            
        if transform_method == "fastfood":
            self.transform_method = self._fastfood_transform
            self.transform_init = self._fastfood_init(sigma)
            
        self.current_parameters = np.random.uniform(-100, 100, size=(2*transform_size, num_outputs))
        self.error = error
        self.lam = lam
        
        super().__init__(**kwargs)
        
    def update(self, x, y):
        y_hat = self.predict(x)
        self.x = x
        self.y = y
        
        # Perform update for each desired output
        for i in range(self.num_outputs):
            if  np.abs(y_hat[i]) > self.error:
                # Perform parameter update
                err = y_hat[i] - self.error
                self.current_parameters[:, i] = self.current_parameters[:, i] - self._control_input(err, i)[0]

            
    def predict(self, x):
        return self.current_parameters.T @ self.transform_method(x)
            
    def evaluate(self, X, y, criterion):
        total_abs = 0.0
        total_mse = 0.0
        total_mae = 0.0
        total_ss_res = 0.0
        total_ss_tot = 0.0
        count = 0

        y_mean = np.mean(y)

        with torch.no_grad():
            for i in range(X.shape[0]):
                y_pred = self.predict(X[i])  
			
                abs = np.abs(y_pred - y[i]).sum()
                
                mse = criterion(torch.from_numpy(y_pred), torch.from_numpy(y[i])).item()
                mae = np.mean(np.abs(y_pred - y[i])).item()

                ss_res = np.sum((y[i] - y_pred) ** 2).item()    
                ss_tot = np.sum((y[i] - y_mean) ** 2).item()

                total_abs += abs
                total_mse += mse
                total_mae += mae
                total_ss_res += ss_res
                total_ss_tot += ss_tot
                count += 1

        avg_abs = total_abs / count if count > 0 else 0.0
        avg_mse = total_mse / count if count > 0 else 0.0
        avg_mae = total_mae / count if count > 0 else 0.0
        r2 = 1 - (total_ss_res / total_ss_tot) if total_ss_tot != 0 else 0.0

        metrics = {
            'abs': avg_abs,
		    'mse': avg_mse,
		    'mae': avg_mae,
		    'r2': r2
	    }

        return metrics
    
    def _loss_matrix(self, d_n, i):
        B = d_n * self.transform_method(self.x).T + self.lam * self.current_parameters[:, i]
        
        return B.reshape(-1, 1)
    
    def _error_matrix(self, d_n, err, i):
        return d_n * err - self.error + 0.5 * self.lam * self.current_parameters[:, i].T @ self.current_parameters[:, i]
            
    def _gram_matrix(self, B):
        return np.linalg.inv(B.T @ B)
            
    def _control_matrix(self, G_inv):
        return np.linalg.inv(0.5 * (1 + np.sqrt(1 + 4 * self.lam * G_inv)))
    
    def _control_input(self, err, i):
        d_n = 1
        if err < -1 * self.error:
            d_n = -1
            
        B = self._loss_matrix(d_n, i)
        G_inv = self._gram_matrix(B)
        P_inv = self._control_matrix(G_inv)
        E = self._error_matrix(d_n, err, i)
                
        return B.T * G_inv.item() * P_inv.item() * E
    
    # Transformation methods for research extension
    def _fourier_transform(self, x):
        Z = np.zeros(2*self.transform_size)

        for i in range(self.transform_size - 1):
            Z[2 * i] = np.sin(self.transform_init[i].T @ x)
            Z[2 * i + 1] = np.cos(self.transform_init[i + 1].T @ x)
                
        Z = Z * np.sqrt(1/self.transform_size)
        return Z
    
    
    # Initialization methods to match transformations
    def _fourier_init(self, variance):
        mean = np.zeros(self.transform_size)
        
        covariance_matrix = variance * np.eye(self.transform_size)
        
        samples = np.random.multivariate_normal(mean, covariance_matrix, size=self.num_features)
        
        return samples.T
    
    # Baseline transformation to see the impact of randomly reducing dimensions
    def _random_transform(self, x):
        Z = np.zeros(2*self.transform_size)
        
        for i in range(self.transform_size):
            Z[i] = self.transform_init.T @ x
            
        return Z
    
    def _random_init(self):
        return np.random.uniform(-1, 1, size=(self.num_features))
    
    # Use a hadamard transformation to compress the input data
    def _hadamard(self, n):
        if n == 0:
            return 1
        
        smaller_hadamard = self._hadamard(n - 1)
        return np.block([
            [smaller_hadamard, smaller_hadamard],
            [smaller_hadamard, -smaller_hadamard]
        ])
        
    def _hadamard_transform(self, x):
        return self.transform_init @ x
    
    def _hadamard_init(self):
        n = 1
        
        while (2**n < self.num_features):
            n += 1
        
        H = self._hadamard(n)
        
        hadamard_indices = np.random.choice(2**n, 2*self.transform_size, replace=False)
        
        return H[hadamard_indices, :self.num_features]
    
    # Use a fastfood transformation
    def _fastfood_transform(self, x):
        x = np.pad(x.reshape(-1), pad_width=((0, self.transform_init.shape[1] - self.num_features)), constant_values=0)
        
        return (self.transform_init @ x)
    
    def _fastfood_init(self, sigma):
        n = 1
        
        while (2**n < self.num_features):
            n += 1
                
        H = self._hadamard(n)
                
        B_diag = np.random.choice([-1, 1], size=2**n)
        
        B = np.diag(B_diag)
                
        G_diag = np.random.normal(0, sigma**2, size=(2**n))
        
        G = np.diag(G_diag)
                
        S_diag = np.random.uniform(0, 1, size=(2**n))
        
        S = np.diag(S_diag)
        
        permute_indices = np.random.permutation(2**n)
        
        P = np.eye(2**n)
        
        P = P[permute_indices]
        
        V = (1 / (sigma * np.sqrt(2**n))) * (S @ H @ G @ P @ H @ B)
        
        permute_V = np.random.randint(0, 2**n, size=(2*self.transform_size))
                
        return V[permute_V]
    
    
            
            
            