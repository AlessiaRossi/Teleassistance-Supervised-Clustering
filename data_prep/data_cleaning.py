import pandas as pd

def remove_disdette(df) -> pd.DataFrame:
    """
    Removes samples with non-zero 'date_deadline'.
    :param df:
    :return: df without samples with non-zero 'date_date'.
    """
    df = df[df['data_disdetta'].isnull()]
    return df

def identify_and_remove_outliers(df, columns):
    """
    Identifies and removes outliers using the IQR method.
    :param df: The original DataFrame.
    :param columns: The columns on which to apply outliers removal.
    :return: A DataFrame with no outliers.
    """
    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df