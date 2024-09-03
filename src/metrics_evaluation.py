import pandas as pd
import numpy as np
from collections import Counter
import logging
from sklearn.metrics import silhouette_samples
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def purity_score(true_labels:pd.Series, clusters:pd.Series) -> float:
    """Calculate the purity score."""
    
    N = len(true_labels) # number of data points
    purity_sum = 0

    for cluster_id in np.unique(clusters):
        # Obtain the indices of data points in the cluster
        # print(cluster_id)

        cluster_indices = np.where(clusters == cluster_id)[0] # [0] to get the array from the tuple, as np.where returns a tuple
        # print('Cluster indices:', cluster_indices)

        # Obtain the true labels of data points in the cluster
        cluster_labels = true_labels[cluster_indices]
        # print('Cluster labels', cluster_labels)

        # Count the number of data points in each class
        most_common_label, count = Counter(cluster_labels).most_common(1)[0] # most_common returns a list of tuples, we take the first one
        # print(f'Most common label: {most_common_label}, count: {count}')

        purity_sum += count

    purity = purity_sum / N
    return purity


def silhouette_score(features, clusters) -> float:
    # Calculate the silhouette scores for each sample
    silhouette_vals = silhouette_samples(features, clusters)
    
    print(silhouette_vals)

    # Calculate the mean silhouette score
    # NOTE, OPTIMIZE: the code work, but the mean silhouette can be calulated in a more efficient way. "np.mean(silhouette_vals)" is enough
    # mean_silhouette = silhouette_score(features, clusters)

    # Normalize the silhouette scores to a range between 0 and 1
    normalized_silhouette_vals = (silhouette_vals - silhouette_vals.min()) / (silhouette_vals.max() - silhouette_vals.min())

    # NOTE, OPTIMIZE: the code work, but the mean silhouette can be calulated in a more efficient way. "np.mean(normalized_silhouette_vals)" is enough
    # normalized_mean_silhouette = (mean_silhouette - silhouette_vals.min()) / (silhouette_vals.max() - silhouette_vals.min())

    return np.mean(normalized_silhouette_vals), silhouette_vals


def label_encoding(df:pd.DataFrame):
    """Label encoding of the categorical columns."""

    # Extract clusters and true labels
    clusters = df['cluster'].to_numpy()
    # Remove the cluster column to get the feature data
    feature_columns = df.drop(columns=['cluster'])
    print(feature_columns.columns)
    
   # Convert non-numeric columns to numeric using LabelEncoder
    for column in feature_columns.columns:
        if feature_columns[column].dtype == 'object':
            le = LabelEncoder()
            feature_columns[column] = le.fit_transform(feature_columns[column])
            
    # NOTE Sarebbe meglio usare OneHotEncoder ma avendo un dataset molto grande non posso permettermi di fare one hot encoding in quanto la memoria non basta

    scaler = StandardScaler()
    X_standardized = scaler.fit_transform(feature_columns)

    X_standardized_df = pd.DataFrame(X_standardized)

    return X_standardized_df, clusters


def plot_silhouette(silhouette_vals, clusters):
    # Plot the silhouette values for each sample
    plt.figure(figsize=(10, 7))
    y_lower = 10
    for i in np.unique(clusters):
        ith_cluster_silhouette_vals = silhouette_vals[clusters == i]
        ith_cluster_silhouette_vals.sort()
        size_cluster_i = ith_cluster_silhouette_vals.shape[0]
        y_upper = y_lower + size_cluster_i

        plt.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_vals, alpha=0.7)
        plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        y_lower = y_upper + 10

    plt.savefig('graphs/silhouette_plot.png')


def metrics_execution(df:pd.DataFrame, config:dict) -> float:
    """Execution of metrics calculation."""
    
    purity = purity_score(df['incremento_teleassistenze'], df['cluster'])
    logging.info(f'Purity score: {purity}')

    X_standardized_df, clusters = label_encoding(df)

    mean_normalized_silhouette_vals, silhouette_vals = silhouette_score(X_standardized_df, clusters)
    logging.info(f'Mean normalized silhouette score: {mean_normalized_silhouette_vals}')

    # Plot the silhouette values for each sample
    plot_silhouette(silhouette_vals, clusters)

    # Calculate the final metrics with a penalty for the number of clusters
    final_metric = ((purity + mean_normalized_silhouette_vals) / 2) - (0.05 * config['modelling_clustering']['n_clusters'])

    return purity, mean_normalized_silhouette_vals, final_metric
    