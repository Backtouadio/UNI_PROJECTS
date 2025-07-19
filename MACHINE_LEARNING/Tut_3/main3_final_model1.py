import gymnasium as gym
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from parser_edited import *  

# Load the custom map and positions
custom_map, start_pos, goal_pos = prepare_for_env("map_10.txt")

# Create the FrozenLake environment
env = gym.make("FrozenLake-v1", desc=custom_map, render_mode="human", is_slippery=False)

# Initialize the decision tree agent with the dynamic start and goal positions

# Set render FPS explicitly (optional)
env.metadata["render_fps"] = 15 #velocidad del agente pa ver si hace algo distinto

# Define movement directions (up, down, left, right)
action_mapping = {
    0: (0, -1),  # Left
    1: (1, 0),   # Down
    2: (0, 1),   # Right
    3: (-1, 0)   # Up
}

class DecisionTreeAgent:
    def __init__(self, env, clf,start,goal):
        self.env = env
        self.clf = clf  # Trained decision tree model
        self.goal = goal  # Goal position based on the map ('G')
        self.start = start  # Starting position based on the map ('S')"""

    # This function will use the decision tree to predict the next action
    def predict_action(self, current_state):
        # Predict the action using the trained decision tree model
        action = self.clf.predict([current_state])[0]  # Pass state as a list
        return action

    # Move to the goal using actions predicted by the decision tree
    def move_to_goal(self):
        current_pos = self.start
        
        while True:  # Loop to keep the game running until interrupted
            try:
                # Render the environment (optional: comment this out to run without GUI)
                self.env.render()

                # Convert the current position to a single state value
                state = self.get_state_from_position(current_pos)

                # Predict the next action based on the current state
                action = self.predict_action([state])  # Ensure state is passed as a list

                # Check if the action is valid
                if action not in action_mapping.keys():
                    print(f"Invalid action: {action}. Resetting position.")
                    current_pos = self.start  # Reset position to start
                    continue

                # Execute the action in the environment
                observation, reward, terminated, truncated, info = self.env.step(action)

                # Update the current position based on the action taken
                current_pos = (
                    current_pos[0] + action_mapping[action][0], 
                    current_pos[1] + action_mapping[action][1]
                )

                # Check if the game ended due to falling into a hole or reaching the goal
                if terminated or truncated:
                    print("Fell into a hole or reached the goal! Restarting...")
                    observation, info = self.env.reset()  # Properly reset the environment
                    current_pos = self.start  # Reset position to start

            except Exception as e:
                print(f"Error encountered: {e}. Exiting loop.")
                break

    # Helper function to convert position (x, y) to a state value
    def get_state_from_position(self, position):
        x, y = position
        # Convert the (x, y) position into a unique state value
        return x * len(custom_map[0]) + y

# Load the previously trained decision tree classifier from Excel data
data = pd.read_excel('step_data(map10)_train.xlsx')
X = data[['state']]
y = data['action']

# Train the decision tree classifier
clf = DecisionTreeClassifier(
criterion='entropy', splitter='best', max_depth=10, min_samples_split=10, class_weight=None)       # Optionally use balanced classes
clf.fit(X.values, y)  # Fit using the values to avoid warnings

# Initialize the decision tree agent
agent = DecisionTreeAgent(env, clf,start_pos,goal_pos)

try:
    # Reset the environment before starting
    observation, info = env.reset(seed=42)

    # Move to the goal using the decision tree model
    agent.move_to_goal()

finally:
    env.close()
