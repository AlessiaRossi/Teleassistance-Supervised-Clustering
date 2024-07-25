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
    for cod, num_desc in gruppi_codice.items():
        if num_desc > 1:
            descrizioni_associate = df[df[codice] == cod][descrizione].unique()
            print(f"The {cod} code is associated with {num_desc} descriptions:: {descrizioni_associate}")

    for desc, num_cod in gruppi_descrizione.items():
        if num_cod > 1:
            codici_associati = df[df[descrizione] == desc][codice].unique()
            print(f"The description '{desc}' is associated with {num_cod} codes: {codici_associati}")

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
                print(f"Correlazione univoca tra {codice} e {descrizione}:\nrimossa colonna {codice}.\n")
                coppie_rimosse.append((codice, descrizione))
        else:
            print(f"Impossibile trovare le colonne {codice} o {descrizione} nel DataFrame.")
            coppie_rimosse.append((codice, descrizione))

    # Update coppie_colonne by removing processed pairs.
    coppie_colonne_aggiornate = [coppia for coppia in coppie_colonne if coppia not in coppie_rimosse]

    return df, coppie_colonne_aggiornate
