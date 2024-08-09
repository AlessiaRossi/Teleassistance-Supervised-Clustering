import pandas as pd
from src.data_prep.data_cleaning import data_cleaning_execution
from src.data_prep.feature_selection import feature_selection_execution

#from feature_extraction.feature_extraction import feature_extraction

# Loading the dataset
file_path = 'data/raw/challenge_campus_biomedico_2024.parquet'
df = pd.read_parquet(file_path)

# Displaying the number of rows and columns in the dataset
num_rows, num_columns = df.shape
print(f"The DataFrame has {num_rows} rows and {num_columns} columns.\n")

print('\nNULLS BEFORE DATA CLEANING\n', df.isnull().sum().sort_values(ascending=False))

# Data Cleaning
df = data_cleaning_execution(df)



print('\nNULLS AFTER DATA CLEANING\n', df.isnull().sum().sort_values(ascending=False))

'''
    NULLS BEFORE DATA CLEANING

    data_disdetta                                460639
    codice_provincia_erogazione                   28776
    codice_provincia_residenza                    28380
    ora_fine_erogazione                           28181
    ora_inizio_erogazione                         28181
    comune_residenza                                135
'''



# Features Selection
df = feature_selection_execution(df)

# Feature extraction
#df = feature_extraction(df)

#df.to_csv('data/raw/challenge_campus_biomedico_2024_imputed_selected_extracted.csv', index=False)

# Displaying the number of rows and columns in the dataset
num_rows, num_columns = df.shape
print(f"The DataFrame has {num_rows} rows and {num_columns} columns.")



'''
    Statistiche valori mancanti dopo l'imputazione:

    codice_provincia_residenza      28380
    comune_residenza                  135 --> da non toccare perché relativi al comune di None in provincia di Torino
    codice_provincia_erogazione     28776
    ora_inizio_erogazione           23652
    ora_fine_erogazione             23652
    data_disdetta                  460639
'''

# TODO: rimuovere colonne relative a 'codice_provincia_residenza' e 'codice_provincia_erogazione' in quanto non utili

# TODO: rimuovere tutti i campioni che hanno una data_disdetta non nulla poiché non significativi dato che la
#  televisita non è avvenuta ma è stata annullata. In questo modo non ci saranno valori mancanti per 'ora_inizio_erogazione' e 'ora_fine_erogazione'

# TODO: rimuovere colonne relative a 'data_disdetta' in quanto non utili. Dopo il secondo TODO per quella feature ci saranno solo valori mancanti

"""
    DOPO TODO:
    Statistiche valori mancanti dopo l'imputazione:

    data_disdetta                                460639
    codice_provincia_erogazione                   27396
    codice_provincia_residenza                    27016
    comune_residenza                                130
    dtype: int64
-----------------------------------
"""