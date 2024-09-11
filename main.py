# 1 DONE TODO: quando costruiamo incremento_teleassistenza, oltre a raggruppare per queste colonne  ['anno', 'quadrimestre', 'regione_residenza', 'fascia_eta'], aggiungiamo anche
#       "descrizione_attivita" 
# DONE 2 TODO: confrontare KProposity con KModes
# 2.1 TODO: confrontare gli n_init del modello scelto (es usare un for con 3 valori [5, 10, 15] e vedere quale è il migliore)
# 4 TODO: PPT
# 5 TODO: fare l'introduzione del progetto nel README.dm
# 6 DONE  TODO: aggiungere qualche commento

# NOTE: IL TODO 2.1 è da studiare con un DS piu piccolo (es. 20% del DS originale). 
# NOTE: per il TODO 2 va fatto il 2.1 prima per un modello e poi per un altro modello e confrontarli


import pandas as pd
from src.data_prep.DataCleaning import DataCleaning
from src.data_prep.FeatureSelection import FeatureSelection
from src.data_prep.FeatureExtraction import FeatureExtraction
from src.ModellingClustering import ModellingClustering
from src.MetricsEvaluation import MetricsEvaluation
from src.AnalysisResults import age_group_bar_chart, teleassistance_variation_bar_chart, \
    healthcare_professional_bar_chart, increment_gender_distribution_chart, scatter_map, year_cluster_increments_chart
import yaml
import logging
import os


# Load the configuration file
def load_config(config_file):
    """Load the configuration file."""
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config


# Load the data
def load_data(config):
    # Load the data
    file_path = config['data']['file_path']
    df = pd.read_parquet(file_path)
    return df


