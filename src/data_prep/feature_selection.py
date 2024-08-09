import pandas as pd

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