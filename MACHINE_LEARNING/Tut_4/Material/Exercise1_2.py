import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

# Set random seed for reproducibility 
np.random.seed(42)

# Load the training data
training_data = pd.read_csv('training_data.csv')
features = training_data[['x', 'y', 'Angular_velocity']]
target = training_data['Action']

# Load the test data
test_data = pd.read_csv('test_data.csv')
X_test = test_data[['x', 'y', 'Angular_velocity']]
y_test = test_data['Action']

# Define the model configurations
model_configs = [
    {'max_depth': None, 'min_samples_split': 40, 'max_features': 0.75, 'criterion': 'squared_error', 'splitter': 'best'},
    {'max_depth': 20, 'min_samples_split': 40, 'max_features': None, 'criterion': 'squared_error', 'splitter': 'best'},
    {'max_depth': 10, 'min_samples_split': 40, 'max_features': 'log2', 'criterion': 'friedman_mse', 'splitter': 'best'}
]

# Function to calculate RMSE
def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

# Evaluate each model using direct evaluation
results = []
for config in model_configs:
    model = DecisionTreeRegressor(max_depth=config['max_depth'],
                                  min_samples_split=config['min_samples_split'],
                                  max_features=config['max_features'],
                                  criterion=config['criterion'],
                                  splitter=config['splitter'])
    model.fit(features, target)  # Fit model on training data
    y_pred = model.predict(X_test)  # Predict on test data
    mse = mean_squared_error(y_test, y_pred)
    rmse_val = rmse(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    results.append({
        'Configuration': config,
        'MSE': mse,
        'RMSE': rmse_val,
        'MAE': mae
    })

# Convert results to a DataFrame for better visualization and print
results_df = pd.DataFrame(results)
print (results_df)