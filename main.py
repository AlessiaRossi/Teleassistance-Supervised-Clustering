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

'''
    The DataFrame has 484291 rows and 33 columns.
'''


print('\nNULLS BEFORE DATA CLEANING\n', df.isnull().sum().sort_values(ascending=False))

'''
    NULLS BEFORE DATA CLEANING

    data_disdetta                                460639
    codice_provincia_erogazione                   28776
    codice_provincia_residenza                    28380
    ora_fine_erogazione                           28181
    ora_inizio_erogazione                         28181
    comune_residenza                                135
'''

# Data Cleaning
df = data_cleaning_execution(df)

print('\nNULLS AFTER DATA CLEANING\n', df.isnull().sum().sort_values(ascending=False))

"""
    NULLS AFTER DATA CLEANING

    data_disdetta                                460639
    codice_provincia_erogazione                   27396
    codice_provincia_residenza                    27016
    comune_residenza                                130
    dtype: int64
-----------------------------------
"""



# Features Selection
df = feature_selection_execution(df)

# Feature extraction
#df = feature_extraction(df)

#df.to_csv('data/raw/challenge_campus_biomedico_2024_imputed_selected_extracted.csv', index=False)

# Displaying the number of rows and columns in the dataset
num_rows, num_columns = df.shape
print(f"The DataFrame has {num_rows} rows and {num_columns} columns.")

'''
    The DataFrame has 460639 rows and 22 columns.
'''


print('\nNULLS AFTER FEATURE SELECTION\n', df.isnull().sum().sort_values(ascending=False))
'''
NULLS AFTER FEATURE SELECTION
 comune_residenza                      130
'''
