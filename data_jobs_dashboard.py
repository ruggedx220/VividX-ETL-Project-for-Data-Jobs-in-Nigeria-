


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Data Jobs Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_csv("Femi_datajobsng.csv", nrows=1861)
df_2 = pd.read_csv("term_freq.csv", nrows=72)

# Sidebar filters
st.sidebar.header("Please Filter here:")
location = st.sidebar.multiselect(
        "Select the location:",
        options=df["Location"].unique(),
        default=df["Location"].unique()
)

job_Type = st.sidebar.multiselect(
        "Select the Job type:",
        options=df["Job_Type"].unique(),
        default=df["Job_Type"].unique()
)

# Update DataFrame based on user selections
if location and job_Type:
    df_selection = df.query("Location in @location and Job_Type in @job_Type")
elif location:
    df_selection = df.query("Location in @location")
elif job_Type:
    df_selection = df.query("Job_Type in @job_Type")
else:
    df_selection = df

# Main page


# Layout for main content
left_column, middle_column, right_column = st.columns(3)

# Display DataFrame in the left column
with left_column:
    st.title(":bar_chart: Data Jobs Dashboard")
    st.markdown("##")

# Calculate metrics
Total_Jobs = len(df_selection['Title'])
Total_loc = df_selection['Location'].nunique()

# Display metrics in the middle and right columns with increased font size
with middle_column:
    st.subheader("Total Jobs")
    st.markdown(f"<h1 color: white;'>{Total_Jobs}</h1>", unsafe_allow_html=True)
    
with right_column:
    st.subheader("Total Distinct Locations")
    st.markdown(f"<h1 color: white;'>{Total_loc}</h1>", unsafe_allow_html=True)


# Create a row for the visualizations

# Select top 15 words by frequency
top_words = df_2.nlargest(15, 'Frequency')

# Create two columns for the visualizations
viz_column1, viz_column2 = st.columns(2)

# Create a bar chart using Plotly Express and display it in the first column
with viz_column1:
    # Display DataFrame with increased size
    st.dataframe(df_selection, height=600, width=800)

    

# Count the occurrences of each job type
job_type_counts = df['Job_Type'].value_counts()

# Create a pie chart using Plotly Express and display it in the second column
with viz_column2:
    fig_job_type_pie = px.pie(
        values=job_type_counts.values, 
        names=job_type_counts.index, 
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    # Adjust size of the chart
    fig_job_type_pie.update_layout(height=500, width=600)
    st.plotly_chart(fig_job_type_pie, use_container_width=True)
    
fig_terms_freq = px.bar(
    top_words,
    x='Term',
    y='Frequency',
    orientation='v',
    color_discrete_sequence=["#008388"] * len(top_words),
    template="plotly_white"
)

# Adjust size and appearance of the chart
fig_terms_freq.update_layout(
    height=600, 
    width=800,
    plot_bgcolor="rgba(0,0,0,0)",  # Set background color to transparent
    xaxis=dict(showgrid=False)  # Hide gridlines on x-axis
)

st.plotly_chart(fig_terms_freq, use_container_width=True)





