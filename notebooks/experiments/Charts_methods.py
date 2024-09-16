import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# Load the data
file_path = 'inserire il file parquet di clustere data alla feature che ho persol il path (='
data = pd.read_parquet(file_path)


data.columns

data.cluster.value_counts()

data[['incremento_teleassistenze', 'cluster']].value_counts()

# 0 -> high increment   143418
# 1 -> medium increment 103043
# 3 -> low increment    71109
# 2 -> decrement        2393

data[data.cluster == 3][['incremento_teleassistenze', 'cluster']].value_counts()

data.head()

# Calculate the percentage of each gender within each cluster
sex_crosstab = pd.crosstab(data['sesso'], data['cluster'], normalize='index') * 100

# Identify the gender with the highest percentage for each cluster
max_sex_per_cluster = sex_crosstab.idxmax(axis=1)

# Extract the corresponding highest percentages of samples for each cluster
max_percentage_per_cluster = sex_crosstab.max(axis=1)

print("Percentage of each gender within each cluster:")
print(sex_crosstab)

print("\nGender with the highest percentage for each cluster:")
print(max_sex_per_cluster)

print("\nHighest percentage for of samples for each cluster:")
print(max_percentage_per_cluster)

def create_gender_distribution_chart(data):
    """
    Function to analyze the distribution of men and women based on teleassistance increment
    and display the results in an interactive bar chart.

    Parameters:
    - data: DataFrame containing the data with 'sesso', 'incremento_teleassistenze', and 'cluster' columns.
    """
    
    # Step 1: Calculate the number of samples for each combination of gender and increment type
    sex_increment_counts = data.groupby(['sesso', 'incremento_teleassistenze']).size().reset_index(name='count')
    
    # Step 2: Identify the dominant cluster for each increment type
    dominant_cluster_per_inc_gen = data.groupby(['incremento_teleassistenze', 'sesso'])['cluster'].agg(lambda x: x.value_counts().idxmax()).reset_index(name='dominant_cluster')
    
    # Step 3: Merge the counts with the dominant cluster information
    merged_data = pd.merge(sex_increment_counts, dominant_cluster_per_inc_gen, on=['incremento_teleassistenze', 'sesso'])
    
    # Step 4: Create the bar chart using Plotly
    fig = px.bar(
        merged_data,
        x='incremento_teleassistenze',
        y='count',
        color='sesso',
        text='dominant_cluster',  # Display the dominant cluster as text
        title='Distribution of Men and Women by Teleassistance Increment Type and Dominant Cluster',
        labels={'incremento_teleassistenze': 'Increment Type', 'count': 'Number of Samples', 'sesso': 'Gender'},
        barmode='group',
        color_discrete_map={'female': '#FF69B4', 'male': '#1E90FF'}
    )

    # Customize the chart
    fig.update_layout(
        xaxis_title='Increment Type',
        yaxis_title='Number of Samples',
        legend_title='Gender',
        bargap=0.4
    )

    # Show the dominant cluster above the bars
    fig.update_traces(textposition='outside')

    # Return the chart
    return fig

def create_increment_distribution_chart(data):
    """
    Creates a bar chart showing the distribution of teleassistance increments by year and dominant cluster.

    Parameters:
    - data: DataFrame containing 'anno', 'incremento_teleassistenze', and 'cluster' columns.
    
    Returns:
    - fig: Plotly figure object with the bar chart.
    """
    
    # Step 1: Calculate the number of samples for each combination of year and increment type
    df_sample_counts = pd.crosstab([data['anno'], data['incremento_teleassistenze']], data['cluster'])

    # Step 2: Identify the dominant cluster for each combination of year and increment type
    df_max_cluster = df_sample_counts.idxmax(axis=1)

    # Step 3: Identify the highest number of samples for each combination of year and increment type
    df_max_sample_count = df_sample_counts.max(axis=1)

    # Step 4: Create a DataFrame with the necessary information
    bar_data = pd.DataFrame({
        'anno': [index[0] for index in df_sample_counts.index],  # Extract the year
        'incremento_teleassistenze': [index[1] for index in df_sample_counts.index],  # Extract the increment type
        'sample_count': df_max_sample_count.values,  # Number of samples
        'dominant_cluster': df_max_cluster.values  # Dominant cluster
    })

    # Step 5: Create the bar chart with Plotly
    fig = px.bar(
        bar_data,
        x='anno',
        y='sample_count',
        color='incremento_teleassistenze',  # Color by increment type
        text='dominant_cluster',  # Display dominant cluster as text on top of the bars
        barmode='group',  # Group bars by year
        title='Distribution of Teleassistance Increments by Year and Dominant Cluster',
        labels={'anno': 'Year', 'sample_count': 'Number of Samples', 'incremento_teleassistenze': 'Teleassistance Variation'},
        color_discrete_sequence=px.colors.qualitative.Pastel  # Use pastel color palette
    )

    # Step 6: Customize the chart
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of Samples',
        xaxis_tickangle=-45,  # Rotate x-axis labels by 45 degrees
        width=900  # Set chart width
    )

    # Step 7: Show the dominant cluster above the bars
    fig.update_traces(textposition='outside')

    # Return the chart
    return fig

