import numpy as np
import gymnasium as gym
from parser import *
import pandas as pd

class CustomRewardFrozenLake(gym.Wrapper):
    """Custom wrapper that modifies the rewards to help the agent learn better"""
    def __init__(self, env):
        super().__init__(env)
        # Define meaningful rewards that guide learning
        self.goal_reward = 10.0      # Substantial reward for reaching the goal
        self.hole_penalty = -5.0     # Clear penalty for falling in holes
        self.step_penalty = -0.1     # Small penalty to encourage efficient paths
        
    def step(self, action):
        next_state, reward, terminated, truncated, info = self.env.step(action)
        
        # Modify rewards based on what happened
        if terminated and reward == 1.0:  # Reached goal
            modified_reward = self.goal_reward
        elif terminated and reward == 0.0:  # Fell in hole
            modified_reward = self.hole_penalty
        else:  # Regular step
            modified_reward = self.step_penalty
            
        return next_state, modified_reward, terminated, truncated, info

class QLearningAgent:
    """Q-Learning agent implementation with enhanced monitoring and saving capabilities"""
    def __init__(self, env, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.001, epsilon_min=0.01):
        self.env = env
        self.alpha = alpha          # Learning rate - how quickly to adopt new information
        self.gamma = gamma          # Discount factor - importance of future rewards
        self.epsilon = epsilon      # Exploration rate - balance between trying new things and using known information
        self.epsilon_decay = epsilon_decay  
        self.epsilon_min = epsilon_min      
        
        # Initialize the Q-table where we'll store our learned values
        self.n_states = env.observation_space.n
        self.n_actions = env.action_space.n
        self.Q_table = np.zeros((self.n_states, self.n_actions))
    
    def select_action(self, state):
        """Choose an action using epsilon-greedy strategy"""
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()  # Explore
        else:
            return np.argmax(self.Q_table[state])  # Exploit
    
    def train(self, n_episodes):
        """Train the agent with improved monitoring"""
        rewards_per_episode = []
        successes = 0  # Track number of successful episodes
        
        for episode in range(n_episodes):
            state, _ = self.env.reset()
            done = False
            episode_reward = 0
            steps = 0
            
            while not done:
                action = self.select_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                
                # Q-learning update
                best_next_action = np.argmax(self.Q_table[next_state])
                td_target = reward + self.gamma * self.Q_table[next_state][best_next_action]
                td_error = td_target - self.Q_table[state][action]
                self.Q_table[state][action] += self.alpha * td_error
                
                state = next_state
                episode_reward += reward
                steps += 1
                
                # Check if we reached the goal
                if terminated and reward > 0:
                    successes += 1
            
            # Decay epsilon
            self.epsilon = max(self.epsilon_min, 
                             self.epsilon * (1 - self.epsilon_decay))
            
            rewards_per_episode.append(episode_reward)
            
            # Print more detailed progress
            if episode % 50 == 0:
                success_rate = (successes / (episode + 1)) * 100
                print(f"Episode {episode}")
                print(f"Success rate: {success_rate:.2f}%")
                print(f"Epsilon: {self.epsilon:.3f}")
                print(f"Last episode steps: {steps}")
                print("-------------------")
        
        return rewards_per_episode, successes/n_episodes

    def evaluate(self, n_episodes=6000):
        """Evaluate the trained agent's performance"""
        eval_rewards = []
        successes = 0
        
        for _ in range(n_episodes):
            state, _ = self.env.reset()
            done = False
            total_reward = 0
            
            while not done:
                # Always choose best action during evaluation
                action = np.argmax(self.Q_table[state])
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                total_reward += reward
                state = next_state
                
                if terminated and reward > 0:
                    successes += 1
                
            eval_rewards.append(total_reward)
        
        success_rate = (successes / n_episodes) * 100
        print(f"\nEvaluation Results:")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average Reward: {np.mean(eval_rewards):.3f}")
        
        return np.mean(eval_rewards)

    def save_qtable_to_excel(self, filename='q_table.xlsx'):
        """
        Save the Q-table to an Excel file with detailed formatting
        This method creates two sheets:
        1. Raw Q-values in a matrix format
        2. Best actions for each state with their corresponding Q-values
        """
        # Create a DataFrame for raw Q-values
        actions = ['LEFT', 'DOWN', 'RIGHT', 'UP']
        df_raw = pd.DataFrame(self.Q_table, columns=actions)
        df_raw.index.name = 'State'
        
        # Create a DataFrame for best actions
        best_actions = []
        for state in range(self.n_states):
            best_action_idx = np.argmax(self.Q_table[state])
            best_action_value = self.Q_table[state][best_action_idx]
            best_actions.append({
                'State': state,
                'Best Action': actions[best_action_idx],
                'Q-Value': best_action_value,
                'All Q-Values': {actions[i]: f"{self.Q_table[state][i]:.3f}" 
                               for i in range(len(actions))}
            })
        
        df_best = pd.DataFrame(best_actions)
        
        # Create an Excel writer object
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Save raw Q-table
            df_raw.to_excel(writer, sheet_name='Raw Q-Values')
            df_best.to_excel(writer, sheet_name='Best Actions', index=False)
            
            # Get the workbook and the worksheets
            workbook = writer.book
            raw_worksheet = writer.sheets['Raw Q-Values']
            best_worksheet = writer.sheets['Best Actions']
            
            # Format the Raw Q-Values sheet
            for column in range(len(actions) + 1):  # +1 for state column
                raw_worksheet.column_dimensions[chr(65 + column)].width = 12
                
            # Format the Best Actions sheet
            for column in range(len(df_best.columns)):
                best_worksheet.column_dimensions[chr(65 + column)].width = 20
            
        print(f"Q-table has been saved to {filename}")

