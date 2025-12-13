import requests
import pandas as pd
from datetime import datetime

# -------------------------------------------------------
# BLS API Settings
# -------------------------------------------------------
API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
SERIES = {
    "nonfarm_employment": "CES0000000001",
    "unemployment_rate": "LNS14000000",
    "labor_force_participation": "LNS11300000",
    "average_hourly_earnings": "CES0500000003"
}

# How many years of data to pull the first time
YEARS = 3
OUTPUT_FILE = "labor_data.csv"


# -------------------------------------------------------
# Function to request BLS series
# -------------------------------------------------------
def fetch_series(series_id, years=YEARS):
    payload = {
        "seriesid": [series_id],
        "startyear": str(datetime.now().year - years),
        "endyear": str(datetime.now().year)
    }

    response = requests.post(API_URL, json=payload)

    if response.status_code != 200:
        raise ValueError(f"BLS API request failed for {series_id}")

    data = response.json()
    observations = data["Results"]["series"][0]["data"]

    df = pd.DataFrame(observations)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["year"] + "-" + df["periodName"] + "-01")

    df = df.sort_values("date")
    return df[["date", "value"]]


# -------------------------------------------------------
# Main collection loop
# -------------------------------------------------------
def collect_all():
    frames = []

    for name, series_id in SERIES.items():
        df = fetch_series(series_id)
        df = df.rename(columns={"value": name})
        frames.append(df)

    # Merge all data on date
    result = frames[0]
    for df in frames[1:]:
        result = pd.merge(result, df, on="date", how="outer")

    result = result.sort_values("date")

    # Save or append
    result.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved updated dataset to {OUTPUT_FILE}")


if __name__ == "__main__":
    collect_all()
