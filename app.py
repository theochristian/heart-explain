import streamlit as st
from helpers import load_data, generate_prediction_rationale, extract_emr_snippets, plot_feature_importance, display_similar_patients

# Set page config for better UX
st.set_page_config(page_title="Hospital in the Home ML Explainability", layout="wide")

# Load patient data
patients = load_data()

# Sidebar: Patient selection
patient_options = {p["name"]: p for p in patients}
selected_patient_name = st.sidebar.selectbox("Select a patient", list(patient_options.keys()))
patient = patient_options[selected_patient_name]

st.sidebar.markdown("---")
st.sidebar.markdown("**Patient Details**")
st.sidebar.write(f"**Age:** {patient['demographics']['age']}")
st.sidebar.write(f"**Gender:** {patient['demographics']['gender']}")
st.sidebar.write(f"**Ward:** {patient['demographics']['ward']} (Bed {patient['demographics']['bed']})")

# Main panel with tabs
tab1, tab2, tab3, tab4 = st.tabs(["Prediction Summary", "EMR Snippets", "Feature Importance", "Similar Patients"])

with tab1:
    st.header("Prediction Summary")
    # Show overall prediction and similarity score
    eligibility_text = "Eligible" if patient["eligible"] else "Not Eligible"
    st.subheader(f"Prediction: {eligibility_text}")
    st.write(f"**Similarity Score:** {patient['similarity_score']}")
    
    # Display text-based rationale for clinicians (simulate hyperlinks using markdown anchors)
    rationale = generate_prediction_rationale(patient)
    st.markdown(rationale)
    
    # Display additional patient info
    st.markdown("#### Additional Patient Information")
    st.write(f"**Diagnosis:** {patient['clinical_info']['diagnosis']}")
    st.write(f"**Vitals:** BP {patient['clinical_info']['vitals']['BP']}, HR {patient['clinical_info']['vitals']['HR']}")
    st.write(f"**Medical Specialty:** {patient['clinical_info']['medical_specialty']}")

with tab2:
    st.header("EMR Snippets")
    snippets = extract_emr_snippets(patient)
    for snippet in snippets:
        st.markdown(f"**{snippet['type']}** - {snippet['title']} ({snippet['date']})")
        # Display snippet with simulated highlighting (here we just mark with emojis)
        snippet_text = snippet["snippet"]
        for hl in snippet["highlights"]:
            if hl["impact"] == "positive":
                # For example, wrap with a green marker
                snippet_text = snippet_text.replace(hl["span"], f"🟢**{hl['span']}**")
            else:
                snippet_text = snippet_text.replace(hl["span"], f"🔴**{hl['span']}**")
        st.write(snippet_text)
        st.markdown("---")

with tab3:
    st.header("Feature Importance Chart")
    plot_feature_importance(patient)

with tab4:
    st.header("Similar Patients")
    display_similar_patients(patient)
