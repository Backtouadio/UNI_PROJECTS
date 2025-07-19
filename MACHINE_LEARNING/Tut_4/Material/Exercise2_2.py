import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_data(filepath):
    # Load data from a CSV file
    return pd.read_csv(filepath)

def plot_3d_scatter(data):
    # Create a 3D scatter plot of the data
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot for feature space
    sc = ax.scatter(data['x'], data['y'], data['Angular_velocity'], c=data['Action'], cmap='viridis', label='Data Points')
    cbar = fig.colorbar(sc, ax=ax)
    cbar.set_label('Action')

    # Set labels and title
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_zlabel('Angular Velocity')
    ax.set_title('3D Scatter Plot of the State Space')

    plt.legend()
    plt.show()

def main():
    # Path to the data file
    data_path = 'test_data.csv'
    
    # Load data
    data = load_data(data_path)
    
    # Visualize the data
    plot_3d_scatter(data)

if __name__ == '__main__':
    main()
