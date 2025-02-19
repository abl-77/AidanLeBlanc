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

class CRFR(OnlineAlgorithm):
    def __init__(self, num_features, num_outputs, fourier_size, sigma, error, lam, **kwargs):
        
        self.x = np.empty((num_features, 0))
        self.y = np.empty((num_outputs, 0))
        self.num_features = num_features
        self.num_outputs = num_outputs
        self.fourier_size = fourier_size
        self.random_samples = self._random_samples(sigma**2)
        self.current_parameters = np.ones((2*fourier_size, num_outputs)) * 100
        self.error = error
        self.lam = lam
        
        super().__init__(**kwargs)
        
    def update(self, x, y):
        y_hat = self.predict(x)
        error = np.abs(y_hat - y).sum()
        if  error > self.error:
            self.x = x
            self.y = y
            self.current_parameters = self.current_parameters - 0.1 * self._control_input(x, y)
            
    def predict(self, x):
        return self.current_parameters.T @ self._fourier_components(x)
            
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
            
    def _fourier_components(self, x):
        Z = np.zeros(2*self.fourier_size)

        for i in range(self.fourier_size - 1):
            Z[2 * i] = np.sin(self.random_samples[i].T @ x)
            Z[2 * i + 1] = np.cos(self.random_samples[i + 1].T @ x)
                
        Z = Z * np.sqrt(1/self.fourier_size)
        return Z
    
    def _parameter_matrix(self, d_n):
        B = np.zeros((self.num_outputs, self.x.shape[1], self.fourier_size*2))
        for i in range(self.num_outputs):
            for j in range(self.x.shape[1]):
                B[i][j] = d_n * self._fourier_components(self.x[:, j]).T + self.lam * self.current_parameters[:, i].T 
            
        return B
    
    def _error_matrix(self, d_n):
        E = np.zeros((self.num_outputs, self.x.shape[1]))
        for i in range(self.num_outputs):
            for j in range(self.x.shape[1]):
                E[i][j] = d_n * (self.current_parameters[:, i].T @ self._fourier_components(self.x[:, j]) - self.y[i, j]) - self.error + 0.5 * self.lam * self.current_parameters[:, i].T @ self.current_parameters[:, i] 
        return E
            
    def _gram_matrix(self, B):
        G_inv = np.zeros((B.shape[0], B.shape[1], B.shape[1]))
        for i in range(B.shape[0]):
            G_inv[i] = np.linalg.inv(B[i] @ B[i].T)
            
        return G_inv
            
    def _control_matrix(self, G_inv):
        P_inv = np.zeros_like(G_inv)
        for i in range(G_inv.shape[0]):
            P_inv[i] = np.linalg.inv(0.5 * (1 + np.sqrt(1 + 4 * self.lam * G_inv[i])))
        
        return P_inv
    
    def _control_input(self, x, y):
        d_n = 1
        if (self.predict(x) - y).sum() < self.error:
            d_n = -1
        B = self._parameter_matrix(d_n)
        G_inv = self._gram_matrix(B)
        P_inv = self._control_matrix(G_inv)
        E = self._error_matrix(d_n)
        
        parameter_update = np.zeros((self.num_outputs, 2 * self.fourier_size))
        
        for i in range(self.num_outputs):
            parameter_update[i] = B[i].T @ G_inv[i] @ P_inv[i] @ E[i]
        
        return parameter_update.T
    
    def _random_samples(self, variance):
        mean = np.zeros(self.fourier_size)
        
        covariance_matrix = variance * np.eye(self.fourier_size)
        
        samples = np.random.multivariate_normal(mean, covariance_matrix, size=self.num_features)
        
        return samples.T
            
            
            