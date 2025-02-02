# Hospital In The Home Model Explainability Prototype

This is a proof-of-concept (PoC) Streamlit application built to provide explainability for the Home-based Eligibility Analysis and Recommendation Tool (HEART). The app uses machine learning to predict patient eligibility for home-based care and is designed to build clinician trust by visualizing model predictions, providing text-based rationales, displaying EMR snippets with relevant highlights, showcasing feature importances, and comparing the patient with similar past cases.

## Features

- **Sidebar for Patient Selection:**  
  Select a patient from the list to view detailed prediction information and clinical data.

- **Prediction Summary Tab:**  
  - Displays the prediction (highlighted in green for eligible, red for not eligible).
  - Shows a similarity score.
  - Provides a text-based rationale that explains why the patient was predicted as eligible or not, including references (hyperlinks) to relevant clinical notes.
  - Displays additional patient information (diagnosis, vitals, medical specialty).

- **EMR Snippets Tab:**  
  - Lists snippets extracted from various clinical notes (e.g., ED Triage, Nursing Progress, Radiology Reports).
  - Highlights relevant text spans using color, bold, and italics to indicate positive or negative contributions to the prediction.

- **Feature Importance Chart Tab:**  
  - Visualizes the top feature importances (using a bar chart) contributing to the prediction.

- **Similar Patients Tab:**  
  - Displays the top 3–5 most similar past patients who were successfully treated at home.
  - Each similar patient is shown in a clickable expander with key clinical factors.

## Data Sources & Structure

- **Data File:**  
  The app uses a JSON file (`data.json`) to load dummy patient data. The dataset includes:
  - Patient demographics and admission details.
  - Clinical notes of various types (e.g., ED Triage, Radiology Report).
  - Similarity scores and feature importance values.
  - Similar patients information for nearest-neighbor visualizations.

- **Helper Functions:**  
  Helper functions for loading data, generating rationale, extracting EMR snippets, plotting feature importance, and displaying similar patients are contained in the `helpers.py` file.

  - **Application Logic:**
  The application logic is implemented in the `app.py` file. It includes:
- Loading patient data from the JSON file.
- Setting up the Streamlit interface with a sidebar for patient selection and multiple tabs for different views.
- Displaying prediction summaries, EMR snippets, feature importance charts, and similar patients.
- Utilizing helper functions from `helpers.py` to process and display data effectively.

## Getting Started

### Prerequisites

Ensure you have Python 3.12+ installed along with the following packages:

- streamlit
- matplotlib

Dependancies and python environment managed by UV. 

### Running app

To run app:

```bash
uv run streamlit run app.py
