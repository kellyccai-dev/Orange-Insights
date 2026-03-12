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
    st.plotly_chart(fig, width="stretch") # Updated width command

with tab2:
    st.subheader("Zone Specific Data")
    st.info("👆 **INTERACTIVE:** Click the checkbox on any row below to instantly send its weather data to the Risk Predictor!")
    
    zone_select = st.selectbox("Pick a District", df['Zone'].unique())
    filtered_df = df[df['Zone'] == zone_select].reset_index(drop=True)
    
    # The interactive dataframe (FIXED HYPHEN AND WIDTH)
    selection_event = st.dataframe(
        filtered_df, 
        width="stretch", 
        on_select="rerun",           
        selection_mode="single-row"  # Changed from single_row to single-row
    )
    
    # If the user clicks a row, update the Predictor Sliders
    if len(selection_event.selection.rows) > 0:
        selected_index = selection_event.selection.rows[0]
        selected_hum = float(filtered_df.loc[selected_index, 'Humidity3pm'])
        selected_wind = float(filtered_df.loc[selected_index, 'WindGustSpeed'])
        
        # Save to memory
        st.session_state.slider_hum = selected_hum
        st.session_state.slider_wind = selected_wind
        
        st.success(f"✅ Data loaded! Go to the **Risk Predictor** tab to see the forecast for {selected_hum}% Humidity and {selected_wind} km/h Wind.")

with tab3:
    st.subheader("Run a Forecast Prediction")
    st.write("Adjust the sliders manually, or click a row in the Drill-Down tab to auto-fill these.")
    
    user_hum = st.slider("Forecasted Humidity at 3 PM (%)", 0.0, 100.0, key="slider_hum")
    user_wind = st.slider("Forecasted Wind Gust (km/h)", 0.0, 100.0, key="slider_wind")
    
    # Logic based on your Orange ML Decision Tree
    if user_hum > 71:
        current_risk = "HIGH RISK (RAIN)"
        risk_color = "red"
    elif user_hum > 55:
        current_risk = "MODERATE RISK"
        risk_color = "orange"
    else:
        current_risk = "LOW RISK (CLEAR)"
        risk_color = "green"
        
    st.markdown(f"### Predicted Status: :{risk_color}[{current_risk}]")
    st.session_state['predicted_risk'] = current_risk

with tab4:
    st.subheader("Managerial Action Plan")
    
    risk = st.session_state.get('predicted_risk', "No Prediction Run Yet")
    
    if risk == "HIGH RISK (RAIN)":
        st.error("🚨 **CRITICAL: RAIN PROTOCOL ACTIVATED**")
        st.markdown("""
        - **Safety:** Dispatch rain ponchos and waterproof shoe covers to all riders.
        - **Routing:** Suspend motorcycle deliveries in flood-prone North District.
        - **Scheduling:** Call in 5 additional 'On-Call' backup drivers for the afternoon shift.
        - **Customer:** Send automated 'Potential Delay' SMS to all customers.
        """)
    elif risk == "MODERATE RISK":
        st.warning("⚠️ **CAUTION: MONITORING CONDITIONS**")
        st.markdown("""
        - **Safety:** Remind riders to carry standard rain gear.
        - **Routing:** Standard routes, but avoid river-side shortcuts.
        - **Scheduling:** No changes needed yet.
        """)
    elif risk == "LOW RISK (CLEAR)":
        st.success("✅ **NORMAL OPERATIONS**")
        st.markdown("""
        - **Strategy:** Focus on maximum delivery volume. 
        - **Riders:** Standard gear. No weather-related safety measures required.
        """)
    else:
        st.info("Please go to the 'Risk Predictor' tab to set the weather conditions first.")

    st.button("Broadcast Action Plan to Team")