def analyze_best_agent(custom_map, best_params):
    """Analyze the behavior of our best agent in detail"""
    # First train the agent without visualization
    print("\nTraining agent with best parameters:", best_params)
    train_env = gym.make("FrozenLake-v1", desc=custom_map, is_slippery=False)
    train_env = CustomRewardFrozenLake(train_env)
    
    agent = QLearningAgent(train_env, **best_params)
    rewards, success_rate = agent.train(n_episodes=6000)
    
    # Save the Q-table to Excel
    # agent.save_qtable_to_excel()
    
    # Now create a visual environment to observe behavior
    env = gym.make("FrozenLake-v1", desc=custom_map, render_mode="human", is_slippery=False)
    env = CustomRewardFrozenLake(env)
    env.metadata["render_fps"] = 15  # Slow down visualization for better observation
    
    # Run and analyze several episodes
    print("\nAnalyzing agent behavior over 5 episodes:")
    for episode in range(5):
        state, _ = env.reset()
        done = False
        path = [state]
        
        while not done:
            action = np.argmax(agent.Q_table[state])
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            state = next_state
            path.append(state)
        
        print(f"\nEpisode {episode + 1} path:", path)
        print("Success!" if reward > 0 else "Failed!")
    
    # Analyze the learned Q-table
    print("\nQ-table analysis (showing learned action values for each state):")
    actions = ['LEFT', 'DOWN', 'RIGHT', 'UP']
    for state in range(agent.n_states):
        print(f"\nState {state}:")
        for action in range(agent.n_actions):
            print(f"{actions[action]}: {agent.Q_table[state][action]:.3f}")
    
    env.close()
    train_env.close()

def main():
    """Main function to run the analysis with our best parameters"""
    # Load the custom map
    custom_map = prepare_for_env("map_1.txt")
    
    # Modified parameters for better learning
    best_params = {
        "alpha": 0.1,           # Learning rate
        "gamma": 0.99,          # Discount factor
        "epsilon": 1.0,         # Initial exploration rate
        "epsilon_decay": 0.001, # Exploration decay rate
        "epsilon_min": 0.01     # Minimum exploration rate
    }
    
    # Analyze the agent with these parameters
    analyze_best_agent(custom_map, best_params)

if __name__ == "__main__":
    main()