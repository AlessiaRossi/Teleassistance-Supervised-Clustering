import pandas as pd
from src.data_prep.DataCleaning import DataCleaning
from src.data_prep.FeatureSelection import FeatureSelection
from src.data_prep.FeatureExtraction import FeatureExtraction
from src.ModellingClustering import ModellingClustering
from src.MetricsEvaluation import MetricsEvaluation
from src.AnalysisResults import (create_gender_distribution_chart, create_increment_distribution_chart, create_increment_scatter_map,
                                 create_cluster_and_increment_pie_charts, create_increment_and_cluster_bar_charts, create_age_vs_increment_box_plot,
                                 create_increment_vs_cluster_bar_chart, create_scatter_plot_by_cluster_and_professional,
                                 create_scatter_plot_by_increment_and_structure, plot_cluster_increment_heatmap)
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
 
        # Create an instance of the FeatureSelection class
        feature_selection = FeatureSelection(df_cleaning)
 
        logging.info('Data Cleaning Execution Completed')
    elif os.path.exists(config['cleaning']['cleaned_file_path']):
        cleaned_file_path = config['cleaning']['cleaned_file_path']
        df_cleaning = pd.read_parquet(cleaned_file_path)
 
        # Create an instance of the FeatureSelection class
        feature_selection = FeatureSelection(df_cleaning)
    elif not config['cleaning']['cleaning_enabled'] and not os.path.exists(config['cleaning']['cleaned_file_path']):
        raise FileNotFoundError(
            'The cleaned_data.parquet file does not exist. Please enable the cleaning process to create it.')
 
 
 
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
 
        # Create an instance of the FeatureExtraction class
        feature_extraction = FeatureExtraction(df_selection)
 
        logging.info('Feature Selection Execution Completed')
    elif os.path.exists(config['feature_selection']['feature_selected_file_path']):
        feature_selected_file_path = config['feature_selection']['feature_selected_file_path']
        df_selection = pd.read_parquet(feature_selected_file_path)
 
        # Create an instance of the FeatureExtraction class
        feature_extraction = FeatureExtraction(df_selection)
    elif not config['feature_selection']['selection_enabled'] and not os.path.exists(config['feature_selection']['feature_selected_file_path']):
        raise FileNotFoundError(
            'The feature_selected_data.parquet file does not exist. Please enable the feature selection process to create it.')
 
 
 
    # Phase 3: Feature Extraction
    if config['feature_extraction']['extraction_enabled']:
        logging.info('Feature Extraction Execution Started')
 
        cols_grouped = config['feature_extraction']['cols_grouped']
 
        df_extraction = feature_extraction.feature_extraction_execution(cols_grouped, config)
 
        logging.info(f'Head of the DataFrame after Feature Extraction \n {df_extraction.head()}')
 
        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df_extraction.to_parquet(feature_extraction_file_path)

        # print(df_extraction.info())

        # Create an instance of the ModellingClustering class
        modelling_clustering = ModellingClustering(df_extraction)

        logging.info('Feature Extraction Execution Completed')
    elif os.path.exists(config['feature_extraction']['feature_extraction_path']):
        feature_extraction_file_path = config['feature_extraction']['feature_extraction_path']
        df_extraction = pd.read_parquet(feature_extraction_file_path)
 

        # print(df_extraction.info())

        # Create an instance of the ModellingClustering class
        modelling_clustering = ModellingClustering(df_extraction)
    elif not config['feature_extraction']['extraction_enabled'] and not os.path.exists(config['feature_extraction']['feature_extraction_path']):
        raise FileNotFoundError(
            'The feature_extracted_data.parquet file does not exist. Please enable the feature extraction process to create it.')
 
    logging.info('Data Preparation Completed')
 
 
    # Phase 4: Clustering
    if config['modelling_clustering']['clustering_enabled']:
        logging.info('Clustering Execution Started')
 
        df_extraction = pd.read_parquet(feature_extraction_file_path)
 
        # Create an instance of the ModellingClustering class
        modelling_clustering = ModellingClustering(df_extraction)
 
        complete_df_clustered, df_clustered = modelling_clustering.clustering_execution(config)
 
        logging.info(f'Head of the DataFrame after Clustering \n {df_clustered.head()}')
 
        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        clustering_file_path_all_feature = config['modelling_clustering']['clustering_file_path_all_feature']
 
        df_clustered.to_parquet(clustering_file_path)
        complete_df_clustered.to_parquet(clustering_file_path_all_feature)
 
        # Create an instance of the MetricsEvaluation class
        metrics_evaluation = MetricsEvaluation(df_clustered)
 
        logging.info('Clustering Execution Completed')
    elif os.path.exists(config['modelling_clustering']['clustering_file_path']):
        clustering_file_path = config['modelling_clustering']['clustering_file_path']
        clustering_file_path_all_feature = config['modelling_clustering']['clustering_file_path_all_feature']
 
        df_clustered = pd.read_parquet(clustering_file_path)
        complete_df_clustered = pd.read_parquet(clustering_file_path_all_feature)
 
        # Create an instance of the MetricsEvaluation class
        metrics_evaluation = MetricsEvaluation(df_clustered)
    elif not config['modelling_clustering']['clustering_enabled'] and not os.path.exists(config['modelling_clustering']['clustering_file_path']):
        raise FileNotFoundError(
            'The clustered_data.parquet file does not exist. Please enable the clustering process to create it.')
 
   
 
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

        # Crea i grafici
        # Gender Distribution Chart
        gender_chart, sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster = create_gender_distribution_chart(complete_df_clustered)
        gender_chart.write_html(charts_output_path + 'gender_chart.html')

        # Increment Distribution Chart
        increment_chart, df_sample_counts, df_max_cluster, df_max_sample_count = create_increment_distribution_chart(complete_df_clustered)
        increment_chart.write_html(charts_output_path + 'increment_chart.html')

        # Scatter Map
        scatter_map, max_cluster_per_region, max_percentage_per_region, max_inc_per_region = create_increment_scatter_map(complete_df_clustered)
        scatter_map.write_html(charts_output_path + 'scatter_map.html')

        # Pie Charts
        pie_charts = create_cluster_and_increment_pie_charts(complete_df_clustered)
        pie_charts.write_html(charts_output_path + 'pie_charts.html')
        # Bar Charts
        bar_charts,incremento_counts, cluster_counts = create_increment_and_cluster_bar_charts(complete_df_clustered)
        bar_charts.write_html(charts_output_path + 'bar_charts.html')

        # Box Plot
        box_plot = create_age_vs_increment_box_plot(complete_df_clustered)
        box_plot.write_html(charts_output_path + 'box_plot.html')

        # Bar Chart
        bar_chart, increment_cluster_counts = create_increment_vs_cluster_bar_chart(complete_df_clustered)
        bar_chart.write_html(charts_output_path + 'bar_chart.html')

        # Scatter Plot Professional
        scatter_plot_professional= create_scatter_plot_by_cluster_and_professional(complete_df_clustered)
        scatter_plot_professional.write_html(charts_output_path + 'scatter_plot_professional.html')

        # Scatter Plot Structure
        scatter_plot_structure = create_scatter_plot_by_increment_and_structure(complete_df_clustered)
        scatter_plot_structure.write_html(charts_output_path + 'scatter_plot_structure.html')

        # Heatmap
        heatmap = plot_cluster_increment_heatmap(complete_df_clustered)
        heatmap.write_html(charts_output_path + 'heatmap.html')



        # Print and log the values
        with open(config['analysis']['analysis_file_path'], 'w') as file:
            file.write(f'\n-Analysis Results- :\n')

            file.write(f'\n-Gender Distribution Analysis- :\n')
            file.write(f'Percentage of each gender within each cluster:\n{sex_crosstab}\n')
            file.write(f'Gender with the highest percentage for each cluster:\n{max_sex_per_cluster}\n')
            file.write(f'Dominant percentages of each gender within each cluster:\n{max_percentage_per_cluster}\n')

            file.write(f'\n-Year Distribution Analysis- :\n')
            file.write(f'Calculate the number of samples for each combination of year and increment type:\n{df_sample_counts}\n')
            file.write(f'Dominant cluster for each combination of year and increment type:\n{df_max_cluster}\n')
            file.write(f'highest number of samples for each combination of year and increment type:\n{df_max_sample_count}\n')

            file.write(f'\n-Geographical Distribution Analysis- :\n')
            file.write(f'Type of increment with the highest percentage for each region:\n{max_inc_per_region}\n')
            file.write(f'Cluster with the highest percentage for each region:\n{max_cluster_per_region}\n')
            file.write(f'Percentage of each region within each cluster:\n{max_percentage_per_region}\n')

            file.write(f'\n-Cluster and Increment Distribution Analysis- :\n')
            file.write(f'Number of samples for each cluster\n{cluster_counts}\n')
            file.write(f'Number of samples for each increment type\n{incremento_counts}\n')
            file.write(f'Number of samples for each combination of teleassistance increment and cluster\n{increment_cluster_counts}\n')






        logging.info('Analysis Results Completed')


if __name__ == '__main__':
    main()
