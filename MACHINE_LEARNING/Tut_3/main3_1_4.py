from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

#esteeee es para sacar los datasheets pa ver que ocurre

# Load your data
data = pd.read_excel('step_data(map10).xlsx')

# Separate features and target
X = data[['episode','step', 'state','action','reward','terminated', 'truncated', 'treasure_pos', 'distance_to_treasure', 'hole_encountered']]
y = data['action']  #action should always be our target variable

# Create copies of original dataset
original_data = data.copy()
all_features_data = data.copy()

# Method 1: Recursive Feature Elimination (RFE)
def apply_rfe_selection(X, y, n_features_to_select=3):
    # Create the RFE object with DecisionTree as estimator
    estimator = DecisionTreeClassifier(random_state=42)
    selector = RFE(estimator=estimator, n_features_to_select=n_features_to_select)
    
    # Fit RFE
    selector = selector.fit(X, y)
    
    # Get selected features
    selected_features = X.columns[selector.support_]
    
    print("\nRFE Selection Results:")
    for feature, selected, rank in zip(X.columns, selector.support_, selector.ranking_):
        print(f'Feature: {feature}, Selected: {selected}, Rank: {rank}')
    
    return X[selected_features], selected_features

# Method 2: SelectFromModel
def apply_select_from_model(X, y):
    # Create DecisionTree model
    estimator = DecisionTreeClassifier(random_state=42)
    
    # Create SelectFromModel object
    selector = SelectFromModel(estimator=estimator, prefit=False)
    
    # Fit and transform the data
    selector.fit(X, y)
    X_selected = selector.transform(X)
    
    # Get selected features
    selected_features = X.columns[selector.get_support()]
    
    print("\nSelectFromModel Results:")
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': selector.estimator_.feature_importances_,
        'Selected': selector.get_support()
    })
    print(feature_importance.sort_values('Importance', ascending=False))
    
    return pd.DataFrame(X_selected, columns=selected_features), selected_features

# Apply both feature selection methods
print("Applying feature selection methods...")

# RFE Selection
X_rfe, rfe_features = apply_rfe_selection(X, y)
rfe_data = pd.concat([X_rfe, y], axis=1)

# SelectFromModel Selection
X_sfm, sfm_features = apply_select_from_model(X, y)
sfm_data = pd.concat([X_sfm, y], axis=1)

# Save all datasets
print("\nSaving all datasets...")

# Original dataset
original_data.to_excel('original_dataset.xlsx', index=False)
print("Saved original dataset")

# Dataset with all features
all_features_data.to_excel('all_features_dataset.xlsx', index=False)
print("Saved dataset with all features")

# Dataset with RFE selected features
rfe_data.to_excel('rfe_selected_features.xlsx', index=False)
print(f"Saved RFE selected features dataset (Selected features: {', '.join(rfe_features)})")

# Dataset with SelectFromModel selected features
sfm_data.to_excel('selectfrommodel_features.xlsx', index=False)
print(f"Saved SelectFromModel features dataset (Selected features: {', '.join(sfm_features)})")

# Print summary of selected features
print("\nFeature Selection Summary:")
print(f"Total features available: {len(X.columns)}")
print(f"Features selected by RFE: {', '.join(rfe_features)}")
print(f"Features selected by SelectFromModel: {', '.join(sfm_features)}")

# Compare the overlap between methods
common_features = set(rfe_features).intersection(set(sfm_features))
print(f"\nFeatures selected by both methods: {', '.join(common_features)}")
