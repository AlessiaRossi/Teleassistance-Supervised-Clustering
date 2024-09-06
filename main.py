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
from src.data_prep.data_cleaning import data_cleaning_execution
from src.data_prep.feature_selection import feature_selection_execution
from src.data_prep.feature_extraction import feature_extraction_execution
from src.modelling_clustering import clustering_execution
from src.metrics_evaluation import metrics_execution
from src.analysis_results import age_group_bar_chart, teleassistance_variation_bar_chart, healthcare_professional_bar_chart, gender_distribution_chart,scatter_map
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

        df_cleaning = data_cleaning_execution(df, missing_threshold, config)

        logging.info(f'NULLS AFTER DATA CLEANING \n {df_cleaning.isnull().sum().sort_values(ascending=False)[df_cleaning.isnull().sum().sort_values(ascending=False) > 0]}' )
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

    else:
        cleaned_file_path = config['cleaning']['cleaned_file_path']
        df_cleaning = pd.read_parquet(cleaned_file_path)

    logging.info('Data Cleaning Execution Completed')


    # Phase 2: Feature Selection
    if config['feature_selection']['selection_enabled']:
        logging.info('Feature Selection Execution Started')

        df_selection = feature_selection_execution(df_cleaning, config)

        logging.info(f'NULLS AFTER FEATURE SELECTION \n {df_selection.isnull().sum().sort_values(ascending=False)[df_selection.isnull().sum().sort_values(ascending=False) > 0]}')
        '''
            NULLS AFTER FEATURE SELECTION
            comune_residenza                      130
        '''

        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df_selection.to_parquet(feature_selected_file_path)

        logging.info('Feature Selection Execution Completed')
    else:
        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df_selection = pd.read_parquet(feature_selected_file_path)




    # Phase 3: Feature Extraction
    if config['feature_extraction']['extraction_enabled']:
        logging.info('Feature Extraction Execution Started')

        cols_grouped = config['feature_extraction']['cols_grouped']

        df_extraction = feature_extraction_execution(df_selection, cols_grouped, config)

        logging.info(f'Head of the DataFrame after Feature Extraction \n {df_extraction.head()}')

        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df_extraction.to_parquet(feature_extraction_file_path)

        logging.info('Feature Extraction Execution Completed')
    else:
        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df_extraction = pd.read_parquet(feature_extraction_file_path)


    logging.info('Data Preparation Completed')
    

    # Phase 4: Clustering
    if config['modelling_clustering']['clustering_enabled']:
        logging.info('Clustering Execution Started')

        complete_df_clustered, df_clustered = clustering_execution(df_extraction, config)

        logging.info(f'Head of the DataFrame after Clustering \n {df_extraction.head()}')

        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        clustering_file_path_all_feature = config['modelling_clustering']['clustering_file_path_all_feature']
        df_clustered.to_parquet(clustering_file_path)
        complete_df_clustered.to_parquet(clustering_file_path_all_feature)

        logging.info('Clustering Execution Completed')
    else:
        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        df_clustered = pd.read_parquet(clustering_file_path)

    
    # Phase 5: Metrics
    if config['metrics']['metrics_enabled']:
        logging.info('Metrics Calculation Started')

        purity_score, silhouette_score, final_metric = metrics_execution(df_clustered, config)

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
        df_max_cluster, df_max_percentage, df_crosstab, age_group_fig = age_group_bar_chart(df_clustered)
        age_group_fig.savefig(charts_output_path + 'age_group_bar_chart.png')

        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\nAge Group Bar Chart Analysis:\n')
            file.write(f'Max Cluster per Age Group:\n{df_max_cluster}\n')
            file.write(f'Max Percentage per Age Group:\n{df_max_percentage}\n')
            file.write(f'Crosstab of Age Group and Cluster:\n{df_crosstab}\n')

        print("Age Group Bar Chart Analysis:")
        print("Max Cluster per Age Group:")
        print(df_max_cluster)
        print("Max Percentage per Age Group:")
        print(df_max_percentage)
        print("Crosstab of Age Group and Cluster:")
        print(df_crosstab)

        # Teleassistance Variation Bar Chart
        teleassistance_fig = teleassistance_variation_bar_chart(df_clustered)
        teleassistance_fig.savefig(charts_output_path + 'teleassistance_variation_bar_chart.png')

        # Healthcare Professional Bar Chart
        healthcare_fig = healthcare_professional_bar_chart(df_clustered)
        healthcare_fig.savefig(charts_output_path + 'healthcare_professional_bar_chart.png')

        # Gender Distribution Bar Chart
        sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster, gender_fig = gender_distribution_chart(df_clustered)
        gender_fig.savefig(charts_output_path + 'gender_distribution_bar_chart.png')

        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\nGender Distribution Analysis:\n')
            file.write(f'Sex Crosstab:\n{sex_crosstab}\n')
            file.write(f'Max Sex per Cluster:\n{max_sex_per_cluster}\n')
            file.write(f'Max Percentage per Cluster:\n{max_percentage_per_cluster}\n')

        print("Gender Distribution Analysis:")
        print("Sex Crosstab:")
        print(sex_crosstab)
        print("Max Sex per Cluster:")
        print(max_sex_per_cluster)
        print("Max Percentage per Cluster:")
        print(max_percentage_per_cluster)

        # Scatter Map
        max_cluster_per_region, max_percentage_per_region, scatter_map_fig = scatter_map(df_clustered)
        scatter_map_fig.savefig(charts_output_path + 'scatter_map.png')

        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'a') as file:
            file.write(f'\nScatter Map Analysis:\n')
            file.write(f'Max Cluster per Region:\n{max_cluster_per_region}\n')
            file.write(f'Max Percentage per Region:\n{max_percentage_per_region}\n')

        print("Scatter Map Analysis:")
        print("Max Cluster per Region:")
        print(max_cluster_per_region)
        print("Max Percentage per Region:")
        print(max_percentage_per_region)

        logging.info('Analysis Results Completed')



if __name__ == '__main__':
    main()


