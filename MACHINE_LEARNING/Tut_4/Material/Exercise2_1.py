import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

def load_data(training_path, test_path):
    # Load the training and test data from CSV files
    training_data = pd.read_csv(training_path)
    test_data = pd.read_csv(test_path)
    return training_data, test_data

def train_model(X_train, y_train):
    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    # Predict and evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    return mse, rmse, mae

def main():
    # Paths to the data files
    training_path = 'training_data.csv'
    test_path = 'test_data.csv'

    # Load data
    training_data, test_data = load_data(training_path, test_path)

    # Prepare the data
    X_train = training_data[['x', 'y', 'Angular_velocity']]
    y_train = training_data['Action']
    X_test = test_data[['x', 'y', 'Angular_velocity']]
    y_test = test_data['Action']

    # Train and evaluate the model
    model = train_model(X_train, y_train)
    mse, rmse, mae = evaluate_model(model, X_test, y_test)

    # Print results
    print(f'Mean Squared Error: {mse:.3f}')
    print(f'Root Mean Squared Error: {rmse:.3f}')
    print(f'Mean Absolute Error: {mae:.3f}')

if __name__ == '__main__':
    main()
