import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import cv2
from pathlib import Path
import tempfile

# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------

API_URL = "http://localhost:5000"

st.set_page_config(
    page_title="AI Wildlife Monitoring",
    layout="wide"
)

st.title("🐾 AI Wildlife Monitoring System")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go To",
    [
        "Dashboard",
        "Species Analytics",
        "Stress Monitoring",
        "Behavior Feed",
        "Video / Live Feed"
    ]
)

# ---------------------------------------------------
# API HELPER
# ---------------------------------------------------

def fetch_api(endpoint):
    try:
        res = requests.get(f"{API_URL}{endpoint}", timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"API error: {endpoint}")
        st.text(str(e))
        return None

# ---------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------

if page == "Dashboard":
    st.header("System Overview")
    dashboard = fetch_api("/dashboard")
    if dashboard:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Animals", dashboard["total_animals"])
        col2.metric("Healthy Animals", dashboard["healthy_animals"])
        col3.metric("Sick Animals", dashboard["sick_animals"])
        col4.metric("Total Enclosures", dashboard["total_enclosures"])

        st.subheader("Species Distribution")
        species_data = dashboard["species_distribution"]
        species_df = pd.DataFrame({
            "Species": list(species_data.keys()),
            "Count": list(species_data.values())
        })
        fig = px.pie(species_df, names="Species", values="Count")
        st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------
# SPECIES ANALYTICS
# ---------------------------------------------------

elif page == "Species Analytics":
    st.header("Species Analytics")
    dashboard = fetch_api("/dashboard")
    if dashboard:
        species_data = dashboard["species_distribution"]
        species_df = pd.DataFrame({
            "Species": list(species_data.keys()),
            "Count": list(species_data.values())
        })
        fig = px.bar(species_df, x="Species", y="Count", color="Species", title="Animals per Species")
        st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------
# STRESS MONITORING
# ---------------------------------------------------

elif page == "Stress Monitoring":
    st.header("Animal Stress Monitoring")
    stress_data = fetch_api("/stress-animals")
    if stress_data:
        stress_df = pd.DataFrame(stress_data, columns=["Name","Species","Stress Events"])
        st.dataframe(stress_df, width="stretch")

        fig = px.bar(stress_df, x="Name", y="Stress Events", color="Stress Events")
        st.plotly_chart(fig, width="stretch")

        # Alerts
        st.subheader("Stress Alerts")
        HIGH_STRESS_THRESHOLD = 5
        alerts = stress_df[stress_df["Stress Events"] > HIGH_STRESS_THRESHOLD]
        if alerts.empty:
            st.success("No animals under high stress.")
        else:
            for _, row in alerts.iterrows():
                st.error(f"{row['Name']} ({row['Species']}) showing HIGH stress!")

        # Heatmap
        st.subheader("Movement Heatmap")
        heatmap_data = stress_df.pivot_table(
            index="Species",
            columns="Name",
            values="Stress Events",
            fill_value=0
        )
        fig_heat = ff.create_annotated_heatmap(
            z=heatmap_data.values,
            x=list(heatmap_data.columns),
            y=list(heatmap_data.index),
            colorscale="Reds"
        )
        st.plotly_chart(fig_heat, width="stretch")

        # AI anomaly detection
        st.subheader("AI Anomaly Detection")
        mean = np.mean(stress_df["Stress Events"])
        std = np.std(stress_df["Stress Events"])
        threshold = mean + 2*std
        anomalies = stress_df[stress_df["Stress Events"] > threshold]
        if anomalies.empty:
            st.success("No abnormal behavior detected.")
        else:
            st.warning("AI detected unusual stress behavior")
            st.dataframe(anomalies, width="stretch")

# ---------------------------------------------------
# BEHAVIOR FEED
# ---------------------------------------------------

elif page == "Behavior Feed":
    st.header("Live Behavior Logs")
    logs = fetch_api("/behavior-logs")
    if logs:
        logs_df = pd.DataFrame(logs, columns=["Name","Species","Behavior","Time"])
        st.dataframe(logs_df, width="stretch")
        st.subheader("Stress Timeline")
        stress_logs = logs_df[logs_df["Behavior"] == "Stress"]
        if not stress_logs.empty:
            timeline = stress_logs.groupby("Time").size().reset_index(name="Events")
            fig = px.line(timeline, x="Time", y="Events", title="Stress Events Over Time")
            st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------
# VIDEO / LIVE FEED
# ---------------------------------------------------

elif page == "Video / Live Feed":
    st.header("Video / Camera Feed Simulation")

    # Upload video
    uploaded_file = st.file_uploader("Upload a video to simulate cage feed", type=["mp4","avi"])
    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        st.video(tfile.name)
        st.info("Video uploaded! YOLO detection can be applied here in future.")

    # Webcam / future cage feed placeholder
    st.subheader("Live Cage Camera Feed (Future)")
    st.markdown("""
    ⚠ Placeholder for live cage camera feeds. Once cameras are installed, live video with real-time analytics will appear here.
    """)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")
st.caption("AI Wildlife Monitoring System | Stress Detection | Real-Time Analytics | Video Ready")
