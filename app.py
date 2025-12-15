import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Labor Market Dashboard",
    layout="wide"
)

# -----------------------------
# Styling
# -----------------------------
BLUE = "#1F4E79"  #Blue

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("labor_data.csv")

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


df = load_data()

if df.empty:
    st.error("labor_data.csv is empty or could not be loaded.")
    st.stop()

# -----------------------------
# Title + subtle blue divider
# -----------------------------
st.markdown(
    f"""
    <h1 style="margin-bottom:0.25rem;">Labor Market Dashboard</h1>
    <hr style="height:3px;border:none;background-color:{BLUE};
        margin-top:0;margin-bottom:1.25rem;" />
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Last updated
# -----------------------------
last_updated = df["date"].max()

st.markdown(
    f"<span style='color:{BLUE}; font-size:13px;'>Last updated: {last_updated.date()}</span>",
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------
# Metric selector (wide format)
# -----------------------------
metric_columns = [
    col for col in df.columns if col != "date"
]

selected_metric = st.selectbox(
    "Select metric",
    metric_columns,
    format_func=lambda x: x.replace("_", " ").title()
)

# -----------------------------
# Prepare data
# -----------------------------
plot_df = df[["date", selected_metric]].dropna()

# -----------------------------
# Section header
# -----------------------------
st.markdown(
    f"<h3 style='color:{BLUE};'>Trend Over Time</h3>",
    unsafe_allow_html=True
)

# -----------------------------
# Line chart
# -----------------------------
fig = px.line(
    plot_df,
    x="date",
    y=selected_metric,
    labels={
        "date": "Date",
        selected_metric: selected_metric.replace("_", " ").title()
    },
    color_discrete_sequence=[BLUE]
)

fig.update_layout(
    height=450,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Summary insight
# -----------------------------
latest_value = plot_df.iloc[-1][selected_metric]
latest_date = plot_df.iloc[-1]["date"].date()

st.write(
    f"Most recent value for **{selected_metric.replace('_', ' ').title()}**: "
    f"**{latest_value}** ({latest_date})"
)

# -----------------------------
# Optional data preview
# -----------------------------
with st.expander("Show data preview"):
    st.dataframe(plot_df, use_container_width=True)