def create_increment_scatter_map(data):
    """
    Creates a scatter map showing the highest percentage increment of teleassistance for each region in Italy.

    Parameters:
    - data: DataFrame containing 'regione_residenza', 'incremento_teleassistenze', and 'cluster' columns.
    
    Returns:
    - fig: Plotly figure object with the scatter map.
    """
    
    # Step 1: Define the coordinates for each region
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
        'Prov. auton. trento': (46.499334, 11.356624),
        'Umbria': (43.112203, 12.388784),
        'Valle d\'aosta': (45.737502, 7.320149),
        'Prov. auton. bolzano': (46.4982953, 11.3547582),
        'Veneto': (45.434904, 12.338452)
    }

    # Step 2: Convert the dictionary to a DataFrame
    coords_df = pd.DataFrame.from_dict(region_coords, orient='index', columns=['latitude', 'longitude']).reset_index()
    coords_df.rename(columns={'index': 'regione_residenza'}, inplace=True)

    # Step 3: Merge the data with the coordinates
    data = pd.merge(data, coords_df, on='regione_residenza')

    # Step 4: Calculate the percentage of each increment for each region
    region_inc_crosstab = pd.crosstab(data['regione_residenza'], data['incremento_teleassistenze'], normalize='index') * 100

    # Step 5: Identify the increment with the highest percentage for each region
    max_inc_per_region = region_inc_crosstab.idxmax(axis=1)

    # Step 6: Extract the corresponding highest percentages of each increment for each region
    max_percentage_per_region = region_inc_crosstab.max(axis=1)

    # Step 7: Calculate the percentage of each cluster for each region
    region_cluster_crosstab = pd.crosstab(data['regione_residenza'], data['cluster'], normalize='index') * 100

    # Step 8: Identify the cluster with the highest percentage for each region
    max_cluster_per_region = region_cluster_crosstab.idxmax(axis=1)

    # Step 9: Create a DataFrame for the map
    map_data = pd.DataFrame({
        'regione_residenza': max_inc_per_region.index,
        'incremento': max_inc_per_region.values,
        'percentage': max_percentage_per_region.values,
        'cluster': max_cluster_per_region.values
    })

    # Step 10: Merge with geographic coordinates
    map_data = pd.merge(map_data, coords_df, on='regione_residenza')

    # Step 11: Create the scatter map with Plotly
    fig = px.scatter_mapbox(
        map_data,
        lat='latitude',
        lon='longitude',
        color='incremento',  # Color by increment
        size='percentage',  # Size based on percentage
        hover_name='regione_residenza',  # Show region name on hover
        hover_data={
            'incremento': True,  # Show increment type
            'percentage': ':.2f',  # Show percentage
            'cluster': True  # Show cluster
        },
        title='Largest Teleassistance Increment by Region in Italy',
        color_continuous_scale=px.colors.cyclical.IceFire,  # Color scale
        mapbox_style='carto-positron',
        zoom=5  # Initial zoom level
    )

    # Step 12: Customize the map layout
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=41.8719, lon=12.5674),  # Center the map on Italy
            zoom=5
        ),
        margin={"r":0, "t":0, "l":0, "b":0},  # Remove extra margins
        legend=dict(
            x=0.99,  # Position the legend at the top-right corner
            y=0.99,
            xanchor='right',
            yanchor='top',
            traceorder='normal',
            font=dict(size=12),
            bgcolor='rgba(0, 0, 0, 0.7)',  # Transparent legend background
            bordercolor='black',
            borderwidth=1
        )
    )

    # Return the map figure
    return fig

