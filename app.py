import os
import sys

# --- FORCED INSTALLATION HACK ---
try:
    import plotly.express as px
except ImportError:
    os.system(f"{sys.executable} -m pip install plotly")
    import plotly.express as px

import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="Logistics Weather Command", page_icon="🛵", layout="wide")

# --- INITIALIZE MEMORY (Session State) ---
# This ensures the sliders have a default starting point
if 'slider_hum' not in st.session_state:
    st.session_state.slider_hum = 75.0
if 'slider_wind' not in st.session_state:
    st.session_state.slider_wind = 40.0

# --- SIMULATED DATA ---
@st.cache_data
def get_data():
    np.random.seed(42)
    df = pd.DataFrame({
        'Zone': np.random.choice(['North District', 'South District', 'East Port', 'West Hills'], 500),
        'Humidity3pm': np.random.randint(20, 95, 500),
        'WindGustSpeed': np.random.randint(10, 80, 500),
    })
    # Rain logic based on your Orange chart: Humidity > 71
    df['RainTomorrow'] = np.where(df['Humidity3pm'] > 71, 'Yes', 'No')
    return df

df = get_data()

# --- APP LOGIC ---
st.title("🛵 LogiWeather City Dispatch")
st.markdown("### *Predictive Operations & Rider Safety*")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Drill-Down", "🔮 Risk Predictor", "📋 Action Plan"])

with tab1:
    st.subheader("Current Fleet KPIs")
    c1, c2, c3 = st.columns(3)
    c1.metric("High-Risk Zones", len(df[df['RainTomorrow']=='Yes']))
    c2.metric("Avg. Humidity", f"{df['Humidity3pm'].mean():.1f}%")
    c3.metric("Fleet Status", "Operational")
    
    fig = px.histogram(df, x="Humidity3pm", color="RainTomorrow", title="Rain Risk vs Humidity Factors")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Zone Specific Data")
    st.info("👆 **INTERACTIVE:** Click the checkbox on any row below to instantly send its weather data to the Risk Predictor!")
    
    zone_select = st.selectbox("Pick a District", df['Zone'].unique())
    filtered_df = df[df['Zone'] == zone_select].reset_index(drop=True)
    
    # The interactive dataframe
    selection_event = st.dataframe(
        filtered_df, 
        use_container_width=True,
        on_select="rerun",           # This tells Streamlit to update the app when a row is clicked
        selection_mode="single_row"  # Only allow one row to be selected at a time
    )
    
    # If the user clicks a row, update the Predictor Sliders
    if len(selection_event.selection.rows) > 0:
        selected_index = selection_event.selection.rows[0]
        selected_hum = float(filtered_df.loc[selected_index, 'Humidity3pm'])
        selected_wind = float(filtered_df.loc[selected_index, 'WindGustSpeed'])
        
        # Save to memory
        st.session_state.slider_hum = selected_hum
        st.session_state.slider_wind = selected_
