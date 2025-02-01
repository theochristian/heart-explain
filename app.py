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
    return (start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))).strftime("%Y-%m-%d")

def create_notes():
    note_types = ["ED Triage Note", "Medical Inpatient Progress Note", "Nursing Progress Note",
                  "Allied Health Assessment", "Lab Results", "Radiology Report"]
    snomed_spans = [
        ("severe hypertension", "C001", "Hypertension"),
        ("mild diabetes mellitus", "C002", "Diabetes Mellitus"),
        ("chronic asthma symptoms", "C003", "Asthma"),
        ("acute COPD exacerbation", "C004", "Chronic Obstructive Pulmonary Disease"),
        ("possible pneumonia", "C005", "Pneumonia"),
        ("minor fracture", "C006", "Fracture")
    ]
    prediction_spans = [
        ("stable condition", "Positive"),
        ("elevated CRP levels", "Negative"),
        ("improving respiratory status", "Positive"),
        ("declining oxygen saturation", "Negative")
    ]
    notes = []
    for i in range(1, 6):
        note_type = random.choice(note_types)
        snomed_span = random.choice(snomed_spans)
        prediction_span = random.choice(prediction_spans)
        note_text = (
            f"This is a detailed {note_type.lower()} for the patient. "
            f"The patient presents with symptoms including fever, cough, and shortness of breath. "
            "Recent lab results show changes that need to be interpreted in context. "
            "For instance, the patient's condition is noted as " + snomed_span[0] + ". "
            "In other areas, the report highlights that the patient has a " + prediction_span[0] + ". "
            "Additional context is provided by other clinical findings and patient history which suggest further investigation. "
            "The overall assessment indicates a need for close monitoring and potential intervention."
        )
        note = {
            "id": f"note-{i}",
            "type": note_type,
            "title": f"{note_type} Title {i}",
            "date": random_date(),
            "text": note_text,
            "snomed_span": snomed_span,  # (phrase, concept_id, concept_name)
            "prediction_span": prediction_span  # (phrase, impact)
        }
        notes.append(note)
    return notes

def generate_feature_importance():
    features = []
    importance = []
    impact = []
    for i in range(1, 51):
        features.append(f"Word/Bi-gram {i}")
        importance.append(random.random())
        impact.append(random.choice(["Positive", "Negative", "Neutral"]))
    total = sum(importance)
    importance = [round(x/total, 3) for x in importance]
    data = pd.DataFrame({"Feature": features, "Importance": importance, "Impact": impact})
    data = data.sort_values(by="Importance", ascending=False)
    return data

def generate_kg():
    nodes = [
        ("C001", "Hypertension"), ("C002", "Diabetes Mellitus"), ("C003", "Asthma"),
        ("C004", "Chronic Obstructive Pulmonary Disease"), ("C005", "Pneumonia"),
        ("C006", "Fracture"), ("C007", "Osteoporosis"), ("C008", "Sepsis")
    ]
    edges = [
        (nodes[0], nodes[1]), (nodes[2], nodes[3]), (nodes[4], nodes[7]),
        (nodes[5], nodes[6]), (nodes[1], nodes[7]), (nodes[3], nodes[7])
    ]
    return {"nodes": nodes, "edges": edges}

dummy_data = {
    "Patient A": {
        "demographics": "65-year-old male with a history of hypertension and type 2 diabetes. Ward: Cardiology, Bed: 12B.",
        "tests": "Blood test: WCC 12x10^9/L, CRP 45 mg/L; Awaiting chest X-ray and PCR results.",
        "specialty": "Cardiology",
        "prediction": "Eligible",
        "summary": {
            "eligible": "Eligible: Stable vital signs, controlled blood results, and improvement noted in recent progress. See [Lab Results](#note-3) and [Nursing Progress Note](#note-2) for details.",
            "not_eligible": "Not Suitable: Elevated CRP and borderline oxygen saturation in ED triage. Refer to [ED Triage Note](#note-1)."
        },
        "notes": create_notes(),
        "feature_importance": generate_feature_importance(),
        "kg": generate_kg()
    },
    "Patient B": {
        "demographics": "72-year-old female with a history of COPD and controlled asthma. Ward: Respiratory, Bed: 7A.",
        "tests": "Blood test: WCC 10x10^9/L, CRP 20 mg/L; Awaiting sputum culture and CT scan.",
        "specialty": "Respiratory",
        "prediction": "Not Eligible",
        "summary": {
            "eligible": "Eligible: Well-controlled respiratory parameters and clear imaging. See [Radiology Report](#note-4) and [Medical Inpatient Progress Note](#note-2).",
            "not_eligible": "Not Suitable: Concerns of COPD exacerbation due to a slight drop in oxygen saturation. Refer to [Nursing Progress Note](#note-3)."
        },
        "notes": create_notes(),
        "feature_importance": generate_feature_importance(),
        "kg": generate_kg()
    },
    "Patient C": {
        "demographics": "58-year-old male with a minor fracture history and concerns about bone density. Ward: Orthopaedics, Bed: 3C.",
        "tests": "Blood test: Calcium normal, Vitamin D low; Awaiting DXA scan results.",
        "specialty": "Orthopaedics",
        "prediction": "Eligible",
        "summary": {
            "eligible": "Eligible: Minor fracture with adequate pain control and stability. See [Allied Health Assessment](#note-5).",
            "not_eligible": "Not Suitable: Suspected underlying osteoporosis; further bone density evaluation required. Refer to [Lab Results](#note-2)."
        },
        "notes": create_notes(),
        "feature_importance": generate_feature_importance(),
        "kg": generate_kg()
    }
}

