# **Program Phases and Outputs**

## **1. Data Cleaning**
**Input:**
- Original dataset with missing values or anomalies.

**Output:**
- After data cleaning, null values are handled based on the threshold defined in the configuration file. The cleaned dataset is saved in Parquet format.

**Relevant Outputs:**
- Cleaned dataset saved in: `data/processed/cleaned_data.parquet`.


## **2. Feature Selection**
**Input:**
- Cleaned dataset from the data cleaning phase.

**Output:**
- Only the most relevant features are selected, and the dataset is updated accordingly.

**Relevant Outputs:**
- Dataset after feature selection saved in: `data/processed/feature_selected_data.parquet`.

## **3. Feature Extraction**
**Input:**
- Dataset selected in the previous phase.

**Output:**
- Key features are grouped and aggregated according to specific columns (such as year, quarter, region of residence, age group, activity description). The resulting dataset is saved.

**Relevant Outputs:**
- Dataset after feature extraction saved in: `data/processed/feature_extracted_data.parquet`.

## **4. Clustering**
**Input:**
- Dataset after feature extraction.

**Output:**
- Clustering is applied to group patients based on common characteristics, using algorithms like K-Modes. Outputs include the dataset with assigned clusters.

**Relevant Outputs:**
- Clustered dataset saved in: `data/processed/clustered_data.parquet`.
- Complete dataset with all clusters saved in: `data/processed/clustered_data_all_feature.parquet`.

## **5. Metrics Evaluation**
**Input:**
- Clustered dataset.

**Output:**
- Key clustering metrics, including Purity Score and Silhouette Score, are calculated to evaluate the quality of the clustering.Metrics file saved in: `logs&metrics/metrics.txt`.

**Relevant Outputs:**
- Purity Score: 0.85
- Mean normalized silhouette score: 0.62
- Final metrics

## **6. Results Analysis**
**Input:**
- Clustered dataset with all features.

**Output:**
- Analyses are conducted on the clustered data to explore the characteristics of patient groups in detail. Visual analyses include charts on age group distributions, teleassistance service variations, gender distributions, geographic maps of clusters and yearly increment distributions. Analyses file saved in: `logs&metrics/analysis_result.txt`

**Produced Analyses:**
- **Analysis of age distribution by cluster**: Analysis of age group distribution among different clusters and their contribution to teleassistance increment.
- **Teleassistance Variations**: Analysis of the teleassistance variation distribution (incremento_teleassistenze) by cluster, using a bar chart
- **Healthcare Professional Distribution**: Analysis of the distribution of healthcare professionals among clusters and their impact on teleassistance increment.
- **Gender Distribution by cluster**: Analysis of the gender distribution (sesso) by cluster, using a bar chart. 
- **Gender Distribution by Increment Type**: Analysis of the gender distribution (sesso) by increment type, using a bar chart.
- **Scatter Map by Region**: Geographic distribution of clusters and increment type across regions.
- **Yearly Increment Distribution**: Analyzes teleassistance data, identifies dominant clusters for each year-increment combination, and creates a bar chart visualizing the distribution.
