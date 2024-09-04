import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

class FeatureExtraction:

    def __init__(self):
        pass


    def __incremento_labelling(self, df: pd.DataFrame, cols_grouped: list) -> pd.DataFrame:
        '''
            This function calculates the increment of the number of services for each group and the average percentage increment.

            Parameters:
            - df: DataFrame containing the data to be processed.
            - cols_grouped: List of columns to be grouped together.

            Returns:
            - incremento_percentuale_medio: DataFrame containing the average percentage increment for each group.
            - df_cols_no_anno: List of columns to be grouped together without the 'anno' column.
        '''

        df_grouped = df.groupby(cols_grouped).size().reset_index(name='num_servizi') # count the number of services for each group and create a new dataframe with the results
        logging.info(df_grouped.sort_values(by=['num_servizi'], ascending=True))

        # Remove the 'anno' column from the dataframe to calculate the increment
        df_cols_no_anno = cols_grouped.copy()
        df_cols_no_anno.remove('anno')

        # Calculate the increment of the number of services for each group
        df_grouped['incremento'] = df_grouped.groupby(df_cols_no_anno)['num_servizi'].diff()
        
        # Calculate the percentage increment of the number of services for each group
        df_grouped['incremento_percentuale'] = df_grouped['incremento'] / df_grouped.groupby(df_cols_no_anno)['num_servizi'].shift(1) * 100   # shift(1) per avere il valore precedente

        # Calculate the average percentage increment of the number of services for each group
        incremento_percentuale_medio = df_grouped.groupby(df_cols_no_anno)['incremento_percentuale'].mean().reset_index()

        logging.info(incremento_percentuale_medio.sort_values(by=['incremento_percentuale'], ascending=False))

        return incremento_percentuale_medio, df_cols_no_anno


    def __classify_increment(self, value):
        '''
            This function classifies the average percentage increment of the number of services.

            Parameters:
            - value: The average percentage increment of the number of services.

            Returns:
            - The classification of the average percentage increment.
        '''

        constat_increment = 5 
        low_increment = 15
        medium_increment = 40

        if value <= constat_increment and value >= 0:
            return 'constant_increment'
        elif value <= low_increment:
            return 'low_increment'
        elif value <= medium_increment:
            return 'medium_increment'
        elif value > medium_increment:
            return 'high_increment'
        else:
            return 'decrement'
        

    def __sample_cassification(self, incremento_percentuale_medio: pd.DataFrame, df: pd.DataFrame, df_cols_no_anno: list):
        '''
            This function classifies the average percentage increment of the number of services and merges the classification with the original DataFrame.

            Parameters:
            - incremento_percentuale_medio: DataFrame containing the average percentage increment for each group.
            - df: DataFrame containing the data to be processed.
            - df_cols_no_anno: List of columns to be grouped together without the 'anno' column.

            Returns:
            - df: DataFrame with the classification of the average percentage increment applied.
        '''

        # Apply the function to classify the average percentage increment
        incremento_percentuale_medio['incremento_teleassistenze'] = incremento_percentuale_medio['incremento_percentuale'].apply(self.__classify_increment)

        logging.info(incremento_percentuale_medio['incremento_teleassistenze'].value_counts())

        # Merge the classification with the original dataframe
        df = df.merge(incremento_percentuale_medio[df_cols_no_anno + ['incremento_teleassistenze']], 
                on=df_cols_no_anno, 
                how='left')
        
        return df


    def __histplot_avg_incremento_distribution(self, incremento_percentuale_medio: pd.DataFrame):
        # Plot the distribution of the average percentage increment
        plt.figure(figsize=(10, 6))
        sns.histplot(incremento_percentuale_medio['incremento_percentuale'], bins=30, kde=True)
        plt.title('Distribuzione degli Incrementi Medi Percentuali')
        plt.xlabel('Incremento Percentuale Medio')
        plt.ylabel('Frequenza')
        plt.savefig('graphs/avg_incremento_percentuale_histplot.png')


    def __boxplot_avg_incremento_distribution(self, incremento_percentuale_medio: pd.DataFrame):
        # Plot the distribution of the average percentage increment
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=incremento_percentuale_medio['incremento_percentuale'])
        plt.title('Boxplot degli Incrementi Medi Percentuali')
        plt.xlabel('Incremento Percentuale')
        plt.savefig('graphs/avg_incremento_percentuale_boxplot.png')
        

    def feature_extraction_execution(self, df: pd.DataFrame, cols_grouped: list, config:dict) -> pd.DataFrame:
        '''
            This function performs the feature extraction process on the DataFrame.

            Parameters:
            - df: DataFrame containing the data to be processed.
            - cols_grouped: List of columns to be grouped together.
            - config: Dictionary containing configuration settings for the feature extraction process.

            Returns:
            - df: DataFrame with the feature extraction process applied.
        '''

        logging.basicConfig(filename=config['general']['logging_level'], format='%(asctime)s - %(message)s', level=logging.INFO)

        # This is a TODO defined in the feature_selection.py but not yet implemented
        df.drop(columns=['codice_struttura_erogazione'], inplace=True)
        df['durata_erogazione_sec'] =  df.durata_erogazione_sec.astype(int)

        incremento_percentuale_medio, df_cols_no_anno = self.__incremento_labelling(df, cols_grouped)

        logging.info(incremento_percentuale_medio['incremento_percentuale'].describe())

        # Plot the distribution of the average percentage increment
        self.__histplot_avg_incremento_distribution(incremento_percentuale_medio)
        self.__boxplot_avg_incremento_distribution(incremento_percentuale_medio)

        # Apply the classification of the average percentage increment
        df = self.__sample_cassification(incremento_percentuale_medio, df, df_cols_no_anno)

        return df