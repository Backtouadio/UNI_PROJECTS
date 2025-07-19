from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.model_selection import train_test_split

# Load your data
data = pd.read_excel('step_data(map10)_train.xlsx')  # Assuming you have this file
X = data[['episode', 'step', 'state', 'reward', 'terminated', 'truncated', 'treasure_pos', 'distance_to_treasure', 'hole_encountered']]
y = data['action']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # 80% train, 20% test

# Initialize your models
model_4 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=5, min_samples_split=2, class_weight=None)

model_1 = DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=10, min_samples_split=10, class_weight=None)

model_5 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=5, min_samples_split=10, class_weight=None)

# Fit the models to the training data
models = [model_1, model_4, model_5]
for model in models:
    model.fit(X_train, y_train)  # Fit each model

# Store results for comparison
comparison_results = []

# Perform predictions and evaluate each model
for model in models:
    y_pred = model.predict(X_test)
    
    # Calculate evaluation metrics
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Extract relevant metrics for comparison
    comparison_results.append({
        'Model': str(model),
        'Accuracy': report['accuracy'],
        'Precision': report['macro avg']['precision'],
        'Recall': report['macro avg']['recall'],
        'F1-Score': report['macro avg']['f1-score']
    })

# Convert results to a DataFrame for better display
comparison_df = pd.DataFrame(comparison_results)

# Save the comparison results to an Excel file
comparison_df.to_excel('model_non_correlation_comparison.xlsx', index=False)

# Display the comparison
print(comparison_df)
