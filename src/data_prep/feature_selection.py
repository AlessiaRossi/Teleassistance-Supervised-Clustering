import pandas as pd
from src.data_prep.data_cleaning import identify_and_remove_outliers_boxplot, impute_durata_erogazione
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt


# List of tuples containing the code-description column pairs to be compared.
columns_pairs = [
    ('codice_provincia_residenza', 'provincia_residenza'),
    ('codice_provincia_erogazione', 'provincia_erogazione'),
    ('codice_regione_residenza', 'regione_residenza'),
    ('codice_asl_residenza', 'asl_residenza'),
    ('codice_comune_residenza', 'comune_residenza'),
    ('codice_descrizione_attivita', 'descrizione_attivita'),
    ('codice_regione_erogazione', 'regione_erogazione'),
    ('codice_asl_erogazione', 'asl_erogazione'),
    ('codice_struttura_erogazione', 'struttura_erogazione'),
    ('codice_tipologia_struttura_erogazione', 'tipologia_struttura_erogazione'),
    ('codice_tipologia_professionista_sanitario', 'tipologia_professionista_sanitario')
]


def print_details_corrections (df, code, description, code_groups, description_groups):
    '''
        This function prints details if there are codes with multiple descriptions or vice versa

        Args:
            df: DataFrame to operate on
            code: Code column to analyze
            description: Description column to be parsed
            code_groups: Code groups with unique description counts
            description_groups: Groups of descriptions with unique code counts
        
        Returns:
            None
    '''


    not_unique = False

    for cod, desc_count in code_groups.items():
        if desc_count > 1:
            associated_descriptions = df[df[code] == cod][description].unique()
            print(f"The {cod} code is associated with {desc_count} descriptions: {associated_descriptions}")
            not_unique = True
            
    for desc, code_count in description_groups.items():
        if code_count > 1:
            associated_codes =df[df[description] == desc][code].unique()
            print(f"The {desc} description is associated with {code_count} codes: {associated_codes}")
            not_unique = True

    if not_unique:
        print(f"--> NOT unique correlation between {code} and {description}\n")



def remove_columns_with_unique_correlation(df, columns_pairs) -> pd.DataFrame:
    '''
    This function removes columns (column code) with unique correlation

    Args:
        df: The DataFrame containing the data.
        columns_pairs: List of tuples containing the code-description column pairs to be compared.

    Returns:
        The DataFrame with removed columns
    '''

    pairs_removed = []

    for code, description in columns_pairs:
        if code in df.columns and description in df.columns:
            code_groups = df.groupby(code)[description].nunique()
            description_groups = df.groupby(description)[code].nunique()

            print_details_corrections(df, code, description, code_groups, description_groups)

            unique_correlation_code_description = all(code_groups <= 1)
            unique_correlation_description_code = all(description_groups <= 1)

            if unique_correlation_code_description and unique_correlation_description_code:
                df.drop(columns=[code], inplace=True)
                print(f'Unique correlation between {code} and {description}. Column {code} removed.')
                pairs_removed.append((code, description))
        else:
            print(f'Columns {code} or {description} not found in the dataframe.')
            pairs_removed.append((code, description))

    # Update the list of columns pairs removing the ones that have been removed
    columns_pairs_updated = [pair for pair in columns_pairs if pair not in pairs_removed]
    return df, columns_pairs_updated

            
def clean_codice_struttura_erogazione(df, column = 'codice_struttura_erogazione'):
    '''
    This function cleans the 'codice_struttura_erogazione' column by converting it to an integer type
    '''

    df[column] = df[column].astype(int)
    return df


def remove_data_disdetta(df) -> pd.DataFrame:
    '''
    This function remove data_disdetta column from the DataFrame
    '''

    df.drop(columns=['data_disdetta'], inplace=True)
    return df


def colonna_durata_erogazione(df:pd.DataFrame) -> pd.DataFrame:
    '''
    This function creates a new column 'durata_erogazione' which is the difference between 'ora_fine_erogazione' and 'ora_inizio_erogazione'
    '''
    # Convert 'ora_inizio_erogazione' and 'ora_fine_erogazione' to datetime
    df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], utc=True, errors='coerce')
    df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], utc=True, errors='coerce')

    df['durata_erogazione_sec'] = (df['ora_fine_erogazione'] - df['ora_inizio_erogazione']).dt.total_seconds()
    
    return df


def remove_ora_inizio_fine_erogazione(df:pd.DataFrame) -> pd.DataFrame:
    '''
    This function removes 'ora_inizio_erogazione' and 'ora_fine_erogazione' columns from the DataFrame
    '''

    df.drop(columns=['ora_inizio_erogazione', 'ora_fine_erogazione'], inplace=True)
    return df


def colonna_eta(df:pd.DataFrame) -> pd.DataFrame:
    '''
    This function creates a new column 'eta' which is the difference between 'ora_fine_erogazione' and 'ora_inizio_erogazione'
    '''

    df['data_nascita'] = pd.to_datetime(df['data_nascita'], utc=True, errors='coerce')
    
    df['eta'] = (pd.to_datetime('today', utc=True) - df['data_nascita']).dt.days // 365
    return df

def colonne_anno_e_quadrimestre(df:pd.DataFrame) -> pd.DataFrame:    
    df['data_erogazione'] = pd.to_datetime(df['data_erogazione'], utc=True, errors='coerce')
    df['anno'] = df['data_erogazione'].dt.year
    df['quadrimestre'] = df['data_erogazione'].dt.quarter

    return df

