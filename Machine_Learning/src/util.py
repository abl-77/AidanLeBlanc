import pandas as pd
import yfinance as yf
import os
from scipy.stats import ttest_rel, wilcoxon, f_oneway
from itertools import combinations
import numpy as np
import torch

def get_data():
	electricity_path = "data/electricity.pkl"
	stock_path = "data/stock.pkl"
	return {"electricity": pd.read_pickle(electricity_path), "stock": pd.read_pickle(stock_path)}


if __name__ == "__main__":


	def load_electricity_data():
		"""
		Loads the Electricity Load Diagrams dataset and returns it in wide format.

		Returns:
			pd.DataFrame: DataFrame with 'timestamp' as index and sensors as columns.
		"""
		
		file_path = '../data/electricityloaddiagrams20112014/LD2011_2014.txt' 

		if not os.path.exists(file_path):
			raise FileNotFoundError(f"The dataset file '{file_path}' was not found.")

		df = pd.read_csv(
			file_path,
			sep=';',
			parse_dates=[0],  # Parse the first column as dates without setting it as index
			low_memory=False
		)

		# Rename the first column to 'timestamp' for easier handling
		df.rename(columns={df.columns[0]: 'timestamp'}, inplace=True)


		# Replace commas with periods and convert columns to numeric
		df = df.replace(',', '.', regex=True)  # Replace commas with periods for decimal
		df = df.apply(pd.to_numeric, errors='coerce')  # Convert all columns to numeric, setting invalid parsing to NaN

		# Drop rows with all NaN values (e.g., incomplete time steps)
		df.dropna(how='all', inplace=True)

		# Ensure the DataFrame is sorted by timestamp
		df.sort_index(inplace=True)

		# Save DataFrame to a pickle file for faster future loading
		save_path = "../data/electricity.pkl"
		df.to_pickle(save_path)
		print(f"Electricity data processed and saved to '{save_path}'.")

		return df


	def load_stock_data():
		"""
		Fetches historical stock data for multiple tickers from yfinance and returns it in wide format,
		including multiple values per symbol per timestamp, with flattened column names.

		Returns:
			pd.DataFrame: DataFrame with 'timestamp' as a column and flattened columns for each ticker's values.
		"""

		# Top 100 most popular symbols
		symbols = [
			'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B', 'JPM', 'JNJ',
			'V', 'UNH', 'HD', 'PG', 'MA', 'BAC', 'DIS', 'XOM', 'PFE', 'KO',
			'NFLX', 'ADBE', 'T', 'CMCSA', 'CRM', 'ABT', 'PEP', 'INTC', 'CSCO', 'ORCL',
			'COST', 'CVX', 'WMT', 'NKE', 'AMD', 'PYPL', 'LLY', 'WFC', 'MRK', 'MDT',
			'DHR', 'MCD', 'IBM', 'INTU', 'LOW', 'NEE', 'QCOM', 'AMGN', 'BA', 'HON',
			'SPGI', 'RTX', 'TXN', 'BLK', 'LIN', 'SBUX', 'UPS', 'MMM', 'GILD', 'ISRG',
			'GE', 'PLD', 'FIS', 'BKNG', 'LMT', 'TMO', 'AXP', 'DE', 'NOW',
			'SYK', 'MO', 'CVS', 'MDLZ', 'CI', 'DUK', 'PNC', 'UBER', 'GM', 'CHTR',
			'C', 'EL', 'CL', 'ZTS', 'ADI', 'D', 'APD', 'TGT', 'BSX',
			'EMR', 'ADP', 'USB', 'SHW', 'REGN', 'WM', 'VRTX', 'TJX', 'ITW', 'COP',
			'ECL', 'F'
		]

		period = '2y'
		data_frames = []

		for ticker in symbols:
			ticker_data = yf.Ticker(ticker)
			df = ticker_data.history(period=period)
			df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
			df.columns = [f"{ticker}_{col}" for col in df.columns]
			data_frames.append(df)

		combined_df = pd.concat(data_frames, axis=1, join='outer')
		combined_df = combined_df.copy()

		combined_df = combined_df.reset_index()
		combined_df.rename(columns={'Date': 'timestamp'}, inplace=True)

		combined_df.sort_values('timestamp', inplace=True)

		# Forward-fill missing values
		combined_df.fillna(method='ffill', inplace=True)
		combined_df.dropna(inplace=True)

		# Save so consistent data (for stock data)
		save_path = "../data/stock.pkl"
		combined_df.to_pickle(save_path)
		print(f"Stock data processed and saved to '{save_path}'.")

		return combined_df


	load_electricity_data()
	#load_stock_data()

