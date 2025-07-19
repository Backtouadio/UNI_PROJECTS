import numpy as np
from mdptoolbox.mdp import ValueIteration, PolicyIteration

# Define the grid dimensions
num_states = 4  # 2x2 grid --> 4 states = {(0,0), (0,1), (1,0), (1,1)}
num_actions = 4  # Up, Down, Left, Right

# Define transition probabilities P
# P[action][current_state][next_state] gives the probability of moving to next_state from current_state given action
P = np.zeros((num_actions, num_states, num_states))

# Actions: 0 = Up, 1 = Down, 2 = Left, 3 = Right
# Transition for each action with 0.9 to the intended direction, and 0.1 to other options
P[0] = np.array([  # Transition probabilities for action: UP
    [0.90, 0.03, 0.04, 0.03],  # moving up from state (0,0)
    [0.05, 0.90, 0.05, 0.00],  # moving up from state (0,1)
    [0.90, 0.05, 0.05, 0.00],  # moving up from state (1,0)
    [0.02, 0.90, 0.04, 0.04]   # moving up from state (1,1)
])
P[1] = np.array([  # Transition probabilities for action: Down
    [0.03, 0.03, 0.9, 0.04],  # moving down from state (0,0)
    [0.03, 0.03, 0.04, 0.9],  # moving down from state (0,1)
    [0.04, 0.03, 0.9, 0.03],  # moving down from state (1,0)
    [0.03, 0.04, 0.03, 0.9]   # moving down from state (1,1)
])
P[2] = np.array([  # Transition probabilities for action: left
    [0.9, 0.03, 0.03, 0.04],  # moving left from state (0,0)
    [0.9, 0.03, 0.04, 0.03],  # moving left from state (0,1)
    [0.04, 0.03, 0.9, 0.03],  # moving left from state (1,0)
    [0.03, 0.04, 0.9, 0.03]   # moving left from state (1,1)
])
P[3] = np.array([  # Transition probabilities for action: right
    [0.03, 0.9, 0.03, 0.04],  # moving right from state (0,0)
    [0.03, 0.9, 0.04, 0.03],  # moving right from state (0,1)
    [0.04, 0.03, 0.03, 0.9],  # moving right from state (1,0)
    [0.03, 0.04, 0.03, 0.9]   # moving right from state (1,1)
])


# ToDo: transition probabilities for actions DOWN, LEFT, RIGHT

# Define rewards matrix R
# R[action][current_state][next_state] gives the reward obtained when moving to next_state from current_state by action
R = np.zeros((num_actions, num_states, num_states))

R[0] = np.array([  # Rewards for action: UP
    [0, 0, -10, 1],  # rewards by Up from state (0,0)
    [0, 0, -10, 1],  # rewards by Up from state (0,1)
    [0, 0, -10, 1],  # rewards by Up from state (1,0)
    [0, 0, -10, 1]   # rewards by Up from state (1,1)
])
R[1] = np.array([  
    [0, 0, -10, 1],  
    [0, 0, -10, 1],  
    [0, 0, -10, 1],  
    [0, 0, -10, 1]   
])
R[2] = np.array([  
    [0, 0, -10, 1],  
    [0, 0, -10, 1],  
    [0, 0, -10, 1],  
    [0, 0, -10, 1]   
])
R[3] = np.array([  
    [0, 0, -10, 1],  
    [0, 0, -10, 1],  
    [0, 0, -10, 1],  
    [0, 0, -10, 1]   
])

# Set MDP parameters
gamma = 0.9 # Discount factor
# Initialize the PolicyIteration MDP and run
vi = PolicyIteration(P, R, gamma)
vi.run()
# Print optimal policy and value for each state
print("Using the PolicyIteration method")
print("Optimal Policy:", vi.policy)
print("State Values:", vi.V)