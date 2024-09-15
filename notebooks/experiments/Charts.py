import pandas as pd
import plotly.express as px
#%%
# Load the data
file_path = '../../data/processed/clustered_data_all_feature.parquet'
data = pd.read_parquet(file_path)

#%%
data.columns
#%%
data.cluster.value_counts()
#%%
data[['incremento_teleassistenze', 'cluster']].value_counts()

# 0 -> high increment   143418
# 1 -> medium increment 103043
# 3 -> low increment    71109
# 2 -> decrement        2393
#%%
data[data.cluster == 3][['incremento_teleassistenze', 'cluster']].value_counts()
#%%
data.head()
#%% md
##
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
#%% md
#This code analyzes the distribution of men and women within the different clusters and displays it in an interactive bar graph with Plotly.
#%%
 #Step 1: Calculate the number of samples for each combination of gender and increment type
sex_increment_counts = data.groupby(['sesso', 'incremento_teleassistenze']).size().reset_index(name='count')
print(sex_increment_counts)
# Step 2: Identify the dominant cluster for each increment type
dominant_cluster_per_inc_gen = data.groupby(['incremento_teleassistenze','sesso'])['cluster'].agg(lambda x: x.value_counts().idxmax()).reset_index(name='dominant_cluster')
print(dominant_cluster_per_inc_gen)
# Step 3: Merge the counts with the dominant cluster information
merged_data = pd.merge(sex_increment_counts, dominant_cluster_per_inc_gen, on=['incremento_teleassistenze','sesso'])
print(merged_data)
# Step 4: Create the bar chart using Plotly
fig = px.bar(
    merged_data,
    x='incremento_teleassistenze',
    y='count',
    color='sesso',
    text='dominant_cluster',  # Display the dominant cluster as text
    title='Distribuzione di uomini e donne per variazione incremento teleassistenza',
    labels={'incremento_teleassistenze': 'Tipologia di incremento', 'count': 'Numero di Campioni', 'sesso': 'Sesso'},
    barmode='group',
    color_discrete_map={'female': '#FF69B4', 'male': '#1E90FF'}
)

# Customize the chart
fig.update_layout(
    xaxis_title='Tipologia di incremento',
    yaxis_title='Numero di Campioni',
    legend_title='Sesso',
    bargap=0.4
)

# Show the dominant cluster above the bars
fig.update_traces(textposition='outside')

# Show the chart
fig.show()


# Calculate the number of samples for each combination of year and increment type
df_sample_counts = pd.crosstab([data['anno'], data['incremento_teleassistenze']], data['cluster'])

# Identify the dominant cluster for each combination of year and increment type
df_max_cluster = df_sample_counts.idxmax(axis=1)

# Identify the highest number of samples for each combination of year and increment type
df_max_sample_count = df_sample_counts.max(axis=1)

print("Number of samples for each combination of year and increment type:")
print(df_sample_counts)
print("Dominant cluster for each combination of year and increment type:")
print(df_max_cluster)
print("Highest number of samples for each combination of year and increment type:")
print(df_max_sample_count)

# Create a DataFrame with all the necessary information
bar_data = pd.DataFrame({
    'anno': [index[0] for index in df_sample_counts.index],  # Extract the year
    'incremento_teleassistenze': [index[1] for index in df_sample_counts.index],  # Extract the increment type
    'sample_count': df_max_sample_count.values,  # Number of samples
    'dominant_cluster': df_max_cluster.values  # Dominant cluster
})

# Create the bar chart with Plotly
fig = px.bar(
    bar_data,
    x='anno',
    y='sample_count',
    color='incremento_teleassistenze',  # Color by increment type
    text='dominant_cluster',  # Add dominant cluster as text on top of the bars
    barmode='group',  # Group the bars by year
    title='Distribuzione delle variazioni delle teleassistenze per anno e cluster dominante',
    labels={'anno': 'Anno', 'sample_count': 'Numero di Campioni', 'incremento_teleassistenze': 'Variazione Teleassistenza'},
    color_discrete_sequence=px.colors.qualitative.Pastel
)

