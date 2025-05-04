
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📞 Call Center EDA Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("CallCenterDataset1.xlsx", engine="openpyxl")


df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

sector_filter = st.sidebar.multiselect("Select Sector", options=df['Sector'].dropna().unique(), default=df['Sector'].dropna().unique())
operator_filter = st.sidebar.multiselect("Select OperatorID", options=df['OperatorID'].dropna().unique(), default=df['OperatorID'].dropna().unique())
location_filter = st.sidebar.multiselect("Select LocationID", options=df['LocationID'].dropna().unique(), default=df['LocationID'].dropna().unique())

# Filter data
filtered_df = df[
    (df['Sector'].isin(sector_filter)) &
    (df['OperatorID'].isin(operator_filter)) &
    (df['LocationID'].isin(location_filter))
]

st.subheader("📊 Average Call Satisfaction by Sector")
avg_satisfaction_by_sector = filtered_df.groupby('Sector')['CallSatisfaction'].mean().reset_index()
fig1, ax1 = plt.subplots(figsize=(8,6))
sns.barplot(data=avg_satisfaction_by_sector, x='Sector', y='CallSatisfaction', palette='Set2', ax=ax1)
ax1.set_title("Average Call Satisfaction by Sector")
ax1.set_ylim(0, 1)
st.pyplot(fig1)

st.subheader("📊 Average Call Satisfaction per Operator")
fig2, ax2 = plt.subplots(figsize=(10,6))
sns.barplot(data=filtered_df, x='OperatorID', y='CallSatisfaction', estimator='mean', ax=ax2)
ax2.set_title("Average Call Satisfaction per Operator")
st.pyplot(fig2)

st.subheader("📊 Average Call Satisfaction by Location")
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.barplot(data=filtered_df, x='LocationID', y='CallSatisfaction', ax=ax3)
ax3.set_title("Average Call Satisfaction by Location")
ax3.set_ylim(0, 1)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader("📈 Daily Call Volume Over Time")
filtered_df['CallDate'] = pd.to_datetime(filtered_df['StartCallDate'])
calls_over_time = filtered_df.groupby('CallDate').size()
fig4, ax4 = plt.subplots(figsize=(12,6))
calls_over_time.plot(ax=ax4)
ax4.set_title("Daily Call Volume")
ax4.set_ylabel("Number of Calls")
st.pyplot(fig4)

st.subheader("📊 Total Calls by Sector")
calls_by_sector = filtered_df.groupby('Sector').size().reset_index(name='TotalCalls')
fig5, ax5 = plt.subplots(figsize=(8,6))
sns.barplot(data=calls_by_sector, x='Sector', y='TotalCalls', palette='magma', ax=ax5)
ax5.set_title("Total Calls by Sector")
st.pyplot(fig5)
