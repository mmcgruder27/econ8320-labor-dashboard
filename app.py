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
    This dashboard tracks key U.S. labor market indicators using data from the 
    Bureau of Labor Statistics Public API. The data updates as new monthly 
    labor statistics are released.
    """
)

# ---------------------------
# Load data
# ---------------------------
df = pd.read_csv("labor_data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# ---------------------------
# Summary metrics
# ---------------------------
latest = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Unemployment Rate",
    f"{latest['unemployment_rate']}%"
)

col2.metric(
    "Labor Force Participation",
    f"{latest['labor_force_participation']}%"
)

col3.metric(
    "Average Hourly Earnings",
    f"${latest['average_hourly_earnings']}"
)

col4.metric(
    "Nonfarm Employment",
    f"{int(latest['nonfarm_employment']):,} (thousands)"
)

# ---------------------------
# Charts
# ---------------------------
st.subheader("Unemployment Rate Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(df["date"], df["unemployment_rate"])
ax1.set_xlabel("Date")
ax1.set_ylabel("Percent")
st.pyplot(fig1)

st.write(
    "Unemployment declined early in the sample and then moved higher in later months, reflecting changing labor market conditions"
)

st.subheader("Labor Force Participation Rate Over Time")
fig2, ax2 = plt.subplots()
ax2.plot(df["date"], df["labor_force_participation"])
ax2.set_xlabel("Date")
ax2.set_ylabel("Percent")
st.pyplot(fig2)

st.write(
    "The labor force participation rate remains relatively stable over time, with only modest month to month fluctuations."
)

st.subheader("Average Hourly Earnings Over Time")
fig3, ax3 = plt.subplots()
ax3.plot(df["date"], df["average_hourly_earnings"])
ax3.set_xlabel("Date")
ax3.set_ylabel("Dollars")
st.pyplot(fig3)

st.write(
    "Average hourly earnings show a steady upward trend, reflecting continued wage growth over the observed period."
)

st.subheader("Total Nonfarm Employment Over Time")
fig4, ax4 = plt.subplots()
ax4.plot(df["date"], df["nonfarm_employment"])
ax4.set_xlabel("Date")
ax4.set_ylabel("Employment (Thousands)")
st.pyplot(fig4)

st.write(
    "Total nonfarm employment has increased steadily, aligning with relatively low unemployment rates during the same period."
)

# ---------------------------
# Footer
# ---------------------------
st.caption(
    "Data Source: U.S. Bureau of Labor Statistics | "
    "Project for ECON 8320 – Tools for Data Analysis"
)
