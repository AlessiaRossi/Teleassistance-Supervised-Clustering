import pandas as pd
import plotly.express as px


def scatter_map(data):
    ''' Analysis of the geographical distribution (region_residence) by cluster, using a scatter map. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'region_residence' and 'cluster'.

    Returns:
        pandas.Series: The dominant cluster for each region.
        pandas.Series: The percentage of the dominant cluster for each region.
        plotly.graph_objects.Figure: The generated scatter map figure.
 '''

    # Add latitude and longitude for each region
    region_coords = {
        'Abruzzo': (42.351221, 13.398438),
        'Basilicata': (40.639470, 15.805148),
        'Calabria': (38.905975, 16.594401),
        'Campania': (40.839565, 14.250849),
        'Emilia-Romagna': (44.494887, 11.342616),
        'Friuli Venezia Giulia': (45.649526, 13.776818),
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
        'Trentino-Alto Adige': (46.499334, 11.356624),
        'Umbria': (43.112203, 12.388784),
        'Valle d\'Aosta': (45.737502, 7.320149),
        'Veneto': (45.434904, 12.338452)
    }

    # Convert the dictionary to a DataFrame
    coords_df = pd.DataFrame.from_dict(region_coords, orient='index', columns=['latitude', 'longitude']).reset_index()
    coords_df.rename(columns={'index': 'regione_residenza'}, inplace=True)

    # Merge the data with the coordinates
    data = pd.merge(data, coords_df, on='regione_residenza')

    # Calculate the percentage of each cluster for each region
    region_cluster_crosstab = pd.crosstab(data['regione_residenza'], data['cluster'], normalize='index') * 100

    # Identify the cluster with the highest percentage for each region
    max_cluster_per_region = region_cluster_crosstab.idxmax(axis=1)

    # Extract the corresponding highest percentages for each region
    max_percentage_per_region = region_cluster_crosstab.max(axis=1)

    # Create a DataFrame for the map
    map_data = pd.DataFrame({
        'regione_residenza': max_cluster_per_region.index,
        'cluster': max_cluster_per_region.values,
        'percentage': max_percentage_per_region.values
    })

    # Merge with coordinates
    map_data = pd.merge(map_data, coords_df, on='regione_residenza')

    # Create a scatter map with Plotly
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

    # Customize the map
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=41.8719, lon=12.5674),  # Centered on Italy
            zoom=5
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(
            x=0.99,  # Positioned at the top right
            y=0.99,  # Positioned at the top right
            xanchor='right',
            yanchor='top',
            traceorder='normal',
            font=dict(size=12),
            bgcolor='rgba(0, 0, 0, 0.7)',  # Dark background color with transparency
            bordercolor='white',  # White border color
            borderwidth=1  # Border width
        )
    )

    return max_cluster_per_region, max_percentage_per_region,fig

t
def age_group_bar_chart(data):
    ''' Analysis of the age group distribution (fascia_eta) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'fascia_eta' and 'cluster'.

    Returns:
        pandas.Series: The dominant cluster for each age group.
        pandas.Series: The percentage of the dominant cluster for each age group.
        pandas.Series: The dominant increment category for each age group.
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''

    # Create crosstab for teleassistance increment per age group
    df_crosstab_increment = pd.crosstab(data['fascia_eta'], data['incremento_teleassistene'], normalize='index') * 100
    
    # Identify the increment category with the highest percentage per age group
    df_max_increment = df_crosstab_increment.idxmax(axis=1)
    df_max_percentage_increment = df_crosstab_increment.max(axis=1)

    #Create crosstab for clusters per age group
    df_crosstab_cluster = pd.crosstab(data['fascia_eta'], data['cluster'], normalize='index') * 100

    # Identify the cluster with the highest percentage per age group
    df_max_cluster = df_crosstab_cluster.idxmax(axis=1)

    # Create a DataFrame for the bar chart
    pie_data = pd.DataFrame({
        'age_group': df_max_increment.index,
        'incremento_teleassistenze': df_max_increment.values,
        'percentage_increment': df_max_percentage_increment,
        'dominant_cluster': df_max_cluster.values  # Add dominant cluster information
    })

    # Create a bar chart using Plotly
    fig = px.bar(
        pie_data,
        x='age_group',
        y='percentage',
        color='incremento_teleassistenze',
        text='dominant_cluster',  # Add dominant cluster as text inside bars
        title='Distrbuzione delle fasce d\'età per variazione teleassistenza e cluster dominante',
        labels={'age_group': 'Fascia età', 'percentage': 'Percentuale massima di appartenenza al cluster (%)', 'incremento_teleassistenze': 'Variazione Teleassistenza'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customize the chart
    fig.update_layout(
        xaxis_title='Fascia d\'età',
        yaxis_title='Percentuale di incremento (%)',
        xaxis_tickangle=-45,
        width=900  # Increase the width of the chart
    )

    return df_max_increment,df_max_percentage_increment,df_max_cluster, fig


def teleassistance_variation_bar_chart(data):
    ''' Analysis of the teleassistance variation distribution (incremento_teleassistenze) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'incremento_teleassistenze' and 'cluster'.

    Returns:
        pandas.DataFrame: The dominant increment category for each cluster and percentage.
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

    # Create an interactive bar chart with Plotly
    fig = px.bar(
        cluster_counts,
        x='cluster',
        y='percentage',
        color='incremento_teleassistenze',
        title='Distribuzione delle variazioni delle teleassistenze per cluster',
        labels={'cluster': 'Cluster', 'percentage': 'Percentuale incremento (%)',
                'incremento_teleassistenze': 'Teleassistance Variation'},
        barmode='group',
    ),

    # Customize the chart
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Percentuale di incremento (%)',
        legend_title='Variazione Teleassistenza',
    )

    return result,fig


