import streamlit as st
import pandas as pd
import plotly.express as px
import glob

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Bank Customer Churn Analytics",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Customer Segmentation & Churn Pattern Analytics")
st.subheader("European Banking Customer Analysis")

st.write(
    "Interactive analysis of customer churn, demographics, "
    "financial characteristics and customer activity."
)

# -----------------------------
# LOAD EXCEL DATA
# -----------------------------
files = glob.glob("*.xlsx")

if not files:
    st.error("Excel dataset not found in the repository.")
    st.stop()

df = pd.read_excel(files[0])

# -----------------------------
# DATA PREPARATION
# -----------------------------

# Remove unnecessary columns for analysis
if "Surname" in df.columns:
    df = df.drop(columns=["Surname"])

# Convert binary columns to labels
df["ActiveStatus"] = df["IsActiveMember"].map({
    1: "Active",
    0: "Inactive"
})

df["ChurnStatus"] = df["Exited"].map({
    1: "Churned",
    0: "Stayed"
})

# Age groups
df["AgeGroup"] = pd.cut(
    df["Age"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)

# Credit score bands
df["CreditScoreBand"] = pd.cut(
    df["CreditScore"],
    bins=[0, 580, 670, 740, 800, 900],
    labels=[
        "Poor",
        "Fair",
        "Good",
        "Very Good",
        "Excellent"
    ]
)

# Balance segments
df["BalanceSegment"] = pd.cut(
    df["Balance"],
    bins=[-1, 50000, 100000, 150000, float("inf")],
    labels=[
        "Low",
        "Medium",
        "High",
        "Very High"
    ]
)

# Tenure groups
df["TenureGroup"] = pd.cut(
    df["Tenure"],
    bins=[-1, 2, 5, 7, 10],
    labels=[
        "0-2 Years",
        "3-5 Years",
        "6-7 Years",
        "8-10 Years"
    ]
)

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

geography = st.sidebar.multiselect(
    "Geography",
    options=sorted(df["Geography"].dropna().unique()),
    default=sorted(df["Geography"].dropna().unique())
)

gender = st.sidebar.multiselect(
    "Gender",
    options=sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

active_status = st.sidebar.multiselect(
    "Member Status",
    options=["Active", "Inactive"],
    default=["Active", "Inactive"]
)

filtered_df = df[
    (df["Geography"].isin(geography)) &
    (df["Gender"].isin(gender)) &
    (df["ActiveStatus"].isin(active_status))
]

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_customers = len(filtered_df)

churned_customers = filtered_df["Exited"].sum()

churn_rate = (
    churned_customers / total_customers * 100
    if total_customers > 0 else 0
)

active_customers = (
    filtered_df["IsActiveMember"].sum()
)

total_balance = filtered_df["Balance"].sum()

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👥 Total Customers",
    f"{total_customers:,}"
)

col2.metric(
    "🚨 Churned Customers",
    f"{churned_customers:,}"
)

col3.metric(
    "📉 Churn Rate",
    f"{churn_rate:.2f}%"
)

col4.metric(
    "🟢 Active Members",
    f"{active_customers:,}"
)

st.divider()

# -----------------------------
# CHURN BY GENDER
# -----------------------------
st.header("📌 Churn Analysis")

col1, col2 = st.columns(2)

with col1:

    gender_churn = (
        filtered_df.groupby("Gender", observed=True)["Exited"]
        .mean()
        .reset_index()
    )

    gender_churn["ChurnRate"] = gender_churn["Exited"] * 100

    fig_gender = px.bar(
        gender_churn,
        x="Gender",
        y="ChurnRate",
        title="Churn Rate by Gender",
        labels={
            "ChurnRate": "Churn Rate (%)"
        }
    )

    st.plotly_chart(fig_gender, use_container_width=True)

# -----------------------------
# CHURN BY AGE GROUP
# -----------------------------
with col2:

    age_churn = (
        filtered_df.groupby("AgeGroup", observed=True)["Exited"]
        .mean()
        .reset_index()
    )

    age_churn["ChurnRate"] = age_churn["Exited"] * 100

    fig_age = px.bar(
        age_churn,
        x="AgeGroup",
        y="ChurnRate",
        title="Churn Rate by Age Group",
        labels={
            "ChurnRate": "Churn Rate (%)"
        }
    )

    st.plotly_chart(fig_age, use_container_width=True)

# -----------------------------
# CHURN BY GEOGRAPHY
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    geo_churn = (
        filtered_df.groupby("Geography", observed=True)["Exited"]
        .mean()
        .reset_index()
    )

    geo_churn["ChurnRate"] = geo_churn["Exited"] * 100

    fig_geo = px.bar(
        geo_churn,
        x="Geography",
        y="ChurnRate",
        title="Churn Rate by Geography",
        labels={
            "ChurnRate": "Churn Rate (%)"
        }
    )

    st.plotly_chart(fig_geo, use_container_width=True)

# -----------------------------
# ACTIVE VS INACTIVE
# -----------------------------
with col2:

    active_churn = (
        filtered_df.groupby("ActiveStatus", observed=True)["Exited"]
        .mean()
        .reset_index()
    )

    active_churn["ChurnRate"] = active_churn["Exited"] * 100

    fig_active = px.bar(
        active_churn,
        x="ActiveStatus",
        y="ChurnRate",
        title="Churn Rate: Active vs Inactive Members",
        labels={
            "ChurnRate": "Churn Rate (%)"
        }
    )

    st.plotly_chart(fig_active, use_container_width=True)

# -----------------------------
# CREDIT SCORE & TENURE
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    credit_churn = (
        filtered_df.groupby("CreditScoreBand", observed=True)["Exited"]
        .mean()
        .reset_index()
    )

    credit_churn["ChurnRate"] = credit_churn["Exited"] * 100

    fig_credit = px.bar(
        credit_churn,
        x="CreditScoreBand",
        y="ChurnRate",
        title="Churn Rate by Credit Score Band",
        labels={
            "ChurnRate": "Churn Rate (%)"
        }
    )

    st.plotly_chart(fig_credit, use_container_width=True)

with col2:

    tenure_churn = (
        filtered_df.groupby("TenureGroup", observed=True)["Exited"]
        .mean()
        .reset_index()
    )

    tenure_churn["ChurnRate"] = tenure_churn["Exited"] * 100

    fig_tenure = px.bar(
        tenure_churn,
        x="TenureGroup",
        y="ChurnRate",
        title="Churn Rate by Tenure",
        labels={
            "ChurnRate": "Churn Rate (%)"
        }
    )

    st.plotly_chart(fig_tenure, use_container_width=True)

# -----------------------------
# BALANCE SEGMENT
# -----------------------------
balance_churn = (
    filtered_df.groupby("BalanceSegment", observed=True)["Exited"]
    .mean()
    .reset_index()
)

balance_churn["ChurnRate"] = balance_churn["Exited"] * 100

fig_balance = px.bar(
    balance_churn,
    x="BalanceSegment",
    y="ChurnRate",
    title="Churn Rate by Balance Segment",
    labels={
        "ChurnRate": "Churn Rate (%)"
    }
)

st.plotly_chart(fig_balance, use_container_width=True)

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.header("📋 Customer Data Preview")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

st.caption(
    "Dashboard developed for Customer Segmentation and "
    "Churn Pattern Analytics in European Banking."
)
