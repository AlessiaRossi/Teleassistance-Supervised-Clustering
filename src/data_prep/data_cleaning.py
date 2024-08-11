import pandas as pd
import numpy as np

def imputate_comune_residenza(df):
    """
    Imputes missing values for 'comune_residenza' using ISTAT codes.

    Args:
        df: The DataFrame containing the data.

    Returns:
        The DataFrame with imputed values.
    """

    # Load ISTAT data
    istat_data = pd.read_excel('data/raw/Codici-statistici-e-denominazioni-al-30_06_2024.xlsx')
    
    # Create the mapping dictionary
    codice_comune_to_nome = pd.Series(istat_data['Denominazione in italiano'].values,
                                      index=istat_data['Codice Comune formato alfanumerico'])


    # Merge DataFrames on 'codice_comune_residenza'
    #df = pd.merge(df, istat_data, left_on='codice_comune_residenza', right_on='Codice Comune formato alfanumerico', how='left')

    df['comune_residenza'].fillna(df['codice_comune_residenza'].map(codice_comune_to_nome), inplace=True)

    # df.drop('comune_residenza', axis=1, inplace=True)

    # Rename the column and remove the excess column (if necessary)
    #df.rename(columns={'Denominazione in italiano': 'comune_residenza'}, inplace=True)
    #df.drop('Codice Comune formato alfanumerico', axis=1, inplace=True)
    
    return df, codice_comune_to_nome



def fill_missing_comune_residenza(df, codice_comune_to_nome) -> pd.DataFrame:
      """
      Fills missing values in the 'comune_residenza' column using a mapping.
    
      Args:
        df: The DataFrame containing the data.
        codice_comune_to_nome: A dictionary mapping the municipality code to the municipality name.
    
      Returns:
        The DataFrame with filled missing values.
      """
    
      # Handle the special case: municipality of None (Turin)
      df['codice_comune_residenza'] = df['codice_comune_residenza'].replace('1168', 'None')
    
      # Fill missing values using the mapping
      df['comune_residenza'] = df['comune_residenza'].fillna(df['codice_comune_residenza'].map(codice_comune_to_nome))

      return df


# NOT USED
def impute_ora_inizio_and_fine_erogazione(df:pd.DataFrame) -> pd.DataFrame:
    """
    Imputes missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione' using the mean duration of the activity.

    Args:
        df: The DataFrame containing the data.

    Returns:
        The DataFrame with imputed values
    """


    # Convert 'ora_inizio_erogazione' and 'ora_fine_erogazione' to datetime
    df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], utc=True, errors='coerce')
    df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], utc=True, errors='coerce')

    df_non_missing_values = df.dropna(subset=['ora_inizio_erogazione', 'ora_fine_erogazione']).copy()
    df_non_missing_values['duration'] = (df['ora_fine_erogazione'] - df['ora_inizio_erogazione']).dt.total_seconds()

    mean_duration_by_attivita = df_non_missing_values.groupby('codice_descrizione_attivita')['duration'].mean()
    mean_duration = pd.to_timedelta(mean_duration_by_attivita, unit='s')
    # print(mean_duration_by_attivita)

    # Convert series to dictionary
    mean_duration_dict = mean_duration.to_dict()
    # return mean_duration_dict


    for index, row in df.iterrows():
        if pd.isnull(row['ora_inizio_erogazione']) and pd.isnull(row['ora_fine_erogazione']) and pd.isnull(row['data_disdetta']):
            codice_attivita = row['codice_descrizione_attivita']
            
            if codice_attivita in mean_duration_dict:
                durata_media = mean_duration_dict[codice_attivita]
                data_erogazione = pd.to_datetime(row['data_erogazione'], utc=True)
                df.at[index, 'ora_inizio_erogazione'] = data_erogazione.strftime('%Y-%m-%d %H:%M:%S%z')
                df.at[index, 'ora_fine_erogazione'] = (data_erogazione + durata_media).strftime('%Y-%m-%d %H:%M:%S%z')

    return df
        



def remove_disdette(df) -> pd.DataFrame: 
    # Remove rows where 'data_disdetta' is not null
    df = df[df['data_disdetta'].isnull()]
    # # Drop columns with more than 50% missing values
    # df = df.loc[:, df.isnull().mean() < 0.5]
    return df



def identify_and_remove_outliers_boxplot(df, columns, threshold=3):
    """
    Identifies and removes outliers using the z-score method (normalization).
    
    :param df: The original DataFrame.
    :param columns: The columns on which to apply outliers removal.
    :param threshold: The z-score threshold for outlier detection (default: 3).
    :return: A DataFrame with no outliers.
    """
    # for col in columns:
    #     z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
    #     print(z_scores)
    #     print('Number of outliers in {}: {}'.format(col, len(z_scores[z_scores > threshold])))
    #     df = df[z_scores <= threshold]
    # return df


    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        print('lower_bound:', lower_bound)
        print('upper_bound:', upper_bound)
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df


# NOT USED
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


def remove_duplicates(df:pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicates from dataset df.
    :param df:
    :return:
    """
    df.drop_duplicates(inplace=True)
    return df


def impute_durata_erogazione(df:pd.DataFrame) -> pd.DataFrame:
    '''
    Imputes missing values for 'durata_erogazione' using the mean duration of the activity.
    '''


    # Convert 'ora_inizio_erogazione' and 'ora_fine_erogazione' to datetime
    df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], utc=True, errors='coerce')
    df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], utc=True, errors='coerce')

    # Imputate missing values for 'durata_erogazione' using the mean duration of the activity 
    df['durata_erogazione_min'] = df.groupby('codice_descrizione_attivita')['durata_erogazione_min'].transform(lambda x: x.fillna(x.mean()))

    return df



def data_cleaning_execution(df:pd.DataFrame) -> pd.DataFrame:
    # Apply the function to imputate missing values for 'comune_residenza'
    df, codice_comune_to_nome = imputate_comune_residenza(df)

    # Fill missing values for 'comune_residenza' using a mapping
    df = fill_missing_comune_residenza(df, codice_comune_to_nome) 

    # Impute missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione'
    # DISABLED
    # df = impute_ora_inizio_and_fine_erogazione(df)  

    # Remove rows where 'data_disdetta' is not null
    df = remove_disdette(df)

    # Identify and remove outliers using the z-score method
    #df = identify_and_remove_outliers_boxplot(df, ['ora_inizio_erogazione', 'ora_fine_erogazione'])

    # Smooth noisy data using moving average
    # DISABLED
    #df = smooth_noisy_data(df, 'ora_inizio_erogazione')

    # Remove duplicates from the dataset
    df = remove_duplicates(df)

    df.to_parquet('data/processed/challenge_campus_biomedico_2024_cleaned.parquet', index=False)

    return df
