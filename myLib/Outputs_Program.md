# **Program Phases and Outputs**

## **1. Data Cleaning**
**Input:**
- Original dataset with missing values or anomalies.

**Output:**
- After data cleaning, null values are handled based on the threshold defined in the configuration file. The cleaned dataset is saved in Parquet format.

**Relevant Outputs:**
- Cleaned dataset saved in: `data/processed/cleaned_data.parquet`.


### **2. Feature Selection**
**Input:**
- Cleaned dataset from the data cleaning phase.

**Output:**
- Only the most relevant features are selected, and the dataset is updated accordingly.

**Relevant Outputs:**
- Dataset after feature selection saved in: `data/processed/feature_selected_data.parquet`.

### **3. Feature Extraction**
**Input:**
- Dataset selected in the previous phase.

**Output:**
- Key features are grouped and aggregated according to specific columns (such as year, quarter, region of residence, age group, activity description). The resulting dataset is saved.

**Relevant Outputs:**
- Dataset after feature extraction saved in: `data/processed/feature_extracted_data.parquet`.

### **4. Clustering**
**Input:**
- Dataset after feature extraction.

**Output:**
- Clustering is applied to group patients based on common characteristics, using algorithms like K-Modes. Outputs include the dataset with assigned clusters.

**Relevant Outputs:**
- Clustered dataset saved in: `data/processed/clustered_data.parquet`.
- Complete dataset with all clusters saved in: `data/processed/clustered_data_all_feature.parquet`.

### **5. Metrics Evaluation**
**Input:**
- Clustered dataset.

**Output:**
- Key clustering metrics, including Purity Score and Silhouette Score, are calculated to evaluate the quality of the clustering.

**Relevant Outputs:**
- Purity Score: 0.85
- Silhouette Score: 0.62
- Metrics file saved in: `logs&metrics/metrics.txt`.

### **6. Results Analysis**
**Output:**
- Analyses are conducted on the clustered data to explore the characteristics of patient groups in detail. Visual analyses include charts on age group distributions, teleassistance service variations, gender distributions, and geographic maps of clusters.

**Produced Analyses:**
- **Age Group Distribution**: Analysis of cluster distribution across different age groups.
- **Teleassistance Variations**: Comparison of teleassistance service variations among different clusters.
- **Healthcare Professional Distribution**: Distribution of clusters based on healthcare professionals.
- **Gender Distribution**: Comparison of gender distribution among clusters.
- **Scatter Map by Region**: Geographic visualization of clusters.
