# **Project Structure**
In this section, we will discuss the project structure of the application. The project structure refers to the organization of files and folders within the application. It plays a crucial role in maintaining the application, adding new features, and facilitating collaboration. A well-defined project structure enhances code readability and navigation.


```plaintext
├── data/                           # Contains all datasets used in the project
│   ├── processed/                  # Processed datasets (cleaned, transformed)
│   ├── raw/                        # Raw datasets (original, unprocessed)
│   └── README.md                   # Documentation for the datasets
├── graphs/                         # Visualizations generated during analysis
│   ├── analysis/                   # Final charts explaining the results obtained
├── logs&metrics/                   # Logs and metrics recorded during model training and evaluation
├── models/                         # Saved models for future use or deployment
├── myLib/                          # Documentation and utility files for the project
├── notebooks/                      # Jupyter notebooks for exploratory data analysis, development, and experiments
│   ├── development/                # Notebooks related to model development
│   ├── EDA/                        # Notebooks for Exploratory Data Analysis
│   └── experiments/                # Experimental notebooks for testing ideas
├── src/                            # Source code for data preparation, model training, and evaluation
│   ├── data_prep/                  # Scripts for data cleaning, feature sselection and extraction
│   ├── __init__.py                 # Initialization script for the source package
├── .gitattributes                  
├── .gitignore                      
├── config.yaml                     # Configuration file for the project (data paths, model parameters, enablers)
├── main.py                         # Main script to run the project
├── README.md                       # Overview and documentation of the project
└── requirements.txt                # List of Python dependencies required for the project
```


