import numpy as np
from hmmlearn import hmm
import random

def initialize_model():
    # Define HMM with 3 hidden states: alone, accompanied, interacting
    model = hmm.CategoricalHMM(n_components=3)
    
    # Initial state probabilities
    model.startprob_ = np.array([0.8, 0.1, 0.1])
    
    # Transition probabilities
    model.transmat_ = np.array([
        [0.3, 0.5, 0.2],  # alone -> [alone, accompanied, interacting]
        [0.3, 0.2, 0.5],  # accompanied -> [alone, accompanied, interacting]
        [0.3, 0.5, 0.2]   # interacting -> [alone, accompanied, interacting]
    ])
    
    # Emission probabilities
    model.emissionprob_ = np.array([
        [0.02,0.02,0.02, 0.02, 0.23, 0.23, 0.23, 0.23],    # alone
        [0.15,0.3,0.15, 0.3, 0.025, 0.025, 0.025, 0.025],  # accompanied
        [0.4,0.05,0.4, 0.05, 0.025, 0.025, 0.025, 0.025]   # interacting
    ])
    
    return model

def get_observation_description(obs):
    # Convert numerical observation to human-readable format
    observations = {
        0: "Body:Yes, Face:Yes, Voice:Yes",
        1: "Body:Yes, Face:Yes, Voice:No",
        2: "Body:Yes, Face:No, Voice:Yes",
        3: "Body:Yes, Face:No, Voice:No",
        4: "Body:No, Face:Yes, Voice:Yes",
        5: "Body:No, Face:Yes, Voice:No",
        6: "Body:No, Face:No, Voice:Yes",
        7: "Body:No, Face:No, Voice:No"
    }
    return f"O_{obs} ({observations[obs]})"

def get_state_description(state):
    states = {
        0: "ALONE",
        1: "ACCOMPANIED",
        2: "INTERACTING"
    }
    return states[state]

def generate_observation(state, emission_probs):
    outcomes = list(range(8))  # 0 to 7 representing different observation combinations
    observation = random.choices(outcomes, weights=emission_probs[state])[0]
    return observation

def execute_action(state):
    actions = {
        0: "Maggie is SLEEPING because no user is detected",
        1: "Maggie is CALLING THE USER because they are not interacting",
        2: "Maggie is PLAYING A GAME with the engaged user"
    }
    return actions[state]

def simulate_maggie():
    print("Starting Maggie's decision-making simulation...\n")
    
    # Initialize the model
    model = initialize_model()
    
    # Initialize state randomly based on initial probabilities
    current_state = random.choices(range(3), weights=model.startprob_)[0]
    
    # Keep track of state counts for summary
    state_counts = {0: 0, 1: 0, 2: 0}
    
    # Simulation loop
    for i in range(10):
        print(f"\n=== Iteration {i+1} ===")
        
        # Generate observation based on current state
        observation = generate_observation(current_state, model.emissionprob_)
        
        # Format observation for hmmlearn
        obs = np.array([[observation]]).T
        
        # Predict most probable state based on observation
        predicted_state = model.predict(obs)[0]
        state_counts[predicted_state] += 1
        
        # Print iteration details
        print(f"Sensor readings: {get_observation_description(observation)}")
        print(f"Predicted state: {get_state_description(predicted_state)}")
        print(f"Action: {execute_action(predicted_state)}")
        
        # Update current state based on transition probabilities
        current_state = random.choices(
            range(3), 
            weights=model.transmat_[predicted_state]
        )[0]
    
    # Print summary
    print("\n=== Simulation Summary ===")
    print(f"Times Maggie was alone: {state_counts[0]}")
    print(f"Times Maggie was accompanied: {state_counts[1]}")
    print(f"Times Maggie was interacting: {state_counts[2]}")

if __name__ == '__main__':
    simulate_maggie()