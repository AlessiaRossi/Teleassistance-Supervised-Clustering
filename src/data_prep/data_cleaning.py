import pandas as pd
import numpy as np
import logging

def imputate_comune_residenza(df:pd.DataFrame) -> pd.DataFrame:
    '''
        Imputes missing values for 'comune_residenza' using ISTAT codes.

        Parameters:
        - df: The DataFrame containing the data.

        Returns:
        - The DataFrame with imputed values.
    '''

    logging.info('Imputate comune residenza...')

    # Load ISTAT data to map the municipality code to the municipality name
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


def fill_missing_comune_residenza(df:pd.DataFrame, codice_comune_to_nome:pd.Series) -> pd.DataFrame:
      '''
        Fills missing values in the 'comune_residenza' column using a mapping.
        
        Args:
        - df: The DataFrame containing the data.
        - codice_comune_to_nome: A dictionary mapping the municipality code to the municipality name.
        
        Returns:
        - The DataFrame with filled missing values.
      '''
    
      # Handle the special case: municipality of None (Turin)
      df['codice_comune_residenza'] = df['codice_comune_residenza'].replace('1168', 'None')
    
      # Fill missing values using the mapping
      df['comune_residenza'] = df['comune_residenza'].fillna(df['codice_comune_residenza'].map(codice_comune_to_nome))

      return df

def remove_comune_residenza(df:pd.DataFrame) -> pd.DataFrame:
    '''
        Removes rows where 'comune_residenza' is missing.

        Args:
        - df: The DataFrame containing the data.

        Returns:
        - The DataFrame with removed rows.
    '''

    logging.info('Removing rows where \'comune_residenza\' is missing...')
    logging.info(f'Number of comune_residenza samples nulls: {df["comune_residenza"].isnull().value_counts()}')

    df = df.dropna(subset=['comune_residenza'])
    return df

# NOT USED 
def impute_ora_inizio_and_fine_erogazione(df:pd.DataFrame) -> pd.DataFrame:
    '''
        Imputes missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione' using the mean duration of the activity.

        Args:
        - df: The DataFrame containing the data.

        Returns:
        - The DataFrame with imputed values
    '''


    # Convert 'ora_inizio_erogazione' and 'ora_fine_erogazione' to datetime
    df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], utc=True, errors='coerce')
    df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], utc=True, errors='coerce')

    # Calculate the mean duration of the activity
    df_non_missing_values = df.dropna(subset=['ora_inizio_erogazione', 'ora_fine_erogazione']).copy()
    df_non_missing_values['duration'] = (df['ora_fine_erogazione'] - df['ora_inizio_erogazione']).dt.total_seconds()

    mean_duration_by_attivita = df_non_missing_values.groupby('codice_descrizione_attivita')['duration'].mean()
    mean_duration = pd.to_timedelta(mean_duration_by_attivita, unit='s')
    # print(mean_duration_by_attivita)

    # Convert series to dictionary
    mean_duration_dict = mean_duration.to_dict()
    # return mean_duration_dict

    # Imputate missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione'
    for index, row in df.iterrows():
        if pd.isnull(row['ora_inizio_erogazione']) and pd.isnull(row['ora_fine_erogazione']) and pd.isnull(row['data_disdetta']):
            codice_attivita = row['codice_descrizione_attivita']
            
            if codice_attivita in mean_duration_dict:
                durata_media = mean_duration_dict[codice_attivita]
                data_erogazione = pd.to_datetime(row['data_erogazione'], utc=True)
                df.at[index, 'ora_inizio_erogazione'] = data_erogazione.strftime('%Y-%m-%d %H:%M:%S%z')
                df.at[index, 'ora_fine_erogazione'] = (data_erogazione + durata_media).strftime('%Y-%m-%d %H:%M:%S%z')

    return df
        


def remove_disdette(df:pd.DataFrame) -> pd.DataFrame: 
    '''
        Removes rows where 'data_disdetta' is not null.

        Parameters:
        - df: The DataFrame containing the data.
        
        Returns:
        - The DataFrame with removed rows.
    '''


    logging.info('Removing rows where \'data_disdetta\' is not null...')
    logging.info(f'Number of data_disdetta samples nulls: {df["data_disdetta"].isnull().value_counts()}')

    # Remove rows where 'data_disdetta' is not null
    df = df[df['data_disdetta'].isnull()]
    # # Drop columns with more than 50% missing values
    # df = df.loc[:, df.isnull().mean() < 0.5]

    return df



