import pandas as pd
from src.data_prep.data_cleaning import data_cleaning_execution
from src.data_prep.feature_selection import feature_selection_execution
from src.data_prep.feature_engineering import feature_engineering_execution
from src.modelling_clustering import clustering_execution
import yaml
import logging

def load_config(config_file):
    """Load the configuration file."""
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_data(config):
    # Load the data
    file_path = config['data']['file_path']
    df = pd.read_parquet(file_path)
    return df


def main():

    # Load the configuration file
    config = load_config('config.yaml')

    # Set up logging
    logging.basicConfig(filename=config['general']['logging_level'], format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Data Preparation Started")

    # Load the data
    df = load_data(config)

    # Display the number of rows and columns in the dataset
    num_rows, num_columns = df.shape
    logging.info(f"The DataFrame has {num_rows} rows and {num_columns} columns.\n")


    logging.info('\nNULLS BEFORE DATA CLEANING\n', df.isnull().sum().sort_values(ascending=False))
    '''
        NULLS BEFORE DATA CLEANING

        data_disdetta                                460639
        codice_provincia_erogazione                   28776
        codice_provincia_residenza                    28380
        ora_fine_erogazione                           28181
        ora_inizio_erogazione                         28181
        comune_residenza                                135
    '''

    # Phase 1: Data Cleaning
    logging.info('Data Cleaning Execution Started')

    if config['cleaning']['cleaning_enabled']:
        missing_threshold = config['cleaning']['missing_threshold']

        df = data_cleaning_execution(df, missing_threshold)

        logging.info('\nNULLS AFTER DATA CLEANING\n', df.isnull().sum().sort_values(ascending=False))
        '''
            NULLS AFTER DATA CLEANING

            data_disdetta                                460639
            codice_provincia_erogazione                   27396
            codice_provincia_residenza                    27016
            comune_residenza                                130
            dtype: int64
        '''

        cleaned_file_path = config['cleaning']['cleaned_file_path']
        df.to_parquet(cleaned_file_path)

    else:
        cleaned_file_path = config['cleaning']['cleaned_file_path']
        df = pd.read_parquet(cleaned_file_path)

    logging.info('Data Cleaning Execution Completed')


    # Phase 2: Feature Selection
    logging.info('Feature Selection Execution Started')

    if config['feature_selection']['selection_enabled']:
        df = feature_selection_execution(df)

        logging.info('\nNULLS AFTER FEATURE SELECTION\n', df.isnull().sum().sort_values(ascending=False))
        '''
            NULLS AFTER FEATURE SELECTION
            comune_residenza                      130
        '''

        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df.to_parquet(feature_selected_file_path)

    else:
        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df = pd.read_parquet(feature_selected_file_path)

    logging.info('Feature Selection Execution Completed')


    # Phase 3: Feature Engineering
    logging.info('Feature Engineering Execution Started')

    if config['feature_engineering']['engineering_enabled']:
        cols_grouped = config['feature_engineering']['cols_grouped']

        df = feature_engineering_execution(df, cols_grouped)

        logging.info('Head of the DataFrame after Feature Engineering\n', df.head())

        feature_engineered_file_path = config['feature_engineering']['feature_engineering_path']
        df.to_parquet(feature_engineered_file_path)
    else:
        feature_engineered_file_path = config['feature_engineering']['feature_engineering_path']
        df = pd.read_parquet(feature_engineered_file_path)

    logging.info('Feature Engineering Execution Completed')


    # Phase 4: Clustering
    logging.info('Clustering Execution Started')
    
    if config['modelling_clustering']['clustering_enabled']:
        df = clustering_execution(df, config)

        logging.info('Head of the DataFrame after Clustering\n', df.head())

        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        df.to_parquet(clustering_file_path)
    else:
        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        df = pd.read_parquet(clustering_file_path)

    logging.info('Clustering Execution Completed')

    
    # Phase 5: Metrics
    logging.info('Metrics Calculation Started')
    
    if config['metrics']['metrics_enabled']:
        pass

    logging.info('Metrics Calculation Completed')


if __name__ == '__main__':
    main()


