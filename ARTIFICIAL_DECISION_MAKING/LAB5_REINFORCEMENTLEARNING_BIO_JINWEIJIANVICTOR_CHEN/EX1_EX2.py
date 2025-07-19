import numpy as np

# Initialization of the environment
grid_size = 5
goal_state = (4, 4)
#obstacles = [(2, 2)]
obstacles = [(1, 2), (1,1), (2,1), (3,1), (3,3), (4,3)] #for other exercise
start_state = (0, 0)
action_map = {0: '↑', 1: '↓', 2: '←', 3: '→'}

# Q-learning parameters
learning_rate = 0.1
discount_factor = 1
episodes = 100
epsilon = 0.8  # used in epsilon-greedy strategy for action selection

# Q-table
q_table = np.zeros((grid_size, grid_size, 4))  # 4 actions: up, down, left, right

# Returns the next state considering the current state and an action.
# All transitions are deterministic.
def get_next_state(current_state, action):
    x, y = current_state
    if action == 0 and x > 0:  # Up
        x -= 1
    elif action == 1 and x < grid_size - 1:  # Down
        x += 1
    elif action == 2 and y > 0:  # Left
        y -= 1
    elif action == 3 and y < grid_size - 1:  # Right
        y += 1
    return (x, y)


# Returns the reward obtained when transiting to a state: goal +10, obstacle -10, other -1
def get_reward(new_state):
    if new_state == goal_state:
        return 20  # Reward for reaching the goal
    elif new_state in obstacles:
        return -10  # Penalty for hitting an obstacle
    else:
        return -1  # Step penalty for every other move



    """
    Gets an action implementing the epsilon-greedy strategy to balance
    exploration and exploitation:
    - with a probability of 1-ϵ, the agent chooses the action with the
      highest Q-value for the current state;
    - with a probability of ϵ, the agent selects a random action,
      regardless of its Q-value.

    Parameters:
    - q_table: A numpy array of shape (grid_size, grid_size, 4)
      representing Q-values for actions.
    - state: The current state of the agent
    """
def get_action_epsilon_greedy(q_table, state):
    x, y = state
    if np.random.rand() < epsilon:
        # Exploration: Choose a random action
        new_action = np.random.choice(4)
    else:
        # Exploitation: Choose the action with the highest Q-value
        new_action = np.argmax(q_table[x, y]) # retrieves the Q-values for the four actions at the current state (x, y)
        # np.argmax() returns the index of the action with the highest Q-value 
        # (e.g., if action 2 has the highest value, np.argmax() returns 2).

    return new_action

"""# Q-learning loop
for episode in range(episodes):
    state = start_state #save current state
    while state != goal_state:
        x,y = state #track current state
        action = get_action_epsilon_greedy(q_table, state)
        next_state = get_next_state(state, action)
        reward = get_reward(next_state)
        # Update Q-value
        # Complete this function
        nx, ny = next_state #track next step
        best_next_action = np.argmax(q_table[nx, ny])
        q_table[x, y, action] += learning_rate * (
            reward + discount_factor * q_table[nx, ny, best_next_action] - q_table[x, y, action])

        state = next_state"""
# Function to print the optimal policy from the Q-table
def print_optimal_policy(q_table):
    policy_grid = []
    for x in range(grid_size):
        row = []
        for y in range(grid_size):
            if (x, y) in obstacles:
                row.append("X")  # Mark obstacles
            elif (x, y) == goal_state:
                row.append("G")  # Mark goal
            else:
                # Find the best action based on the Q-values
                best_action = np.argmax(q_table[x, y])
                row.append(action_map[best_action])
        policy_grid.append(row)
    
    # Print the policy grid
    for row in policy_grid:
        print(" ".join(row))

# Main block to run the code
if __name__ == "__main__":
    # Q-learning loop
    for episode in range(episodes):
        state = start_state
        while state != goal_state:
            x, y = state
            action = get_action_epsilon_greedy(q_table, state)
            next_state = get_next_state(state, action)
            reward = get_reward(next_state)

            # Update Q-value
            nx, ny = next_state
            best_next_action = np.argmax(q_table[nx, ny])
            q_table[x, y, action] += learning_rate * (
                reward + discount_factor * q_table[nx, ny, best_next_action] - q_table[x, y, action])

            state = next_state

    # Print the resulting Q-table (optional)
    print("\nFinal Q-table:")
    #print(q_table)

    # Print the optimal policy
    print("\nOptimal Policy:")
    print_optimal_policy(q_table)

