import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from CRFR import *
from CRFRExtension import *
from sklearn.preprocessing import StandardScaler
from util import split_data
import torch.nn as nn
import time
import pickle
np.random.seed(1)

def create_sequences(data, seq_length):
        sequences = []
        targets = []
        for i in range(len(data) - seq_length):
            seq = data[i:i + seq_length]
            target = data[i + seq_length]
            sequences.append(seq)
            targets.append(target)
        return np.array(sequences), np.array(targets)
    
def prepare_data(data, transform_method, data_size=1000, seq_length=10, transform_size=10, sigma=0.1, regularization_tradeoff=0.1, loss_parameter=0.1, gamma=0.1, error=0.1):

    data = get_data()[data]
    data = data.iloc[:data_size]

    train_data, test_data = split_data(data, train_ratio=0.8)

    scaler = StandardScaler()
    train_values = train_data.iloc[:, 1:].values
    scaler.fit(train_values)
    train_data.iloc[:, 1:] = scaler.transform(train_values)
    test_data.iloc[:, 1:] = scaler.transform(test_data.iloc[:, 1:].values)

    X_train, y_train = create_sequences(train_data.iloc[:, 1:].values, seq_length)
    X_test, y_test = create_sequences(test_data.iloc[:, 1:].values, seq_length)

    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)
    
    model = CRFRExtension(
        num_features=train_values.shape[1]*seq_length,
        num_outputs=train_values.shape[1],
		transform_size=transform_size,
        transform_method=transform_method,
        sigma=sigma,
        error=error,
        regularization=regularization_tradeoff,
        lam=loss_parameter,
        gam=gamma,
	)

    return X_train_tensor, y_train_tensor, X_test_tensor, y_test_tensor, model

def train(model, X_train, y_train, X_test, y_test, num_epochs=10):
    criterion = nn.MSELoss()
        
    X_test = X_test.permute(0, 2, 1).numpy()
    X_test = X_test.reshape(X_test.shape[0], -1)
        
    metrics = model.evaluate(X_test, y_test.numpy(), criterion)
    print(f"Random Initialization: Test abs = {metrics['abs']:.4f}, Test MSE = {metrics['mse']:.4f}, "
			f"Test MAE = {metrics['mae']:.4f}, Test R^2 = {metrics['r2']:.4f}")
    
        
    for epoch in range(num_epochs):
        permutation = torch.randperm(X_train.size(0))
        X_train_shuffled = X_train[permutation]
        y_train_shuffled = y_train[permutation]
        
        for i in range(X_train_shuffled.size(0)):
            X = X_train_shuffled[i:i+1]
            y = y_train_shuffled[i:i+1].numpy().squeeze()
        
            X = X.permute(0, 2, 1).numpy().squeeze()
            
            X = X.reshape(-1, 1)
            y = y.reshape(-1, 1)
                                    
            model.update(X, y)
            
        metrics = model.evaluate(X_test, y_test.numpy(), criterion)
        print(f"Epoch {epoch + 1}: Test abs = {metrics['abs']:.4f}, Test MSE = {metrics['mse']:.4f}, "
				f"Test MAE = {metrics['mae']:.4f}, Test R^2 = {metrics['r2']:.4f}")
        

def main(data, transform_method, num_epochs):
    # Prepare
    X_train, y_train, X_test, y_test, model = prepare_data(
	    data=data,
        transform_method=transform_method,
		data_size=1000,
		seq_length=10,
		transform_size=25,
		sigma=0.1,
		regularization_tradeoff=0.1,
		loss_parameter=0.1,
		gamma=0.1,
        error=0.1
    )
    
    # Train
    train(
		model=model,
		X_train=X_train,
		y_train=y_train,
		X_test=X_test,
		y_test=y_test,
		num_epochs=num_epochs,
	)
    
    return model
 
if __name__ == "__main__":
    transform_methods = ["fourier", "fastfood", "random"]
    data_sets = ["stock", "electricity"]
    epochs = [1, 5, 10, 25]
    for transform_method in transform_methods:
        training_times = []
        for data in data_sets:
            for num_epochs in epochs:
                start_time = time.time()
                model = main(data, transform_method, num_epochs)
                training_times.append(time.time() - start_time)
                model.save_model(f"./abl77/models/CRFR{transform_method}{num_epochs}_{data}_model.pkl")
        with open(f"./abl77/results/{transform_method}_times.pkl", "wb") as f:
            pickle.dump(training_times, f)
    