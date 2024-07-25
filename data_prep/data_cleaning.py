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

def check_missing_values_same_row(df):
    """
    Checks whether the missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione' are at the same rows.
    :param df:
    :return:
    """
    missing_both = df['ora_inizio_erogazione'].isna() & df['ora_fine_erogazione'].isna()
    rows_with_both_missing = df[missing_both]
    num_rows_with_both_missing = len(rows_with_both_missing)
    print(f"Number of rows with 'ora_inizio_erogazione' and 'ora_fine_erogazione' missing: {num_rows_with_both_missing}")

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

def check_missing_values_end(df):
    """
    Check for missing values for 'ora_fine_erogazione'.
    :param df:
    :return:
    """
    missing_end = df['ora_fine_erogazione'].isna()
    rows_with_end_missing = df[missing_end]
    num_rows_with_end_missing = len(rows_with_end_missing)
    print(f"Number of rows with 'ora_fine_erogazione' missing: {num_rows_with_end_missing}")

def imputate_ora_inizio_erogazione_and_ora_fine_erogazione(df) -> pd.DataFrame:
    """
    Imputes missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione' of dataset df.
    :param df:
    :return:
    """
    # Check if the missing values are related to the same rows in the dataset:
    check_missing_values_same_row(df)

    # Conversion of 'ora_inizio_erogazione' and 'ora_fine_erogazione' columns to datetime format.
    df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], errors='coerce', utc=True)
    df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], errors='coerce', utc=True)

    # Calculation of average task duration for each 'codice_descrizione_attivita'
    df_non_missing = df.dropna(subset=['ora_inizio_erogazione', 'ora_fine_erogazione']).copy()
    df_non_missing['durata'] = (
            df_non_missing['ora_fine_erogazione'] - df_non_missing['ora_inizio_erogazione']).dt.total_seconds()
    media_durata_sec = df_non_missing.groupby('codice_descrizione_attivita')['durata'].mean()
    media_durata = pd.to_timedelta(media_durata_sec, unit='s')

    # Convert the resulting Series to a dictionary.
    media_durata_dict = media_durata.to_dict()

    # Iterates through each row of the original DataFrame and imputes the missing values for 'ora_inizio_erogazione' and 'ora_fine_erogazione'
    for index, row in df.iterrows():
        if pd.isnull(row['ora_inizio_erogazione']) and pd.isnull(row['ora_fine_erogazione']) and pd.isnull(
                row['data_disdetta']):
            codice_attivita = row['codice_descrizione_attivita']
            if codice_attivita in media_durata_dict:
                durata_media = media_durata_dict[codice_attivita]
                data_erogazione = pd.to_datetime(row['data_erogazione'], utc=True)
                df.at[index, 'ora_inizio_erogazione'] = data_erogazione.strftime('%Y-%m-%d %H:%M:%S%z')
                df.at[index, 'ora_fine_erogazione'] = (data_erogazione + durata_media).strftime('%Y-%m-%d %H:%M:%S%z')

    check_missing_values_start(df)
    check_missing_values_end(df)

    return df

def imputate_missing_values(df) -> pd.DataFrame:
    """
    Impute missing values from the df dataset. After an initial analysis, the following results are obtained:
    Statistics missing values before imputation:

    codice_provincia_residenza      28380
    comune_residenza                  135
    codice_provincia_erogazione     28776
    ora_inizio_erogazione           28181
    ora_fine_erogazione             28181
    data_disdetta                  460639

    'codice_provincia_residenza' and 'codice_provincia_erogazione' are not imputed as they will be removed
    later. In addition, 'data_disdetta' is also not imputed. The imputation done for 'comune_residenza' does not
    produces results because the missing values are related to the municipality of 'None', which is why we cannot
    speak of missing values. 'ora_inizio_erogazione' and 'ora_fine_erogazione' are imputed correctly.
    :param df:
    :return:
    """
    # Display statistics of missing values before imputation.
    print("Statistics missing values before imputation:\n")
    colonne_con_mancanti = df.columns[df.isnull().any()]
    print(df[colonne_con_mancanti].isnull().sum())
    print('-----------------------------------')

    # Imputation of missing values related to 'comune_residenza'
    df = imputate_comune_residenza(df)

    # Imputation of missing values related to 'ora_inizio_erogazione' and 'ora_fine_erogazione'
    df = imputate_ora_inizio_erogazione_and_ora_fine_erogazione(df)

    # Display statistics of missing values after imputation
    print("Statistics missing values after imputation:\n")
    colonne_con_mancanti = df.columns[df.isnull().any()]
    print(df[colonne_con_mancanti].isnull().sum())
    print('-----------------------------------')

    return df

