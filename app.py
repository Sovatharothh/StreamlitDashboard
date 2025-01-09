import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Configuration
st.set_page_config(page_title="Student Performance Dashboard", page_icon="📊", layout="wide")
st.title("📊 Student Performance Dashboard")

# Load Data
uploaded_file = "student-scores.csv"
df = pd.read_csv(uploaded_file)

# Reshape Data for Subject Scores
subject_scores = df.melt(
    id_vars=["id", "gender"],
    value_vars=[
        "math_score", "history_score", "physics_score", "chemistry_score", 
        "biology_score", "english_score", "geography_score"
    ],
    var_name="Subject",
    value_name="Score"
)

# Sidebar Filters
st.sidebar.header("Filters")
subjects = st.sidebar.multiselect("Select Subjects", options=subject_scores["Subject"].unique(), default=subject_scores["Subject"].unique())
genders = st.sidebar.multiselect("Select Gender", options=subject_scores["gender"].unique(), default=subject_scores["gender"].unique())

filtered_df = subject_scores.query("Subject in @subjects and gender in @genders")

# KPI Section
st.markdown("### Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Score", f"{filtered_df['Score'].mean():.2f}")
col2.metric("Highest Score", f"{filtered_df['Score'].max():.2f}")
col3.metric("Lowest Score", f"{filtered_df['Score'].min():.2f}")
col4.metric("Total Students", f"{filtered_df['id'].nunique()}")

# Charts Section
st.markdown("### Visual Insights")
tab1, tab2 = st.tabs(["Score Distribution", "Performance Trends"])

with tab1:
    st.subheader("Score Distribution by Subject and Gender")
    fig = px.histogram(filtered_df, x="Score", color="gender", facet_col="Subject", marginal="box", nbins=20,
                       title="Score Distribution")
    fig.update_layout(bargap=0.2, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Trends in Average Scores")
    trends = filtered_df.groupby(["Subject", "gender"])["Score"].mean().reset_index()
    fig = px.line(trends, x="Subject", y="Score", color="gender", markers=True,
                  title="Average Score Trends by Gender and Subject")
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)



