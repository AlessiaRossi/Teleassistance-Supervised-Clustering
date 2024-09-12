import pandas as pd
import plotly.express as px
import logging
import seaborn as sns
import matplotlib.pyplot as plt


def scatter_map(data):
    ''' Analysis of the geographical distribution (region_residence) by cluster, using a scatter map. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'region_residence' and 'cluster'.

    Returns:
        pandas.Series: The dominant cluster for each region.
        pandas.Series: Percentage of each region within each cluster
        pandas.Series: The dominant increment category for each region.
        plotly.graph_objects.Figure: The generated scatter map figure.
 '''

    # Define latitude and longitude for each region in Italy
    # These coordinates are used to accurately place each region on the map
    # Add latitude and longitude for each region
    region_coords = {
        'Abruzzo': (42.351221, 13.398438),
        'Basilicata': (40.639470, 15.805148),
        'Calabria': (38.905975, 16.594401),
        'Campania': (40.839565, 14.250849),
        'Emilia romagna': (44.494887, 11.342616),
        'Friuli venezia giulia': (45.649526, 13.776818),
        'Lazio': (41.892770, 12.482520),
        'Liguria': (44.411308, 8.932699),
        'Lombardia': (45.466797, 9.190498),
        'Marche': (43.616759, 13.518875),
        'Molise': (41.561918, 14.668747),
        'Piemonte': (45.070312, 7.686856),
        'Puglia': (41.125595, 16.866667),
        'Sardegna': (39.215311, 9.110616),
        'Sicilia': (37.600000, 14.015356),
        'Toscana': (43.769560, 11.255814),
        'Prov. auton. trento': (46.074779, 11.121749),
        'Prov. auton. bolzano': (46.4982953, 11.3547582),
        'Umbria': (43.112203, 12.388784),
        'Valle d\'aosta': (45.737502, 7.320149),
        'Veneto': (45.434904, 12.338452)
    }

    # Convert the dictionary to a DataFrame for easier manipulatio
    coords_df = pd.DataFrame.from_dict(region_coords, orient='index', columns=['latitude',
                                                                               'longitude']).reset_index()  # Reset the index, so 'regione_residenza' becomes a column
    coords_df.rename(columns={'index': 'regione_residenza'}, inplace=True)  # Rename the columns

    # Merge the data with the coordinates based on the region of residence
    # This step adds latitude and longitude to the main data for each region
    data = pd.merge(data, coords_df, on='regione_residenza')

    # Calculate the percentage distribution of clusters within each region
    # The result is a crosstab that shows the percentage of each cluster in each region
    region_cluster_crosstab = pd.crosstab(data['regione_residenza'], data['cluster'], normalize='index') * 100

    # Identify the cluster with the highest percentage for each region
    max_cluster_per_region = region_cluster_crosstab.idxmax(axis=1)

    # Extract the max percentages for each region
    max_percentage_per_region = region_cluster_crosstab.max(axis=1)

    # Identify the incremento_teleassistenze with the highest percentage for each region
    max_increment_teleassistenze = data.groupby('regione_residenza')['incremento_teleassistenze'].max()

    # Create a DataFrame for visualization containing the region, dominant cluster, and percentage
    map_data = pd.DataFrame({
        'regione_residenza': max_cluster_per_region.index,
        'cluster': max_cluster_per_region.values,
        'percentage': max_percentage_per_region.values,
        'incremento_teleassistenze': max_increment_teleassistenze.values  # Incremento teleassistenza
    })

    # Merge with coordinates to plot the map
    map_data = pd.merge(map_data, coords_df, on='regione_residenza')

    # Create a scatter map using Plotly
    fig = px.scatter_mapbox(
        map_data,
        lat='latitude',
        lon='longitude',
        color='cluster',
        size='percentage',
        hover_name='regione_residenza',
        hover_data={
            'cluster': True,  # Mostra il numero del cluster
            'percentage': ':.2f',  # Mostra la percentuale di incremento
            'incremento_teleassistenze': True  # Mostra incremento teleassistenza
        },
        title='Cluster con percentuale di appartenenza maggiore per regione in Italia',
        color_continuous_scale=px.colors.cyclical.IceFire,
        mapbox_style='carto-positron',
        zoom=5
    )

    # Customize the map layout, including centering on Italy and adjusting the legend
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=41.8719, lon=12.5674),  # Centered on Italy
            zoom=5
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            x=0.99,  # Positioned at the top right
            y=0.99,  # Positioned at the top right
            xanchor='right',
            yanchor='top',
            traceorder='normal',
            font=dict(size=12),
            bgcolor='rgba(0, 0, 0, 0.7)',  # Dark background color with transparency
            bordercolor='black',  # black  border color
            borderwidth=1  # Border width
        )
    )

    # fig.savefig('graphs/scatter_map.png')
    return max_increment_teleassistenze, max_cluster_per_region, max_percentage_per_region, fig


