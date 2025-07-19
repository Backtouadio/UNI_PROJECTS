from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# Load your training data
train_data = pd.read_excel('step_data(map10)_train.xlsx')  # Assuming you have this file
X_train = train_data[['episode', 'step', 'state', 'reward', 'terminated', 'truncated', 'treasure_pos', 'distance_to_treasure', 'hole_encountered']]
y_train = train_data['action']

# Initialize your models
model_1 = DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=10, min_samples_split=10, class_weight=None)
model_2 = DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=None, min_samples_split=10, class_weight=None)
model_3 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=None, min_samples_split=10, class_weight=None)
model_4 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=5, min_samples_split=2, class_weight=None)
model_5 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=5, min_samples_split=10, class_weight=None)
model_6 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=10, min_samples_split=2, class_weight=None)
model_7 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=10, min_samples_split=2, class_weight='balanced')
model_8 = DecisionTreeClassifier(criterion='entropy', splitter='best', max_depth=None, min_samples_split=2, class_weight=None)
model_9 = DecisionTreeClassifier(criterion='gini', splitter='best', max_depth=None, min_samples_split=2, class_weight='balanced')

# Fit the models to the training data
models = [model_1, model_2, model_3, model_4, model_5, model_6, model_7, model_8, model_9]
for model in models:
    model.fit(X_train, y_train)  # Fit each model

# Load your test data
test_data = pd.read_excel('step_data(map9)_test.xlsx')
X_test = test_data[['episode', 'step', 'state', 'reward', 'terminated', 'truncated', 'treasure_pos', 'distance_to_treasure', 'hole_encountered']]
y_test = test_data['action']

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
comparison_df.to_excel('model_comparison_results.xlsx', index=False)

# Display the comparison
print(comparison_df)
