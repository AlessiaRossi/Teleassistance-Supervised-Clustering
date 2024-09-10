import pandas as pd
import numpy as np
from collections import Counter
import logging
from sklearn.metrics import silhouette_samples
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class MetricsEvaluation:

    def __init__(self, df:pd.DataFrame):
        self.df = df
            

    def __purity_score(self, true_labels:pd.Series, clusters:pd.Series) -> float:
        '''
            This function calculates the purity score of a clustering algorithm.

            Parameters:
            - true_labels: The true labels of the data points.
            - clusters: The cluster labels assigned by the clustering algorithm.

            Returns:
            - The purity score of the clustering algorithm.
        '''
        
        N = len(true_labels) # number of data points
        purity_sum = 0

        # Iterate over each cluster
        for cluster_id in np.unique(clusters):
            # Obtain the indices of data points in the cluster
            print(cluster_id)

            cluster_indices = np.where(clusters == cluster_id)[0] # [0] to get the array from the tuple, as np.where returns a tuple
            # print('Cluster indices:', cluster_indices)

            # Obtain the true labels of data points in the cluster
            cluster_labels = true_labels[cluster_indices]
            # print('Cluster labels', cluster_labels.value_counts())
            # print('Cluster labels', cluster_labels.count())

            # Count the number of data points in each class
            most_common_label, count = Counter(cluster_labels).most_common(1)[0] # most_common returns a list of tuples, we take the first one
            print(f'Most common label: {most_common_label}, count: {count}')

            purity_sum += count

        purity = purity_sum / N # Calculate the purity score
        return purity


    def __silhouette_score(self, features, clusters) -> float:
        '''
            This function calculates the silhouette score of a clustering algorithm.

            Parameters:
            - features: The feature data used for clustering.
            - clusters: The cluster labels assigned by the clustering algorithm.

            Returns:
            - The silhouette score of the clustering algorithm.
        '''

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


    def __label_encoding(self, df:pd.DataFrame):
        '''
            This function performs label encoding on non-numeric columns in the DataFrame.

            Parameters:
            - df: DataFrame containing the labeled data for clustering.

            Returns:
            - X_standardized_df: DataFrame containing the standardized feature data.
            - clusters: The cluster labels assigned by the clustering algorithm.
        '''

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
                
        # NOTE It would be better to use OneHotEncoder, but since I have a very large dataset, I cannot afford to do one-hot encoding as it would exceed the memory limit.

        # Standardize the feature data
        scaler = StandardScaler()
        X_standardized = scaler.fit_transform(feature_columns)

        X_standardized_df = pd.DataFrame(X_standardized)
        print(X_standardized_df.head())

        return X_standardized_df, clusters


    def __plot_silhouette(self, silhouette_vals, clusters):
        '''
            This function plots the silhouette values for each sample, grouped by cluster.

            Parameters:
            - silhouette_vals: The silhouette values for each sample.
            - clusters: The cluster labels assigned by the clustering algorithm.
        '''

        # Plot the silhouette values for each sample
        plt.figure(figsize=(10, 7))
        y_lower = 10

        # Iterate over each cluster
        for i in np.unique(clusters):
            ith_cluster_silhouette_vals = silhouette_vals[clusters == i] # Get the silhouette values for the current cluster
            ith_cluster_silhouette_vals.sort() # Sort the silhouette values
            size_cluster_i = ith_cluster_silhouette_vals.shape[0]   # Get the size of the cluster
            y_upper = y_lower + size_cluster_i  # Calculate the upper limit for the cluster plot

            # Fill the area for each cluster
            plt.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_cluster_silhouette_vals, alpha=0.7)
            plt.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for the next plot
            y_lower = y_upper + 10

        plt.savefig(f'graphs/silhouette_plot.png')


    def metrics_execution(self, config:dict) -> float:
        '''
            This function calculates the purity and silhouette scores of a clustering algorithm.

            Parameters:
            - config: Dictionary containing configuration settings for the clustering process.

            Returns:
            - The purity score of the clustering algorithm.
            - The mean normalized silhouette score of the clustering algorithm.
            - The final metric, with a penalty for the number of clusters, of the clustering algorithm.
        '''
        
        purity = self.__purity_score(self.df['incremento_teleassistenze'], self.df['cluster'])
        logging.info(f'Purity score: {purity}')

        X_standardized_df, clusters = self.__label_encoding(self.df)

        mean_normalized_silhouette_vals, silhouette_vals = self.__silhouette_score(X_standardized_df, clusters)
        logging.info(f'Mean normalized silhouette score: {mean_normalized_silhouette_vals}')

        # Plot the silhouette values for each sample
        self.__plot_silhouette(silhouette_vals, clusters)
        logging.info(f'Silhouette plot saved as silhouette_plot.png')

        # Calculate the final metrics with a penalty for the number of clusters
        final_metric = ((purity + mean_normalized_silhouette_vals) / 2) - (0.05 * config['modelling_clustering']['n_clusters'])
        logging.info(f'Final metric: {final_metric}')

        return purity, mean_normalized_silhouette_vals, final_metric
        