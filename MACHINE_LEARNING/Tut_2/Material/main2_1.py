import gymnasium as gym
import pandas as pd  # Import pandas for Excel file operations
from parser import *

# Load the custom map
custom_map = prepare_for_env("map_1.txt")

# Create the FrozenLake environment
env = gym.make("FrozenLake-v1", desc=custom_map, render_mode="human", is_slippery=False)

# Define movement directions (up, down, left, right)
action_mapping = {
    0: (0, -1),  # Left
    1: (1, 0),   # Down
    2: (0, 1),   # Right
    3: (-1, 0)   # Up
}

class IntelligentAgent:
    def __init__(self, env):
        self.env = env
        self.goal = (0, 0)  # Goal position based on the map ('G')
        self.start = (11, 10)  # Starting position based on the map ('S')
        self.data = []  # Initialize a list to store state and action data

    # Check if a position is valid (not hitting a hole and within bounds)
    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < len(custom_map) and 0 <= y < len(custom_map[0]) and custom_map[x][y] != 'H'

    # Select the best action based on the current position and the goal
    def select_action(self, current_pos):
        best_action = None
        best_distance = float('inf')

        # Evaluate each possible action
        for action, (dx, dy) in action_mapping.items():
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if self.is_valid_move(new_pos):
                # Calculate Manhattan distance to the goal
                distance = abs(new_pos[0] - self.goal[0]) + abs(new_pos[1] - self.goal[1])
                if distance < best_distance:
                    best_distance = distance
                    best_action = action

        return best_action

    # Move to the goal using the best actions determined
    def move_to_goal(self):
        current_pos = self.start
        
        while current_pos != self.goal:
            env.render()
            action = self.select_action(current_pos)

            if action is not None:
                observation, reward, terminated, truncated, info = env.step(action)
                current_pos = (current_pos[0] + action_mapping[action][0], current_pos[1] + action_mapping[action][1])

                # Store the state (current position) and action in the data list
                self.data.append({"state": current_pos, "action": action})

                if terminated or truncated:
                    print(f"Game Over! Reward: {reward}")
                    observation, info = env.reset(seed=42)  # Reset environment after game over
                    break
            else:
                print("No valid action found!")
                break

    # Save data to an Excel file
    def save_data(self, filename="test_data.xlsx"):
        df = pd.DataFrame(self.data)  # Convert the data list to a DataFrame
        df.to_excel(filename, index=False)  # Save the DataFrame to an Excel file

# Initialize intelligent agent
agent = IntelligentAgent(env)

try:
    # Reset the environment before starting
    observation, info = env.reset(seed=42)
    
    # Move towards the goal using the selected actions
    agent.move_to_goal()

    # Save the collected data to an Excel file
    agent.save_data()
    print("Data saved successfully to test_data.xlsx.")  # Check if data was saved


finally:
    env.close()
