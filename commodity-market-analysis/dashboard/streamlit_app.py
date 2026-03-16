import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add src to path to import ml functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from forecasting_model import load_data, train_ml_models, detect_market_regimes

st.set_page_config(page_title="Global Commodity Intelligence", layout="wide", page_icon="🌎")

# DB Connection Helper
@st.cache_data
def get_data():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'commodity_data.db')
    return load_data(db_path)

@st.cache_data
def get_cluster_data():
    df = get_data()
    return detect_market_regimes(df)

@st.cache_data
def get_ml_metrics():
    df = get_data()
    return train_ml_models(df)

st.title("🌎 Global Commodity Intelligence: Price Analysis and Forecasting (1960–2026)")
st.markdown("A portfolio project demonstrating Data Engineering, EDA, Correlation Networks, and Machine Learning.")

df = get_data()

# Sidebar
st.sidebar.header("Controls")
categories = df['category'].unique()
selected_cat = st.sidebar.selectbox("Select Category", ['All'] + list(categories))

if selected_cat != 'All':
    commodities = df[df['category'] == selected_cat]['commodity_name'].unique()
else:
    commodities = df['commodity_name'].unique()

selected_comm = st.sidebar.selectbox("Select Commodity", commodities)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["Historical Trends & Volatility", "Market Regimes & Correlation", "ML Price Forecasting"])

with tab1:
    st.header(f"Historical Trends for {selected_comm}")
    
    comm_df = df[df['commodity_name'] == selected_comm].copy()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_price = px.line(comm_df, x='date', y='price_nominal_usd', title=f'{selected_comm} Price Evolution')
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        fig_vol = px.line(comm_df, x='date', y='price_12m_volatility', title=f'{selected_comm} 12-Month Rolling Volatility', color_discrete_sequence=['red'])
        st.plotly_chart(fig_vol, use_container_width=True)

with tab2:
    st.header("Market Regime Detection (KMeans Clustering)")
    st.markdown("We dynamically cluster market states using Momentum and 12-Month Volatility.")
    
    reg_df = get_cluster_data()
    comm_reg_df = reg_df[reg_df['commodity_name'] == selected_comm].copy()
    
    fig_reg = px.scatter(comm_reg_df, x='date', y='price_nominal_usd', color='regime_cluster', 
                         title=f'{selected_comm} Colored by Market Regime (0: Stable, 1: High Vol, 2: Shock)',
                         color_continuous_scale=px.colors.qualitative.Set1)
    st.plotly_chart(fig_reg, use_container_width=True)
    
    st.header("Category Correlation")
    st.markdown("Correlation among key benchmark commodities:")
    
    pivot_df = df.groupby(['date', 'commodity_name'])['price_nominal_usd'].mean().unstack()
    comp_list = ['Crude oil, average', 'Natural gas, US', 'Gold', 'Silver', 'Copper', 'Wheat, US SRW', 'Maize']
    comp_df = pivot_df[comp_list].dropna().corr()
    
    fig_corr = px.imshow(comp_df, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.header("Machine Learning Price Forecasting")
    st.markdown("We trained Random Forest and XGBoost models using Lag Features (ARIMA style) to predict the closing prices of key benchmark commodities.")
    
    metrics = get_ml_metrics()
    
    m_cols = st.columns(3)
    idx = 0
    for comm, stat in metrics.items():
        with m_cols[idx]:
            st.subheader(comm)
            st.metric("Latest Price (USD)", f"${stat['latest_price']:.2f}")
            st.markdown("**Random Forest**")
            st.text(f"RMSE: {stat['RF_RMSE']:.2f} | MAE: {stat['RF_MAE']:.2f}")
            st.markdown("**XGBoost**")
            st.text(f"RMSE: {stat['XGB_RMSE']:.2f} | MAE: {stat['XGB_MAE']:.2f}")
        idx += 1