# Customize the chart
fig.update_layout(
    xaxis_title='Anno',
    yaxis_title='Numero di Campioni',
    xaxis_tickangle=-45,
    width=900  # Chart width
)

# Show the dominant cluster above the bars
fig.update_traces(textposition='outside')

# Display the chart
fig.show()

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

# Calculate the percentage of each increment for each region
region_inc_crosstab = pd.crosstab(data['regione_residenza'], data['incremento_teleassistenze'], normalize='index') * 100

# Identify the increment with the highest percentage for each region
max_inc_per_region = region_inc_crosstab.idxmax(axis=1)

# Extract the corresponding highest percentages of each increment for each region
max_percentage_per_region = region_inc_crosstab.max(axis=1)

# Extract the maximum increment of teleassistance for each region
max_increment_teleassistenze = data.groupby('regione_residenza')['incremento_teleassistenze'].max()
print("Type of increment with the highest percentage for each region:")
print(max_increment_teleassistenze)

# Print the cluster with the highest percentage for each region
for region, cluster in max_inc_per_region.items():
    print(
        f"Regione: {region}, Cluster: {cluster}, Percentuale di campioni apparteneneti a quel tipo di incremento : {max_percentage_per_region[region]:.2f}%")

# Calculate the percentage of each cluster for each region
region_cluster_crosstab = pd.crosstab(data['regione_residenza'], data['cluster'], normalize='index') * 100

# Identify the cluster with the highest percentage for each region
max_cluster_per_region = region_cluster_crosstab.idxmax(axis=1)

# Extract the corresponding highest percentages of each cluster for each region
max_percentage_per_region = region_cluster_crosstab.max(axis=1)

# Extract the maximum increment of teleassistance for each region
max_increment_teleassistenze = data.groupby('regione_residenza')['incremento_teleassistenze'].max()
print("Type of increment with the highest percentage for each region:")
print(max_increment_teleassistenze)

# Print the cluster with the highest percentage for each region
for region, cluster in max_cluster_per_region.items():
    print(
        f"Regione: {region}, Cluster: {cluster}, Percentuale di campioni apparteneneti a quel cluster: {max_percentage_per_region[region]:.2f}%")

# Creare un DataFrame per la mappa
map_data = pd.DataFrame({
    'regione_residenza': max_inc_per_region.index,
    'incremento': max_inc_per_region.values,
    'percentage': max_percentage_per_region.values,
    'incremento_teleassistenze': max_increment_teleassistenze.values,  # Incremento teleassistenza
    'cluster': max_cluster_per_region.values  # Cluster
})

# Unire con le coordinate geografiche
map_data = pd.merge(map_data, coords_df, on='regione_residenza')

# Creare la mappa scatter con Plotly
fig = px.scatter_mapbox(
    map_data,
    lat='latitude',
    lon='longitude',
    color='incremento',  # Colora in base al cluster
    size='percentage',  # Dimensione basata sulla percentuale di incremento
    hover_name='regione_residenza',  # Mostra il nome della regione
    hover_data={
        'incremento': True,  # Mostra il numero del cluster
        'percentage': ':.2f',  # Mostra la percentuale di incremento
        'cluster': True  # Mostra incremento teleassistenza
     },
    title='Incremento teleassistenza maggiore per regione in Italia',
    color_continuous_scale=px.colors.cyclical.IceFire,  # Scala colori per il cluster
    mapbox_style='carto-positron',
    zoom=5
)

# Personalizzare la mappa
fig.update_layout(
    mapbox=dict(
        center=dict(lat=41.8719, lon=12.5674),  # Centra la mappa sull'Italia
        zoom=5
    ),
    margin={"r":0, "t":0, "l":0, "b":0},  # Margini ridotti
    legend=dict(
        x=0.99,  # Posiziona la legenda in alto a destra
        y=0.99,
        xanchor='right',
        yanchor='top',
        traceorder='normal',
        font=dict(size=12),
        bgcolor='rgba(0, 0, 0, 0.7)',  # Sfondo della legenda trasparente
        bordercolor='black',  # Bordo bianco
        borderwidth=1
    )
)

# Mostra la mappa
fig.show()

