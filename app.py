import os
import sys

# --- FORCED INSTALLATION HACK ---
# This ensures plotly is installed even if the server hiccups
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

# Use Tabs for a clean mobile/PC UI
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
    zone_select = st.selectbox("Pick a District", df['Zone'].unique())
    st.dataframe(df[df['Zone'] == zone_select], use_container_width=True)

with tab3:
    st.subheader("Run a Forecast Prediction")
    st.write("Input tomorrow's expected weather factors to generate the plan.")
    
    # Input sliders
    user_hum = st.slider("Forecasted Humidity at 3 PM (%)", 0, 100, 75)
    user_wind = st.slider("Forecasted Wind Gust (km/h)", 0, 100, 40)
    
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
    
    # SAVE TO SESSION STATE so Tab 4 can see it
    st.session_state['predicted_risk'] = current_risk
    st.session_state['predicted_hum'] = user_hum

with tab4:
    st.subheader("Managerial Action Plan")
    
    # Get the risk from the Predictor tab
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
