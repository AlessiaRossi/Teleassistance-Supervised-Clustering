import pandas as pd
import plotly.express as px



def scatter_map(data):

    '''
    Analyzes the geographical distribution of clusters by region (regione_residenza) in Italy using a scatter map.
    This function identifies the dominant cluster in each region and visualizes the result on an interactive map.
    '''

    # Define latitude and longitude for each region in Italy
    # These coordinates are used to accurately place each region on the map
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

    # Convert the dictionary to a DataFrame for easier manipulatio
    coords_df = pd.DataFrame.from_dict(region_coords, orient='index', columns=['latitude', 'longitude']).reset_index()  # Reset the index, so 'regione_residenza' becomes a column
    coords_df.rename(columns={'index': 'regione_residenza'}, inplace=True) # Rename the columns

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

    # Create a DataFrame for visualization containing the region, dominant cluster, and percentage
    map_data = pd.DataFrame({
        'regione_residenza': max_cluster_per_region.index,
        'cluster': max_cluster_per_region.values,
        'percentage': max_percentage_per_region.values
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
        hover_data=['percentage'],
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


def age_group_bar_chart(data):
    '''
    Analysis of the age group distribution (fascia_eta) by cluster, using a bar chart.
    This function identifies the dominant cluster within each age group and visualizes the results.
    '''

    # Calculate the percentage of each age group belonging to each cluster
    # The result is a crosstab that shows the percentage distribution of clusters within each age group
    df_crosstab = pd.crosstab(data['fascia_eta'], data['cluster'], normalize='index') * 100

    # Find the cluster with the highest percentage for each age group
    df_max_cluster = df_crosstab.idxmax(axis=1)

    # Extract the corresponding highest percentages for each age group
    df_max_percentage = df_crosstab.max(axis=1)

    # Create a DataFrame for plotting the bar chart with age group, cluster, and percentage
    pie_data = pd.DataFrame({
        'age_group': df_max_cluster.index,
        'percentage': df_max_percentage,
        'cluster': df_max_cluster.values
    })

    # Define a color map for clusters
    cluster_colors = {
        0: 'skyblue',
        1: 'lightgreen',
        2: 'lightcoral',
        3: 'gold',
        # Add more colors if there are more clusters
    }

    # Create a bar chart using Plotly to visualize the age group distribution by cluster
    fig = px.bar(
        pie_data,
        x='age_group',
        y='percentage',
        color='cluster',
        color_discrete_map=cluster_colors,
        title='Distribuzione delle fasce d\'età per cluster',
        labels={'age_group': 'fascia età', 'percentage': 'Percentuale massima di appartenenza al cluster (%)',
                'cluster': 'Cluster'},
    )

    # Customize the chart layout, including the axis labels and chart width
    fig.update_layout(
        xaxis_title='Fascia d\'età',
        yaxis_title='Percentuale (%)',
        legend_title='Cluster',
        xaxis_tickangle=-45,
        width=900  # Increase the width of the chart
    )

    return df_max_cluster, df_max_percentage, df_crosstab, fig


def teleassistance_variation_bar_chart(data):
    '''
    Analysis of the teleassistance variation distribution (incremento_teleassistenze) by cluster, using a bar chart.
    This function visualizes how teleassistance variations are distributed across different clusters.
    '''

    # Calculate the frequency of each 'incremento_teleassistenze' category per cluster
    # This groups the data by cluster and teleassistance variation and counts the occurrences
    cluster_counts = data.groupby(['cluster', 'incremento_teleassistenze']).size().reset_index(name='count')

    # Create an interactive bar chart with Plotly to visualize the distribution of teleassistance variations by cluster
    fig = px.bar(
        cluster_counts,
        x='cluster',
        y='count',
        color='incremento_teleassistenze',
        title='Distribuzione delle variazioni delle teleassistenze per cluster',
        labels={'cluster': 'Cluster', 'count': 'Numero di occorrenze',
                'incremento_teleassistenze': 'Teleassistance Variation'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customize the chart layout, including the axis labels and legend title
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Numero di occorrenze',
        legend_title='Variazione Teleassistenza',
    )

    return fig


def healthcare_professional_bar_chart(data):
    '''
    Analysis of the healthcare professional distribution (tipologia_professionista_sanitario) by cluster, using a bar chart.
    This function visualizes the distribution of different types of healthcare professionals across clusters.
    '''

    # Calculate the frequency of each type of healthcare professional per cluster
    # This groups the data by cluster and type of healthcare professional and counts the occurrences
    cluster_counts = data.groupby(['cluster', 'tipologia_professionista_sanitario']).size().reset_index(name='count')

    # Create an interactive bar chart with Plotly to visualize the distribution of healthcare professionals by cluster
    fig = px.bar(
        cluster_counts,
        x='cluster',
        y='count',
        color='tipologia_professionista_sanitario',
        title='Distribuzione dei professionisti sanitari per cluster',
        labels={'cluster': 'Cluster', 'count': 'Numero di professionisti', 'tipologia_professionista_sanitario': 'Tipo di Professionista'},
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Customize the chart layout, including the axis labels and legend title
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
    '''
    Analysis of the gender distribution (sesso) by cluster, using a bar chart.
    This function visualizes the percentage distribution of genders across different clusters.
    '''

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

    return sex_crosstab, max_sex_per_cluster, max_percentage_per_cluster, fig
