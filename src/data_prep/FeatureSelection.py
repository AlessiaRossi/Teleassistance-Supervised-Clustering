import pandas as pd
from data_prep.DataCleaning import DataCleaning
import numpy as np
from scipy.stats import chi2_contingency
import seaborn as sns
import matplotlib.pyplot as plt
import logging

class FeatureSelection:

    def __init__(self,  df:pd.DataFrame):
        # List of tuples containing the code-description column pairs to be compared.
        self.columns_pairs = [
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

        self.dataCleaning = DataCleaning()
        self.df = df.copy()


    def __print_details_corrections (self, df:pd.DataFrame, code:str, description:str, code_groups:dict, description_groups):
        '''
            This function prints details if there are codes with multiple descriptions or vice versa

            Parameters:
            - df: DataFrame to operate on
            - code: Code column to analyze
            - description: Description column to be parsed
            - code_groups: Code groups with unique description counts
            - description_groups: Groups of descriptions with unique code counts
            
            Returns:
            - None
        '''

        not_unique = False

        for cod, desc_count in code_groups.items():
            if desc_count > 1:
                associated_descriptions = df[df[code] == cod][description].unique()
                logging.info(f"The {cod} code is associated with {desc_count} descriptions: {associated_descriptions}")
                not_unique = True
                
        for desc, code_count in description_groups.items():
            if code_count > 1:
                associated_codes =df[df[description] == desc][code].unique()
                logging.info(f"The {desc} description is associated with {code_count} codes: {associated_codes}")
                not_unique = True

        if not_unique:
            logging.info(f"--> NOT unique correlation between {code} and {description}\n")



    def __remove_columns_with_unique_correlation(self, df:pd.DataFrame, columns_pairs:list) -> pd.DataFrame:
        '''
        This function removes columns (column code) with unique correlation

        Args:
            df: The DataFrame containing the data.
            columns_pairs: List of tuples containing the code-description column pairs to be compared.

        Returns:
            The DataFrame with removed columns
        '''

        logging.info('Removing columns with unique correlation')

        pairs_removed = []

        for code, description in columns_pairs:
            if code in df.columns and description in df.columns:
                code_groups = df.groupby(code)[description].nunique()
                description_groups = df.groupby(description)[code].nunique()

                self.__print_details_corrections(df, code, description, code_groups, description_groups)

                unique_correlation_code_description = all(code_groups <= 1)
                unique_correlation_description_code = all(description_groups <= 1)

                if unique_correlation_code_description and unique_correlation_description_code:
                    df.drop(columns=[code], inplace=True)
                    logging.info(f'Unique correlation between {code} and {description}. Column {code} removed.')
                    pairs_removed.append((code, description))
            else:
                logging.info(f'Columns {code} or {description} not found in the dataframe.')
                pairs_removed.append((code, description))

        # Update the list of columns pairs removing the ones that have been removed
        columns_pairs_updated = [pair for pair in columns_pairs if pair not in pairs_removed]
        return df, columns_pairs_updated

                
    def __clean_codice_struttura_erogazione(self, df:pd.DataFrame, column='codice_struttura_erogazione') -> pd.DataFrame:
        '''
        This function cleans the 'codice_struttura_erogazione' column by converting it to an integer type
        '''

        logging.info(f"Cleaning {column} column")

        df[column] = df[column].astype(int)
        return df


    def __remove_data_disdetta(self, df:pd.DataFrame) -> pd.DataFrame:
        '''
        This function remove data_disdetta column from the DataFrame
        '''

        logging.info('Removing data_disdetta column')

        df.drop(columns=['data_disdetta'], inplace=True)
        return df


    def __colonna_durata_erogazione(self, df:pd.DataFrame) -> pd.DataFrame:
        '''
        This function creates a new column 'durata_erogazione' which is the difference between 'ora_fine_erogazione' and 'ora_inizio_erogazione'
        '''

        logging.info('Creating durata_erogazione column')

        # Convert 'ora_inizio_erogazione' and 'ora_fine_erogazione' to datetime
        df['ora_inizio_erogazione'] = pd.to_datetime(df['ora_inizio_erogazione'], utc=True, errors='coerce')
        df['ora_fine_erogazione'] = pd.to_datetime(df['ora_fine_erogazione'], utc=True, errors='coerce')

        df['durata_erogazione_sec'] = (df['ora_fine_erogazione'] - df['ora_inizio_erogazione']).dt.total_seconds()
        
        return df


    def __remove_ora_inizio_fine_erogazione(self, df:pd.DataFrame) -> pd.DataFrame:
        '''
            This function removes 'ora_inizio_erogazione' and 'ora_fine_erogazione' columns from the DataFrame

            Parameters:
            - df: DataFrame containing the data.

            Returns:
            - df: DataFrame with the columns removed.
        '''

        logging.info('Removing ora_inizio_erogazione and ora_fine_erogazione columns')

        df.drop(columns=['ora_inizio_erogazione', 'ora_fine_erogazione'], inplace=True)
        return df


    def __colonna_fascia_eta(self, df:pd.DataFrame) -> pd.DataFrame:
        '''
            This function creates a new column 'fascia_eta' which is the age range of the patient

            Parameters:
            - df: DataFrame containing the data.

            Returns:
            - df: DataFrame with the 'fascia_eta' column added.
        '''

        logging.info('Creating fascia_eta column')

        df['data_nascita'] = pd.to_datetime(df['data_nascita'], utc=True, errors='coerce')

        # print(df.shape) #dim: (460509, 21)
        
        eta = (pd.to_datetime('today', utc=True) - df['data_nascita']).dt.days // 365
        
        # print(eta.shape) #dim: (460509,)

        age_labels = ['0-11', '12-23', '24-35', '36-47', '48-59', '60-69', '70+']
        eta = pd.cut(eta, bins=[0, 12, 24, 36, 48, 60, 70, 120], labels=age_labels)
        # print(eta)
        
        df['fascia_eta'] = eta.astype(str)

        return df

    def __colonne_anno_e_quadrimestre(self, df:pd.DataFrame) -> pd.DataFrame:
        '''
            This function creates the 'anno' and 'quadrimestre' columns from the 'data_erogazione' column.

            Parameters:
            - df: DataFrame containing the data.

            Returns:
            - df: DataFrame with the 'anno' and 'quadrimestre' columns added.
        '''
        
        logging.info('Creating anno and quadrimestre columns')

        df['data_erogazione'] = pd.to_datetime(df['data_erogazione'], utc=True, errors='coerce')
        df['anno'] = df['data_erogazione'].dt.year
        df['quadrimestre'] = df['data_erogazione'].dt.quarter

        return df


    def __cramer_v(self, x, y):
        '''
            This function calculates Cramér's V for two categorical variables.

            Parameters:
            - x: First categorical variable.
            - y: Second categorical variable.

            Returns:
            - Cramér's V statistic.
        '''
        # Create a contingency table
        contingency = pd.crosstab(x, y)

        # Calculate the chi-square test statistic and other values
        chi2, _, _, _ = chi2_contingency(contingency)
        n = contingency.sum().sum()
        min_dim = min(contingency.shape) - 1

        # Calculate Cramér's V
        return np.sqrt(chi2 / (n * min_dim))


    def __calculate_correlation_matrix(self, df:pd.DataFrame, corr_cols:list):
        '''
            This function calculates the correlation matrix using Cramér's V.

            Parameters:
            - df: DataFrame containing the data.
            - corr_cols: List of columns to calculate the correlation matrix for.

            Returns:
            - DataFrame containing the correlation matrix.
        '''

        logging.info('Calculating correlation matrix using Cramér\'s V')

        correlations = pd.DataFrame(index=corr_cols, columns=corr_cols)

        # Calculate Cramér's V for each pair of columns
        for col1 in corr_cols:
            for col2 in corr_cols:
                if col1 != col2:
                    correlations.loc[col1, col2] = self.__cramer_v(df[col1], df[col2])
                else:
                    correlations.loc[col1, col2] = 1.0  # Perfect correlation with itself
        return correlations


    def __visualize_correlation_matrix(self, correlations:pd.DataFrame, name:str):
        '''
            This function visualizes the correlation matrix using a heatmap.

            Parameters:
            - correlations: DataFrame containing the correlation matrix.

            Returns:
            - None
        '''
        plt.figure(figsize=(16, 12))
        sns.heatmap(correlations.astype(float), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, square=True)

        plt.xticks(rotation=45, ha="right", fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()

        plt.savefig(name)


    def __remove_highly_correlated_columns(self, df:pd.DataFrame, columns_to_remove:list) -> pd.DataFrame:
        '''
            This function removes columns based on the correlation analysis.

            Parameters:
            - df: DataFrame containing the data.
            - columns_to_remove: List of columns to be removed.

            Returns:
            - DataFrame with the specified columns removed.
        '''

        logging.info(f'Removing highly correlated columns: {columns_to_remove}')

        df.drop(columns=columns_to_remove, inplace=True)
        return df



    # TODO: decidere se eliminare la feature struttura_erogazione con il dato sbagliato 'PRESIDIO OSPEDALIERO UNIFICATO' e usarlo nel post-processing o se gestirlo prima.
    # Modifichiamo PRESIDIO OSPEDALIERO UNIFICATO con le relative provincie e rimuoviamo la colonna codice_struttura_erogazione

    # 11/08/2024
    # DONE - TODO: aggiungere colonna eta
    # DONE - TODO: rimuovere colonne ora inizio e fine erogazione e aggiungere durata
    # DONE - TODO: imputare in valori mancanti in durata erogazione con la media della durata per attività
    def feature_selection_execution(self, config:dict) -> pd.DataFrame:

        logging.basicConfig(filename=config['general']['logging_level'], format='%(asctime)s - %(message)s', level=logging.INFO)

        '''
            This function executes the feature selection process

            Parameters:
            - df: The DataFrame containing the data.

            Returns:
            - The DataFrame with removed columns
        '''

        global columns_pairs


        # Clean 'codice_struttura_erogazione' column
        df = self.__clean_codice_struttura_erogazione(self.df)

        # Remove 'data_disdetta' column cause all the data is null
        df = self.__remove_data_disdetta(df)

        # Create 'durata_erogazione' column, and remove outliers
        logging.info('Pipeline for durata_erogazione column')
        df = self.__colonna_durata_erogazione(df)
        df = self.dataCleaning.impute_durata_erogazione(df)
        df = self.dataCleaning.identify_and_remove_outliers_boxplot(df, ['durata_erogazione_sec'])
        df = self.__remove_ora_inizio_fine_erogazione(df)
        logging.info('End of pipeline for durata_erogazione column')

        # Remove code columns with unique correlation
        df, columns_pairs = self.__remove_columns_with_unique_correlation(df, columns_pairs)

        # Create 'eta' column
        df = self.__colonna_fascia_eta(df)
        df = self.__colonne_anno_e_quadrimestre(df)


        ''' 
            Remove highly correlated columns 
        '''
        # Calculate the correlation matrix
        corr_cols = [
            'sesso', 'regione_residenza', 'asl_residenza', 'provincia_residenza', 'comune_residenza',
            'descrizione_attivita', 'regione_erogazione', 'asl_erogazione', 'provincia_erogazione',
            'struttura_erogazione', 'tipologia_struttura_erogazione', 'tipologia_professionista_sanitario', 'fascia_eta'
        ]

        correlations = self.__calculate_correlation_matrix(df, corr_cols)
        self.__visualize_correlation_matrix(correlations, name = 'graphs/Heatmap_1.png')

        # After analyzing the heatmap, we decide to remove the following columns
        columns_to_remove = [
                'comune_residenza', 'asl_residenza', 'provincia_residenza', 'regione_erogazione', 'asl_erogazione', 'provincia_erogazione', 'struttura_erogazione'
        ]
        # Remove the highly correlated columns
        df = self.__remove_highly_correlated_columns(df, columns_to_remove)

        # Update the list of columns pairs removing the ones that have been removed
        new_corr_cols = ['sesso', 
            'regione_residenza', 
            # 'asl_residenza', 
            # 'provincia_residenza',
            # 'comune_residenza',
            'descrizione_attivita',
            # 'regione_erogazione',
            # 'asl_erogazione',
            # 'provincia_erogazione',
            # 'struttura_erogazione',
            'tipologia_struttura_erogazione',
            'tipologia_professionista_sanitario',
            'fascia_eta']
        
        # Calculate the correlation matrix
        correlations = self.__calculate_correlation_matrix(df, new_corr_cols)
        self.__visualize_correlation_matrix(correlations, name = 'graphs/Heatmap_2.png')

        '''
            End of remove highly correlated columns
        '''

        # Save the DataFrame to a parquet file
        df.to_parquet('data/processed/feature_selected_data.parquet')
    
        return df