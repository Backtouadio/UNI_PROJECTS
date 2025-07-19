import nashpy as nash
import numpy as np
if __name__ == '__main__':
 print("The prisoner's dilemma")
 # Define the payoff matrices
 A = np.array([[-1, -3], [0, -2]])
 B = np.array([[-1, 0], [-3, -2]])
 # Create the game  
 game = nash.Game(A, B)
 # Find Nash equilibrium
 equilibrium = list(game.support_enumeration())
 print(equilibrium)