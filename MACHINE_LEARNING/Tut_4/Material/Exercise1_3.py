import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

np.random.seed(42)

# Load the training data
training_data = pd.read_csv('training_data.csv')
features = training_data[['x', 'y', 'Angular_velocity']]
target = training_data['Action']

# Load the test data
test_data = pd.read_csv('test_data.csv')
X_test = test_data[['x', 'y', 'Angular_velocity']]
y_test = test_data['Action']

# Define the model configuration for Model 1
model_config = {'max_depth': 20, 'min_samples_split': 40, 'max_features': None, 'criterion': 'squared_error', 'splitter': 'random'}

# Initialize the Decision Tree Regressor with Model 1 configuration
model = DecisionTreeRegressor(max_depth=model_config['max_depth'],
                              min_samples_split=model_config['min_samples_split'],
                              max_features=model_config['max_features'],
                              criterion=model_config['criterion'],
                              splitter=model_config['splitter'])

# Fit the model on the entire training dataset
model.fit(features, target)

# Predict on the test data
y_pred = model.predict(X_test)

# Calculate MSE, RMSE, and MAE
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

# Print the results
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"MAE: {mae}")