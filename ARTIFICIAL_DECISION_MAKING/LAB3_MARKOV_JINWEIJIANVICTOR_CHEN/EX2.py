import numpy as np

#states (0,0 : 0,1 : 1,0 : 1,1)

# Define transition matrix
transition_matrix = np.array([
    [0.1, 0.4, 0.4, 0.1],  
    [0.4, 0.1, 0.1, 0.4],  
    [0.4, 0.1, 0.1, 0.4],
    [0.1, 0.4, 0.4, 0.1]   
])

# Simulate Markov Chain for a number of steps
def simulate_mc(transition_matrix, steps=10):
    state = 3  # Start in state (0,0)
    states = [state]
    for _ in range(steps):
        state = np.random.choice([0, 1, 2, 3], p=transition_matrix[state])
        states.append(state)
    return states

# Simulate the chain
states = simulate_mc(transition_matrix, steps=10)
print("States visited:", states)
