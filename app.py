import streamlit as st
from helpers import load_data, generate_prediction_rationale, extract_emr_snippets, plot_feature_importance, display_similar_patients

# Set page config for better UX
st.set_page_config(page_title="Hospital In The Home Model Explainability", layout="wide")

# Global title for all pages
st.title("HEART Model Explainability")
st.caption("Prototype designed to build confidence and support the safe and responsible \
           adoption of Machine Learning and Artifificial Intelligence at Alfred Health")

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
    # Use color to highlight the prediction. Green for eligible, red for not eligible.
    if patient["eligible"]:
        prediction_display = '<span style="color: green; font-size:24px;">Eligible</span>'
    else:
        prediction_display = '<span style="color: red; font-size:24px;">Not Eligible</span>'
    
    st.markdown(f"**Prediction:** {prediction_display}", unsafe_allow_html=True)
    st.write(f"**Similarity Score:** {patient['similarity_score']}")

    # Display text-based rationale for clinicians (simulate hyperlinks using markdown anchors)
    rationale = generate_prediction_rationale(patient)
    st.markdown(rationale, unsafe_allow_html=True)
    
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
        
        snippet_text = snippet["snippet"]
        # For each highlight, replace the key text with styled HTML markup
        for hl in snippet["highlights"]:
            if hl["impact"] == "positive":
                styled_span = f'<span style="color: green; font-weight: bold;">{hl["span"]}</span>'
            else:
                styled_span = f'<span style="color: red; font-style: italic; font-weight: bold;">{hl["span"]}</span>'
            snippet_text = snippet_text.replace(hl["span"], styled_span)
        
        st.markdown(snippet_text, unsafe_allow_html=True)
        st.markdown("---")

with tab3:
    st.header("Feature Importance Chart")
    plot_feature_importance(patient)

with tab4:
    st.header("Similar Patients")
    display_similar_patients(patient)

# Global footnote for all pages
# st.caption("Prototype for Model Explainability Data Tool")