import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt

# Load the Excel file with the step data (update this path)
file_path = r'C:\Users\Victo\OneDrive\Escritorio\machine_learning\Tut_2\Tutorial2-100496795-100496723\Material\step_data.xlsx'
data = pd.read_excel(file_path)

# Separate features (state) and labels (action)
X = data[['state']]
y = data['action']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate the accuracy, precision and recall of the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')  # Change average as needed
recall = recall_score(y_test, y_pred, average='weighted')  # Change average as needed

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"Model Precision: {precision * 100:.2f}%")
print(f"Model Recall: {recall * 100:.2f}%")



# Visualize the decision tree using matplotlib
plt.figure(figsize=(12,8))  # Set the size of the plot
plot_tree(clf, feature_names=['state'], class_names=['left', 'down', 'right', 'up'], filled=True, rounded=True, fontsize=10)
plt.title("Decision Tree Visualization")
plt.show()
