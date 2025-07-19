import nashpy as nash
import numpy as np
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
 print("The prisoner's dilemma")
 # Define the payoff matrices
 A = np.array([[-1, -3], [0, -2]])
 B = np.array([[-1, 0], [-3, -2]])
 # Create the game
 game = nash.Game(A, B)
 # Defining strategies for both players
 sigma_p1 = [1, 0] # P1 cooperates always using a pure strategy
 sigma_p2 = [0.5, 0.5] # P2 cooperates 50% of times using a mixed strategy
 utilities = game[sigma_p1, sigma_p2]
 print(f"Utility for P1 = {utilities[0]}")
 print(f"Utility for P2 = {utilities[1]}")
