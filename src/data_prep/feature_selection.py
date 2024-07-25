import pandas as pd

# List of tuples containing the code-description column pairs to be compared.
coppie_colonne = [
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

def print_details_corrections(df, codice, descrizione, gruppi_codice, gruppi_descrizione):
    '''
    Print details if there are codes with multiple descriptions or vice versa
    :param df: DataFrame to operate on
    :param codice: Code column to analyze
    :param descrizione: Description column to be parsed
    :param gruppi_codice: Code groups with unique description counts
    :param gruppi_descrizione: Groups of descriptions with unique code counts
    '''
    non_univoco = False

    for cod, num_desc in gruppi_codice.items():
        if num_desc > 1:
            descrizioni_associate = df[df[codice] == cod][descrizione].unique()
            print(f"The {cod} code is associated with {num_desc} descriptions: {descrizioni_associate}")
            non_univoco = True

    for desc, num_cod in gruppi_descrizione.items():
        if num_cod > 1:
            codici_associati = df[df[descrizione] == desc][codice].unique()
            print(f"The description '{desc}' is associated with {num_cod} codes: {codici_associati}")
            non_univoco = True

    if non_univoco:
        print(f"--> NOT unique correlation between {codice} and {descrizione}\n")


def remove_columns_with_unique_correlation(df, coppie_colonne) -> pd.DataFrame:
    '''
    Removes columns with unique correlation
    :param df:
    :return:
    '''
    coppie_rimosse = []
    for codice, descrizione in coppie_colonne:
        if codice in df.columns and descrizione in df.columns:
            gruppi_codice = df.groupby(codice)[descrizione].nunique()
            gruppi_descrizione = df.groupby(descrizione)[codice].nunique()


            print_details_corrections(df, codice, descrizione, gruppi_codice, gruppi_descrizione)

            correlazione_univoca_codice_descrizione = all(gruppi_codice <= 1)
            correlazione_univoca_descrizione_codice = all(gruppi_descrizione <= 1)

            if correlazione_univoca_codice_descrizione and correlazione_univoca_descrizione_codice:
                df.drop(columns=[codice], inplace=True)
                print(f"Unique correlation between {codice} and {descrizione}:\nremoved column {codice}.\n")
                coppie_rimosse.append((codice, descrizione))
        else:
            print(f"Cannot find the {codice} or {descrizione} in the DataFrame.")
            coppie_rimosse.append((codice, descrizione))

    # Update coppie_colonne by removing processed pairs.
    coppie_colonne_aggiornate = [coppia for coppia in coppie_colonne if coppia not in coppie_rimosse]

    return df, coppie_colonne_aggiornate

def remove_data_disdetta(df) -> pd.DataFrame:
    """
    Removes samples with non-zero 'data_disdetta'.
    :param df:
    :return: df without samples with non-zero 'data_disdetta'.
    """
    df.drop(columns=['data_disdetta'], inplace=True)
    return df

def clean_codice_struttura(df, colonna='codice_struttura_erogazione'):
    """
    Cleans the values in the specified column by removing everything following the period, if any.
    :param df: DataFrame to operate on
    :param colonna: Name of column to clean.
    :return: DataFrame with the values in the specified column cleaned
    """
    # Use a lambda function to divide the value based on the point and take the first element
    df[colonna] = df[colonna].apply(lambda x: str(x).split('.')[0])
    # df.to_csv('df_cod_strut_pulito.csv', index=False)
    return df


def feature_selection_execution(df) -> pd.DataFrame:
    '''
    Executes feature selection
    :param df:
    :return:
    '''
    global coppie_colonne
    df, coppie_colonne_aggiornate = remove_columns_with_unique_correlation(df, coppie_colonne)
    print("------------ cleanup feature code_structure finished ------------\n")
    df = remove_data_disdetta(df)
    return df