import pandas as pd

def remove_disdette(df) -> pd.DataFrame:
    """
    Removes samples with non-zero 'data_disdetta'.
    :param df:
    :return: df without samples with non-zero 'data_disdetta'.
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

def remove_duplicati(df) -> pd.DataFrame:
    """
    Removes duplicates from dataset df.
    :param df:
    :return:
    """
    df.drop_duplicates(inplace=True)
    return df

def imputate_comune_residenza(df) -> pd.DataFrame:
    """
       Impute missing values for 'comune_residenza' from dataset df.
       :param df:
       :return:
    """
    # Load the dataset related to the ISTAT codes of Italian municipalities so that I can make imputation
    df_istat = pd.read_excel('datasets/Codici-statistici-e-denominazioni-al-30_06_2024.xlsx')

    codice_comune_to_nome = pd.Series(df_istat['Denominazione in italiano'].values,
                                      index=df_istat['Codice Comune formato alfanumerico'])

    def fill_missing_comune_residenza(row):
        if row['comune_residenza'] is None:
            return codice_comune_to_nome.get(row['codice_comune_residenza'])
        return row['comune_residenza']

    df['comune_residenza'] = df.apply(fill_missing_comune_residenza, axis=1)

    '''
    # N.B. After imputation, missing values related to comune_residenza continue to be missing 
    as they relate to the municipality of None in the province of Turin with ISTAT code 1168.
    '''

    return df

def check_missing_values_start(df):
    """
    Checks for missing values for 'ora_inizio_erogazione'.
    :param df:
    :return:
    """
    missing_start = df['ora_inizio_erogazione'].isna()
    rows_with_start_missing = df[missing_start]
    num_rows_with_start_missing = len(rows_with_start_missing)
    print(f"Number of rows with 'ora_inizio_erogazione' missing: {num_rows_with_start_missing}")