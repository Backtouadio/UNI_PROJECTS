import numpy as np
import gymnasium as gym
from parser import *
import pandas as pd
from datetime import datetime

class CustomRewardFrozenLake(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)
        self.goal_reward = 10.0      
        self.hole_penalty = -5.0     
        self.step_penalty = -0.1     
        
    def step(self, action):
        next_state, reward, terminated, truncated, info = self.env.step(action)
        
        if terminated and reward == 1.0:  
            modified_reward = self.goal_reward
        elif terminated and reward == 0.0:  
            modified_reward = self.hole_penalty
        else:  
            modified_reward = self.step_penalty
            
        return next_state, modified_reward, terminated, truncated, info

class QLearningAgent:
    def __init__(self, env, alpha=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.0, epsilon_min=0.01):
        self.env = env
        self.alpha = alpha          
        self.gamma = gamma          
        self.epsilon = epsilon      
        self.epsilon_decay = epsilon_decay  
        self.epsilon_min = epsilon_min      
        
        self.n_states = env.observation_space.n
        self.n_actions = env.action_space.n
        self.Q_table = np.zeros((self.n_states, self.n_actions))
    
    def select_action(self, state):
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()
        else:
            return np.argmax(self.Q_table[state])
    
    def train(self, n_episodes):
        # Lists to store the metrics we want to track
        rewards_per_episode = []
        running_averages = []
        epsilons = []
        window_size = 100
        
        for episode in range(n_episodes):
            state, _ = self.env.reset()
            done = False
            episode_reward = 0
            
            while not done:
                action = self.select_action(state)
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                
                best_next_action = np.argmax(self.Q_table[next_state])
                td_target = reward + self.gamma * self.Q_table[next_state][best_next_action]
                td_error = td_target - self.Q_table[state][action]
                self.Q_table[state][action] += self.alpha * td_error
                
                state = next_state
                episode_reward += reward
            
            rewards_per_episode.append(episode_reward)
            current_avg = np.mean(rewards_per_episode[-window_size:]) if len(rewards_per_episode) >= window_size else np.mean(rewards_per_episode)
            running_averages.append(current_avg)
            epsilons.append(self.epsilon)
            
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
            
            # Print progress every 100 episodes
            #if episode % 100 == 0:
                #print(f"Episode {episode}, Running Average Reward: {current_avg:.3f}, 
                # Epsilon: {self.epsilon:.3f}")
        
        cumulative_reward = np.sum(rewards_per_episode)
        return rewards_per_episode, cumulative_reward, running_averages, epsilons

    def evaluate(self, n_episodes=1000):
        eval_rewards = []
        for _ in range(n_episodes):
            state, _ = self.env.reset()
            done = False
            total_reward = 0
            
            while not done:
                action = np.argmax(self.Q_table[state])
                next_state, reward, terminated, truncated, _ = self.env.step(action)
                done = terminated or truncated
                total_reward += reward
                state = next_state
                
            eval_rewards.append(total_reward)
        
        return np.mean(eval_rewards)
# First, let's create a function to generate our configurations systematically
def generate_configurations():
    # Define our parameter ranges
    alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    gammas = [0.99, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70]
    epsilons = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4]
    
    configurations = []
    
    # Generate all combinations
    for gamma in gammas:
        for alpha in alphas:
            for epsilon in epsilons:
                configurations.append({
                    "alpha": alpha,
                    "gamma": gamma,
                    "epsilon": epsilon
                })
    
    return configurations
def test_configurations(custom_map):
    # Lists to store our milestone data and final results
    milestone_data = []
    results_data = []
    
    configurations = generate_configurations()
    
    for i, config in enumerate(configurations, 1):
        #print(f"\nTesting Configuration {i}:")
        #print(f"Parameters: {config}")
        # base_env = gym.make("FrozenLake-v1", desc=custom_map, render_mode="human", is_slippery=False) 
        #uncomment if visualization is needed.

        base_env = gym.make("FrozenLake-v1", desc=custom_map, is_slippery=False)
        # base_env.metadata["render_fps"] = 999999
        env = CustomRewardFrozenLake(base_env)
        
        agent = QLearningAgent(env, **config)
        rewards, cumulative_reward, running_averages, epsilons = agent.train(n_episodes=1000)
        eval_reward = agent.evaluate()
        
        # Store milestone data (every 100 episodes)
        for episode in range(0, 1000, 100):
            milestone_data.append({
                'Configuration': f"Configuration {i}",
                'Parameters': str(config),
                'Episode': episode,
                'Running_Average_Reward': running_averages[episode],
                'Epsilon': epsilons[episode]
            })
        
        # Store configuration results
        results_data.append({
            'Configuration': f"Configuration {i}",
            'Parameters': str(config),
            'Total_Cumulative_Reward': cumulative_reward,
            'Average_Reward_per_Episode': cumulative_reward/len(rewards),
            'Final_Running_Average': running_averages[-1],
            'Evaluation_Reward': eval_reward
        })
        
        env.close()
    
    # Save to Excel with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create and save the milestone data
    milestone_df = pd.DataFrame(milestone_data)
    milestone_df.to_excel(f'nodecayfinal_training_milestones_{timestamp}.xlsx', index=False)
    
    # Create and save the final results
    results_df = pd.DataFrame(results_data)
    results_df.to_excel(f'nodecayfinal_configuration_results_{timestamp}.xlsx', index=False)
    
    return milestone_df, results_df

def main():
    custom_map = prepare_for_env("map_1.txt")
    
    print("Starting configuration testing with custom rewards...")
    milestone_df, results_df = test_configurations(custom_map)
    
    print("\nResults have been saved to Excel files!")
    print("Check the current directory for files with timestamp in their names.")

if __name__ == "__main__":
    main()