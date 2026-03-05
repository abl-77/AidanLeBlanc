from CRFRMain import *
import pickle
import numpy
import pandas as pd

def load_models(file_path):
    files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]

    electricity_models = []
    electricity_names = []
    stock_models = []
    stock_names = []
    for file in files:
        model = OnlineAlgorithm.load_model(file_path + "/" + file)
        if "electricity" in file:
            electricity_models.append(model)
            electricity_names.append(file.split("_")[0])
        elif "stock" in file:
            stock_models.append(model)
            stock_names.append(file.split("_")[0])
        else:
            continue
    return electricity_models, electricity_names, stock_models, stock_names

def generate_tests(data):
    scaler = StandardScaler()
    data = get_data()[data]
    scaler.fit(data.iloc[:, 1:].values)
    data.iloc[:, 1:] = scaler.transform(data.iloc[:, 1:].values)

    data_values = data.iloc[:, 1:].values
    X, y = create_sequences(data_values, 10)

    indices = np.arange(len(X))
    np.random.shuffle(indices)

    split_index = int(len(indices) * 0.8)
    test_indices = indices[split_index:]

    X_test = X[test_indices]
    y_test = y[test_indices]

    X_test = torch.tensor(X_test, dtype=torch.float32)
    
    X_test.permute(0, 2, 1)
    X_test = X_test.reshape(X_test.shape[0], -1).numpy()
    
    return X_test, y_test

if __name__ == "__main__":
    e_models, e_names, s_models, s_names = load_models("./abl77/models")
    
    e_X_tests, e_y_tests = generate_tests("electricity")
    s_X_tests, s_y_tests = generate_tests("stock")
    
    e_results = np.zeros(shape=(len(e_models), len(e_y_tests), len(e_y_tests[0])))
    for i in range(len(e_models)):
        for j in range(len(e_X_tests)):
            e_results[i][j] = e_models[i].predict(e_X_tests[i])
            
    s_results = np.zeros(shape=(len(s_models), len(s_y_tests), len(s_y_tests[0])))
    for i in range(len(s_models)):
        for j in range(len(s_X_tests)):
            s_results[i][j] = s_models[i].predict(s_X_tests[i])
    
    df = pd.DataFrame(columns=['names', 'MAE', 'MSE'])
    
    for i in range(len(e_models)):
        mae = np.mean(np.abs(e_results[i] - e_y_tests))
        mse = np.mean((e_results[i] - e_y_tests) ** 2)
        
        df.loc[len(df)] = [e_names[i] + ' Electricity', mae, mse]
        
    for i in range(len(s_models)):
        mae = np.mean(np.abs(e_results[i] - e_y_tests))
        mse = np.mean((e_results[i] - e_y_tests) ** 2)
        
        df.loc[len(df)] = [s_names[i] + ' Stock', mae, mse]
    
    df.to_pickle("./abl77/results/Results.pkl")
  