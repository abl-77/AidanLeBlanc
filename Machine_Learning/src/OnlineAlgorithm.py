import pickle
import random
import numpy as np
import torch

class OnlineAlgorithm:
	def __init__(self, **kwargs):
		"""Initialize shared parameters and algorithm-specific settings."""
		self.seed = kwargs.get('seed', 12345)
		random.seed(self.seed)
		np.random.seed(self.seed)
		torch.manual_seed(self.seed)
	
	def update(self, x, y):
		"""Update the model with a new data point (x, y).
		
		Args:
			x: Input features for the current time step.
			y: Target value for the current time step.
		"""
		raise NotImplementedError("Each algorithm must implement the update method.")

	def predict(self, x):
		"""Predict the output based on the current model state and input x.
		
		Args:
			x: Input features for the current time step.
			
		Returns:
			Predicted value.
		"""
		raise NotImplementedError("Each algorithm must implement the predict method.")
	
	def evaluate(self, x, y):
		"""Evaluate the model.
		
		Args:
			x: Input features (tensor of shape [batch_size, num_features, sequence_length]).
			y: Target values (tensor of shape [batch_size, num_features]).
			
		Returns:
			Error or evaluation metrics.
		"""
		
		criterion = torch.nn.MSELoss()  # Define the loss function

		total_mse = 0.0
		total_mae = 0.0
		total_ss_res = 0.0
		total_ss_tot = 0.0
		count = 0

		y_mean = torch.mean(y, dim=0)  # Mean of y for R^2 calculation

		with torch.no_grad():  # Disable gradient calculation
			for i in range(x.size(0)):
				x_sample = x[i].unsqueeze(0).permute(0, 2, 1)  # Shape: [1, num_features, sequence_length]
				y_sample = y[i].unsqueeze(0)  # Shape: [1, num_features]
				y_pred = self.predict(x_sample)  # Shape: [1, num_features]

				# Calculate MSE and MAE
				mse = criterion(y_pred, y_sample).item()
				mae = torch.abs(y_pred - y_sample).mean().item()

				# Calculate R^2 components
				ss_res = torch.sum((y_sample - y_pred) ** 2).item()
				ss_tot = torch.sum((y_sample - y_mean) ** 2).item()

				total_mse += mse
				total_mae += mae
				total_ss_res += ss_res
				total_ss_tot += ss_tot
				count += 1

		# Compute average metrics
		avg_mse = total_mse / count if count > 0 else 0.0
		avg_mae = total_mae / count if count > 0 else 0.0
		r2 = 1 - (total_ss_res / total_ss_tot) if total_ss_tot != 0 else 0.0

		metrics = {
			'mse': avg_mse,
			'mae': avg_mae,
			'r2': r2
		}

		return metrics

	def save_model(self, filepath):
		"""Save model state to a file.
		
		Args:
			filepath: Path to the file where the model will be saved.
		"""
		with open(filepath, 'wb') as f:
			pickle.dump(self, f)
		print(f"Model saved to {filepath}")

	@staticmethod
	def load_model(filepath):
		"""Load model state from a file.
		
		Args:
			filepath: Path to the file where the model is saved.
		
		Returns:
			Loaded model instance.
		"""
		with open(filepath, 'rb') as f:
			model = pickle.load(f)
		print(f"Model loaded from {filepath}")
		return model
