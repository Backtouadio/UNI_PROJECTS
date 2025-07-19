import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import numpy as np

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

# Define the MLPRegressor model with specified best parameters
model = MLPRegressor(
    hidden_layer_sizes=(50,),
    activation='tanh',
    solver='adam',
    learning_rate_init=0.01,
    early_stopping=False,  # Early stopping is now disabled
    max_iter=500,  # Adjust as necessary to allow for convergence
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

# Output the metrics
print(f"MSE: {mse}")
print(f"RMSE: {rmse}")
print(f"MAE: {mae}")
