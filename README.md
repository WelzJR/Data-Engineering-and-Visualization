# Data-Engineering-and-Visualization
NYC Motor Vehicle Collisions – Data Processing & Insights (Milestone 1)

This repository contains the work for Milestone 1 of the NYC Motor Vehicle Collisions project. It includes the complete workflow for loading, cleaning, integrating, and analyzing NYC crash data using Python and Google Colab. The processed dataset provides insights into temporal patterns, spatial distribution, crash severity, and contributing factors. This milestone also prepares the data foundation required for the interactive dashboard in Milestone 2.

Project Highlights:

Loading data from NYC Open Data (Crashes + Persons)

Pre-cleaning and handling missing values

Standardizing formats and extracting temporal features

Outlier detection and data validation

Aggregating persons data per collision

Integrating datasets into a single analytical table

Visualizing crash patterns (hour, day, borough)

Severity and contributing factor analysis

Research questions with coded answers

Setup Instructions:

Clone the repository using:
git clone https://github.com/
<your-username>/<your-repo>.git

(Optional) Install dependencies locally using:
pip install -r requirements.txt

Open the main notebook (Milestone1_DataProcessing.ipynb) in Google Colab, Jupyter Notebook, or VS Code.

Run all cells to reproduce the cleaning, integration, and analysis steps.

Running the Notebook in Google Colab:

Open Google Colab.

Click File → Upload notebook.

Select Milestone1_DataProcessing.ipynb.

Run all cells.

Deployment Instructions (for Milestone 2 Web App):
The web dashboard will be added in the next milestone. The deployment workflow will include:

Installing necessary web libraries such as Dash, Plotly, and Pandas.

Running the app locally using:
python app/app.py

Deploying to Render, Vercel, or Heroku:

Build command: pip install -r requirements.txt

Start command: gunicorn app:server

Team Members & Contributions:


[Ali Waleed] – Data Exploration , Data Cleaning  , pre and post Data Integration , Visualization.



Milestone 1 Deliverables Completed:

Dataset loading and initial exploration

Cleaning and preprocessing of crashes and persons tables

Extraction of hour, weekday, month features

Borough standardization

Outlier detection and validation

Persons aggregation and dataset integration

Visualizing patterns and severity

Answering research questions

Preparing dataset for dashboard use
