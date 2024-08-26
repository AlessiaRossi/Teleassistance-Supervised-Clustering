import pandas as pd
import numpy as np
from collections import Counter
import logging
from sklearn.metrics import silhouette_samples
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


def purity_score(y_true, y_pred):
    """Calculate the purity score."""
    
    N = len(y_true) # number of data points
    purity_sum = 0

    for cluster_id in np.unique(y_pred):
        # Obtain the indices of data points in the cluster
        #print(cluster_id)

        cluster_indices = np.where(y_pred == cluster_id)[0] # [0] to get the array from the tuple, as np.where returns a tuple
        # print('Cluster indices:', cluster_indices)

        # Obtain the true labels of data points in the cluster
        cluster_labels = y_true[cluster_indices]
        # print('Cluster labels', cluster_labels)

        # Count the number of data points in each class
        most_common_label, count = Counter(cluster_labels).most_common(1)[0] # most_common returns a list of tuples, we take the first one
        # print(f'Most common label: {most_common_label}, count: {count}')

        purity_sum += count

    purity = purity_sum / N
    return purity


def silhouette_score(X, y):
    pass


def metrics_execution(df:pd.DataFrame, config:dict) -> None:
    """Execution of metrics calculation."""
    
    purity_score = purity_score(df['incremento_teleassistenze'], df['cluster'])
    logging.info(f'Purity score: {purity_score}')

    pass