import pandas as pd
import numpy as np
from kmodes.kmodes import KModes
import matplotlib.pyplot as plt
import pickle
import logging


def _elbow_method(df:pd.DataFrame, max_clusters:int) -> None:
    """Elbow method to determine the optimal number of clusters."""
    
    cost = []
    K = range(1, max_clusters) # Number of clusters
    # print(K)
    print(df.head())

    for numero_cluster in K:
        print(numero_cluster)
        kmodes = KModes(n_clusters=numero_cluster, init='Huang', n_init=5, verbose=1)
        kmodes.fit_predict(df)
        cost.append(kmodes.cost_) # Cost of the model

    # Graph of the elbow method
    plt.plot(K, cost, 'bx-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Cost')
    plt.title('Elbow Method For Optimal k')
    plt.savefig('graphs/elbow_method.png')


def _kmodes_clustering(kmodes:KModes, df:pd.DataFrame) -> pd.DataFrame:
    """Clustering using the K-Modes algorithm."""
    clusters = kmodes.fit_predict(df)
    df['cluster'] = clusters

    return df


def clustering_execution(df_labeled:pd.DataFrame, config:dict) -> pd.DataFrame:

    logging.basicConfig(filename=config['general']['logging_level'], format='%(asctime)s - %(message)s', level=logging.INFO)

    list_cols_to_drop = config['modelling_clustering']['list_cols_to_drop']
    
    cols_to_drop = df_labeled.columns[list_cols_to_drop]
    logging.info(f'Columns to drop: {cols_to_drop}')
    df = df_labeled.drop(columns=cols_to_drop)
    logging.info(f'Columns after dropping: {df.columns}')

    # Elbow method
    if config['modelling_clustering']['elbow_enabled']:
        max_clusters = config['modelling_clustering']['max_clusters']
        # print('max_clusters', max_clusters, type(max_clusters))
        _elbow_method(df, max_clusters)


    # Clustering
    if config['modelling_clustering']['prediction_enabled']:
        n_clusters = config['modelling_clustering']['n_clusters']
        kmodes = KModes(n_clusters=n_clusters, init='Huang', n_init=10, verbose=1)

        model_pkl_file = config['modelling_clustering']['model_pkl_file']

        with open(model_pkl_file, 'wb') as file:
            pickle.dump(kmodes, file)


        df = _kmodes_clustering(kmodes, df)

        df_labeled['cluster'] = df['cluster']

    return df_labeled, df