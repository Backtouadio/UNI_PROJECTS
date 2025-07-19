import numpy as np

# Grid world parameters
grid_size = 5
obstacles = [(1, 2), (1,1), (2,1), (3,1), (3,3), (4,3)]
start_state = (0, 0)
charger_locations = [(0, 3)]
people_locations = [(3, 4), (4, 0)]  # Added locations of people

# Actions = {up, down, left, right, charge, interact}
action_map = {0: '↑', 1: '↓', 2: '←', 3: '→', 4: '⚡', 5: '★'}  # Added interact action

# Q-learning parameters
learning_rate = 0.1
discount_factor = 0.9
episodes = 100
epsilon = 0.8

# Drive and motivation parameters
drive_energy_increment_rate = 2
drive_social_increment_rate = 1  # Added increment rate for social drive

# Added social motivation and drive
motivation_intensities = {
    'recharge': 0.0,
    'interact': 0.0  # New motivation for interaction
}
drive_values = {
    'energy': 0.0,
    'socialized': 0.0  # New drive for social needs
}

# Q-table (now with 6 actions including interact)
q_table = np.zeros((grid_size, grid_size, 6))

def get_next_state(current_state, action):
    x, y = current_state
    new_x, new_y = x, y
    
    if action == 0 and x > 0:  # Up
        new_x = x - 1
    elif action == 1 and x < grid_size - 1:  # Down
        new_x = x + 1
    elif action == 2 and y > 0:  # Left
        new_y = y - 1
    elif action == 3 and y < grid_size - 1:  # Right
        new_y = y + 1
    # Actions 4 (charge) and 5 (interact) don't change position
    
    if (new_x, new_y) in obstacles:
        return current_state
    return (new_x, new_y)

def get_reward(state, next_state, old_energy, new_energy, old_social, new_social, action):
    if next_state in obstacles:
        return -10
    
    # Reward for successful charging
    if state in charger_locations and action == 4:
        return 20
    
    # Reward for successful interaction
    if state in people_locations and action == 5:
        return 15
    
    # Combined penalty based on both drives
    energy_change = new_energy - old_energy
    social_change = new_social - old_social
    return -(energy_change + social_change)

def get_action_epsilon_greedy(q_table, state):
    x, y = state
    if np.random.rand() < epsilon:
        return np.random.choice(6)  # Now 6 actions
    return np.argmax(q_table[x, y])

def update_motivation_drive(drive, increment, ext_stimuli=0):
    if drive < 100:
        drive += increment
        if drive > 100:
            drive = 100
    return drive + ext_stimuli, drive

def execute_action(state, action):
    next_state = get_next_state(state, action)
    
    # Handle charging action
    if action == 4 and state in charger_locations:
        drive_values['energy'] = 0.0
    
    # Handle interact action
    if action == 5 and state in people_locations:
        drive_values['socialized'] = 0.0
    
    return next_state

def print_optimal_policy(q_table):
    policy_grid = []
    for x in range(grid_size):
        row = []
        for y in range(grid_size):
            if (x, y) in obstacles:
                row.append("X")
            elif (x, y) in charger_locations:
                row.append("C")
            elif (x, y) in people_locations:
                row.append("P")
            else:
                best_action = np.argmax(q_table[x, y])
                row.append(action_map[best_action])
        policy_grid.append(row)
    
    for row in policy_grid:
        print(" ".join(row))

if __name__ == "__main__":
    # Q-learning loop
    for episode in range(episodes):
        state = start_state
        steps = 0
        
        while steps < 100:  # Limit steps per episode
            x, y = state
            
            # Store current values for reward calculation
            old_energy = drive_values['energy']
            old_social = drive_values['socialized']
            
            # Get action and execute it
            action = get_action_epsilon_greedy(q_table, state)
            next_state = execute_action(state, action)
            
            # Update energy motivation
            if state in charger_locations:
                ext_stimuli_recharge = 10
            else:
                ext_stimuli_recharge = 0
            
            # Update social motivation
            if state in people_locations:
                ext_stimuli_social = 10
            else:
                ext_stimuli_social = 0
                
            # Update both drives and motivations
            motivation_intensities['recharge'], drive_values['energy'] = update_motivation_drive(
                drive_values['energy'],
                drive_energy_increment_rate,
                ext_stimuli_recharge
            )
            
            motivation_intensities['interact'], drive_values['socialized'] = update_motivation_drive(
                drive_values['socialized'],
                drive_social_increment_rate,
                ext_stimuli_social
            )
            
            # Calculate reward considering both drives
            reward = get_reward(state, next_state, old_energy, drive_values['energy'], 
                              old_social, drive_values['socialized'], action)
            
            # Update Q-value
            nx, ny = next_state
            best_next_action = np.argmax(q_table[nx, ny])
            q_table[x, y, action] += learning_rate * (
                reward + discount_factor * q_table[nx, ny, best_next_action] - q_table[x, y, action]
            )
            
            state = next_state
            steps += 1

    print("\nLearned Policy:")
    print_optimal_policy(q_table)