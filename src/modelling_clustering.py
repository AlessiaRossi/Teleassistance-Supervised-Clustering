import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
import matplotlib.pyplot as plt
import pickle
import logging


def _elbow_method(df:pd.DataFrame, max_clusters:int) -> None:
    '''
    Determines the optimal number of clusters using the Elbow Method.

    The Elbow Method evaluates the cost (sum of dissimilarities) for different numbers of clusters
    and helps to identify the optimal number by looking for an 'elbow' point where the cost curve
    starts to level off.

    Parameters:
    - df: DataFrame containing the data to cluster.
    - max_clusters: Maximum number of clusters to test for the Elbow Method.
    '''
    
    cost = []
    K = range(1, max_clusters) # Range of cluster numbers to test
    # print(K)
    print(df.head())

    # Calculate the cost for different numbers of clusters
    for numero_cluster in K:
        print(numero_cluster)
        kmodes = KModes(n_clusters=numero_cluster, init='Huang', n_init=5, verbose=1)
        kmodes.fit_predict(df)
        cost.append(kmodes.cost_) # Append the cost for the current number of clusters

    # Plot the Elbow Method results
    plt.plot(K, cost, 'bx-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Cost')
    plt.title('Elbow Method For Optimal k')
    plt.savefig('graphs/elbow_method.png')


def _kmodes_clustering(kmodes:KModes, df:pd.DataFrame) -> pd.DataFrame:
    '''
    Applies K-Modes clustering to the DataFrame.

    This function fits the K-Modes algorithm to the data and adds the resulting cluster labels
    to the DataFrame.

    Parameters:
    - kmodes: An instance of the KModes class, configured with the desired number of clusters.
    - df: DataFrame containing the data to be clustered.

    Returns:
    - DataFrame with an additional 'cluster' column indicating the cluster assignment.
    '''
    clusters = kmodes.fit_predict(df) # Fit the model and predict the clusters
    df['cluster'] = clusters # Add the cluster labels to the DataFrame

    return df


def clustering_execution(df_labeled:pd.DataFrame, config:dict) -> pd.DataFrame:
    '''
    Executes the clustering process based on the provided configuration.

    This function performs feature selection, applies the Elbow Method (if enabled),
    performs K-Modes clustering (if enabled), and saves the trained model.

    Parameters:
    - df_labeled: DataFrame containing the labeled data for clustering.
    - config: Dictionary containing configuration settings for the clustering process.

    Returns:
    - df_labeled: Original DataFrame with an additional 'cluster' column indicating the cluster assignment.
    - df: DataFrame used for clustering, with cluster labels added.
    '''

    # Configure logging
    logging.basicConfig(filename=config['general']['logging_level'], format='%(asctime)s - %(message)s', level=logging.INFO)

    # Drop unnecessary columns based on the configuration
    list_cols_to_drop = config['modelling_clustering']['list_cols_to_drop']
    cols_to_drop = df_labeled.columns[list_cols_to_drop]
    logging.info(f'Columns to drop: {cols_to_drop}')
    df = df_labeled.drop(columns=cols_to_drop)
    logging.info(f'Columns after dropping: {df.columns}')

    # # Apply the Elbow Method if enabled in the configuration
    if config['modelling_clustering']['elbow_enabled']:
        max_clusters = config['modelling_clustering']['max_clusters']
        # print('max_clusters', max_clusters, type(max_clusters))
        _elbow_method(df, max_clusters)


    # Apply K-Modes clustering if enabled in the configuration
    if config['modelling_clustering']['prediction_enabled']:
        n_clusters = config['modelling_clustering']['n_clusters']
        kmodes = KModes(n_clusters=n_clusters, init='Huang', n_init=10, verbose=1)

        model_pkl_file = config['modelling_clustering']['model_pkl_file']

        # Save the trained K-Modes model to a pickle file
        with open(model_pkl_file, 'wb') as file:
            pickle.dump(kmodes, file)

        # Perform clustering and add the cluster labels to the DataFrame
        df = _kmodes_clustering(kmodes, df)
        # Add the cluster labels to the labeled DataFrame
        df_labeled['cluster'] = df['cluster']

    return df_labeled, df