def healthcare_professional_bar_chart(data):
    ''' Analysis of the healthcare professional distribution (tipologia_professionista_sanitario) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'tipologia_professionista_sanitario' and 'cluster'.

    Returns:
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''

    # Calculate the frequency of each type of healthcare professional per cluster
    cluster_counts = data.groupby(['cluster', 'tipologia_professionista_sanitario','incremento_teleassistenze']).size().reset_index(name='count')

    # Calculate the total for each cluster to obtain percentages
    total_counts_per_cluster = cluster_counts.groupby('cluster')['count'].sum().reset_index(name='total_count')

    # Merge total counts with clusters to calculate percentages
    cluster_counts = cluster_counts.merge(total_counts_per_cluster, on='cluster')
    cluster_counts['percentage'] = (cluster_counts['count'] / cluster_counts['total_count']) * 100

    # Identify the dominant 'incremento_teleassistenze' category for each healthcare professional
    dominant_increment_per_professional = cluster_counts.loc[
        cluster_counts.groupby('tipologia_professionista_sanitario')['percentage'].idxmax()]

    # Create an interactive bar chart with Plotly
    fig = px.bar(
        dominant_increment_per_professional,
        y='tipologia_professionista_sanitario',
        x='percentage',
        color='tipologia_professionista_sanitario',
        text='cluster',  # Show the cluster number inside the bars
        title='Distribuzione dei professionisti sanitari per cluster ed incremento teleassistenza',
        labels={
            'tipologia_professionista_sanitario': 'Type of Professional',
            'percentage': 'Increment Percentage (%)',
            'cluster': 'Cluster',
            'incremento_teleassistenze': 'Teleassistance Increment'
        },
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
        xaxis_title='Cluster',
        yaxis_title='Numero di professionisti',
        legend_title='Tipo di Professionista',
        legend=dict(
            x=1.05,  # Horizontal position of the legend
            y=1,     # Vertical position of the legend
            traceorder='normal'  # Order of items in the legend
        )
    )

    return fig


def gender_distribution_chart(data):
    ''' Analysis of the gender distribution (sesso) by cluster, using a bar chart. 
    
    Args:
        data (pandas.DataFrame): The DataFrame containing the teleassistance data with columns 'sesso' and 'cluster'.

    Returns:
        pandas.DataFrame: The percentage of each gender within each cluster 
        pandas.Series: The dominant percentages for each cluster
        pandas.Series: The dominant percentages of each gender within each cluster
        plotly.graph_objects.Figure: The generated bar chart figure.
    '''

    # Calculate the percentage of each gender within each cluster
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

    return sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster, fig


def teleassistance_cluster_increments_chart(data):
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
  df_max_cluster = df_crosstab_increment.idxmax(axis=1)
  # Extract the corresponding highest percentages for each year-increment combination
  df_max_percentage_increment = df_crosstab_increment.max(axis=1)

  # Create a DataFrame with bar chart data
  bar_data = pd.DataFrame({
      'anno': [index[0] for index in df_crosstab_increment.index],
      'incremento_teleassistenze': [index[1] for index in df_crosstab_increment.index],
      'percentage_increment': df_max_percentage_increment.values,
      'dominant_cluster': df_max_cluster.values
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
      labels={'anno': 'Anno', 'percentage_increment': 'Percentuale Incremento (%)', 'incremento_teleassistenze': 'Variazione Teleassistenza'},
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

  return df_max_cluster,df_max_percentage_increment,fig