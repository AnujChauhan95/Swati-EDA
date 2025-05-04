import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Call Center Data Dashboard")

# Sidebar filters
st.sidebar.header("Filter Options")
uploaded_file = st.sidebar.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Explicitly specify the engine to avoid ImportError
    df = pd.read_excel(uploaded_file, engine='openpyxl')

    # Preprocess
    df['CallDate'] = pd.to_datetime(df['StartCallDate'])

    # Dropdown filters
    sectors = st.sidebar.multiselect("Select Sector", options=df['Sector'].unique(), default=df['Sector'].unique())
    operators = st.sidebar.multiselect("Select Operator ID", options=df['OperatorID'].unique(), default=df['OperatorID'].unique())
    locations = st.sidebar.multiselect("Select Location ID", options=df['LocationID'].unique(), default=df['LocationID'].unique())

    # Filter DataFrame
    df_filtered = df[
        df['Sector'].isin(sectors) &
        df['OperatorID'].isin(operators) &
        df['LocationID'].isin(locations)
    ]

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Call Satisfaction by Sector")
        avg_satisfaction_by_sector = df_filtered.groupby('Sector')['CallSatisfaction'].mean().reset_index()
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=avg_satisfaction_by_sector, x='Sector', y='CallSatisfaction', palette='Set2', ax=ax1)
        ax1.set_ylim(0, 1)
        st.pyplot(fig1)

    with col2:
        st.subheader("Average Call Satisfaction per Operator")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=df_filtered, x='OperatorID', y='CallSatisfaction', estimator='mean', ax=ax2)
        st.pyplot(fig2)

    st.subheader("Average Call Satisfaction by Location")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.barplot(data=df_filtered, x='LocationID', y='CallSatisfaction', ax=ax3)
    ax3.set_ylim(0, 1)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
    st.pyplot(fig3)

    st.subheader("Daily Call Volume")
    fig4, ax4 = plt.subplots(figsize=(12, 5))
    df_filtered.groupby('CallDate').size().plot(ax=ax4)
    ax4.set_xlabel("Date")
    ax4.set_ylabel("Number of Calls")
    st.pyplot(fig4)

    st.subheader("Total Calls by Sector")
    calls_by_sector = df_filtered.groupby('Sector').size().reset_index(name='TotalCalls')
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=calls_by_sector, x='Sector', y='TotalCalls', palette='magma', ax=ax5)
    st.pyplot(fig5)

else:
    st.info("Please upload a Call Center Excel file to begin.")
