from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import cross_validate, KFold
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import numpy as np
from itertools import product

def evaluate_tree_cv(X, y, params, cv_splits=5):
    """
    Train and evaluate a decision tree with given parameters using cross validation
    """
    clf = DecisionTreeClassifier(**params)
    
    # Define the scoring metrics we want to track
    scoring = {
        'accuracy': 'accuracy',
        'precision_macro': 'precision_macro',
        'recall_macro': 'recall_macro',
        'f1_macro': 'f1_macro'
    }
    
    # Perform cross validation
    cv_results = cross_validate(
        clf, X, y,
        cv=KFold(n_splits=cv_splits, shuffle=True, random_state=42),
        scoring=scoring,
        return_train_score=True,
        return_estimator=True  # This will return the fitted classifiers
    )
    
    # Calculate average metrics across all folds
    avg_results = {
        'test_accuracy': cv_results['test_accuracy'].mean(),
        'test_accuracy_std': cv_results['test_accuracy'].std(),
        'test_precision': cv_results['test_precision_macro'].mean(),
        'test_precision_std': cv_results['test_precision_macro'].std(),
        'test_recall': cv_results['test_recall_macro'].mean(),
        'test_recall_std': cv_results['test_recall_macro'].std(),
        'test_f1': cv_results['test_f1_macro'].mean(),
        'test_f1_std': cv_results['test_f1_macro'].std()
    }
    
    return {**avg_results, 'cv_results': cv_results, 'parameters': params}

# Load your data
data = pd.read_excel('step_data(RFE).xlsx')
X = data[['distance_to_treasure', 'hole_encountered']]
y = data['action']

# Define parameter combinations to test
param_grid = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best'],  # Simplified parameter set
    'max_depth': [5, 10, None],
    'min_samples_split': [2, 10],
    'class_weight': [None, 'balanced']
}

# Generate all combinations of parameters
param_combinations = [dict(zip(param_grid.keys(), v)) for v in product(*param_grid.values())]

# Store results
results = []

# Test each combination
print("Starting cross-validation for all parameter combinations...")
for params in param_combinations:
    print(f"\nTesting parameters: {params}")
    result = evaluate_tree_cv(X, y, params)
    
    # Store the results
    results.append({
        **params,
        'accuracy': result['test_accuracy'],
        'accuracy_std': result['test_accuracy_std'],
        'precision': result['test_precision'],
        'precision_std': result['test_precision_std'],
        'recall': result['test_recall'],
        'recall_std': result['test_recall_std'],
        'f1': result['test_f1'],
        'f1_std': result['test_f1_std']
    })
    
    print(f"Cross-validated Accuracy: {result['test_accuracy']:.4f} (±{result['test_accuracy_std']:.4f})")
    print(f"Cross-validated Precision: {result['test_precision']:.4f} (±{result['test_precision_std']:.4f})")
    print(f"Cross-validated Recall: {result['test_recall']:.4f} (±{result['test_recall_std']:.4f})")
    print(f"Cross-validated F1: {result['test_f1']:.4f} (±{result['test_f1_std']:.4f})")

# Convert results to DataFrame for easy analysis
results_df = pd.DataFrame(results)

# Format the results DataFrame for better readability
formatted_results = results_df.copy()
for metric in ['accuracy', 'precision', 'recall', 'f1']:
    formatted_results[metric] = formatted_results.apply(
        lambda row: f"{row[metric]:.4f} (±{row[metric+'_std']:.4f})",
        axis=1
    )

# Drop the standard deviation columns for display
display_columns = ['criterion', 'splitter', 'max_depth', 'min_samples_split', 
                  'class_weight', 'accuracy', 'precision', 'recall', 'f1']
formatted_results = formatted_results[display_columns]

# Show best performing combinations
print("\nTop 5 Best Performing Models (by accuracy):")
print(formatted_results.sort_values('accuracy', key=lambda x: pd.to_numeric(x.str.split('(').str[0])).head())

# Save results to Excel
formatted_results.to_excel('results_rfe.xlsx', index=False)

# Calculate average performance for each parameter value
print("\nParameter Analysis (averaged across all other parameters):")
for param in param_grid.keys():
    print(f"\nAverage metrics by {param}:")
    avg_by_param = results_df.groupby(param).agg({
        'accuracy': ['mean', 'std'],
        'precision': ['mean', 'std'],
        'recall': ['mean', 'std'],
        'f1': ['mean', 'std']
    }).round(4)
    print(avg_by_param)