patients = list(dummy_data.keys())

st.sidebar.title("Patient Selection")
selected_patient = st.sidebar.selectbox("Select a Patient", patients)
patient_info = dummy_data[selected_patient]

st.title("Hospital In The Home Model Explainability")
tabs = st.tabs(["Prediction Summary", "EMR Snippets", "Feature Importance", "SNOMED-CT-AU"])

with tabs[0]:
    st.header("Prediction Summary")
    st.markdown(f"**Demographics & Background:** {patient_info['demographics']}")
    st.markdown(f"**Medical Specialty:** {patient_info['specialty']}")
    st.markdown(f"**Tests & Blood Results:** {patient_info['tests']}")
    prediction = patient_info["prediction"]
    color = "green" if prediction == "Eligible" else "red"
    st.markdown(f"<h3 style='color: {color};'>Prediction: {prediction}</h3>", unsafe_allow_html=True)
    st.write(patient_info["summary"]["eligible"])
    st.write(patient_info["summary"]["not_eligible"])

with tabs[1]:
    st.header("EMR Snippets")
    st.write("Below are multiple clinical notes from different sources. Click on a note hyperlink from the Prediction Summary to jump here.")
    mode = st.radio("Highlight Mode", ["SNOMED", "Prediction Impact"])
    for note in patient_info["notes"]:
        st.markdown(f"<a name='{note['id']}'></a>", unsafe_allow_html=True)
        st.subheader(f"{note['title']} ({note['type']}) - {note['date']}")
        snippet = note["text"]
        if mode == "SNOMED":
            phrase, concept_id, concept_name = note["snomed_span"]
            snippet = snippet.replace(phrase, f"<span title='Concept ID: {concept_id}, {concept_name}' style='background-color: yellow;'>{phrase}</span>")
        else:
            phrase, impact = note["prediction_span"]
            hl_color = "lightgreen" if impact == "Positive" else "lightcoral" if impact == "Negative" else "lightgray"
            snippet = snippet.replace(phrase, f"<span style='background-color: {hl_color};'>{phrase}</span>")
        st.markdown(snippet[:300] + " ...", unsafe_allow_html=True)
        st.markdown("---")

with tabs[2]:
    st.header("Feature Importance")
    st.write("This chart displays the importance of various words/bi-grams extracted from patient records. The features are sorted in descending order by importance.")
    fi = patient_info["feature_importance"]
    fig = px.bar(fi, x="Importance", y="Feature", orientation="h", 
                 color="Impact", color_discrete_map={"Positive": "green", "Negative": "red", "Neutral": "gray"})
    fig.update_layout(xaxis_title="Importance Score", yaxis_title="Word/Bi-gram", bargap=0.4, height=800)
    fig.update_yaxes(categoryorder="total descending")
    st.plotly_chart(fig)

def render_knowledge_graph(kg_data):
    G = nx.Graph()
    for concept in kg_data["nodes"]:
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
        textposition="bottom center", hoverinfo='text', hovertext=hover_text,
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

with tabs[3]:
    st.header("SNOMED-CT-AU")
    st.write("This visualization shows the relationships between SNOMED-CT-AU concepts derived from the patient records. Hover over nodes to see details.")
    kg_fig = render_knowledge_graph(patient_info["kg"])
    st.plotly_chart(kg_fig)

st.caption("Prototype for Model Explainability Dashboard")
