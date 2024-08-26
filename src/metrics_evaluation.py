import pandas as pd
import numpy as np
from collections import Counter
import logging
from sklearn.metrics import silhouette_samples
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


def purity_score(true_labels, clusters):
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


def silhouette_score(features, clusters):
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

    return np.mean(normalized_silhouette_vals)


def label_encoding(df:pd.DataFrame) -> pd.DataFrame:
    """Label encoding of the categorical columns."""

    # Extract clusters and true labels
    clusters = df['cluster'].to_numpy()
    # Remove the cluster column to get the feature data
    feature_columns = df.drop(columns=['cluster'])
    
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


def metrics_execution(df:pd.DataFrame, config:dict) -> None:
    """Execution of metrics calculation."""
    
    purity_score = purity_score(df['incremento_teleassistenze'], df['cluster'])
    logging.info(f'Purity score: {purity_score}')

    X_standardized_df, clusters = label_encoding(df)

    mean_normalized_silhouette_vals = silhouette_score(X_standardized_df, clusters)
    logging.info(f'Mean normalized silhouette score: {mean_normalized_silhouette_vals}')

    # Calculate the final metrics with a penalty for the number of clusters
    final_metrics = ((purity_score + mean_normalized_silhouette_vals) / 2) - (0.05 * config['modelling_clustering']['n_clusters'])

    return final_metrics
    