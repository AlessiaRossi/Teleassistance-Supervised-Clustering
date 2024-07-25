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

def smooth_noisy_data(df, column, window_size=3):
    """
    Smooth noisy data using moving average.
    :param df: The original DataFrame.
    :param column: The column on which to apply smoothing.
    :param window_size: The window size for the moving average.
    :return: A DataFrame with the smoothed data.
    """
    if pd.api.types.is_datetime64_any_dtype(df[column]):
        # Convert datetime to timestamp
        df[column] = df[column].apply(lambda x: x.timestamp() if pd.notnull(x) else x)
        # Apply rolling mean
        df[column] = df[column].rolling(window=window_size, min_periods=1).mean()
        # Convert timestamp back to datetime
        df[column] = pd.to_datetime(df[column], unit='s', utc=True)
    else:
        df[column] = df[column].rolling(window=window_size, min_periods=1).mean()

    return df