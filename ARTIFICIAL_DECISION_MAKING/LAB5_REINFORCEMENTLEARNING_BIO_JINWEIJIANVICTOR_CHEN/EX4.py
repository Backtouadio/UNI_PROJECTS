import numpy as np

# Grid world parameters
GRID_SIZE = 5
START_STATE = (0, 0)
MAX_ITER = 1000

# Actions = {up, down, left, right, charge}
ACTION_MAP = {0: '↑', 1: '↓', 2: '←', 3: '→', 4: '⚡'} 

# Defining motivations and drives
MOTIVATIONS_MAP = {0: 'recharge'}
DRIVES_MAP = {0: 'energy'}
DRIVE_ENERGY_INCREMENT_RATE = 2
motivation_intensities = {'recharge': 0.0}  # Initialization of motivations
drive_values = {'energy': 0.0}  # Initialization of drives: from 0.0 to 100.0

# Locations of external stimuli
CHARGER_LOCATIONS = [(0, 3)]  # Can be changed to any position!

# Initialize Q-table
q_table = np.zeros((GRID_SIZE, GRID_SIZE, 5))  # 5 actions including charging

def set_manual_policy():
    charger_x, charger_y = CHARGER_LOCATIONS[0]  # Get charger position
    
    # For each cell in the grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if (x, y) in CHARGER_LOCATIONS:
                # At charger location, set charging as best action
                q_table[x, y, 4] = 100  # Charge
            else:
                # Horizontal movement
                if y < charger_y:  # Charger is to the right
                    q_table[x, y, 3] = 80  # Right
                elif y > charger_y:  # Charger is to the left
                    q_table[x, y, 2] = 80  # Left
                
                # Vertical movement
                if x > charger_x:  # Charger is above
                    q_table[x, y, 0] = 90  # Up
                elif x < charger_x:  # Charger is below
                    q_table[x, y, 1] = 90  # Down

def update_motivation_drive(drive, increment, ext_stimuli=0):
    if drive < 100:  # we limit the drive value to 100
        drive += increment
        if drive > 100:
            drive = 100
    return drive + ext_stimuli, drive

def execute_action(current_state, action):
    x, y = current_state
    if action == 0 and x > 0:  # Up
        x -= 1
    elif action == 1 and x < GRID_SIZE - 1:  # Down
        x += 1
    elif action == 2 and y > 0:  # Left
        y -= 1
    elif action == 3 and y < GRID_SIZE - 1:  # Right
        y += 1
    elif action == 4:  # Charge action
        if current_state in CHARGER_LOCATIONS:
            drive_values['energy'] = 0.0  # Reset energy need when charging
    return x, y

def print_policy():
    for x in range(GRID_SIZE):
        row = []
        for y in range(GRID_SIZE):
            if (x, y) in CHARGER_LOCATIONS:
                row.append('C')  # Charger location
            else:
                best_action = np.argmax(q_table[x, y])
                row.append(ACTION_MAP[best_action])
        print(' '.join(row))

# Main execution
if __name__ == "__main__":
    # Set the manual policy
    set_manual_policy()
    
    # Print initial policy
    print("Manual Policy for Energy Management:")
    print_policy()
    
    # Run simulation
    state = START_STATE
    for iter in range(MAX_ITER):
        # Update motivation intensity and drive value
        if state in CHARGER_LOCATIONS:
            ext_stimuli_recharge = 10
        else:
            ext_stimuli_recharge = 0
        
        # Update M_recharge intensity and d_energy value
        motivation_intensities['recharge'], drive_values['energy'] = update_motivation_drive(
            drive_values['energy'], 
            DRIVE_ENERGY_INCREMENT_RATE, 
            ext_stimuli_recharge
        )
        
        # Select action based on manual policy
        x, y = state
        action = np.argmax(q_table[x, y])
        
        # Execute action and observe next state
        next_state = execute_action(state, action)
        state = next_state
        
        # Print status every 100 iterations
        if iter % 100 == 0:
            print(f"\nIteration {iter}")
            print(f"Energy level: {drive_values['energy']:.2f}")
            print(f"Position: {state}") 