def identify_and_remove_outliers_boxplot(df:pd.DataFrame, columns:list, threshold:float=3) -> pd.DataFrame:
    '''
        This function identifies and removes outliers using the boxplot method.    
    
        Parameters:
        - df: The DataFrame containing the data.
        - columns: The columns on which to identify and remove outliers.
        - threshold: The threshold for identifying outliers.
        
        Returns:
        - The DataFrame with removed outliers.
    '''

    # for col in columns:
    #     z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
    #     print(z_scores)
    #     print('Number of outliers in {}: {}'.format(col, len(z_scores[z_scores > threshold])))
    #     df = df[z_scores <= threshold]
    # return df

    logging.info('Identifying and removing outliers using the boxplot method...')

    # Identify and remove outliers using the boxplot method for each column
    for column in columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        # print('lower_bound:', lower_bound)
        # print('upper_bound:', upper_bound)
        df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

        logging.info(f'Number of outliers in {column}: {len((df[column] >= lower_bound) & (df[column] <= upper_bound))}')

    return df


def smooth_noisy_data(df:pd.DataFrame, column:str, window_size:int=3) -> pd.DataFrame:
    '''
        This function smooths noisy data using a moving average.

        Args:
        - df: The DataFrame containing the data.
        - column: The column to smooth.
        - window_size: The window size for the moving average.
        
        Returns:
        - The DataFrame with smoothed data.
    '''

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
    '''
        This function removes duplicates from the dataset.

        Parameters:
        - df: DataFrame containing the data.

        Returns:
        - DataFrame with duplicates removed.
    '''


    logging.info('Removing duplicates...')
    logging.info(f'Number of duplicates removed: {df.duplicated().sum()}')
    df.drop_duplicates(inplace=True)

    return df


def impute_durata_erogazione(df:pd.DataFrame) -> pd.DataFrame:
    '''
        This function imputes missing values for 'durata_erogazione' using the mean duration of the activity.

        Parameters:
        - df: DataFrame containing the data.

        Returns:
        - DataFrame with imputed values.
    '''

    logging.info('Imputating durata_erogazione...')


    # Convert 'ora_inizio_erogazione' and 'ora_fine_erogazione' to datetime
    df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], utc=True, errors='coerce')
    df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], utc=True, errors='coerce')

    # Imputate missing values for 'durata_erogazione' using the mean duration of the activity 
    df['durata_erogazione_sec'] = df.groupby('codice_descrizione_attivita')['durata_erogazione_sec'].transform(lambda x: x.fillna(x.mean()))

    return df

def missing_values(df:pd.DataFrame, missing_threshold) -> pd.DataFrame:
    '''
        This function drops columns with more than 60% missing values, except for 'data_disdetta'.

        Parameters:
        - df: DataFrame containing the data.

        Returns:
        - DataFrame with dropped columns.
    '''

    logging.info('Missing Values...')

    escluded_column = 'data_disdetta'
    data_disdetta = df[escluded_column]

    df_filtered = df.loc[:, df.columns != escluded_column] # Create a copy of the DataFrame without 'data_disdetta'
    df_filtered = df_filtered.loc[:, df_filtered.isnull().mean() < missing_threshold] # Drop columns with more than 60% missing values
    df_filtered[escluded_column] = data_disdetta # Add 'data_disdetta' back to the DataFrame

    logging.info(f'Cols dropped after missing_values with threshold: {df.shape[1] - df_filtered.shape[1]}')

    return df_filtered




def data_cleaning_execution(df:pd.DataFrame, missing_threshold:float, config:dict) -> pd.DataFrame:
    '''
        Executes the data cleaning process based on the provided configuration.

        This function performs data cleaning operations such as imputing missing values, removing duplicates, and identifying outliers.

        Parameters:
        - df: DataFrame containing the data to be cleaned.
        - missing_threshold: The threshold for missing values.
        - config: Dictionary containing configuration settings for the data cleaning process.

        Returns:
        - DataFrame with cleaned data.
    '''
    

    logging.basicConfig(filename=config['general']['logging_level'], format='%(asctime)s - %(message)s', level=logging.INFO)

    # Drop columns with more than 60% missing values
    df = missing_values(df, missing_threshold)

    # Apply the function to imputate missing values for 'comune_residenza'
    df, codice_comune_to_nome = imputate_comune_residenza(df)

    # Fill missing values for 'comune_residenza' using a mapping
    df = fill_missing_comune_residenza(df, codice_comune_to_nome) 

    df = remove_comune_residenza(df)

    # Impute missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione'
    # NOTE: DEPRECATED
    # df = impute_ora_inizio_and_fine_erogazione(df)  

    # Remove rows where 'data_disdetta' is not null
    df = remove_disdette(df)

    # Identify and remove outliers using the z-score method
    # NOTE: DEPRECATED
    # df = identify_and_remove_outliers_boxplot(df, ['ora_inizio_erogazione', 'ora_fine_erogazione'])

    # Smooth noisy data using moving average
    # NOTE: DEPRECATED
    # df = smooth_noisy_data(df, 'ora_inizio_erogazione')

    # Remove duplicates from the dataset
    df = remove_duplicates(df)

    return df
