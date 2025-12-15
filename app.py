import os
import datetime as dt

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(
    page_title="U.S. Labor Market Dashboard",
    layout="wide"
)

st.title("U.S. Labor Market Dashboard")
st.write(
    """
    This dashboard explores several U.S. labor market indicators using data from the
    Bureau of Labor Statistics (BLS) Public API. Use the filters in the sidebar to
    change the time range and view how the indicators move over time.
    """
)

# ---------------------------
# Load data (cached)
# ---------------------------
@st.cache_data
def load_data(path="labor_data.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

df = load_data()

# ---------------------------
# Last updated (from file timestamp)
# ---------------------------
try:
    last_updated = dt.datetime.fromtimestamp(os.path.getmtime("labor_data.csv"))
    st.caption(f"Data last updated: {last_updated:%B %d, %Y}")
except Exception:
    pass

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("Filters")

min_d, max_d = df["date"].min(), df["date"].max()
start, end = st.sidebar.date_input(
    "Date range",
    value=(min_d.date(), max_d.date())
)

filtered = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)].copy()
filtered = filtered.sort_values("date")

# ---------------------------
# Summary metrics (latest in selected range + change from previous month)
# ---------------------------
st.subheader("Summary metrics")
st.write("Values shown are the latest month in the selected range. The change shows the difference from the previous month.")

def metric_with_delta(label, series, value_format, delta_format):
    """
    Displays a metric for the latest value in 'series' and a delta vs prior value.
    If fewer than 2 observations exist, delta is omitted.
    """
    if len(series) == 0:
        st.metric(label, "—")
        return

    latest_val = series.iloc[-1]

    if len(series) < 2:
        st.metric(label, value_format(latest_val))
        return

    prev_val = series.iloc[-2]
    delta = latest_val - prev_val
    st.metric(label, value_format(latest_val), delta_format(delta))

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_with_delta(
        "Unemployment Rate",
        filtered["unemployment_rate"],
        lambda v: f"{v:.1f}%",
        lambda d: f"{d:+.1f} pts"
    )

with col2:
    metric_with_delta(
        "Labor Force Participation",
        filtered["labor_force_participation"],
        lambda v: f"{v:.1f}%",
        lambda d: f"{d:+.1f} pts"
    )

with col3:
    metric_with_delta(
        "Average Hourly Earnings",
        filtered["average_hourly_earnings"],
        lambda v: f"${v:,.2f}",
        lambda d: f"{d:+.2f}"
    )

with col4:
    metric_with_delta(
        "Nonfarm Employment",
        filtered["nonfarm_employment"],
        lambda v: f"{int(v):,} (thousands)",
        lambda d: f"{int(d):+,} (thousands)"
    )

# ---------------------------
# Charts
# ---------------------------
st.subheader("Unemployment Rate Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(filtered["date"], filtered["unemployment_rate"])
ax1.set_xlabel("Date")
ax1.set_ylabel("Percent")
st.pyplot(fig1)

st.write(
    "This chart shows how the unemployment rate changes over the selected time period."
)

st.subheader("Labor Force Participation Rate Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(filtered["date"], filtered["labor_force_participation"])
ax2.set_xlabel("Date")
ax2.set_ylabel("Percent")
st.pyplot(fig2)

st.write(
    "This chart shows how the labor force participation rate moves over time."
)

st.subheader("Average Hourly Earnings Over Time")
fig3, ax3 = plt.subplots()
ax3.plot(filtered["date"], filtered["average_hourly_earnings"])
ax3.set_xlabel("Date")
ax3.set_ylabel("Dollars")
st.pyplot(fig3)

st.write(
    "This chart shows the trend in average hourly earnings over the selected months."
)

st.subheader("Total Nonfarm Employment Over Time")
fig4, ax4 = plt.subplots()
ax4.plot(filtered["date"], filtered["nonfarm_employment"])
ax4.set_xlabel("Date")
ax4.set_ylabel("Employment (Thousands)")
st.pyplot(fig4)

st.write(
    "This chart shows total nonfarm employment over time (in thousands)."
)

# ---------------------------
# Download + data preview
# ---------------------------
st.subheader("Download data")
st.download_button(
    label="Download filtered data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="labor_data_filtered.csv",
    mime="text/csv",
)

with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True)

# ---------------------------
# Footer
# ---------------------------
st.caption(
    "Data Source: U.S. Bureau of Labor Statistics | "
    "Project for ECON 8320 – Tools for Data Analysis"
)
