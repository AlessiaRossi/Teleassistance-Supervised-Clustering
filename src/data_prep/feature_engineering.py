import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

def incremento_labelling(df: pd.DataFrame, cols_grouped: list) -> pd.DataFrame:
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


def classify_increment(value):
    constat_increment = 5 
    low_increment = 15
    medium_increment = 40

    # DONE - TODO: fixare, bisogna mettere >= 0 nel primo if
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
    

def sample_cassification(incremento_percentuale_medio: pd.DataFrame, df: pd.DataFrame, df_cols_no_anno: list):
    # Apply the function to classify the average percentage increment
    incremento_percentuale_medio['incremento_teleassistenze'] = incremento_percentuale_medio['incremento_percentuale'].apply(classify_increment)

    logging.info(incremento_percentuale_medio['incremento_teleassistenze'].value_counts())

    # Merge the classification with the original dataframe
    df = df.merge(incremento_percentuale_medio[df_cols_no_anno + ['incremento_teleassistenze']], 
              on=df_cols_no_anno, 
              how='left')
    
    return df


def histplot_avg_incremento_distribution(incremento_percentuale_medio: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.histplot(incremento_percentuale_medio['incremento_percentuale'], bins=30, kde=True)
    plt.title('Distribuzione degli Incrementi Medi Percentuali')
    plt.xlabel('Incremento Percentuale Medio')
    plt.ylabel('Frequenza')
    plt.savefig('graphs/avg_incremento_percentuale_histplot.png')


def boxplot_avg_incremento_distribution(incremento_percentuale_medio: pd.DataFrame):
    # Boxplot per identificare outliers
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=incremento_percentuale_medio['incremento_percentuale'])
    plt.title('Boxplot degli Incrementi Medi Percentuali')
    plt.xlabel('Incremento Percentuale')
    plt.savefig('graphs/avg_incremento_percentuale_boxplot.png')
    

def feature_engineering_execution(df: pd.DataFrame, cols_grouped: list) -> pd.DataFrame:

    # questo è un TODO definito nel file feature_selection.py ma ancora non fatto
    df.drop(columns=['codice_struttura_erogazione'], inplace=True)

    incremento_percentuale_medio, df_cols_no_anno = incremento_labelling(df, cols_grouped)

    logging.info(incremento_percentuale_medio['incremento_percentuale'].describe())

    # Plot the distribution of the average percentage increment
    histplot_avg_incremento_distribution(incremento_percentuale_medio)
    boxplot_avg_incremento_distribution(incremento_percentuale_medio)

    # Apply the classification of the average percentage increment
    df = sample_cassification(incremento_percentuale_medio, df, df_cols_no_anno)

    return df