# Main function to execute the data preparation pipeline, including data cleaning, feature selection, feature extraction, clustering, metrics calculation and analysis results
def main():
    # Load the configuration file
    config = load_config('config.yaml')

    # Set up logging
    log_file_path = config['general']['log_file_path']
    open(log_file_path, 'w').close()  # Clear the log file
    logging.basicConfig(filename=log_file_path, format='%(asctime)s - %(message)s', level=logging.INFO)

    logging.info("Data Preparation Started")

    # Load the data
    df = load_data(config)

    # Create an instance of the DataCleaning class
    data_cleaning = DataCleaning(df)

    # Display the number of rows and columns in the dataset
    num_rows, num_columns = df.shape
    logging.info(f"The DataFrame has {num_rows} rows and {num_columns} columns.\n")

    logging.info(
        f'NULLS BEFORE DATA CLEANING \n {df.isnull().sum().sort_values(ascending=False)[df.isnull().sum().sort_values(ascending=False) > 0]}')
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
    if config['cleaning']['cleaning_enabled']:
        logging.info('Data Cleaning Execution Started')

        missing_threshold = config['cleaning']['missing_threshold']

        df_cleaning = data_cleaning.data_cleaning_execution(missing_threshold, config)

        logging.info(
            f'NULLS AFTER DATA CLEANING \n {df_cleaning.isnull().sum().sort_values(ascending=False)[df_cleaning.isnull().sum().sort_values(ascending=False) > 0]}')
        '''
            NULLS AFTER DATA CLEANING

            data_disdetta                                460639
            codice_provincia_erogazione                   27396
            codice_provincia_residenza                    27016
            comune_residenza                                130
            dtype: int64
        '''

        cleaned_file_path = config['cleaning']['cleaned_file_path']
        df_cleaning.to_parquet(cleaned_file_path)

        logging.info('Data Cleaning Execution Completed')
    elif os.path.exists(config['cleaning']['cleaned_file_path']):
        cleaned_file_path = config['cleaning']['cleaned_file_path']
        df_cleaning = pd.read_parquet(cleaned_file_path)
    else:
        raise FileNotFoundError(
            'The cleaned_data.parquet file does not exist. Please enable the cleaning process to create it.')

    # Create an instance of the FeatureSelection class
    feature_selection = FeatureSelection(df_cleaning)

    # Phase 2: Feature Selection
    if config['feature_selection']['selection_enabled']:
        logging.info('Feature Selection Execution Started')

        df_selection = feature_selection.feature_selection_execution(config)

        logging.info(
            f'NULLS AFTER FEATURE SELECTION \n {df_selection.isnull().sum().sort_values(ascending=False)[df_selection.isnull().sum().sort_values(ascending=False) > 0]}')
        '''
            NULLS AFTER FEATURE SELECTION
            comune_residenza                      130
        '''

        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df_selection.to_parquet(feature_selected_file_path)

        logging.info('Feature Selection Execution Completed')
    elif os.path.exists(config['feature_selection']['feature_selected_file_path']):
        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df_selection = pd.read_parquet(feature_selected_file_path)
    else:
        raise FileNotFoundError(
            'The feature_selected_data.parquet file does not exist. Please enable the feature selection process to create it.')

    # Create an instance of the FeatureExtraction class
    feature_extraction = FeatureExtraction(df_selection)

    # Phase 3: Feature Extraction
    if config['feature_extraction']['extraction_enabled']:
        logging.info('Feature Extraction Execution Started')

        cols_grouped = config['feature_extraction']['cols_grouped']

        df_extraction = feature_extraction.feature_extraction_execution(cols_grouped, config)

        logging.info(f'Head of the DataFrame after Feature Extraction \n {df_extraction.head()}')

        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df_extraction.to_parquet(feature_extraction_file_path)

        logging.info('Feature Extraction Execution Completed')
    elif os.path.exists(config['feature_extraction']['feature_extraction_path']):
        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df_extraction = pd.read_parquet(feature_extraction_file_path)
    else:
        raise FileNotFoundError(
            'The feature_extracted_data.parquet file does not exist. Please enable the feature extraction process to create it.')

    logging.info('Data Preparation Completed')

    # Create an instance of the ModellingClustering class
    modelling_clustering = ModellingClustering(df_extraction)

    # Phase 4: Clustering
    if config['modelling_clustering']['clustering_enabled']:
        logging.info('Clustering Execution Started')

        complete_df_clustered, df_clustered = modelling_clustering.clustering_execution(config)

        logging.info(f'Head of the DataFrame after Clustering \n {df_clustered.head()}')

        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        clustering_file_path_all_feature = config['modelling_clustering']['clustering_file_path_all_feature']

        df_clustered.to_parquet(clustering_file_path)
        complete_df_clustered.to_parquet(clustering_file_path_all_feature)

        logging.info('Clustering Execution Completed')
    elif os.path.exists(config['modelling_clustering']['clustering_file_path']):
        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        clustering_file_path_all_feature = config['modelling_clustering']['clustering_file_path_all_feature']

        df_clustered = pd.read_parquet(clustering_file_path)
        complete_df_clustered = pd.read_parquet(clustering_file_path_all_feature)
    else:
        raise FileNotFoundError(
            'The clustered_data.parquet file does not exist. Please enable the clustering process to create it.')

    # Create an instance of the MetricsEvaluation class
    metrics_evaluation = MetricsEvaluation(df_clustered)

    # Phase 5: Metrics
    if config['metrics']['metrics_enabled']:
        logging.info('Metrics Calculation Started')

        purity_score, silhouette_score, final_metric = metrics_evaluation.metrics_execution(config)

        with open(config['metrics']['metrics_file_path'], 'w') as file:
            file.write(f'Purity score: {purity_score}\n')
            file.write(f'Mean normalized silhouette score: {silhouette_score}\n')
            file.write(f'Final metric: {final_metric}\n')

        logging.info('Metrics Calculation Completed')

    # Phase 6: Analysis Results
    if config['analysis']['analysis_enabled']:
        logging.info('Analysis Results Started')
        charts_output_path = config['analysis']['charts_output_path']

        # Age Group Bar Chart
        df_max_cluster, df_max_increment, df_max_percentage_increment, df_crosstab_cluster, df_crosstab_increment, age_group_fig = age_group_bar_chart(
            df_clustered)
        age_group_fig.write_html(charts_output_path + 'age_group_bar_chart.html')

        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'w') as file:
            file.write(f'\n-Age Group Bar Chart Analysis- :\n')
            file.write(f'Cluster with the highest percentage for each age group:\n{df_max_cluster}\n')
            file.write(f'Increment category with the highest percentage per age group :\n{df_max_increment}\n')
            file.write(f'Highest percentage of increment type per age group:\n{df_max_percentage_increment}\n')
            file.write(f'Percentage of samples of increment type per age group:\n{df_crosstab_increment}\n')
            file.write(f'Percentage of samples of cluster per age group:\n{df_crosstab_increment}\n')

        # Teleassistance Variation Bar Chart
        cluster_counts, result, teleassistance_fig = teleassistance_variation_bar_chart(df_clustered)
        teleassistance_fig.write_html(charts_output_path + 'teleassistance_variation_bar_chart.html')

        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\n-Teleassistance Variation Bar Chart Analysis- :\n')
            file.write(f'Frequency of incremento_teleassistenze categories per cluster: \n{cluster_counts}\n')
            file.write(f'Cluster with the highest percentage for each increment category: \n{result}\n')

        # Healthcare Professional Bar Chart
        dominant_increment_per_professional, healthcare_fig = healthcare_professional_bar_chart(df_clustered)
        healthcare_fig.write_html(charts_output_path + 'healthcare_professional_bar_chart.html')

        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\n-Healthcare Professional Bar Chart Analysis- :\n')
            file.write(
                f'Frequency of each type of healthcare professional per teleassistance increment and dominant cluster: \n{dominant_increment_per_professional}\n')

        # Gender-Cluster Distribution Bar Chart
        sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster, gender_fig = increment_gender_distribution_chart(
            complete_df_clustered)
        gender_fig.write_html(charts_output_path + 'gender_distribution_bar_chart.html')
        # Gender-Increment Distribution Bar Chart
        sex_crosstab_inc, max_sex_per_inc, max_percentage_per_inc, gender_inc_fig = increment_gender_distribution_chart(
            complete_df_clustered)
        gender_inc_fig.write_html(charts_output_path + 'gender_distribution_bar_chart.html')
        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\n-Gender Distribution Analysis- :\n')
            file.write(f'Percentage of each gender within each cluster:\n{sex_crosstab}\n')
            file.write(f'Gender with the highest percentage for each cluster:\n{max_sex_per_cluster}\n')
            file.write(f'Dominant percentages of each gender within each cluster:\n{max_percentage_per_cluster}\n')
            file.write(f'Percentage of each gender within each increment type:\n{sex_crosstab_inc}\n')
            file.write(f'Gender with the highest percentage for each increment type:\n{max_sex_per_inc}\n')
            file.write(f'Dominant percentages of each gender within each increment type:\n{max_percentage_per_inc}\n')

        # Scatter Map
        max_cluster_per_region, max_percentage_per_region, max_increment_teleassistenze, scatter_map_fig = scatter_map(
            df_clustered)
        scatter_map_fig.write_html(charts_output_path + 'scatter_map.html')

        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\n-Scatter Map Analysis- :\n')
            file.write(
                f'Type of increment with the highest percentage for each region:\n{max_increment_teleassistenze}\n')
            file.write(f'Cluster with the highest percentage for each region:\n{max_cluster_per_region}\n')
            file.write(f'Percentage of each region within each cluster:\n{max_percentage_per_region}\n')

        # Year Cluser Increment Chart
        df_max_cluster_inc, df_max_percentage_increment_cla, df_crosstab_cluster, fig = year_cluster_increments_chart(
            complete_df_clustered)
        fig.write_html(charts_output_path + 'teleassistance_increment_cluster.html')

        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\n-Year Increment Cluster Analysis- :\n')
            file.write(f'Dominant cluster for each combination of year and increment type:\n{df_max_cluster_inc}\n')
            file.write(
                f'Highest percentage for each combination of year and increment type:\n{df_max_percentage_increment_cla}\n')

        logging.info('Analysis Results Completed')


if __name__ == '__main__':
    main()
