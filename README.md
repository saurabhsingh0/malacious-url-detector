# Malacious-URL-Detector
Main Idea: To develop an efficient system to classify web-based URLs by extracting features from the link structure itself. In this approach, we will use N-gram for mining text and classify it using SVMs (Support Vector Machines).

## Content
To understand better, here's a link the our Medium Article:

<a target="_blank" href="https://github-readme-medium-recent-article.vercel.app/medium/@datadive/0"><img src="https://github-readme-medium-recent-article.vercel.app/medium/@datadive/0" alt="Recent Article 0"> 

## Directory Structure

### Extracting Feature Vectors
Contains three .py files for each of type of feature extraction from the URL: Host Based, Content Based, Lexical
The main python notebook can be run to invoke the previous three. Upon executing this, we extract additonal features from our initial dataset and are able to collect data with rich features.

### UI

1. **Web Interface:** There is an interactive interface for users that they can acess to check the validity of our URL

2. **Chrome Extension:** We enabled a chrome extension so our users can identify malicious and non-malicious URLs. The details on how to use it can be found in it's respective readme

### Model

1. **Datasets:** It contains the three datasets that were merged to obtain a final dataset. That dataset was then cleaned features were extracted. The final updated dataset that is being used for our model and visualizations is: "feature-updated-dataset.csv"

2. **ML_Models:** We trained the new dataset using XGBoost Classifier. The relevant files can be found under Malacious_URL_Detection_Using_XGBoostClassifier.ipynb

### Visualization
This directory contains all graphs and visualizations from our rich dataset



