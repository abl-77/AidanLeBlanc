import os
import pickle
from sklearn.preprocessing import StandardScaler
from util import get_data, create_sequences
import numpy as np
import pandas as pd
from itertools import combinations
from scipy.stats import ttest_rel, wilcoxon, f_oneway

seed = 12345
model_path = './final_results'

# Get a list of all files in the directory
files = [f for f in os.listdir(model_path) if os.path.isfile(os.path.join(model_path, f))]

# Load each .pkl file
predictions = {}
for file in files:
	file_path = os.path.join(model_path, file)
	with open(file_path, 'rb') as f:
		predictions[file] = pickle.load(f)  # Store the loaded object in a dictionary

print(f"Loaded models: {list(predictions.keys())}")

def get_ground_truth(data):
	# Get testing data
	scaler = StandardScaler()
	data = get_data()[data]
	scaler.fit(data.iloc[:, 1:].values)
	data.iloc[:, 1:] = scaler.transform(data.iloc[:, 1:].values)

	# Create sequences
	data_values = data.iloc[:, 1:].values
	_, y = create_sequences(data_values, 10)

	# Split indices into training and testing sets
	split_index = int(len(y) * 0.8)  # 80% training, 20% testing
	y_test = y[split_index:]
	
	return y_test[:100]

# Calculate MAE and MSE
df = pd.DataFrame(columns=['names', 'MAE', 'MSE'])
y_test_stock = get_ground_truth('stock')
y_test_electricity = get_ground_truth('electricity')
for name, prediction in predictions.items():
	if not isinstance(prediction, np.ndarray):
		prediction = prediction.to_numpy()
	if 'stock' in name:
		mae = np.mean(np.abs(prediction - y_test_stock))
		mse = np.mean((prediction - y_test_stock) ** 2)
		#print(f"Mean Absolute Error (MAE) for Stock: {mae}")
		#print(f"Mean Squared Error (MSE) for Stock: {mse}")
		df.loc[len(df)] = [name.split('_')[0] + ' Stock', mae, mse]
	elif 'electricity' in name:
		mae = np.mean(np.abs(prediction - y_test_electricity))
		mse = np.mean((prediction - y_test_electricity) ** 2)
		#print(f"Mean Absolute Error (MAE) for Electricity: {mae}")
		#print(f"Mean Squared Error (MSE) for Electricity: {mse}")
		df.loc[len(df)] = [name.split('_')[0] + ' Electricity', mae, mse]
	else:
		continue

print(df)


# Compare
df = pd.DataFrame(columns=['Model 1', 'Model 2', 'T-Test MAE', 'Wilcoxon MAE', 'T-Test MSE', 'Wilcoxon MSE'])
for name1, name2 in combinations(predictions.keys(), 2):
	prediction1 = predictions[name1]
	prediction2 = predictions[name2]
	if not isinstance(prediction1, np.ndarray):
		prediction1 = prediction1.to_numpy()
	if not isinstance(prediction2, np.ndarray):
		prediction2 = prediction2.to_numpy()
	if 'stock' in name1 and 'stock' in name2:
		mae1 = np.abs(prediction1 - y_test_stock).flatten()
		mse1 = ((prediction1 - y_test_stock) ** 2).flatten()
		mae2 = np.abs(prediction2 - y_test_stock).flatten()
		mse2 = ((prediction2 - y_test_stock) ** 2).flatten()
		_, ttest_p_mae = ttest_rel(mae1, mae2)
		_, ttest_p_mse = ttest_rel(mse1, mse2)
		_, wilcoxon_p_mae = wilcoxon(mae1, mae2)
		_, wilcoxon_p_mse = wilcoxon(mse1, mse2)
		df.loc[len(df)] = [name1.split('_')[0] + ' Stock', name2.split('_')[0] + ' Stock', ttest_p_mae, wilcoxon_p_mae, ttest_p_mse, wilcoxon_p_mse]
	elif 'electricity' in name1 and 'electricity' in name2:
		mae1 = np.abs(prediction1 - y_test_electricity).flatten()
		mse1 = ((prediction1 - y_test_electricity) ** 2).flatten()
		mae2 = np.abs(prediction2 - y_test_electricity).flatten()
		mse2 = ((prediction2 - y_test_electricity) ** 2).flatten()
		_, ttest_p_mae = ttest_rel(mae1, mae2)
		_, ttest_p_mse = ttest_rel(mse1, mse2)
		_, wilcoxon_p_mae = wilcoxon(mae1, mae2)
		_, wilcoxon_p_mse = wilcoxon(mse1, mse2)
		df.loc[len(df)] = [name1.split('_')[0] + ' Electricity', name2.split('_')[0] + ' Electricity', ttest_p_mae, wilcoxon_p_mae, ttest_p_mse, wilcoxon_p_mse]
	else:
		continue

print('\n\n', df)