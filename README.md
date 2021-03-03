# Customer-Segmentation-and-Acquisition
## Udacity Data Science Nanodegree Capstone Project

This repository contains a customer segmentation report for Bertelsmann Arvato Financial Services. The goal is to identify features of individuals that form the customer base a mail-order company and design a prediction model for customer acquisition through a mail marketing campaign.

## Contents

- [Project Description](#projectdescription)
- [The Data](#data)
- [Files](#files)
- [Methods](#methods)
- [Results](#results)

## Project Description
Demographics data for customers of a mail-order sales company in Germany is analyzed and compared against demographics information for the general population to improve customer acquisition. The data was provided by Bertelsmann Arvato Analytics, a company that offers financial services, Information Technology (IT) services, and Supply Chain Management (SCM) solutions for business customers on a global scale. Two main questions motivate this work:

- How can our client (a mail-order company) acquire clients more efficiently?
- Which people in Germany are more likely to become new customers of our client?

Using unsupervised learning, we present a customer segmentation of the company that identifies parts of the population that best describe its core customer base. 

The information used in the customer segmentation is then incorporated in a model designed for targeting a marketing campaign more efficiently. We develop a  classification model to predict which individuals are most likely to become new customers.


## The Data
There are six data files associated with this project:

* `Udacity_AZDIAS_052018.csv`: Demographics data for the general population of Germany; 891 211 persons (rows) x 366 features (columns)
* `Udacity_CUSTOMERS_052018.csv`: Demographics data for customers of a mail-order company; 191 652 persons (rows) x 369 features (columns)
* `Udacity_MAILOUT_052018_TRAIN.csv`: Demographics data for individuals who were targets of a marketing campaign; 42 982 persons (rows) x 367 (columns)
* `Udacity_MAILOUT_052018_TEST.csv`: Demographics data for individuals who were targets of a marketing campaign; 42 833 persons (rows) x 366 (columns)
* `DIAS Information Levels - Attributes 2017.xlsx`: is a top-level list of attributes and descriptions, organized by informational category
* `DIAS Attributes - Values 2017.xlsx`: is a detailed mapping of data values for each feature in alphabetical order

A detailed exploration and processing can be found in the notebook [Data Cleaning and Processing.ipynb](https://github.com/camilomesa/Customer-Segmentation-and-Acquisition/blob/main/Data%20Cleaning%20and%20Processing.ipynb)

## Files
* clean_data.py (Module with cleaning and processing functions)
* Data cleaning and processing.ipynb (Sparsity analysis and cleaning)
* Feature Selection.ipynb (Dimensionality Reduction Using Gini Importance)
* Customer Segmentation and Acquisition.ipynb (Custumer clusters and predictive models)
* Report.pdf

## Methods
This project consisted of creating a data pipeline in which we mine the datasets as follows.

- Data is cleaned and processed.
- The most important features are selected using a customer classification model and their contribution to the prediction.
- Principal components analysis is implemented to further reduce the data set’s dimension and select a combination of the features that explained most of the data set variance.
- The general population is segmented using clustering (k-means). Then we used the distribution of customers among the clusters to find distinctive features of the company’s typical clients. This analysis also helped engineered a feature used in the next step.
- Finally, we trained a gradient boost classification algorithm to classify clients who were likely to respond to a mailout campaign. The final model had an area under the receiver operating characteristic curve score of 0.77.


## Results
The file `Report.pdf` contains a summary of the results and the Jupyter notebooks detailed analysis of the results explanation of the methods. This [medium post](https://mesag-camilo.medium.com/customer-segmentation-report-for-arvato-financial-solutions-5cba34d40c3a) alos presents a summary of the results and methods of this project.
