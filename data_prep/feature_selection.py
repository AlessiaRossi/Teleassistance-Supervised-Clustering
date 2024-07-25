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