def create_cluster_and_increment_pie_charts(data):
    """
    Creates a figure with two pie charts displaying the distribution of clusters and the distribution of 
    the types of 'incremento_teleassistenze'.

    Parameters:
    - data: DataFrame containing 'cluster' and 'incremento_teleassistenze' columns.

    Returns:
    - fig: Plotly figure object with two pie charts.
    """
    
    # Step 1: Create DataFrame for the cluster distribution
    cluster_counts = data['cluster'].value_counts().reset_index()
    cluster_counts.columns = ['cluster', 'count']

    # Step 2: Create DataFrame for the distribution of incremento_teleassistenze types
    tipologia_counts = data['incremento_teleassistenze'].value_counts().reset_index()
    tipologia_counts.columns = ['incremento_teleassistenze', 'count']

    # Step 3: Create a figure with two subplots (one for clusters, one for incremento_teleassistenze)
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            'Cluster Distribution',
            'Distribution of Incremento Teleassistenze Types'
        ),
        specs=[[{'type': 'domain'}, {'type': 'domain'}]]  # 'domain' specifies pie charts
    )

    # Step 4: Add pie chart for cluster distribution
    fig.add_trace(
        px.pie(
            cluster_counts,
            names='cluster',
            values='count',
            color_discrete_sequence=px.colors.qualitative.Dark2
        ).update_traces(
            textinfo='label+percent',
            texttemplate='Cluster %{label} %{percent:.1%}'  # Custom label + percentage
        ).data[0],
        row=1, col=1
    )

    # Step 5: Add pie chart for incremento_teleassistenze distribution
    fig.add_trace(
        px.pie(
            tipologia_counts,
            names='incremento_teleassistenze',
            values='count',
            color_discrete_sequence=px.colors.qualitative.Dark2
        ).update_traces(
            textinfo='label+percent',
            texttemplate='%{label} %{percent:.1%}'  # Custom label + percentage
        ).data[0],
        row=1, col=2
    )

    # Step 6: Update layout of the figure
    fig.update_layout(
        title_text='Distribution of Clusters and Types of Incremento Teleassistenze',
        height=600,
        width=1200,
        showlegend=True,  # Keep legend visible
        legend_title_text="Legend"
    )

    # Return the figure object
    return fig

def create_increment_and_cluster_bar_charts(data):
    """
    Creates a figure with two bar charts: one showing the distribution of `incremento_teleassistenze` 
    types and the other showing the distribution of clusters.

    Parameters:
    - data: DataFrame containing 'incremento_teleassistenze' and 'cluster' columns.

    Returns:
    - fig: Plotly figure object with two bar charts.
    """
    
    # Step 1: Calculate the number of samples for each increment type
    incremento_counts = data['incremento_teleassistenze'].value_counts()

    # Step 2: Calculate the number of samples for each cluster
    cluster_counts = data['cluster'].value_counts()
    print("Number of samples per cluster:")
    print(cluster_counts)

    # Step 3: Create a figure with two subplots (one for incremento and one for clusters)
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            'Number of Samples per Increment Type',
            'Number of Samples per Cluster'
        ),
        column_widths=[0.5, 0.5]
    )

    # Step 4: Add bar chart for incremento_teleassistenze distribution
    fig.add_trace(
        go.Bar(
            x=incremento_counts.index,
            y=incremento_counts.values,
            name='Increment Type',
            marker_color=px.colors.sequential.Viridis
        ),
        row=1, col=1
    )

    # Step 5: Add bar chart for cluster distribution
    fig.add_trace(
        go.Bar(
            x=cluster_counts.index,
            y=cluster_counts.values,
            name='Cluster',
            marker_color=px.colors.qualitative.Pastel
        ),
        row=1, col=2
    )

    # Step 6: Customize the general layout
    fig.update_layout(
        height=600,
        width=1200,
        showlegend=False,  # Hide legends to avoid repetition
        title_text='Distribution of Samples by Increment Type and Cluster'
    )

    # Step 7: Add axis titles to both charts
    fig.update_xaxes(title_text='Increment Type', row=1, col=1)
    fig.update_yaxes(title_text='Number of Samples', row=1, col=1)

    fig.update_xaxes(title_text='Cluster', row=1, col=2)
    fig.update_yaxes(title_text='Number of Samples', row=1, col=2)

    # Return the figure object
    return fig

