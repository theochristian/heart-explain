import json
import random
import streamlit as st
import matplotlib.pyplot as plt

def load_data(filepath="data.json"):
    """Load patient data from a JSON file."""
    with open(filepath, "r") as f:
        data = json.load(f)
    return data["patients"]

def generate_prediction_rationale(patient):
    """
    Generate a text-based rationale by matching patient EMR info against
    Hospital in the Home criteria.
    """
    criteria = {
        "Condition": patient["clinical_info"]["diagnosis"],
        "Vitals": f"BP {patient['clinical_info']['vitals']['BP']}, HR {patient['clinical_info']['vitals']['HR']}",
        "Blood Results": patient["clinical_info"].get("blood_results", {}),
        "Medical Specialty": patient["clinical_info"]["medical_specialty"]
    }
    
    # Build a simple rationale text (hyperlinks to notes will be simulated using markdown anchors)
    rationale_lines = [f"#### Prediction based on:"]
    for key, value in criteria.items():
        # For blood results (a dict), convert to a string
        if isinstance(value, dict):
            value = ", ".join([f"{k}: {v}" for k,v in value.items()])
        # Create a fake link that in the UI could scroll to a note in the EMR Snippets tab
        rationale_lines.append(f"- **{key}**: {value} ([view note](#emr-snippet))")
    
    # Add similar past cases if available
    if patient["similar_patients"]:
        similar_names = ", ".join([p["name"] for p in patient["similar_patients"]])
        rationale_lines.append(f"- **Similar past cases**: {similar_names}")
    
    return "\n".join(rationale_lines)

def extract_emr_snippets(patient):
    """
    For each note, extract a snippet (limit to 300 characters) and highlight key terms.
    In a real app, you would run an NER model and match against criteria. Here we simulate it.
    """
    snippets = []
    for note in patient["clinical_info"]["notes"]:
        content = note["content"]
        # Simulate a search for key terms: if "pneumonia" or "stable" is found, mark it as positive; "sepsis" as negative.
        highlights = []
        if "pneumonia" in content.lower():
            highlights.append({"span": "pneumonia", "impact": "positive"})
        if "stable" in content.lower():
            highlights.append({"span": "stable", "impact": "positive"})
        if "sepsis" in content.lower():
            highlights.append({"span": "sepsis", "impact": "negative"})
        
        # Trim content to 300 characters while preserving context (here, simply slicing)
        snippet_text = content if len(content) < 300 else content[:300] + "..."
        snippets.append({
            "note_id": note["note_id"],
            "type": note["type"],
            "title": note["title"],
            "date": note["date"],
            "snippet": snippet_text,
            "highlights": highlights
        })
    return snippets

def plot_feature_importance(patient):
    """
    Plot a bar chart of the top features.
    For demo purposes, use matplotlib.
    """
    features = patient["feature_importance"]
    # Sort and select top 10 (or 50 if available)
    sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)[:50]
    labels, scores = zip(*sorted_features)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(labels, scores, color="skyblue")
    ax.invert_yaxis()  # highest scores on top
    ax.set_xlabel("Feature Importance Score")
    ax.set_title("Top Feature Importances")
    st.pyplot(fig)

def display_similar_patients(patient):
    """
    Display similar patients in a clickable format.
    In a real app, clicking could trigger a modal or update the UI.
    """
    similar_patients = patient.get("similar_patients", [])
    if not similar_patients:
        st.info("No similar past patients found.")
        return
    
    for sp in similar_patients:
        with st.expander(f"{sp['name']} - {sp['key_factors']}"):
            st.write(f"**Patient ID:** {sp['id']}")
            st.write(f"**Key Factors:** {sp['key_factors']}")
            # In a full app, you might load more details here.