def age_group_bar_chart(data):
    ''' Analysis of the age group distribution (fascia_eta) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'fascia_eta' and 'cluster'.

    Returns:
        pandas.Series: The dominant cluster for each age group.
        pandas.Series: Highest percentage of increment type per age group.
        pandas.Series: The dominant increment category for each age group.
        pandas.DataFrame: The percentage of each cluster per age group.
        pandas.DataFrame: The percentage of each increment type per age group.
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''

    # Create crosstab for teleassistance increment per age group
    df_crosstab_increment = pd.crosstab(data['fascia_eta'], data['incremento_teleassistenze'], normalize='index') * 100

    # Identify the increment category with the highest percentage per age group
    df_max_increment = df_crosstab_increment.idxmax(axis=1)
    ## Identify the highest percentage of increment type per age group
    df_max_percentage_increment = df_crosstab_increment.max(axis=1)

    # Create crosstab for clusters per age group
    df_crosstab_cluster = pd.crosstab(data['fascia_eta'], data['cluster'], normalize='index') * 100

    # Identify the cluster with the highest percentage per age group
    df_max_cluster = df_crosstab_cluster.idxmax(axis=1)

    # Create a DataFrame for plotting the bar chart with age group, cluster, and percentage
    pie_data = pd.DataFrame({
        'age_group': df_max_increment.index,
        'incremento_teleassistenze': df_max_increment.values,
        'percentage_increment': df_max_percentage_increment,
        'dominant_cluster': df_max_cluster.values  # Add dominant cluster information
    })

    # Create a bar chart using Plotly to visualize the age group distribution by cluster
    fig = px.bar(
        pie_data,
        x='age_group',
        y='percentage_increment',
        color='incremento_teleassistenze',
        text='dominant_cluster',  # Add dominant cluster as text inside bars
        title='Distrbuzione delle fasce d\'età per variazione teleassistenza e cluster dominante',
        labels={'age_group': 'Fascia età', 'percentage_increment': 'Percentuale massima per tipo di incremento (%)',
                'incremento_teleassistenze': 'Variazione Teleassistenza'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customize the chart layout, including the axis labels and chart width
    fig.update_layout(
        xaxis_title='Fascia d\'età',
        yaxis_title='Percentuale di incremento (%)',
        xaxis_tickangle=-45,
        width=900  # Increase the width of the chart
    )
    # Show text (cluster numbers) on top of the bars
    fig.update_traces(textposition='outside')

    # fig.savefig('graphs/age_group_bar_chart.png')
    return df_max_increment, df_max_percentage_increment, df_max_cluster,df_crosstab_cluster,df_crosstab_increment,fig


def teleassistance_variation_bar_chart(data):
    ''' Analysis of the teleassistance variation distribution (incremento_teleassistenze) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'incremento_teleassistenze' and 'cluster'.

    Returns:
        pandas.DataFrame: Frequency of incremento_teleassistenze categories per cluster.
        pandas.DataFrame: Cluster with the highest percentage for each increment category.
        plotly.graph_objects.Figure: The generated bar chart figure.

    '''

    # Calculate the frequency of each 'incremento_teleassistenze' category per cluster
    cluster_counts = data.groupby(['cluster', 'incremento_teleassistenze']).size().reset_index(name='count')

    # Calculate the total count per cluster to compute percentages
    total_counts_per_cluster = cluster_counts.groupby('cluster')['count'].sum().reset_index(name='total_count')

    # Merge total counts with cluster counts to calculate percentages
    cluster_counts = cluster_counts.merge(total_counts_per_cluster, on='cluster')
    cluster_counts['percentage'] = (cluster_counts['count'] / cluster_counts['total_count']) * 100

    # Identify the 'incremento_teleassistenze' category with the highest count for each cluster
    dominant_increment_per_cluster = cluster_counts.loc[cluster_counts.groupby('cluster')['count'].idxmax()]

    # Extract the cluster, 'incremento_teleassistenze' category, and percentage
    result = dominant_increment_per_cluster[['cluster', 'incremento_teleassistenze', 'percentage']]

    # Create an interactive bar chart with Plotly to visualize the distribution of teleassistance variations by cluster
    fig = px.bar(
        cluster_counts,
        x='cluster',
        y='percentage',
        color='incremento_teleassistenze',
        title='Distribuzione delle variazioni delle teleassistenze per cluster',
        labels={'cluster': 'Cluster', 'percentage': 'Percentuale incremento (%)',
                'incremento_teleassistenze': 'Teleassistance Variation'},
        barmode='group',
    )

    # Customize the chart layout, including the axis labels and legend title
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Percentuale di incremento (%)',
        legend_title='Variazione Teleassistenza',
    )

    # fig.savefig('graphs/teleassistance_variation_bar_chart.png')
    return cluster_counts , result, fig


def healthcare_professional_bar_chart(data):
    ''' Analysis of the healthcare professional distribution (tipologia_professionista_sanitario) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'tipologia_professionista_sanitario' and 'cluster'.

    Returns:
        pandas.DataFrame: Frequency of healthcare professionals per teleassistence increment and dominant cluster.
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''

    # Calculate the frequency of each type of healthcare professional per cluster
    cluster_counts = data.groupby(
        ['cluster', 'tipologia_professionista_sanitario', 'incremento_teleassistenze']).size().reset_index(name='count')

    # Calculate the total for each cluster to obtain percentages
    total_counts_per_cluster = cluster_counts.groupby('cluster')['count'].sum().reset_index(name='total_count')

    # Merge total counts with clusters to calculate percentages
    cluster_counts = cluster_counts.merge(total_counts_per_cluster, on='cluster')
    cluster_counts['percentage'] = (cluster_counts['count'] / cluster_counts['total_count']) * 100

    # Identify the dominant 'incremento_teleassistenze' category for each healthcare professional
    dominant_increment_per_professional = cluster_counts.loc[
        cluster_counts.groupby('tipologia_professionista_sanitario')['percentage'].idxmax()]

    # Create an interactive bar chart with Plotly to visualize the distribution of healthcare professionals by cluster
    fig = px.bar(
        dominant_increment_per_professional,
        x='tipologia_professionista_sanitario',
        y='percentage',
        color='incremento_teleassistenze',
        text='cluster',
        title='Distribuzione dei professionisti sanitari per incremento teleassistenza e cluster dominante ',
        labels={'tipologia_professionista_sanitario': 'Tipo di professionista',
                'percentage': 'Percentuale incremento(%)',
                'cluster': 'Cluster',
                'incremento_teleassistenze': 'Incremento Teleassistenza'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Customize the appearance of text labels inside the bars
    fig.update_traces(
        textposition='outside',  # Text displayed inside the bars
        textfont_size=12,
        textfont_color='black'  # Black text color
    )

    # Customize the chart
    fig.update_layout(
        xaxis_title='Tipo di professionista sanitario',
        yaxis_title='Percentuale di incremento (%)',
        showlegend=True,  # Show the legend
        legend=dict(
            x=1.05,  # Horizontal position of the legend
            y=1,  # Vertical position of the legend
            traceorder='normal'  # Order of items in the legend
        )
    )

    # fig.savefig('graphs/healtcare_professional_bar_chart.png')
    return dominant_increment_per_professional , fig


def gender_cluster_distribution_chart(data):
    ''' Analysis of the gender distribution (sesso) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'sesso' and 'cluster'.

    Returns:
        pandas.DataFrame: The percentage of each gender within each cluster 
        pandas.Series: The dominant cluster for each gender.
        pandas.Series: The dominant percentages of each gender within each cluster
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''
    print(data.columns)

    # Calculate the percentage of each gender within each cluster
    # The result is a crosstab that shows the gender distribution within each cluster
    sex_crosstab = pd.crosstab(data['sesso'], data['cluster'], normalize='index') * 100

    max_sex_per_cluster = sex_crosstab.idxmax(axis=1)

    # Extract the corresponding highest percentages for each cluster
    max_percentage_per_cluster = sex_crosstab.max(axis=1)

    # Melt the crosstab DataFrame for easier plotting
    melted_gender_data = sex_crosstab.reset_index().melt(id_vars='sesso', var_name='cluster', value_name='percentage')

    # Create a bar chart using Plotly
    fig = px.bar(
        melted_gender_data,
        x='cluster',
        y='percentage',
        color='sesso',
        title='Distribuzione di uomini e donne per cluster',
        labels={'cluster': 'Cluster', 'percentage': 'Percentuale (%)', 'sesso': 'Sesso'},
        barmode='group',
        color_discrete_map={'female': '#FF69B4', 'male': '#1E90FF'}
    )

    # Customize the chart
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Percentuale',
        legend_title='Sesso',
        bargap=0.4
    )

    # fig.savefig('graphs/gender_distribution_chart.png')
    return sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster, fig

def increment_gender_distribution_chart(data):
    ''' Analysis of the gender distribution (sesso) by increment type, using a bar chart.

    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'sesso' and 'incremento_teleassistenze'.

    Returns:
        pandas.DataFrame: The percentage of each gender within each increment type.
        pandas.Series: The dominant increment type for each gender.
        pandas.Series: The dominant percentages of each gender within each increment type.
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''
    # Calculate the percentage of each gender within each increment type
    sex_crosstab = pd.crosstab(data['sesso'], data['incremento_teleassistenze'], normalize='index') * 100

    # Identify the gender with the highest percentage for each increment type
    max_sex_per_inc = sex_crosstab.idxmax(axis=1)

    # Extract the corresponding highest percentages of samples for each increment type
    max_percentage_per_inc = sex_crosstab.max(axis=1)

    # Melt the crosstab DataFrame for easier plotting
    melted_gender_data = sex_crosstab.reset_index().melt(id_vars='sesso', var_name='incremento_teleassistenze',
                                                         value_name='percentage')

    # Create a bar chart using Plotly
    fig = px.bar(
        melted_gender_data,
        x='incremento_teleassistenze',
        y='percentage',
        color='sesso',
        title='Distribuzione di uomini e donne per variazione incremento teleassistenza',
        labels={'cluster': 'Cluster', 'percentage': 'Percentuale (%)', 'sesso': 'Sesso'},
        barmode='group',
        color_discrete_map={'female': '#FF69B4', 'male': '#1E90FF'}

    )

    # Customize the chart
    fig.update_layout(
        xaxis_title='Tipologia di incremento',
        yaxis_title='Percentuale (%)',
        legend_title='Sesso',
        bargap=0.4
    )

    return sex_crosstab,max_sex_per_inc,max_percentage_per_inc, fig


def year_cluster_increments_chart(data):
    """ Analyzes teleassistance data, identifies dominant clusters for each year-increment combination,
  and creates a bar chart visualizing the distribution.

    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'anno', 'incremento_teleassistenze', and 'cluster'.

    Returns:
        pandas.Series: The dominant cluster for each year-increment combination.
        pandas.Series: The percentage of the dominant cluster for each year-increment combination.
        plotly.graph_objects.Figure: The generated bar chart figure.
  """

    # Create crosstab for percentage and identify dominant clusters
    df_crosstab_increment = (
            pd.crosstab([data['anno'], data['incremento_teleassistenze']], data['cluster'], normalize='index') * 100
    )
    # Identify the cluster with the highest percentage for each year-increment combination
    df_max_cluster_inc = df_crosstab_increment.idxmax(axis=1)
    # Identify the highest percentage of samples of increment type for each combination of year and increment type
    df_crosstab_cluster = (
            pd.crosstab([data['anno'], data['incremento_teleassistenze']], data['cluster'], normalize='index') * 100
    )
    # Identify the percentage of samples of increment type for each combination of year and increment type
    df_max_percentage_increment_cla = df_crosstab_increment.max(axis=1)

    # Create a DataFrame with bar chart data
    bar_data = pd.DataFrame({
        'anno': [index[0] for index in df_crosstab_increment.index],
        'incremento_teleassistenze': [index[1] for index in df_crosstab_increment.index],
        'percentage_increment': df_max_percentage_increment_cla.values,
        'dominant_cluster': df_max_cluster_inc.values
    })

    # Create the bar chart with Plotly
    fig = px.bar(
        bar_data,
        x='anno',
        y='percentage_increment',
        color='incremento_teleassistenze',
        text='dominant_cluster',
        barmode='group',
        title='Distribuzione delle variazioni delle teleassistenze per anno e cluster dominante',
        labels={'anno': 'Anno', 'percentage_increment': 'Percentuale Incremento (%)',
                'incremento_teleassistenze': 'Variazione Teleassistenza'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customize the chart layout
    fig.update_layout(
        xaxis_title='Anno',
        yaxis_title='Percentuale Incremento (%)',
        xaxis_tickangle=-45,
        width=900
    )

    # Show dominant cluster above bars
    fig.update_traces(textposition='outside')

    # fig.savefig('graphs/teleassistance_cluster_increments_chart.png')

    return df_max_cluster_inc, df_max_percentage_increment_cla,df_crosstab_cluster, fig

def heatmap(data):
    ''' Analysis of the cluster distribution by increment type, using a heatmap.

    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'cluster' and 'incremento_teleassistenze'.

    Returns:
        plotly.graph_objects.Figure: The generated heatmap figure.
    '''
    # Calculate the frequency of each combination of cluster and increment type
    cluster_increment_counts = data.groupby(['cluster', 'incremento_teleassistenze']).size().unstack(fill_value=0)

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(cluster_increment_counts, annot=True, fmt='d', cmap='coolwarm', cbar=True)

    # Set titles and labels
    plt.title('Heatmap of Cluster Distribution by Increment Type')
    plt.xlabel('Increment Type')
    plt.ylabel('Cluster')

    # fig.savefig('graphs/heatmap.png')
    return plt

'''def chart_execution(df:pd.DataFrame, config:dict): 
    ''' 'Execute the analysis of the teleassistance data and generate the charts.' '''

    max_cluster_per_region, max_percentage_per_region = scatter_map(df)
    logging.info(f'Dominant cluster per region: {max_cluster_per_region}')
    logging.info(f'Dominant percentage per region: {max_percentage_per_region}')

    df_max_increment,df_max_percentage_increment,df_max_cluster = age_group_bar_chart(df)
    logging.info(f'Dominant increment per age group: {df_max_increment}')
    logging.info(f'Dominant percentage increment per age group: {df_max_percentage_increment}')
    logging.info(f'Dominant cluster per age group: {df_max_cluster}')

    result = teleassistance_variation_bar_chart(df)
    logging.info(f'Dominant increment per cluster: {result}')
    
    healthcare_professional_bar_chart(df)

    sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster = gender_distribution_chart(df)
    logging.info(f'The percentage of each gender within each cluster: {sex_crosstab}')
    logging.info(f'The dominant percentages for each cluster: {max_sex_per_cluster}')
    logging.info(f'The dominant percentagesof each gender within each cluster {max_percentage_per_cluster}')
    

    df_max_cluster_inc,df_max_percentage_increment = teleassistance_cluster_increments_chart(df)
    logging.info(f'Dominant cluster per year-increment combination: {df_max_cluster}')

    return max_cluster_per_region, max_percentage_per_region, df_max_increment, df_max_percentage_increment, df_max_cluster, result,sex_crosstab,max_sex_per_cluster,max_percentage_per_cluster,df_max_cluster_inc,df_max_percentage_increment
'''
