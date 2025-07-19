import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import numpy as np
from itertools import product

# Load your dataset
training_data = pd.read_csv('training_data.csv')
testing_data = pd.read_csv('test_data.csv')

# Assuming 'Action' is the target column
X_train = training_data.drop('Action', axis=1)
y_train = training_data['Action']
X_test = testing_data.drop('Action', axis=1)
y_test = testing_data['Action']

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the parameter grid
param_grid = {
    'hidden_layer_sizes': [(50,), (100,)],
    'activation': ['tanh', 'relu'],
    'solver': ['sgd', 'adam'],
    'learning_rate_init': [0.01, 0.001]
}

# Generate all combinations of parameters
param_combinations = list(product(*param_grid.values()))

# Prepare to collect results
results = []

# Iterate over all combinations of parameters
for combination in param_combinations:
    params = dict(zip(param_grid.keys(), combination))
    model = MLPRegressor(
        hidden_layer_sizes=params['hidden_layer_sizes'],
        activation=params['activation'],
        solver=params['solver'],
        learning_rate_init=params['learning_rate_init'],
        early_stopping=True,
        max_iter=500,
        random_state=42
    )
    
    # Train the model on the scaled training data
    model.fit(X_train_scaled, y_train)
    
    # Predict on the scaled test data
    y_pred = model.predict(X_test_scaled)
    
    # Calculate error metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    
    # Store results including the parameters
    results.append({
        'params': str(params),
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv('mlp_model_evaluation_results.csv', index=False)

print("Results saved successfully to 'mlp_model_evaluation_results.csv'.")
