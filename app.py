import streamlit as st
import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import datetime

# --- Generate Realistic Dummy Data ---
def random_date():
    start = datetime.datetime(2023, 1, 1)
    end = datetime.datetime(2023, 12, 31)
    return (start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )).strftime("%Y-%m-%d")

# Create multiple dummy notes per patient of different types.
def create_notes():
    note_types = ["ED Triage Note", "Medical Inpatient Progress Note", "Nursing Progress Note",
                  "Allied Health Assessment", "Lab Results", "Radiology Report"]
    notes = []
    for i in range(1, 6):
        note_type = random.choice(note_types)
        note = {
            "id": f"note-{i}",
            "type": note_type,
            "title": f"{note_type} Title {i}",
            "date": random_date(),
            "text": (
                f"This is a detailed {note_type.lower()} for the patient. "
                "The patient presents with symptoms including fever, cough, and shortness of breath. "
                "Blood results indicate elevated white cell count and CRP levels. "
                "Further testing is pending, including a COVID-19 PCR and a chest X-ray. "
                "Clinical findings are consistent with a mild to moderate infection, and the patient is currently "
                "stable on the ward. Additional notes mention a history of hypertension and diabetes. "
                "There is also evidence of improvement in respiratory parameters over the past 24 hours."
            )
        }
        notes.append(note)
    return notes

# Generate dummy feature importance data with ~50 features.
def generate_feature_importance():
    features = []
    importance = []
    impact = []
    for i in range(1, 51):
        features.append(f"Feature {i}")
        # Generate random importance scores between 0 and 1, normalized later
        importance.append(random.random())
        impact.append(random.choice(["Positive", "Negative", "Neutral"]))
    # Normalize importance so they sum roughly to 1
    total = sum(importance)
    importance = [round(x/total, 3) for x in importance]
    return {"Feature": features, "Importance": importance, "Impact": impact}

# Generate dummy knowledge graph data with more nodes and edges.
def generate_kg():
    # Each node is a tuple (concept_id, concept_name)
    nodes = [
        ("C001", "Hypertension"), ("C002", "Diabetes Mellitus"), ("C003", "Asthma"),
        ("C004", "Chronic Obstructive Pulmonary Disease"), ("C005", "Pneumonia"),
        ("C006", "Fracture"), ("C007", "Osteoporosis"), ("C008", "Sepsis")
    ]
    # Define some dummy edges between concepts
    edges = [
        (nodes[0], nodes[1]), (nodes[2], nodes[3]), (nodes[4], nodes[7]),
        (nodes[5], nodes[6]), (nodes[1], nodes[7]), (nodes[3], nodes[7]), (nodes[0], nodes[8]) if len(nodes) > 8 else None
    ]
    # Filter out any None entries
    edges = [edge for edge in edges if edge is not None]
    return {"nodes": nodes, "edges": edges}

# Define dummy data per patient.
dummy_data = {
    "Patient A": {
        "demographics": "65-year-old male, with a history of hypertension and type 2 diabetes. Ward: Cardiology, Bed: 12B.",
        "tests": "Blood test: WCC 12x10^9/L, CRP 45 mg/L; Awaiting chest X-ray and PCR results.",
        "specialty": "Cardiology",
        "summary": {
            "eligible": "Eligible: Stable vital signs, controlled blood results, and improvement noted in recent progress. "
                        "See [Lab Results](#note-3) and [Nursing Progress Note](#note-2) for details.",
            "not_eligible": "Not Suitable: Elevated CRP and borderline oxygen saturation in ED triage. "
                            "Refer to [ED Triage Note](#note-1)."
        },
        "notes": create_notes(),
        "feature_importance": generate_feature_importance(),
        "kg": generate_kg()
    },
    "Patient B": {
        "demographics": "72-year-old female, history of COPD and controlled asthma. Ward: Respiratory, Bed: 7A.",
        "tests": "Blood test: WCC 10x10^9/L, CRP 20 mg/L; Awaiting sputum culture and CT scan.",
        "specialty": "Respiratory",
        "summary": {
            "eligible": "Eligible: Well-controlled respiratory parameters, clear imaging. "
                        "See [Radiology Report](#note-4) and [Medical Inpatient Progress Note](#note-2).",
            "not_eligible": "Not Suitable: Concerns of COPD exacerbation due to slight drop in oxygen saturation. "
                            "Refer to [Nursing Progress Note](#note-3)."
        },
        "notes": create_notes(),
        "feature_importance": generate_feature_importance(),
        "kg": generate_kg()
    },
    "Patient C": {
        "demographics": "58-year-old male, minor fracture history with concerns about bone density. Ward: Orthopaedics, Bed: 3C.",
        "tests": "Blood test: Calcium normal, Vitamin D low; Awaiting DXA scan results.",
        "specialty": "Orthopaedics",
        "summary": {
            "eligible": "Eligible: Minor fracture with adequate pain control and stability. "
                        "See [Allied Health Assessment](#note-5).",
            "not_eligible": "Not Suitable: Underlying osteoporosis suspected; further bone density evaluation required. "
                            "Refer to [Lab Results](#note-2)."
        },
        "notes": create_notes(),
        "feature_importance": generate_feature_importance(),
        "kg": generate_kg()
    }
}

