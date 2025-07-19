import nashpy as nash
import numpy as np
if __name__ == '__main__':
 print("Ballet or theater")
 # Define the payoff matrices
 P1 = np.array([[4, 0], [0, 2]])
 P2 = np.array([[2, 0], [0, 4]])
 # Create the game
 game = nash.Game(P1, P2)
 # Find Nash equilibrium
 equilibrium = list(game.support_enumeration())
 print(equilibrium)