def create_age_vs_increment_box_plot(data):
    """
    Creates a box plot to compare age categories (`fascia_eta`) with teleassistance increments 
    (`incremento_teleassistenze`).

    Parameters:
    - data: DataFrame containing 'incremento_teleassistenze' and 'fascia_eta' columns.

    Returns:
    - fig: Plotly figure object with the box plot.
    """
    
    # Create the box plot with Plotly
    fig = px.box(
        data,
        x='incremento_teleassistenze',
        y='fascia_eta',
        color='incremento_teleassistenze',
        title='Age Category vs Teleassistance Increment',
        labels={
            'incremento_teleassistenze': 'Teleassistance Increment',
            'fascia_eta': 'Age Category'
        },
        color_discrete_sequence=px.colors.sequential.Blues
    )

    # Return the figure object
    return fig

def create_cluster_vs_increment_violin_plot(data):
    """
    Creates a violin plot to visualize the distribution of teleassistance increments (`incremento_teleassistenze`) 
    across different clusters (`cluster`).

    Parameters:
    - data: DataFrame containing 'cluster' and 'incremento_teleassistenze' columns.

    Returns:
    - fig: Plotly figure object with the violin plot.
    """
    
    # Create the violin plot with Plotly
    fig = px.violin(
        data,
        x='cluster',
        y='incremento_teleassistenze',
        title='Distribution of Teleassistance Increment by Cluster',
        labels={
            'cluster': 'Cluster',
            'incremento_teleassistenze': 'Teleassistance Increment'
        },
        box=True,  # Show box plot inside the violin
        points='all'  # Show all points
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title='Cluster',
        yaxis_title='Teleassistance Increment'
    )

    # Return the figure object
    return fig

def create_increment_vs_cluster_bar_chart(data):
    """
    Creates a grouped bar chart to visualize the distribution of samples across different teleassistance increments 
    (`incremento_teleassistenze`) and clusters (`cluster`).

    Parameters:
    - data: DataFrame containing 'incremento_teleassistenze' and 'cluster' columns.

    Returns:
    - fig: Plotly figure object with the grouped bar chart.
    """
    
    # Step 1: Calculate the number of samples for each combination of teleassistance increment and cluster
    increment_cluster_counts = data.groupby(['incremento_teleassistenze', 'cluster']).size().reset_index(name='count')
    
    # Step 2: Create the bar chart with Plotly
    fig = px.bar(
        increment_cluster_counts,
        x='incremento_teleassistenze',
        y='count',
        color='cluster',
        title='Distribution of Samples by Teleassistance Increment and Cluster',
        labels={
            'incremento_teleassistenze': 'Teleassistance Increment',
            'count': 'Number of Samples',
            'cluster': 'Cluster'
        },
        barmode='group',
        color_continuous_scale=px.colors.cyclical.IceFire  # Use a cyclical color scale
    )

    # Customize the layout of the chart
    fig.update_layout(
        xaxis_title='Teleassistance Increment',
        yaxis_title='Number of Samples',
        legend_title='Cluster',
        bargap=0.4  # Gap between bars
    )

    # Return the figure object
    return fig