patients = list(dummy_data.keys())

# --- Streamlit App ---
st.sidebar.title("Patient Selection")
selected_patient = st.sidebar.selectbox("Select a Patient", patients)
patient_info = dummy_data[selected_patient]

st.title("Hospital In The Home Model Explainability")

tabs = st.tabs(["Prediction Summary", "Knowledge Graph", "EMR Snippets", "Feature Importance"])

# --- Prediction Summary ---
with tabs[0]:
    st.header("Prediction Summary")
    st.subheader(f"Eligibility Summary for {selected_patient}")
    st.markdown(f"**Demographics & Background:** {patient_info['demographics']}")
    st.markdown(f"**Medical Specialty:** {patient_info['specialty']}")
    st.markdown(f"**Tests & Blood Results:** {patient_info['tests']}")
    st.write(patient_info["summary"]["eligible"])
    st.write(patient_info["summary"]["not_eligible"])

# --- Knowledge Graph Visualization ---
def render_knowledge_graph(kg_data):
    G = nx.Graph()
    for concept in kg_data["nodes"]:
        # concept: (concept_id, concept_name)
        G.add_node(concept[1], concept_id=concept[0], concept_name=concept[1])
    for edge in kg_data["edges"]:
        G.add_edge(edge[0][1], edge[1][1])
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=2, color='#888'),
                            hoverinfo='none', mode='lines')
    node_x, node_y, node_text = [], [], []
    hover_text = []
    for node in G.nodes(data=True):
        x, y = pos[node[0]]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node[0])
        hover_text.append(f"Concept ID: {node[1]['concept_id']}<br>Name: {node[1]['concept_name']}")
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=node_text,
        textposition="bottom center", hoverinfo='text',
        hovertext=hover_text,
        marker=dict(showscale=False, color='#FFA07A', size=20, line_width=2)
    )
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="SNOMED-CT-AU Knowledge Graph",
                        showlegend=False,
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))
    return fig

with tabs[1]:
    st.header("Knowledge Graph Visualization")
    kg_fig = render_knowledge_graph(patient_info["kg"])
    st.plotly_chart(kg_fig)

# --- EMR Snippets ---
with tabs[2]:
    st.header("EMR Snippets")
    toggle = st.toggle("Toggle Highlight Mode (SNOMED vs. Prediction Impact)")
    # Display each note with title, type, date and snippet
    for note in patient_info["notes"]:
        st.markdown(f"<a name='{note['id']}'></a>", unsafe_allow_html=True)
        st.subheader(f"{note['title']} ({note['type']}) - {note['date']}")
        # For demonstration, assume the highlight span is the phrase 'elevated' or 'stable' randomly
        snippet = note["text"]
        if toggle:
            # SNOMED highlight view: highlight concepts with tooltips (dummy example)
            snippet = snippet.replace("hypertension", "<span title='Concept ID: C001, Hypertension' style='background-color:yellow;'>hypertension</span>")
            snippet = snippet.replace("diabetes", "<span title='Concept ID: C002, Diabetes Mellitus' style='background-color:yellow;'>diabetes</span>")
        else:
            # Prediction impact view: highlight positive vs negative terms
            snippet = snippet.replace("stable", "<span style='background-color:lightgreen;'>stable</span>")
            snippet = snippet.replace("elevated", "<span style='background-color:lightcoral;'>elevated</span>")
        # Show some context before and after the highlight by truncating to 300 characters
        st.markdown(snippet[:300] + " ...", unsafe_allow_html=True)
        st.markdown("---")

# --- Feature Importance Visualization ---
with tabs[3]:
    st.header("Feature Importance")
    fi = patient_info["feature_importance"]
    feature_data = pd.DataFrame(fi)
    fig = px.bar(feature_data, x="Importance", y="Feature", orientation="h", 
                 color="Impact", color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"})
    fig.update_layout(xaxis_title="Importance Score", yaxis_title="Feature", bargap=0.4, height=800)
    st.plotly_chart(fig)

st.caption("Prototype for Model Explainability Dashboard")
