# Data Directory

This repository contains data used for analysis and modeling in the context of a biomedical challenge. The data is organized into two main subdirectories: `raw` for the unprocessed original data and `processed` for the data that has undergone various preprocessing steps. This document provides a detailed overview of the files within these directories, including their purpose and structure.

## Index
1. [raw/](#1-raw-directory)
2. [processed/](#2-processed-directory)

- [Return to README](../README.md)

## Directory Structure

```plaintext
data/
├── processed/
│   ├── cleaned_data.parquet
│   ├── clustered_data.parquet
│   ├── feature_extracted_data.parquet
│   └── feature_selected_data.parquet
└── raw/
    ├── challenge_campus_biomedico_2024.parquet
    └── Codici-statistici-e-denominazioni-al-30_06_2024.xlsx
```


## 1. `raw/` Directory
This folder contains the raw data files as obtained from the source. The files in this directory should be considered read-only, meaning they should not be modified or overwritten.

- **`challenge_campus_biomedico_2023.parquet`**:
  - This file contains the main dataset for the challenge. The data is stored in Parquet format for efficient reading and writing operations.
  - **Schema Overview**:
    - **`id_prenotazione`**: Unique identifier of a single Teleassistance.
    - **`id_paziente`**: Patient’s unique identifier code.
    - **`data_nascita`**: Patient’s birth date.
    - **...** (Please refer to this [file](../myLib/challenge_campus_biomedico.pdf) from page 9, for the full list of variables and descriptions).

- **`Codici-statistici-e-denominazioni-aggiornato-2023.xlsx`**:
  - This Excel file contains updated statistical codes and denominations relevant to the dataset. In particular, this dataset is used for imputate_comune_residenza method that you can find in the [data_cleaning.py](../src/data_prep/data_cleaning.py) script.

## 2. `processed/` Directory
This folder contains data that has been processed or transformed in some way from the raw data. These files are typically the result of various preprocessing steps and are used for analysis and modeling.

- **`cleaned_data.parquet`**:
  - Contains the dataset after initial cleaning, which may include handling missing values, correcting inconsistencies, and removing irrelevant information.

- **`feature_selected_data.parquet`**:
  - Contains the dataset after feature selection, where only the most relevant features for modeling are retained.

- **`feature_extracted_data.parquet`**:
  - This file includes the data after feature extraction, where new features have been generated from the raw attributes.

- **`clustered_data.parquet`**:
  - Contains the data after applying clustering algorithms. Each record has been assigned a cluster label based on the analysis.

## Notes
- The Parquet format is used for its efficiency in storage and processing, especially for large datasets. It allows for faster data reading and writing compared to traditional formats like CSV.
- Ensure that any code referencing these files correctly points to the appropriate directory and filename to avoid errors during execution.


[Quickly return to the top](#data-directory)