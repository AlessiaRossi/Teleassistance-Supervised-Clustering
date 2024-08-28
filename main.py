import pandas as pd
from src.data_prep.data_cleaning import data_cleaning_execution
from src.data_prep.feature_selection import feature_selection_execution
from src.data_prep.feature_extraction import feature_extraction_execution
from src.modelling_clustering import clustering_execution
from src.metrics_evaluation import metrics_execution
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
    log_file_path = config['general']['log_file_path']
    open(log_file_path, 'w').close() # Clear the log file
    logging.basicConfig(filename=log_file_path, format='%(asctime)s - %(message)s', level=logging.INFO)
    
    logging.info("Data Preparation Started")

    # Load the data
    df = load_data(config)

    # Display the number of rows and columns in the dataset
    num_rows, num_columns = df.shape
    logging.info(f"The DataFrame has {num_rows} rows and {num_columns} columns.\n")


    logging.info(f'NULLS BEFORE DATA CLEANING \n {df.isnull().sum().sort_values(ascending=False)[df.isnull().sum().sort_values(ascending=False) > 0]}')
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

        df = data_cleaning_execution(df, missing_threshold, config)

        logging.info(f'NULLS AFTER DATA CLEANING \n {df.isnull().sum().sort_values(ascending=False)[df.isnull().sum().sort_values(ascending=False) > 0]}' )
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
    if config['feature_selection']['selection_enabled']:
        logging.info('Feature Selection Execution Started')

        df = feature_selection_execution(df, config)

        logging.info(f'NULLS AFTER FEATURE SELECTION \n {df.isnull().sum().sort_values(ascending=False)[df.isnull().sum().sort_values(ascending=False) > 0]}')
        '''
            NULLS AFTER FEATURE SELECTION
            comune_residenza                      130
        '''

        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df.to_parquet(feature_selected_file_path)

        logging.info('Feature Selection Execution Completed')
    else:
        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df = pd.read_parquet(feature_selected_file_path)




    # Phase 3: Feature Extraction
    if config['feature_extraction']['extraction_enabled']:
        logging.info('Feature Extraction Execution Started')

        cols_grouped = config['feature_extraction']['cols_grouped']

        df = feature_extraction_execution(df, cols_grouped, config)

        logging.info(f'Head of the DataFrame after Feature Extraction \n {df.head()}')

        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df.to_parquet(feature_extraction_file_path)

        logging.info('Feature Extraction Execution Completed')
    else:
        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df = pd.read_parquet(feature_extraction_file_path)


    # Phase 4: Clustering
    if config['modelling_clustering']['clustering_enabled']:
        logging.info('Clustering Execution Started')

        df = clustering_execution(df, config)

        logging.info(f'Head of the DataFrame after Clustering \n {df.head()}')

        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        df.to_parquet(clustering_file_path)

        logging.info('Clustering Execution Completed')
    else:
        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        df = pd.read_parquet(clustering_file_path)

    
    # Phase 5: Metrics
    if config['metrics']['metrics_enabled']:
        logging.info('Metrics Calculation Started')

        purity_score, silhouette_score, final_metric = metrics_execution(df, config)

        with open(config['metrics']['metrics_file_path'], 'w') as file:
            file.write(f'Purity score: {purity_score}\n')
            file.write(f'Mean normalized silhouette score: {silhouette_score}\n')
            file.write(f'Final metric: {final_metric}\n')

        logging.info('Metrics Calculation Completed')


if __name__ == '__main__':
    main()


