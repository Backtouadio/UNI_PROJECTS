from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import matplotlib.pyplot as plt

# Load your data from an Excel file
data = pd.read_excel('step_data.xlsx')

# Assuming your data has columns named 'state' and 'action'
X = data[['state']]  # Features (State)
y = data['action']   # Target (Action)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a decision tree classifier with custom parameters
clf = DecisionTreeClassifier(
    criterion='gini',        # or 'entropy' for information gain
    splitter='best',         # or 'random'
    max_depth=10,             # Set maximum depth of the tree
    min_samples_split=20,    # Minimum number of samples required to split an internal node
    class_weight=None        # Can be 'balanced' or a dictionary with class weights
)

# Train the decision tree classifier
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Print the accuracy of the model
accuracy = clf.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2f}")

# Generate a classification report to show precision, recall, and F1-score
report = classification_report(y_test, y_pred, target_names=['Down', 'Right', 'Up', 'Left'])
print(report)

# Plot the decision tree
plt.figure(figsize=(20,10))
plot_tree(clf, feature_names=['state'], class_names=['Down', 'Right', 'Up', 'Left'], filled=True)
plt.show()
