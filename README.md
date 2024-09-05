# **_Teleassistance-Supervised-Clustering_**
To read the README.md in Italian, click [here](myLib/README_ita.md)

## Index

1. [Overview](#1-overview)
   - [Project Structure](./myLib/Project_Structure.md)
2. [Enviroment setup](#2-enviroment-setup)
3. [Installation Instructions](#3-installation-instructions)
4. [Data Sources](#4-data-sources)
5. [Pipeline](#5-pipeline)
8. [Outputs Program](./myLib/Outputs_Program.md)


## **1. Overview**
This project explores the integration of teleassistance services with supervised clustering techniques.
- **Objective**: Profile patients to understand their contribution to the increase in teleassistance services.
- **Key Focus**: Identify common patterns and behaviors among patients that are linked to the rise in teleassistance usage.
- **Approach**:
  - Group patients based on common patterns or similar behaviors related to the target variable (`incremento_teleassistenze`).
  - Analyze differences among patient groups to determine which features contribute to the increase in teleassistance.
- **Methods**:
  - Use advanced clustering techniques that consider both patient characteristics and the outcome variable (`incremento_teleassistenze`).
 
[Quickly return to the top](#teleassistance-supervised-clustering)

## **2. Enviroment setup**
Before running the code, it's important to take some precautions and set up your environment properly. Follow these steps:
1. Create a Virtual Environment:
   - Open your terminal or command prompt.
   - Run the following command to create a virtual environment named "venv":` python -m venv venv`
2. Activate the Virtual Environment:
   - If you're using Windows:    `.\venv\Scripts\activate`
   - If you're using Unix or MacOS:    `source ./venv/Scripts/activate`
3. Deactivate the Environment (When Finished):
   - Use the following command to deactivate the virtual environment:    `deactivate`
4. Install Dependencies:
   - After cloning the project and activating the virtual environment, install the required dependencies using:    `pip install -r requirements.txt`
     This command downloads all the non-standard modules required by the application.
5. If your Python version used to generate the virtual environment doesn't contain an updated version of pip, update pip using:  `pip install --upgrade pip `
  
Once you've set up your virtual environment and installed the dependencies, you're ready to run the application. Simply navigate to the `main.py` file and execute it.

[Quickly return to the top](#teleassistance-supervised-clustering)

## **3. Installation Instructions**
1. Clone the repository:
   ```sh
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```sh
   cd Teleassistance-Supervised-Clustering
   ```
3. Follow the steps in the [Environment setup](#2-environment-setup) section to set up your virtual environment and install dependencies.

[Quickly return to the top](#teleassistance-supervised-clustering)

## **4. Data Sources**
The data used in this project is organized into two main subdirectories: `raw` for the unprocessed original data and `processed` for the data that has undergone various preprocessing steps. For more details, refer to the [Data Directory](./data/README.md).

[Quickly return to the top](#teleassistance-supervised-clustering)

## **5. Pipeline**
The data processing and analysis pipeline includes the following steps:
1. **Data Cleaning**: Handle missing values, correct inconsistencies, and remove irrelevant information.
2. **Feature Extraction**: Generate new features from the raw attributes.
3. **Feature Selection**: Retain only the most relevant features for modeling.
4. **Clustering**: Apply clustering algorithms to group patients based on common patterns or behaviors.
5. **Analysis**: Analyze the differences among patient groups to determine which features contribute to the increase in teleassistance.

[Quickly return to the top](#teleassistance-supervised-clustering)

## **6. Outputs Program**
The goal of the challenge is to profile patients by analyzing their contribution to the increase in teleassistance services. This involves identifying common patterns and behaviors among patients that are linked to the rise in teleassistance usage.

For more details on the outputs and results of the program, refer to the [Outputs Program Documentation](myLib/Outputs_Program.md).