def create_scatter_plot_by_cluster_and_professional(data):
    """
    Creates a 2D scatter plot to visualize the distribution of clusters relative to the type of increment 
    (`incremento_teleassistenze`) and the type of professional (`tipologia_professionista_sanitario`).

    Parameters:
    - data: DataFrame containing 'cluster', 'incremento_teleassistenze', and 'tipologia_professionista_sanitario' columns.

    Returns:
    - fig: Plotly figure object with the scatter plot.
    """
    
    # Step 1: Group the data by cluster, increment type, and professional type
    df_grouped = data.groupby(['cluster', 'incremento_teleassistenze', 'tipologia_professionista_sanitario']).size().reset_index(name='count')

    # Step 2: Create the scatter plot with Plotly
    fig = px.scatter(
        df_grouped,
        x='incremento_teleassistenze',  # Teleassistance increment on the x-axis
        y='tipologia_professionista_sanitario',  # Professional type on the y-axis
        size='count',  # Size of the points based on the number of samples
        color='cluster',  # Color of the points based on the cluster
        symbol='cluster',  # Different symbols for different clusters
        hover_data=['count'],  # Show the count on hover
        title='Distribution of Clusters by Professional Type and Teleassistance Increment',
        size_max=50  # Increase the maximum size of the points
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title='Type of Increment',
        yaxis_title='Professional Type',
        width=900,
        height=600
    )

    # Return the figure object
    return fig

def create_scatter_plot_by_increment_and_structure(data):
    """
    Creates a 2D scatter plot to visualize the distribution of clusters relative to the type of increment 
    (`incremento_teleassistenze`) and the type of structure (`tipologia_struttura_erogazione`).

    Parameters:
    - data: DataFrame containing 'cluster', 'incremento_teleassistenze', and 'tipologia_struttura_erogazione' columns.

    Returns:
    - fig: Plotly figure object with the scatter plot.
    """
    
    # Step 1: Group the data by cluster, increment type, and structure type
    df_grouped = data.groupby(['cluster', 'incremento_teleassistenze', 'tipologia_struttura_erogazione']).size().reset_index(name='count')

    # Step 2: Create the scatter plot with Plotly
    fig = px.scatter(
        df_grouped,
        x='incremento_teleassistenze',  # Teleassistance increment on the x-axis
        y='tipologia_struttura_erogazione',  # Structure type on the y-axis
        size='count',  # Size of the points based on the number of samples
        color='cluster',  # Color of the points based on the cluster
        symbol='cluster',  # Different symbols for different clusters
        hover_data=['count'],  # Show the count on hover
        title='Distribution of Clusters by Increment Type and Structure',
        size_max=50  # Increase the maximum size of the points
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title='Type of Increment',
        yaxis_title='Type of Structure',
        width=900,
        height=600
    )

    # Return the figure object
    return fig

# 1. Gender Distribution Chart
gender_dist_fig = create_gender_distribution_chart(data)
gender_dist_fig.show()

# 2. Increment Distribution Chart
increment_dist_fig = create_increment_distribution_chart(data)
increment_dist_fig.show()

# 3. Increment Scatter Map
increment_scatter_map_fig = create_increment_scatter_map(data)
increment_scatter_map_fig.show()

# 4. Cluster and Increment Pie Charts
cluster_increment_pie_fig = create_cluster_and_increment_pie_charts(data)
cluster_increment_pie_fig.show()

# 5. Increment and Cluster Bar Charts
increment_cluster_bar_fig = create_increment_and_cluster_bar_charts(data)
increment_cluster_bar_fig.show()

# 6. Age vs Increment Box Plot
age_vs_increment_box_fig = create_age_vs_increment_box_plot(data)
age_vs_increment_box_fig.show()

# 7. Cluster vs Increment Violin Plot
cluster_vs_increment_violin_fig = create_cluster_vs_increment_violin_plot(data)
cluster_vs_increment_violin_fig.show()

# 8. Increment vs Cluster Bar Chart
increment_vs_cluster_bar_fig = create_increment_vs_cluster_bar_chart(data)
increment_vs_cluster_bar_fig.show()

# 9. Scatter Plot by Cluster and Professional
scatter_cluster_professional_fig = create_scatter_plot_by_cluster_and_professional(data)
scatter_cluster_professional_fig.show()

# 10. Scatter Plot by Increment and Structure
scatter_increment_structure_fig = create_scatter_plot_by_increment_and_structure(data)
scatter_increment_structure_fig.show()