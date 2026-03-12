import os
try:
    import plotly.express as px
except ImportError:
    os.system('pip install plotly')
    import plotly.express as px
    
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="LogiWeather City Dispatch",
    page_icon="🛵",
    layout="wide"
)

# --- DATA ENGINE (Simulating your Orange ML Dataset) ---
@st.cache_data
def get_logistics_data():
    np.random.seed(42)
    rows = 500
    zones = ['North District', 'South District', 'East Port', 'West Hills']
    vehicles = ['Motorcycle', 'Cargo Van', 'Bicycle']
    
    # Logic derived from your Orange Decision Tree: Humidity3pm is the main driver
    rain_tomorrow = np.random.choice(['Yes', 'No'], size=rows, p=[0.3, 0.7])
    hum_3pm = [np.random.normal(75, 10) if r == 'Yes' else np.random.normal(45, 12) for r in rain_tomorrow]
    
    df = pd.DataFrame({
        'Zone': np.random.choice(zones, rows),
        'Vehicle': np.random.choice(vehicles, rows, p=[0.6, 0.3, 0.1]),
        'Humidity3pm': np.clip(hum_3pm, 15, 100),
        'RainTomorrow': rain_tomorrow,
        'WindGustSpeed': np.random.randint(20, 80, size=rows)
    })
    
    # Business metrics
    df['Delay_Risk_Mins'] = np.where(df['RainTomorrow'] == 'Yes', np.random.randint(30, 90), np.random.randint(0, 15))
    return df

df = get_logistics_data()

# --- UI HEADER ---
st.title("🛵 LogiWeather Command Center")
st.markdown("### *Data-Driven Dispatch & Rider Safety*")
st.divider()

# --- NAVIGATION ---
# Optimized for mobile (tabs instead of a deep sidebar)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Drill-Down", "🔮 Risk Predictor", "📋 Action Plan"])

# --- TAB 1: DASHBOARD ---
with tab1:
    col1, col2, col3 = st.columns(3)
    
    # KPIs based on your ML data
    high_risk_count = len(df[df['Humidity3pm'] > 71])
    col1.metric("High-Risk Routes", f"{high_risk_count}", "Weather Warning")
    col2.metric("Avg. Humidity Today", f"{df['Humidity3pm'].mean():.1f}%")
    col3.metric("Fleet Readiness", "88%", "-2% vs Yesterday")
    
    st.subheader("Delay Risk by City Zone")
    fig = px.bar(df, x='Zone', y='Delay_Risk_Mins', color='RainTomorrow', 
                 barmode='group', color_discrete_map={'Yes': '#ef553b', 'No': '#00cc96'})
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: DRILL-DOWN ---
with tab2:
    st.subheader("Filter Active Shipments")
    selected_zone = st.selectbox("Select Zone to Inspect", df['Zone'].unique())
    filtered = df[df['Zone'] == selected_zone]
    
    st.dataframe(filtered[['Vehicle', 'Humidity3pm', 'RainTomorrow', 'Delay_Risk_Mins']], 
                 use_container_width=True, hide_index=True)

# --- TAB 3: RISK PREDICTOR ---
with tab3:
    st.subheader("Tomorrow's Weather Input")
    st.info("Based on your ML Model: Humidity at 3 PM is the strongest factor for rain.")
    
    c1, c2 = st.columns(2)
    with c1:
        in_hum = st.slider("Forecasted Humidity @ 3pm (%)", 0, 100, 72)
        in_wind = st.slider("Wind Gust Speed (km/h)", 0, 100, 45)
    
    with c2:
        # Implementing the specific Logic from your Orange Image
        if in_hum > 71:
            st.error("### prediction: RAIN LIKELY")
            st.warning("Factor Triggered: Humidity > 71%")
            st.metric("Estimated Delay", "+60-90 Mins")
        else:
            st.success("### prediction: NO RAIN")
            st.metric("Estimated Delay", "0-10 Mins")

# --- TAB 4: ACTION PLAN ---
with tab4:
    st.subheader("Managerial Directives")
    
    # Dynamic recommendations based on the data
    if df['Humidity3pm'].mean() > 65:
        st.error("🚨 **CRITICAL ACTION REQUIRED**")
        st.markdown("""
        1. **Rider Gear:** Issue raincoats and waterproof parcel covers to all motorcycle riders.
        2. **Rerouting:** Divert North District e-bikes to West Hills to avoid flood zones.
        3. **Customer Alert:** Trigger 'Weather Delay' SMS to all pending deliveries.
        """)
    else:
        st.success("✅ **STANDARD OPERATIONS**")
        st.write("No weather factors currently disrupting the schedule.")


    st.button("Broadcast Instructions to Fleet")
