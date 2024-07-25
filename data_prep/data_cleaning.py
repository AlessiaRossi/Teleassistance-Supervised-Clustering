import pandas as pd

def remove_disdette(df) -> pd.DataFrame:
    """
    Rimuove i campioni con 'data_disdetta' non nullo.
    :param df:
    :return: df senza campioni con 'data_disdetta' non nullo.
    """
    df = df[df['data_disdetta'].isnull()]
    return df