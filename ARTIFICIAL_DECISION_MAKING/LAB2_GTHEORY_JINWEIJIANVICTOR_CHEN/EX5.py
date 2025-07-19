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
# Learning Nash equilibrium
 np.random.seed(0)
 iterations = 100
 play_counts = game.fictitious_play(iterations=iterations)
 for row_play_counts, column_play_counts in play_counts:
    print(row_play_counts, column_play_counts)