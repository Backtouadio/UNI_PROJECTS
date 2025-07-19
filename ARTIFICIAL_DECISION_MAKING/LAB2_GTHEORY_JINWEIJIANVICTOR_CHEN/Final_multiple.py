import nashpy as nash
import numpy as np
if __name__ == '__main__':
 print("RobotA and RobotB working")
 # Define the payoff matrices
 RA = np.array([[-2, -2, -2], [-6, -6, -6], [-17, -17, -17]])
 RB = np.array([[-8, -8, -8], [-13, -13, -13], [-3, -3, -3]])
 # Create the game
 game = nash.Game(RA, RB)
 # Find Nash equilibrium
equilibrium = list(game.support_enumeration())
print(equilibrium)
# Learning Nash equilibrium
"""np.random.seed(0)
iterations = 100
play_counts = game.fictitious_play(iterations=iterations)
for row_play_counts, column_play_counts in play_counts:
   print(row_play_counts, column_play_counts)"""

"""sigma_RA = [1,0.05,0.05] # P1 cooperates always using a pure strategy
sigma_RB = [0.1, 0.1,0.8] # P2 cooperates 50% of times using a mixed strategy
utilities = game[sigma_RA, sigma_RB]
print(f"Utility for RobotA = {utilities[0]}")
print(f"Utility for RobotB = {utilities[1]}")"""