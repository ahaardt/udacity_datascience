# Disaster Response Pipeline Project

### Introduction:
This Udacity project entails a creation of a model that classifies messages that people send during any kind of catastrophy. It uses ETL and Machine Learning pipelines to categorize these messages into pre-defined categories based on their content. This allows an automated processingfor further use such as a high level assessment of the underlying issue and notifying the correct authorities. 

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/


### File Descriptions
1. README: Containing basic introduction and overview of how to run the program
2. App Folder: Contains run.py to run the web application
3. Data Folder: Containing the data raw data - the actual messages received and categories. The process_data.py file contains the ETL process
4. Models Folder: Contains train_classifier.py, the machine learning model and evaluation
5. Main Folder: model.pkl - pkl file w/ machine learning model results and response.db - databsase containing all responses structured and cleaned