# Crea un DataFrame per la distribuzione dei cluster
cluster_counts = data['cluster'].value_counts().reset_index()
cluster_counts.columns = ['cluster', 'count']

# Crea un DataFrame per la distribuzione della tipologia di incremento_teleassistenze
tipologia_counts = data['incremento_teleassistenze'].value_counts().reset_index()
tipologia_counts.columns = ['incremento_teleassistenze', 'count']

# Crea una figura con due subplot
fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=('Distribuzione dei Cluster', 'Distribuzione della Tipologia di incremento_teleassistenze'),
    specs=[[{'type': 'domain'}, {'type': 'domain'}]]
)

# Aggiungi il grafico a torta per i cluster con percentuali e nomi
fig.add_trace(
    px.pie(
        cluster_counts,
        names='cluster',
        values='count',
        color_discrete_sequence=px.colors.qualitative.Dark2,

    ).update_traces(
        textinfo='label+percent',  # Mostra sia l'etichetta che la percentuale
        texttemplate='Cluster %{label}  %{percent:.1%}'  # Personalizza il testo con label e percentuale
    ).data[0],
    row=1, col=1
)

# Aggiungi il grafico a torta per la tipologia di incremento teleassistenze con percentuali e nomi
fig.add_trace(
    px.pie(
        tipologia_counts,
        names='incremento_teleassistenze',
        values='count',
        color_discrete_sequence=px.colors.qualitative.Dark2,

    ).update_traces(
        textinfo='label+percent',  # Mostra sia l'etichetta che la percentuale
        texttemplate='%{label}  %{percent:.1%}'  # Personalizza il testo con label e percentuale
    ).data[0],
    row=1, col=2
)

# Aggiorna il layout della figura
fig.update_layout(
    title_text='Distribuzione dei Cluster e della Tipologia di incremento_teleassistenze',
    height=600,
    width=1200,
    showlegend=True,  # Mantieni la legenda visibile
    legend_title_text="Legenda"  # Aggiungi un titolo alla legenda
)

# Mostra la figura
fig.show()

# %%

# Calcola il numero di campioni per ciascun tipo di incremento
incremento_counts = data['incremento_teleassistenze'].value_counts()

# Calcola il numero di campioni per ciascun cluster
cluster_counts = data['cluster'].value_counts()
print("Numero di campioni per cluster:")
print(cluster_counts)

import plotly.graph_objects as go

# Crea una figura con due subplot (uno per i cluster e uno per la tipologia di incremento)
fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=('Numero di Campioni per Tipologia di Incremento', 'Numero di Campioni per Cluster'),
    column_widths=[0.5, 0.5]
)

# Grafico a barre per la distribuzione della tipologia di incremento
fig.add_trace(
    go.Bar(
        x=incremento_counts.index,
        y=incremento_counts.values,
        name='Tipologia di Incremento',
        marker_color=px.colors.sequential.Viridis
    ),
    row=1, col=1
)

# Grafico a barre per la distribuzione dei cluster
fig.add_trace(
    go.Bar(
        x=cluster_counts.index,
        y=cluster_counts.values,
        name='Cluster',
        marker_color=px.colors.qualitative.Pastel
    ),
    row=1, col=2
)

# Personalizza il layout generale
fig.update_layout(
    height=600,
    width=1200,
    showlegend=False,  # Nascondi le leggende per evitare ripetizioni
    title_text='Distribuzione dei Campioni per Tipologia di Incremento e Cluster',
)

# Aggiungi titoli agli assi di entrambi i grafici
fig.update_xaxes(title_text='Tipologia di Incremento', row=1, col=1)
fig.update_yaxes(title_text='Numero di Campioni', row=1, col=1)

fig.update_xaxes(title_text='Cluster', row=1, col=2)
fig.update_yaxes(title_text='Numero di Campioni', row=1, col=2)

# Mostra il grafico
fig.show()
# %%
# Create the box plot with Plotly
fig = px.box(data, x='incremento_teleassistenze', y='fascia_eta', color='incremento_teleassistenze',
             title='Fascia di Età vs Incremento Teleassistenze',
             labels={'incremento_teleassistenze': 'Incremento Teleassistenze', 'fascia_eta': 'Fascia di Età'},
             color_discrete_sequence=px.colors.sequential.Blues)