def split_data(data, train_ratio=0.8):
	"""
	Split the data into training and testing sets without reshaping.
	
	Args:
		data (DataFrame): DataFrame with 'timestamp' as the first column, followed by sensor columns (MT_001, MT_002, etc.).
		train_ratio (float): Proportion of the data to use for training (e.g., 0.8 for 80% training data).
	
	Returns:
		tuple: Two DataFrames (train_df, test_df) split chronologically.
	"""
	# Calculate the split index
	split_index = int(len(data) * train_ratio)
	
	# Split chronologically
	train_df = data.iloc[:split_index].copy()
	test_df = data.iloc[split_index:].copy()
	
	return train_df, test_df

def create_sequences(data, seq_length):
	sequences = []
	targets = []
	for i in range(len(data) - seq_length):
		seq = data[i:i + seq_length]
		target = data[i + seq_length]
		sequences.append(seq)
		targets.append(target)
	return np.array(sequences), np.array(targets)

def compare(models, x_test, y_test, metric='mae'):
	"""
	Compare multiple models.
	
	Args:
		models: List of models.
		x_test: Test input features.
		y_test: Test target values.
		metric: The metric to use for comparison ('mae', 'mse').
	
	Returns:
		dict: Results of pairwise and overall statistical tests.
	"""
	
	errors = []
	for model in models:
		predictions = np.array([model.predict(x).detach().numpy() for x in x_test])
		
		# If batch is still there, remove
		if predictions.ndim == 3 and predictions.shape[1] == 1:
			predictions = np.squeeze(predictions, axis=1)
		
		if metric == 'mae':
			error = np.abs(y_test - predictions)
		elif metric == 'mse':
			error = (y_test - predictions) ** 2
		else:
			return None

		errors.append(error.flatten())
	
	errors = np.array(errors)
	
	# Pairwise comparisons
	pairwise_results = {}
	for (i, model1), (j, model2) in combinations(enumerate(models), 2):
		# Differences
		diff = errors[i] - errors[j]
		
		# Paired t-test
		if np.all(diff == 0):
			ttest_stat, ttest_p = 0, 1  # If all differences are zero
		else:
			ttest_stat, ttest_p = ttest_rel(errors[i], errors[j])
		
		# Wilcoxon test
		if np.all(diff == 0):
			wilcoxon_stat, wilcoxon_p = 0, 1  # If all differences are zero
		else:
			wilcoxon_stat, wilcoxon_p = wilcoxon(errors[i], errors[j])
		
		pairwise_results[f"Model_{i+1} vs Model_{j+1}"] = {
			'paired_t_test': {'statistic': ttest_stat, 'p_value': ttest_p},
			'wilcoxon_test': {'statistic': wilcoxon_stat, 'p_value': wilcoxon_p}
		}
	
	# ANOVA for overall comparison
	anova_stat, anova_p = f_oneway(*errors) if len(models) > 2 else (None, None)  # Requires it to be at least 3 models
	
	results = {
		'metric': metric,
		'pairwise_comparisons': pairwise_results,
		'anova': {
			'F_statistic': anova_stat,
			'p_value': anova_p
		}
	}
	
	return results