## Index
1. [Overview](#1-overview)
    - [Directory Descriptions](#directory-descriptions)
    - [Pipeline Description](#pipeline-description)
2. [Flow Chart](#2-flow-chart)
3. [Branching Strategy](#3-branching-strategy)


- [Return to README](../README.md)


## **1. Overview**
The project structure of the application is organized into the following directories:

- ## Directory Descriptions

    ### `data/`
    This directory contains all the data used in the project.

    - **`raw/`**: Stores the raw data files that are used as input for data processing.
    - **`processed/`**: Contains the data that has been cleaned and processed, ready for use in model training or analysis.
    - **`README.md`**: Provides documentation about the data, including descriptions of the files, data sources, and any other relevant information. You can find the detailed description of the data directory [here](../data/README.md).

    ### `graphs/`
    This [directory](../graphs/) stores the visualizations generated during the analysis and modeling phases.

    ### `logs&metrics/`
    This directory contains [log files](../logs&metrics/INFO.txt) and [metrics](../logs&metrics/metrics.txt) generated during the execution of the pipeline.

    ### `models/`
    This [directory](../models/) stores the trained machine learning models, usually in `.pkl` format.

    ### `myLib/`
    This [directory](../myLib/) contains additional documentation and resources related to the project.

    ### `notebooks/`
    This directory holds Jupyter Notebooks used for various stages of the project.

    - **`EDA/`**: Notebooks focused on Exploratory Data Analysis (EDA) to understand the data better.
    - **`development/`**: Notebooks used during the model development phase, including model selection, tuning, and validation.
    - **`experiments/`**: Contains experimental notebooks used for trying out different approaches or techniques not part of the core model development.

    ### `src/`
    This is the main source code directory containing all Python scripts and modules.

    - **`__init__.py`**: Initializes the `src` directory as a Python package.
    - **`data_prep/`**: This subdirectory includes scripts for data preparation, such as:
        - **`DataCleaning.py`**: Handles data cleaning tasks.
        - **`FeatureSelection.py`**: Focuses on selecting relevant features.
        - **`FeatureExtraction.py`**: Manages feature extraction processes.
    - **`ModellingClustering.py`**: Script for defining and training clustering models.
    - **`MetricsEvaluation.py`**: Contains functions and classes for evaluating model performance.
    - **`AnalysisResults.py`**: Focuses on data visualization and storytelling to present the results of the analysis or modeling in an understandable way.


- ## Pipeline Description
    This project follows a structured pipeline that guides the process from raw data to model evaluation and visualization. Below is a detailed description of each phase, with references to the relevant files and folders.

    ### 1. **Configuration and Setup**
    The pipeline begins with loading configurations and setting up logging. 

    - **Loading Configuration**: The configuration settings for the entire project are stored in the [config.yaml](../config.yaml) file located at the root of the project. These settings control various aspects of the pipeline, such as data paths, processing options, and model parameters. The `load_config` function in the [main.py](../main.py) script reads these settings and makes them available throughout the pipeline.
    
    - **Logging Setup**: To ensure that the execution of the pipeline is properly tracked, logging is initialized at the start. Logs are recorded in a file specified in the configuration, typically stored as [INFO.txt](../logs&metrics/INFO.txt) at the root of the project. This log file is cleared at the beginning of each run to maintain a clean record of the current pipeline execution.

    ### 2. **Data Loading**
    Once the configurations are loaded, the pipeline proceeds to load the dataset.

    - **Data Source**: The data, typically stored in the [data/raw/](../data/raw/) folder, is loaded into the pipeline. The `load_data` function in [main.py](../main.py) is responsible for reading the data file as specified in the [config.yaml](../config.yaml). This raw data is then stored in a Pandas DataFrame, which is used as the base for all subsequent operations.

    ### 3. **Data Preparation**
    Data preparation is a crucial phase where the raw data is transformed into a cleaner and more structured format suitable for modeling. This phase is divided into several steps, each handled by specific scripts within the [src/data_prep/](../src/data_prep/) directory.

    - **Data Cleaning**:
        - **Process**: The first step in data preparation is cleaning the dataset to remove or correct any errors, value imputing, handle missing values, and remove duplicates. This is done using the `data_cleaning_execution` function located in [src/data_prep/DataCleaning.py](../src/data_prep/DataCleaning.py).
        - **Output**: The cleaned data is then saved to the [data/processed/](../data/processed/) folder, making it ready for the next stages of processing.

    - **Feature Selection**:
        - **Process**: After cleaning, the pipeline selects the most relevant features from the dataset. This step, managed by the `feature_selection_execution` function in [src/data_prep/FeatureSelection.py](../src/data_prep/FeatureSelection.py), involves filtering out unimportant or redundant features to improve model performance and interpretability.
        - **Output**: The resulting dataset, now streamlined with only the selected features, is saved again in the [data/processed/](../data/processed/) folder.

    - **Feature Extraction**:
        - **Process**: In this step, the pipeline enhances the dataset by calculating and classifying the increment of services over time, as well as creating new features. The `feature_extraction_execution` function in [src/data_prep/FeatureExtraction.py](../src/data_prep/FeatureExtraction.py) handles this task. This process includes calculating the year-over-year increment of services, categorizing these increments into different levels, and visualizing the distribution of these increments. The resulting dataset is enriched with these new features and classifications.
        - **Output**: The enriched dataset, now containing new features and classifications based on service increments, is stored in the [data/processed/](../data/processed/) folder for further use in the pipeline.


    ### 4. **Modeling - Clustering**
    With the data prepared, the pipeline moves on to the modeling phase, where clustering is performed.

    - **Process**: The `clustering_execution` function in [src/ModellingClustering.py](../src/ModellingClustering.py) applies **_"Elbow method"_** to determine the optimal number of clusters and then uses one of the clustering algorithms _"**KModes Clustering"**_ to group the data into distinct clusters based on the patterns identified in the features.
    - **Output**: The model is saved in the [models/](../models/) folder. The clustered data is saved in the [data/processed](../data/processed/) folder, ready for evaluation and further analysis. This step is essential for understanding the natural groupings within the data and forms the basis for later evaluation.

    ### 5. **Model Evaluation - Metrics**
    After clustering, the pipeline evaluates the performance of the model using various metrics.

    - **Process**: The `metrics_execution` function in [src/MetricsEvaluation.py](../src/MetricsEvaluation.py) calculates key performance metrics such as the Purity Score and the Silhouette Score, which help assess the quality and coherence of the clusters formed during modeling.
    - **Output**: These metrics are written to a file as specified in the [config.yaml](../config.yaml), saved in [logs&metrics/](../logs&metrics/) folder. This step provides valuable feedback on the effectiveness of the clustering model and guides any necessary adjustments.

    ### 6. **Storytelling and Visualization**
    The final phase of the pipeline focuses on visualizing the results and communicating the findings in an accessible format.

    - **Process**: The `AnalysisResults.py` script in [src/AnalysisResults.py](../src/AnalysisResults.py) is dedicated to creating visualizations and narratives that make the data insights clear and understandable. This can include charts, graphs, and other forms of data representation.
    - **Output**: The visualizations and any associated summaries are either saved to a file or displayed as specified in the script, providing a comprehensive view of the data and the results of the analysis.

    The visualizations generated during the analysis can be found in the [Presentazione_progetto_FIA](./Presentazione_proggetto_FIA.pdf) file.

    ---

    This pipeline is designed to be modular, with each phase building on the previous one to transform raw data into meaningful insights. By following this structure, the project ensures a clear and efficient workflow from data preparation to final visualization.

[Quickly return to the top](#project-structure)

## **2. Flow Chart**
The flow chart below illustrates the high-level process of the application, from data loading to model evaluation and visualization. The flow chart provides a visual representation of the pipeline described in the previous section.

![Flow Chart](https://github.com/AlessiaRossi/Teleassistance-Supervised-Clustering/blob/main/myLib/teleassistenze_flowchart%20v_2.drawio.png?raw=true)

[Quickly return to the top](#project-structure)


## **3. Branching Strategy**
We have adopted the Gitflow branching strategy for managing the source code. It is a robust branching model that provides a clear path for creating new features and fixing bugs. The Gitflow model consists of two main branches: main and develop. The main branch contains the production-ready code, while the develop branch contains the latest code that is ready for release. Additionally, it uses feature, and hotfix branches to manage new features and bug fixes, respectively.

In particular, the Gitflow model consists of the following branches:
- **Main**: The main branch contains the production-ready code. It is the branch from which the application is deployed to the production environment.
- **Develop**: The develop branch contains the latest code that is ready for release. It is the branch from which the code is deployed to the staging environment for testing.
- **Feature**: The feature branches are used to develop new features. They are created from the develop branch and merged back into the develop branch once the feature is complete.
    - Feature branches are named using the following convention: `features/<feature-name>`.
    - Feature branches should be created for each new feature and are deleted once the feature is merged into the develop branch.
    - For example, we created some feature branches such as `features/data_prep`, `features/modelling`, `features/projectSetup`, etc.
- **Hotfix**: The hotfix branches are used to fix bugs in the production code. They are created from the main branch and merged back into both the main and develop branches once the bug is fixed.
    - Hotfix branches are named using the following convention: `hotfix/<bug-name>`.
    - Hotfix branches should be created for each bug fix and are deleted once the bug is merged into the main and develop branches.
    - For example, we created some hotfix branches such as `hotfix/requirementsFile`, etc.

[Quickly return to the top](#project-structure)