# Show the plot
fig.show()


# Create the violin plot with Plotly
fig = px.violin(
    data,
    x='cluster',
    y='incremento_teleassistenze',
    title='Distribuzione delle tipologie di incremento per cluster',
    labels={'cluster': 'Cluster', 'incremento_teleassistenze': 'Tipologia di Incremento'},
    box=True,  # Show box plot inside the violin
    points='all'  # Show all points
)

# Customize the layout
fig.update_layout(
    xaxis_title='Cluster',
    yaxis_title='Tipologia di Incremento'
)

# Show the chart
fig.show()
#%%

# Step 1: Calcola il numero di campioni per ciascuna combinazione di incremento_teleassistenze e cluster
increment_cluster_counts = data.groupby(['incremento_teleassistenze', 'cluster']).size().reset_index(name='count')
print (increment_cluster_counts)
# Step 2: Crea il grafico a barre con Plotly
fig = px.bar(
    increment_cluster_counts,
    x='incremento_teleassistenze',
    y='count',
    color='cluster',
    title='Distribuzione dei campioni per tipologia di incremento e cluster',
    labels={'incremento_teleassistenze': 'Tipologia di Incremento', 'count': 'Numero di Campioni', 'cluster': 'Cluster'},
    barmode='group',
    color_continuous_scale=px.colors.cyclical.IceFire  # Usa una scala di colori ciclica
)

# Personalizza il layout del grafico
fig.update_layout(
    xaxis_title='Tipologia di Incremento',
    yaxis_title='Numero di Campioni',
    legend_title='Cluster',
    bargap=0.4
)

# Mostra il grafico
fig.show()
#%%

# Raggruppa i dati per cluster, tipologia di incremento e tipologia di struttura
df_grouped = data.groupby(['cluster', 'incremento_teleassistenze', 'tipologia_professionista_sanitario']).size().reset_index(name='count')

# Crea un grafico scatter 2D
fig = px.scatter(
    df_grouped,
    x='incremento_teleassistenze',  # Tipologia di incremento sull'asse x
    y='tipologia_professionista_sanitario',  # Tipologia di struttura sull'asse y
    size='count',  # Dimensione dei punti basata sulla numerosità dei campioni
    color='cluster',  # Colore dei punti basato sui cluster
    symbol='cluster',  # Simboli diversi per cluster
    hover_data=['count'],  # Mostra il conteggio al passaggio del mouse
    title='Distribuzione dei Cluster rispetto a tipologia_professionista_sanitario',
    size_max=50  # Aumenta la dimensione massima dei punti
)

# Personalizza il layout
fig.update_layout(
    xaxis_title='Tipo di Incremento',
    yaxis_title='tipologia_professionista_sanitario',
    width=900,
    height=600
)

# Mostra il grafico
fig.show()
#%%

# Raggruppa i dati per cluster, tipologia di incremento e tipologia di struttura
df_grouped = data.groupby(['cluster', 'incremento_teleassistenze', 'tipologia_struttura_erogazione']).size().reset_index(name='count')

# Crea un grafico scatter 2D
fig = px.scatter(
    df_grouped,
    x='incremento_teleassistenze',  # Tipologia di incremento sull'asse x
    y='tipologia_struttura_erogazione',  # Tipologia di struttura sull'asse y
    size='count',  # Dimensione dei punti basata sulla numerosità dei campioni
    color='cluster',  # Colore dei punti basato sui cluster
    symbol='cluster',  # Simboli diversi per cluster
    hover_data=['count'],  # Mostra il conteggio al passaggio del mouse
    title='Distribuzione dei Cluster rispetto a Tipologia di Incremento e Struttura',
    size_max=50  # Aumenta la dimensione massima dei punti
)

# Personalizza il layout
fig.update_layout(
    xaxis_title='Tipo di Incremento',
    yaxis_title='Tipologia di Struttura',
    width=900,
    height=600
)

# Mostra il grafico
fig.show()