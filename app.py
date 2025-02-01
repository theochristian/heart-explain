import streamlit as st
import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dummy data for patients
dummy_data = {
    "Patient A": {
        "summary": {
            "eligible": "Eligible: stable vitals and no acute issues.",
            "not_eligible": "Not Suitable: history of falls."
        },
        "emr_positive": "Stable vitals recorded on multiple occasions.",
        "emr_negative": "Recent falls noted in nursing notes.",
        "feature_importance": {
            "Feature": ["Vital Stability", "Recent Falls", "Comorbidities"],
            "Importance": [0.6, 0.3, 0.1],
            "Impact": ["Positive", "Negative", "Neutral"]
        },
        "kg": {
            "nodes": ["Hypertension", "Obesity", "Diabetes"],
            "edges": [("Hypertension", "Diabetes"), ("Obesity", "Diabetes")]
        }
    },
    "Patient B": {
        "summary": {
            "eligible": "Eligible: controlled asthma.",
            "not_eligible": "Not Suitable: risk of COPD exacerbation."
        },
        "emr_positive": "Asthma appears well-controlled.",
        "emr_negative": "Signs of COPD detected in recent tests.",
        "feature_importance": {
            "Feature": ["Asthma Control", "COPD Risk", "Smoking History"],
            "Importance": [0.5, 0.4, 0.1],
            "Impact": ["Positive", "Negative", "Negative"]
        },
        "kg": {
            "nodes": ["Asthma", "COPD", "Pneumonia"],
            "edges": [("Asthma", "COPD")]
        }
    },
    "Patient C": {
        "summary": {
            "eligible": "Eligible: minor fracture with low risk.",
            "not_eligible": "Not Suitable: concerns of underlying osteoporosis."
        },
        "emr_positive": "X-ray shows a minor fracture.",
        "emr_negative": "Osteoporosis risk factors present.",
        "feature_importance": {
            "Feature": ["Fracture Severity", "Bone Density", "Age"],
            "Importance": [0.4, 0.4, 0.2],
            "Impact": ["Positive", "Negative", "Neutral"]
        },
        "kg": {
            "nodes": ["Fracture", "Osteoporosis"],
            "edges": [("Fracture", "Osteoporosis")]
        }
    }
}

patients = list(dummy_data.keys())

st.sidebar.title("Patient Selection")
selected_patient = st.sidebar.selectbox("Select a Patient", patients)
patient_info = dummy_data[selected_patient]

st.title("Hospital In The Home Model Explainability")

tabs = st.tabs(["Prediction Summary", "Knowledge Graph", "EMR Snippets", "Feature Importance"])

with tabs[0]:
    st.header("Prediction Summary")
    st.subheader(f"Eligibility Summary for {selected_patient}")
    st.write(patient_info["summary"]["eligible"])
    st.write(patient_info["summary"]["not_eligible"])

def render_knowledge_graph(kg_data):
    G = nx.Graph()
    for node in kg_data["nodes"]:
        G.add_node(node)
    for edge in kg_data["edges"]:
        G.add_edge(*edge)
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='#888'),
                            hoverinfo='none', mode='lines')
    node_x, node_y, node_text, node_color = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        node_color.append('#FFA07A')
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=node_text,
        textposition="bottom center",
        marker=dict(showscale=False, color=node_color, size=20, line_width=2)
    )
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="SNOMED-CT-AU Knowledge Graph",
                        showlegend=False,
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    return fig

with tabs[1]:
    st.header("Knowledge Graph Visualization")
    kg_fig = render_knowledge_graph(patient_info["kg"])
    st.plotly_chart(kg_fig)

with tabs[2]:
    st.header("EMR Snippets")
    toggle = st.toggle("Highlight SNOMED-CT-AU Concepts")
    if toggle:
        st.markdown("**Detected SNOMED-CT-AU Concepts Highlighted:**")
        st.markdown("Patient shows *<span style='background-color: yellow;'>Hypertension</span>*.", unsafe_allow_html=True)
    else:
        st.markdown("**Prediction Impact Highlighted:**")
        st.markdown(f"Positive: *<span style='background-color: lightgreen;'>{patient_info['emr_positive']}</span>*.", unsafe_allow_html=True)
        st.markdown(f"Negative: *<span style='background-color: lightcoral;'>{patient_info['emr_negative']}</span>*.", unsafe_allow_html=True)

with tabs[3]:
    st.header("Feature Importance")
    fi = patient_info["feature_importance"]
    feature_data = pd.DataFrame(fi)
    fig = px.bar(feature_data, x="Importance", y="Feature", orientation="h", 
                 color="Impact", color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"})
    fig.update_layout(xaxis_title="Importance Score", yaxis_title="Feature", bargap=0.4)
    st.plotly_chart(fig)

st.caption("Prototype for Model Explainability Dashboard")
