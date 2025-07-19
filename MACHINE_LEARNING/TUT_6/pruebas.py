import numpy as np
import gymnasium as gym
from parser import *

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
    """Q-Learning agent implementation"""
    def __init__(self, env, alpha=0.9, gamma=0.99, epsilon=0.9, epsilon_decay=0.001, epsilon_min=0.01):
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
        """Train the agent for a specified number of episodes"""
        rewards_per_episode = []
        running_averages = []
        window_size = 100
        
        for episode in range(n_episodes):
            state, _ = self.env.reset()
            done = False
            episode_reward = 0
            
            while not done:
                # Select and perform an action
                action = self.select_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                
                # Update Q-values using the Q-learning update rule
                best_next_action = np.argmax(self.Q_table[next_state])
                td_target = reward + self.gamma * self.Q_table[next_state][best_next_action]
                td_error = td_target - self.Q_table[state][action]
                self.Q_table[state][action] += self.alpha * td_error
                
                state = next_state
                episode_reward += reward
            
            # Track performance metrics
            rewards_per_episode.append(episode_reward)
            current_avg = np.mean(rewards_per_episode[-window_size:]) if len(rewards_per_episode) >= window_size else np.mean(rewards_per_episode)
            running_averages.append(current_avg)
            
            # Print progress periodically
            if episode % 100 == 0:
                print(f"Episode {episode}, Running Average Reward: {current_avg:.3f}")
        
        return rewards_per_episode, current_avg

    def evaluate(self, n_episodes=10000):
        """Evaluate the trained agent's performance"""
        eval_rewards = []
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
                
            eval_rewards.append(total_reward)
        
        return np.mean(eval_rewards)

def analyze_best_agent(custom_map, best_params):
    """Analyze the behavior of our best agent in detail"""
    # First train the agent without visualization
    print("\nTraining agent with best parameters:", best_params)
    train_env = gym.make("FrozenLake-v1", desc=custom_map, is_slippery=False)
    train_env = CustomRewardFrozenLake(train_env)
    
    agent = QLearningAgent(train_env, **best_params)
    agent.train(n_episodes=10000)
    
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
        print("Success!" if reward == 1.0 else "Failed!")
    
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
    
    # Best parameters determined from previous testing
    best_params = {
        "alpha": 0.9,
        "gamma": 0.99,
        "epsilon": 0.9
    }
    
    # Analyze the agent with these parameters
    analyze_best_agent(custom_map, best_params)

if __name__ == "__main__":
    main()