def cramer_v(x, y):
    '''
    This function calculates Cramér's V for two categorical variables.

    Args:
        x: First categorical variable.
        y: Second categorical variable.

    Returns:
        Cramér's V statistic.
    '''
    # Create a contingency table
    contingency = pd.crosstab(x, y)

    # Calculate the chi-square test statistic and other values
    chi2, _, _, _ = chi2_contingency(contingency)
    n = contingency.sum().sum()
    min_dim = min(contingency.shape) - 1

    # Calculate Cramér's V
    return np.sqrt(chi2 / (n * min_dim))

def calculate_correlation_matrix(df, corr_cols):
    '''
    This function calculates the correlation matrix using Cramér's V.

    Args:
        df: DataFrame containing the data.
        corr_cols: List of columns to calculate the correlation matrix for.

    Returns:
        DataFrame containing the correlation matrix.
    '''
    correlations = pd.DataFrame(index=corr_cols, columns=corr_cols)
    for col1 in corr_cols:
        for col2 in corr_cols:
            if col1 != col2:
                correlations.loc[col1, col2] = cramer_v(df[col1], df[col2])
            else:
                correlations.loc[col1, col2] = 1.0  # Perfect correlation with itself
    return correlations


def visualize_correlation_matrix(correlations):
    '''
    This function visualizes the correlation matrix using a heatmap.

    Args:
        correlations: DataFrame containing the correlation matrix.

    Returns:
        None
    '''
    plt.figure(figsize=(16, 12))
    sns.heatmap(correlations.astype(float), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, square=True)

    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    plt.show()


def remove_highly_correlated_columns(df, columns_to_remove):
    '''
    This function removes columns based on the correlation analysis.

    Args:
        df: DataFrame containing the data.
        columns_to_remove: List of columns to be removed.

    Returns:
        DataFrame with the specified columns removed.
    '''

    df.drop(columns=columns_to_remove, inplace=True)
    return df



# TODO: decidere se eliminare la feature struttura_erogazione con il dato sbagliato 'PRESIDIO OSPEDALIERO UNIFICATO' e usarlo nel post-processing o se gestirlo prima.
# Modifichiamo PRESIDIO OSPEDALIERO UNIFICATO con le relative provincie e rimuoviamo la colonna codice_struttura_erogazione

# 11/08/2024
# DONE - TODO: aggiungere colonna eta
# DONE - TODO: rimuovere colonne ora inizio e fine erogazione e aggiungere durata
# DONE - TODO: imputare in valori mancanti in durata erogazione con la media della durata per attività
def feature_selection_execution(df:pd.DataFrame) -> pd.DataFrame:
    '''
    This function executes the feature selection process

    Args:
        df: The DataFrame containing the data.

    Returns:
        The DataFrame with removed columns
    '''

    global columns_pairs


    # Clean 'codice_struttura_erogazione' column
    df = clean_codice_struttura_erogazione(df)

    # Remove 'data_disdetta' column cause all the data is null
    df = remove_data_disdetta(df)

    # Create 'durata_erogazione' column, and remove outliers
    df = colonna_durata_erogazione(df)
    df = impute_durata_erogazione(df)
    df = identify_and_remove_outliers_boxplot(df, ['durata_erogazione_sec'])
    df = remove_ora_inizio_fine_erogazione(df)

    # Remove code columns with unique correlation
    df, columns_pairs = remove_columns_with_unique_correlation(df, columns_pairs)

    # Create 'eta' column
    df = colonna_eta(df)
    df = colonne_anno_e_quadrimestre(df)


    ''' 
        Remove highly correlated columns 
    '''
    # Calculate the correlation matrix
    corr_cols = [
        'sesso', 'regione_residenza', 'asl_residenza', 'provincia_residenza', 'comune_residenza',
        'descrizione_attivita', 'regione_erogazione', 'asl_erogazione', 'provincia_erogazione',
        'struttura_erogazione', 'tipologia_struttura_erogazione', 'tipologia_professionista_sanitario', 'eta'
    ]

    correlations = calculate_correlation_matrix(df, corr_cols)
    visualize_correlation_matrix(correlations)

    # Remove highly correlated columns
    columns_to_remove = [
            'comune_residenza', 'asl_residenza', 'provincia_residenza', 'regione_erogazione', 'asl_erogazione', 'provincia_erogazione', 'struttura_erogazione'
    ]
    # Remove the highly correlated columns
    df = remove_highly_correlated_columns(df, columns_to_remove)

    # Update the list of columns pairs removing the ones that have been removed
    new_corr_cols = ['sesso', 
        'regione_residenza', 
        # 'asl_residenza', 
        # 'provincia_residenza',
        # 'comune_residenza',
        'descrizione_attivita',
        # 'regione_erogazione',
        # 'asl_erogazione',
        # 'provincia_erogazione',
        # 'struttura_erogazione',
        'tipologia_struttura_erogazione',
        'tipologia_professionista_sanitario',
        'eta']
    
    # Calculate the correlation matrix
    correlations = calculate_correlation_matrix(df, new_corr_cols)
    visualize_correlation_matrix(correlations)

    '''
        End of remove highly correlated columns
    '''

    # Save the DataFrame to a parquet file
    df.to_parquet('data/processed/feature_selected_data.parquet')
   
    return df