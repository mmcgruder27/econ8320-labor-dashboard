# Econ 8320 Labor Dashboard

This project pulls monthly labor market data from the BLS Public API and puts everything into one clean file so I can use it for a Streamlit dashboard. The goal is to have the dashboard update automatically whenever new data is released.

## What’s in here

**collect_bls.py**  
My Python script that talks to the BLS API, grabs a few key labor market series, and merges them into one dataset.

**labor_data.csv**  
The dataset created by the script. It includes the last few years of monthly data for:
- Total nonfarm employment  
- Unemployment rate  
- Labor force participation  
- Average hourly earnings  

## How to update the data

From the repo folder, just run:

```
python collect_bls.py
```

That updates `labor_data.csv` with the newest monthly data.

## Why I built this
I wanted a simple way to pull BLS data each month without doing everything by hand.  
This repo is the base for a Streamlit dashboard I'm building for my Econ 8320 class.  
It’s straightforward, easy to update, and keeps everything in one place while I work on the dashboard.

## Notes for future Makaila
- Add more BLS series once I finalize which metrics I want in the dashboard  
- Might create a separate script just for cleaning/transforms  
- Streamlit app will eventually read straight from `labor_data.csv`  

---
Just keeping it simple and functional for now.
