# ECON 8320 Labor Dashboard

This project explores several U.S. labor market indicators using data from the Bureau of Labor Statistics (BLS) Public API. The goal is to practice working with an external data source, organizing time-series data, and building a simple interactive dashboard.

## Project overview
The repository includes a Python script that requests monthly labor market data from the BLS API and combines several indicators into a single dataset. That dataset is then used in a Streamlit application to display summary statistics and time-series charts.

## What’s included

**collect_bls.py**  
A Python script that connects to the BLS Public API, requests selected labor market series, and merges them into one dataset.

**labor_data.csv**  
The dataset created by the script. It contains monthly data for:
- Total nonfarm employment  
- Unemployment rate  
- Labor force participation  
- Average hourly earnings  

**app.py**  
A Streamlit application that visualizes the data using summary metrics and charts. The app includes simple interactive options such as switching between indicators and adjusting how charts are displayed.

## How the data updates
The data can be updated manually by running the Python script:
python collect_bls.py
