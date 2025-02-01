import streamlit as st
from py2neo import Graph
import pandas as pd
import plotly.express as px

# --- Neo4j Connection Setup ---
# Replace with your Neo4j credentials
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# --- Sample Data ---
# Placeholder for patient data and model outputs
patients = ["Patient A", "Patient B", "Patient C"]

# --- Streamlit App ---
st.sidebar.title("Patient Selection")
selected_patient = st.sidebar.selectbox("Select a Patient", patients)

st.title("Hospital In The Home Model Explainability")

# Tabs for different explainability modules
tabs = st.tabs(["Prediction Summary", "Knowledge Graph", "EMR Snippets", "Feature Importance"])

# --- Prediction Summary ---
with tabs[0]:
    st.header("Prediction Summary")
    st.subheader(f"Eligibility Summary for {selected_patient}")
    st.write("- Eligible due to stable vital signs and no acute care needs.")
    st.write("- Not suitable due to recent history of falls.")

# --- Knowledge Graph Visualization ---
with tabs[1]:
    st.header("Knowledge Graph Visualization")
    st.write("Visualizing SNOMED-CT-AU concepts linked to detected terms.")

    # Placeholder for graph query and visualization
    query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 10"
    results = graph.run(query)
    st.write("[Knowledge Graph will be rendered here]")

# --- EMR Snippets ---
with tabs[2]:
    st.header("EMR Snippets")
    toggle = st.toggle("Highlight SNOMED-CT-AU Concepts")

    if toggle:
        st.markdown("**Detected SNOMED-CT-AU Concepts Highlighted:**")
        st.markdown("Patient shows *<span style='background-color: yellow;'>Hypertension (SNOMED-CT)</span>*.", unsafe_allow_html=True)
    else:
        st.markdown("**Prediction Impact Highlighted:**")
        st.markdown("Patient has *<span style='background-color: lightgreen;'>stable vitals</span>* but recent *<span style='background-color: lightcoral;'>falls</span>*.", unsafe_allow_html=True)

# --- Feature Importance Visualization ---
with tabs[3]:
    st.header("Feature Importance")

    # Sample feature importance data
    feature_data = pd.DataFrame({
        "Feature": ["Vital Stability", "Recent Falls", "Comorbidities"],
        "Importance": [0.6, 0.3, 0.1],
        "Impact": ["Positive", "Negative", "Neutral"]
    })

    fig = px.bar(feature_data, x="Importance", y="Feature", orientation="h", 
                 color="Impact", color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"})
    fig.update_layout(
        xaxis_title="Importance Score",
        yaxis_title="Feature",
        showlegend=True,
        legend_title="Impact",
        bargap=0.4
    )
    st.plotly_chart(fig)

# --- Footer ---
st.caption("Prototype for Model Explainability Dashboard")
