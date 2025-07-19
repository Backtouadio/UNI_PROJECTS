import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import scipy.cluster.hierarchy as shc

def load_and_prepare_data():
    """
    Loads the state and action data from CSV files and prepares them for analysis.
    Returns both datasets separately and prints information about their shape.
    """
    try:
        states_data = pd.read_csv('states_data.csv')
        actions_data = pd.read_csv('actions_data.csv')
        
        print("States data shape:", states_data.shape)
        print("Actions data shape:", actions_data.shape)
        
        if states_data.isnull().any().any() or actions_data.isnull().any().any():
            print("\nWarning: Dataset contains missing values!")
            print("\nMissing values in states data:")
            print(states_data.isnull().sum())
            print("\nMissing values in actions data:")
            print(actions_data.isnull().sum())
        
        print("\nFirst few rows of states data:")
        print(states_data.head())
        print("\nFirst few rows of actions data:")
        print(actions_data.head())
        
        return states_data, actions_data
    except FileNotFoundError as e:
        print(f"Error: Could not find one or both data files.")
        print(f"Detailed error: {str(e)}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None, None

def examine_data(data, dataset_name):
    """
    Prints useful information about the dataset to help understand its structure.
    """
    print(f"\nExamining {dataset_name}:")
    print("-" * 50)
    print(f"Number of rows and columns: {data.shape}")
    print("\nColumn names:")
    print(data.columns.tolist())
    print("\nData types of columns:")
    print(data.dtypes)
    print("\nBasic statistical description:")
    print(data.describe())

def prepare_data(data):
    """
    Prepare the data using StandardScaler
    """
    scaler = StandardScaler()
    return scaler.fit_transform(data)

def analyze_hierarchical_clustering(data, linkage_method='ward'):
    """
    Analyze hierarchical clustering with visualizations
    """
    # All the hierarchical clustering code remains the same here
    # (The entire function remains unchanged)
    scaled_data = prepare_data(data)
    
    n_clusters_range = [2,3,4,5,6,7,8,9,16,32,64]
    silhouette_scores = []
    
    for n_clusters in n_clusters_range:
        clusterer = AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage=linkage_method
        )
        cluster_labels = clusterer.fit_predict(scaled_data)
        silhouette_avg = silhouette_score(scaled_data, cluster_labels)
        silhouette_scores.append(silhouette_avg)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    dendrogram = shc.dendrogram(
        shc.linkage(scaled_data, method=linkage_method),
        ax=ax1,
        truncate_mode='lastp',
        p=32
    )
    ax1.set_title(f'Hierarchical Clustering Dendrogram\n({linkage_method} linkage)')
    ax1.set_xlabel('Sample Index or (Cluster Size)')
    ax1.set_ylabel('Distance')
    
    ax2.plot(n_clusters_range, silhouette_scores, 'bo-', linewidth=2)
    ax2.set_title('Silhouette Score vs Number of Clusters')
    ax2.set_xlabel('Number of Clusters')
    ax2.set_ylabel('Silhouette Score')
    ax2.grid(True)
    ax2.set_xscale('log', base=2)
    
    plt.tight_layout()
    plt.show()
    
    optimal_clusters = n_clusters_range[np.argmax(silhouette_scores)]
    print(f"\nOptimal number of clusters: {optimal_clusters}")
    print(f"Best silhouette score: {max(silhouette_scores):.3f}")
    
    if data.shape[1] == 2:
        final_clustering = AgglomerativeClustering(
            n_clusters=optimal_clusters,
            linkage=linkage_method
        )
        cluster_labels = final_clustering.fit_predict(scaled_data)
        
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(scaled_data[:, 0], scaled_data[:, 1], 
                            c=cluster_labels, cmap='viridis')
        plt.title(f'Hierarchical Clustering Results\n{optimal_clusters} clusters')
        plt.colorbar(scatter)
        plt.show()

if __name__ == "__main__":
    # First load and examine the data
    states_data, actions_data = load_and_prepare_data()
    
    if states_data is not None and actions_data is not None:
        # Examine both datasets
        examine_data(states_data, "States Data")
        examine_data(actions_data, "Actions Data")
        print("\nData loaded successfully and ready for clustering analysis!")
        
        # Now perform the clustering analysis
        methods = ['ward', 'complete', 'average', 'single']
        
        for method in methods:
            print(f"\nAnalyzing with {method} linkage method:")
            analyze_hierarchical_clustering(actions_data, linkage_method=method) #change states_data for action data