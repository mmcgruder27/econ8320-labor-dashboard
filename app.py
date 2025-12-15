import os
import datetime as dt

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(
    page_title="U.S. Labor Market Dashboard",
    layout="wide"
)

st.title("U.S. Labor Market Dashboard")
st.write(
    """
    This dashboard explores several U.S. labor market indicators using data from the
    Bureau of Labor Statistics (BLS) Public API. Use the options below to change how
    the charts are displayed.
    """
)

# Load data 

@st.cache_data
def load_data(path="labor_data.csv"):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

df = load_data()

# Last updated (from file timestamp)
try:
    last_updated = dt.datetime.fromtimestamp(os.path.getmtime("labor_data.csv"))
    st.caption(f"Data last updated: {last_updated:%B %d, %Y}")
except Exception:
    pass

# Display options
st.subheader("Display options")

c1, c2, c3 = st.columns(3)

with c1:
    chart_style = st.radio("Chart style", ["Line", "Scatter"], horizontal=True)

with c2:
    show_mavg = st.checkbox("Show moving average", value=False)

with c3:
    window = st.slider("Moving average window (months)", min_value=2, max_value=12, value=3, disabled=not show_mavg)

show_table = st.checkbox("Show data table", value=False)


# Summary metrics 
st.subheader("Summary metrics (latest month)")

latest = df.iloc[-1]
prev = df.iloc[-2] if len(df) >= 2 else None

col1, col2, col3, col4 = st.columns(4)

def mom_delta(col):
    if prev is None:
        return None
    return latest[col] - prev[col]

col1.metric(
    "Unemployment Rate",
    f"{latest['unemployment_rate']:.1f}%",
    f"{mom_delta('unemployment_rate'):+.1f} pts" if prev is not None else None
)

col2.metric(
    "Labor Force Participation",
    f"{latest['labor_force_participation']:.1f}%",
    f"{mom_delta('labor_force_participation'):+.1f} pts" if prev is not None else None
)

col3.metric(
    "Average Hourly Earnings",
    f"${latest['average_hourly_earnings']:,.2f}",
    f"{mom_delta('average_hourly_earnings'):+.2f}" if prev is not None else None
)

col4.metric(
    "Nonfarm Employment",
    f"{int(latest['nonfarm_employment']):,} (thousands)",
    f"{int(mom_delta('nonfarm_employment')):+,} (thousands)" if prev is not None else None
)

# plot

def plot_series(y_col, y_label, note_text):
    fig, ax = plt.subplots()

    if chart_style == "Scatter":
        ax.scatter(df["date"], df[y_col])
    else:
        ax.plot(df["date"], df[y_col])

    if show_mavg:
        mavg = df[y_col].rolling(window=window).mean()
        ax.plot(df["date"], mavg)

    ax.set_xlabel("Date")
    ax.set_ylabel(y_label)
    st.pyplot(fig)

    st.write(note_text)

# Tabs 

tab1, tab2, tab3, tab4 = st.tabs([
    "Unemployment",
    "Participation",
    "Hourly Earnings",
    "Nonfarm Employment"
])

with tab1:
    st.subheader("Unemployment Rate Over Time")
    plot_series(
        "unemployment_rate",
        "Percent",
        "This chart shows how the unemployment rate changes over time."
    )

with tab2:
    st.subheader("Labor Force Participation Rate Over Time")
    plot_series(
        "labor_force_participation",
        "Percent",
        "This chart shows how the labor force participation rate moves over time."
    )

with tab3:
    st.subheader("Average Hourly Earnings Over Time")
    plot_series(
        "average_hourly_earnings",
        "Dollars",
        "This chart shows the trend in average hourly earnings over time."
    )

with tab4:
    st.subheader("Total Nonfarm Employment Over Time")
    plot_series(
        "nonfarm_employment",
        "Employment (Thousands)",
        "This chart shows total nonfarm employment over time (in thousands)."
    )


# Download 

st.subheader("Download data")

st.download_button(
    label="Download full dataset (CSV)",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="labor_data.csv",
    mime="text/csv",
)

if show_table:
    st.dataframe(df, use_container_width=True)


# Footer

st.caption(
    "Data Source: U.S. Bureau of Labor Statistics | "
    "Project for ECON 8320 – Tools for Data Analysis"
)
