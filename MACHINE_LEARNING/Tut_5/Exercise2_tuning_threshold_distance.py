import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def tune_distance_threshold(data, linkage_method='ward'):
    """
    Analyze different distance thresholds for hierarchical clustering with proper validation
    of the number of clusters.
    """
    # Prepare the data with standardization
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    # Use a clustering object to help determine a reasonable range of distances
    temp_clustering = AgglomerativeClustering(
        n_clusters=2,  # Start with 2 clusters to get an idea of distances
        linkage=linkage_method
    )
    temp_clustering.fit(scaled_data)
    
    # Create a more reasonable range of thresholds that won't create too many clusters
    if linkage_method == 'ward':
        # Ward tends to need larger thresholds
        thresholds = np.linspace(5, 20, 10)
    else:
        # Other methods might work with smaller thresholds
        thresholds = np.linspace(2, 15, 10)
    
    # Test each threshold
    results = []
    for threshold in thresholds:
        # Perform clustering with current threshold
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=threshold,
            linkage=linkage_method
        )
        labels = clustering.fit_predict(scaled_data)
        n_clusters = len(np.unique(labels))
        
        # Only calculate silhouette score if we have a valid number of clusters
        # (between 2 and n_samples - 1)
        if 2 <= n_clusters <= len(scaled_data) - 1:
            try:
                silhouette = silhouette_score(scaled_data, labels)
            except Exception as e:
                print(f"Warning: Could not calculate silhouette score for threshold {threshold}")
                print(f"Number of clusters: {n_clusters}")
                print(f"Error: {str(e)}")
                silhouette = 0
        else:
            silhouette = 0
            
        results.append({
            'threshold': threshold,
            'n_clusters': n_clusters,
            'silhouette': silhouette
        })
        
        # Print progress for each threshold
        print(f"Threshold {threshold:.2f}: {n_clusters} clusters, silhouette = {silhouette:.3f}")
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    thresholds = [r['threshold'] for r in results]
    n_clusters = [r['n_clusters'] for r in results]
    silhouette_scores = [r['silhouette'] for r in results]
    
    # Plot number of clusters
    plt.plot(thresholds, n_clusters, 'bo-', label='Number of Clusters')
    plt.xlabel('Distance Threshold')
    plt.ylabel('Number of Clusters')
    
    # Add silhouette scores to the same plot with a different scale
    plt.twinx()
    plt.plot(thresholds, silhouette_scores, 'r--', label='Silhouette Score')
    plt.ylabel('Silhouette Score')
    
    plt.title(f'Clustering Results with {linkage_method} Linkage')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Find and print the best threshold that gives a reasonable number of clusters
    valid_results = [r for r in results if 2 <= r['n_clusters'] <= 20 and r['silhouette'] > 0]
    if valid_results:
        best_result = max(valid_results, key=lambda x: x['silhouette'])
        print("\nBest clustering result:")
        print(f"Distance threshold: {best_result['threshold']:.2f}")
        print(f"Number of clusters: {best_result['n_clusters']}")
        print(f"Silhouette score: {best_result['silhouette']:.3f}")
    else:
        print("\nNo valid clustering results found. Try adjusting the threshold range.")

# Example usage
if __name__ == "__main__":
    try:
        # Load your data
        print("Loading data...")
        data = pd.read_csv('states_data.csv')  # or states_data.csv
        print(f"Data shape: {data.shape}")
        
        # Try different linkage methods
        methods = ['ward', 'complete', 'average', 'single']
        for method in methods:
            print(f"\nAnalyzing with {method} linkage method:")
            tune_distance_threshold(data, linkage_method=method)
            
    except FileNotFoundError:
        print("Error: Make sure your data file is in the correct location")