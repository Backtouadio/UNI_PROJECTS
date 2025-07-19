import gymnasium as gym
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt

class PendulumGameLoop:
    def __init__(self, model, model_type, scaler=None):
        self.env = gym.make('Pendulum-v1')
        self.model = model
        self.model_type = model_type
        self.scaler = scaler
        
    def run_episode(self, render=False):
        if render:
            env = gym.make('Pendulum-v1', render_mode='human')
        else:
            env = self.env
            
        state, _ = env.reset()
        total_reward = 0
        steps = 0
        terminated = False
        truncated = False
        episode_states = []
        episode_actions = []
        
        while not (terminated or truncated) and steps < 200: #change if need to change steps
            # Format state for model input
            if self.model_type == 'nn':
                # For Neural Network, convert to numpy array without feature names
                state_formatted = np.array([[state[0], state[1], state[2]]])
                if self.scaler is not None:
                    state_formatted = self.scaler.transform(state_formatted)
            else:
                # For other models, use DataFrame with feature names
                state_formatted = pd.DataFrame(
                    [[state[0], state[1], state[2]]],
                    columns=['x', 'y', 'Angular_velocity']
                )
            
            # Get action from model
            action = self.model.predict(state_formatted)
            
            # Ensure action is in correct format (scalar in [-2, 2])
            action = np.clip(action, -2, 2)
            if isinstance(action, np.ndarray):
                action = action.reshape(-1)
            
            # Take step in environment
            next_state, reward, terminated, truncated, _ = env.step(action)
            
            # Store state and action
            episode_states.append(state)
            episode_actions.append(action)
            
            total_reward += reward
            state = next_state
            steps += 1
        
        if render:
            env.close()
            
        return total_reward, steps, episode_states, episode_actions

    def evaluate(self, n_episodes=10, render_last=True):
        rewards = []
        steps_list = []
        all_states = []
        all_actions = []
        
        for episode in range(n_episodes):
            render = (episode == n_episodes - 1) and render_last
            reward, steps, states, actions = self.run_episode(render)
            rewards.append(reward)
            steps_list.append(steps)
            all_states.extend(states)
            all_actions.extend(actions)
        
        return {
            'mean_reward': np.mean(rewards),
            'std_reward': np.std(rewards),
            'mean_steps': np.mean(steps_list),
            'std_steps': np.std(steps_list),
            'all_states': np.array(all_states),
            'all_actions': np.array(all_actions)
        }

    def close(self):
        self.env.close()

def plot_results(results):
    models = list(results.keys())
    means = [results[model]['mean_reward'] for model in models]
    stds = [results[model]['std_reward'] for model in models]
    
    plt.figure(figsize=(10, 6))
    plt.bar(models, means, yerr=stds, capsize=5)
    plt.title('Model Performance Comparison')
    plt.ylabel('Mean Reward')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('model_comparison.png')
    plt.close()

if __name__ == "__main__":
    try:
        # Load training data
        print("Loading training data...")
        training_data = pd.read_csv('training_data.csv')
        X_train = training_data[['x', 'y', 'Angular_velocity']]
        y_train = training_data['Action']
        
        # 1. Decision Tree Model
        print("\nTraining Decision Tree Model...")
        dt_model = DecisionTreeRegressor(
            max_depth=20,
            min_samples_split=40,
            max_features=None,
            criterion='squared_error',
            splitter='random'
        )
        dt_model.fit(X_train, y_train)
        
        # 2. Linear Regression Model
        print("\nTraining Linear Regression Model...")
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        
        # 3. Neural Network Model
        print("\nTraining Neural Network Model...")
        scaler = StandardScaler()
        # Convert to numpy array before scaling for neural network
        X_train_np = X_train.to_numpy()
        X_train_scaled = scaler.fit_transform(X_train_np)
        
        nn_model = MLPRegressor(
            hidden_layer_sizes=(50,),
            activation='tanh',
            solver='adam',
            learning_rate_init=0.01,
            max_iter=500,
            random_state=42
        )
        nn_model.fit(X_train_scaled, y_train)
        
        # Create dictionary of models to evaluate
        models = {
            'Decision Tree': (dt_model, 'dt', None),
            'Linear Regression': (lr_model, 'lr', None),
            'Neural Network': (nn_model, 'nn', scaler)
        }
        
        # Evaluate all models
        results = {}
        for model_name, (model, model_type, scaler) in models.items():
            print(f"\nEvaluating {model_name}...")
            game_loop = PendulumGameLoop(model, model_type, scaler)
            results[model_name] = game_loop.evaluate(n_episodes=50) #change for increasing number of episodes
            game_loop.close()
            
            print(f"Results for {model_name}:")
            print(f"Mean reward: {results[model_name]['mean_reward']:.2f} ± {results[model_name]['std_reward']:.2f}")
            print(f"Mean steps: {results[model_name]['mean_steps']:.2f} ± {results[model_name]['std_steps']:.2f}")
        
        # Plot results
        plot_results(results)
        print("\nEvaluation complete! Check 'model_comparison.png' for visual results.")
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        print("\nFull error trace:")
        print(traceback.format_exc())