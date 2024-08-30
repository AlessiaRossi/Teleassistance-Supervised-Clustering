# Teleassistance-Supervised-Clustering
To read the README.md in Italian, click [here](myLib/README_ita.md)

## Index
- [Enviroment set up](#enviroment-set-up)
- [Overview](#overview)

## Enviroment set up
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

## Overview
This project explores the integration of teleassistance services with supervised clustering techniques.
- **Objective**: Profile patients to understand their contribution to the increase in teleassistance services.
- **Key Focus**: Identify common patterns and behaviors among patients that are linked to the rise in teleassistance usage.
- **Approach**:
  - Group patients based on common patterns or similar behaviors related to the target variable (`incremento_teleassistenze`).
  - Analyze differences among patient groups to determine which features contribute to the increase in teleassistance.
- **Methods**:
  - Use advanced clustering techniques that consider both patient characteristics and the outcome variable (`incremento_teleassistenze`).
 
