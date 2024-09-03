import pandas as pd
import plotly.express as px



def scatter_map(data):
    ''' Analysis of the geographical distribution (region_residence) by cluster, using a scatter map. '''

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
        hover_data=['percentage'],
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




