import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import make_scorer, mean_squared_error, mean_absolute_error
import numpy as np

# Function to calculate RMSE
def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

# Load the data
training_data = pd.read_csv('training_data.csv')
features = training_data[['x', 'y', 'Angular_velocity']]
target = training_data['Action']

# Initialize the model
regressor = DecisionTreeRegressor()

# Define the parameter grid
param_grid = {
    'criterion': ['squared_error', 'friedman_mse', 'absolute_error'], #CAMBIAAAAAR
    'splitter': ['best', 'random'],
    'max_depth': [None, 10, 20, 30, 50, 100],
    'min_samples_split': [2, 5, 10, 20, 40],
    'max_features': [None, 'sqrt', 'log2', 0.5, 0.75]
}

# Define the scorers
scoring = {
    'MSE': make_scorer(mean_squared_error, greater_is_better=False),
    'RMSE': make_scorer(rmse, greater_is_better=False),
    'MAE': make_scorer(mean_absolute_error, greater_is_better=False)
}

# Setup the GridSearchCV
cv = KFold(n_splits=5, shuffle=True, random_state=42)  # Ensure reproducibility
grid_search = GridSearchCV(estimator=regressor, param_grid=param_grid, scoring=scoring, cv=cv, refit='MSE', verbose=1, return_train_score=True)

# Fit GridSearchCV
grid_search.fit(features, target)

# Extract results
results = pd.DataFrame(grid_search.cv_results_)

# Define the output column mapping
output_columns = {
    'param_max_depth': 'Max Depth',
    'param_min_samples_split': 'Min Samples Split',
    'param_max_features': 'Max Features',
    'param_criterion': 'Criterion',
    'param_splitter': 'Splitter',
    'mean_test_MSE': 'MSE',
    'mean_test_RMSE': 'RMSE',
    'mean_test_MAE': 'MAE'
}

# Select and rename the columns in the DataFrame
selected_data = results[list(output_columns.keys())].copy()
selected_data.rename(columns=output_columns, inplace=True)

# Adjust scores to display as positive
selected_data['MSE'] = selected_data['MSE'].abs()
selected_data['RMSE'] = selected_data['RMSE'].abs()
selected_data['MAE'] = selected_data['MAE'].abs()

# Save the DataFrame to a CSV file
selected_data.to_csv('grid_search_results.csv', index=False)

# Print best parameters and best score
print("Best parameters:", grid_search.best_params_)
print("Best score (MSE):", -grid_search.best_score_)