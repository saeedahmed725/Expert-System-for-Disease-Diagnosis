import streamlit as st
import subprocess
import os
import re
import tempfile
import platform
import json

# Configuration
TEMP_DIR = tempfile.gettempdir()
FACTS_FILE = os.path.join(TEMP_DIR, "user_symptoms.pl")
RESULTS_FILE = os.path.join(TEMP_DIR, "diagnosis_results.json")

# Get the path to the Prolog knowledge base
def get_prolog_kb_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "expert_system.pl")

# Extract all symptoms from the Prolog file
def extract_symptoms_from_pl_file():
    symptoms = []
    try:
        with open(get_prolog_kb_path(), 'r') as file:
            content = file.read()
            # Find all symptom definitions
            symptom_matches = re.findall(r'symptom\((.*?)\)\.', content)
            symptoms = [s.strip() for s in symptom_matches]
    except Exception as e:
        st.error(f"Error reading Prolog file: {e}")
    return sorted(symptoms)

# Extract all diseases and their treatments from the Prolog file
def extract_diseases_and_treatments():
    diseases_and_treatments = {}
    try:
        with open(get_prolog_kb_path(), 'r') as file:
            content = file.read()
            # Find all treatment definitions
            treatment_matches = re.findall(r'treatment\((.*?),\s*"(.*?)"\)\.', content)
            for match in treatment_matches:
                disease = match[0].strip()
                treatment = match[1].strip()
                diseases_and_treatments[disease] = treatment
    except Exception as e:
        st.error(f"Error reading Prolog treatments: {e}")
    return diseases_and_treatments

# Write selected symptoms to a temporary Prolog facts file
def write_symptoms_to_file(selected_symptoms):
    try:
        with open(FACTS_FILE, 'w') as file:
            for symptom in selected_symptoms:
                file.write(f"has_symptom({symptom}).\n")
    except Exception as e:
        st.error(f"Error writing symptoms to file: {e}")
        return False
    return True

# Run Prolog consultation using direct subprocess call
def run_prolog_diagnosis():
    kb_path = get_prolog_kb_path()
    query_script = f"""
    :- consult('{kb_path}').
    :- consult('{FACTS_FILE}').
    
    % Find all diagnoses and write to file
    :- findall(json([disease=Disease, treatment=Treatment]), 
              (disease(Disease), treatment(Disease, Treatment)), 
              Results),
       open('{RESULTS_FILE}', write, Stream),
       json_write(Stream, Results, []),
       close(Stream).
    
    % Exit Prolog
    :- halt.
    """
    
    # Write the query to a temp file
    query_file = os.path.join(TEMP_DIR, "diagnosis_query.pl")
    with open(query_file, 'w') as f:
        f.write(query_script)
    
    # Run SWI-Prolog with the query file
    try:
        # Determine the command based on OS
        if platform.system() == "Windows":
            # Try both common Windows command names for SWI-Prolog
            try:
                result = subprocess.run(["swipl", "-s", query_file], 
                                      capture_output=True, text=True, timeout=10)
            except FileNotFoundError:
                # If swipl isn't found, try another common name on Windows
                result = subprocess.run(["pl", "-s", query_file], 
                                      capture_output=True, text=True, timeout=10)
        else:
            # Unix-based systems
            result = subprocess.run(["swipl", "-s", query_file], 
                                  capture_output=True, text=True, timeout=10)
            
        # Check for errors
        if result.returncode != 0:
            st.error(f"Prolog execution error: {result.stderr}")
            return []
    except FileNotFoundError:
        st.error("SWI-Prolog not found. Please install SWI-Prolog and make sure it's in your PATH.")
        return []
    except subprocess.TimeoutExpired:
        st.error("Prolog query timed out.")
        return []
    
    # Read results from file
    try:
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r') as f:
                results = json.load(f)
                return results
        else:
            return []
    except Exception as e:
        st.error(f"Error reading results: {e}")
        return []

# Fallback method that doesn't rely on Prolog - uses our own rule engine
def fallback_diagnose(selected_symptoms):
    selected_symptoms_set = set(selected_symptoms)
      # Define disease rules
    disease_rules = {
        "common_cold": {
            "required": {"cough", "runny_nose", "sneezing", "sore_throat"},
            "not_present": {"high_fever", "severe_headache"},
            "min_match": 2
        },
        "flu": {
            "required": {"fever", "body_ache", "fatigue", "cough", "headache"},
            "min_match": 2
        },
        "covid_19": {
            "required": {"fever", "cough", "fatigue"},
            "any_of": {"loss_of_taste", "loss_of_smell"},
            "min_match": 2
        },
        "allergies": {
            "required": {"sneezing", "runny_nose", "itchy_eyes"},
            "not_present": {"fever"},
            "min_match": 2
        },        "food_poisoning": {
            "required": {"nausea", "vomiting", "diarrhea", "abdominal_pain"},
            "min_match": 2
        },
        "migraine": {
            "required": {"severe_headache", "sensitivity_to_light", "nausea"},
            "any_of": {"dizziness", "blurred_vision"},
            "min_match": 1
        },
        "gastroenteritis": {
            "required": {"diarrhea", "abdominal_pain", "nausea", "vomiting", "fever"},
            "min_match": 2
        },
        "pneumonia": {
            "required": {"cough", "fever", "shortness_of_breath", "chest_pain", "fatigue"},
            "min_match": 2
        }
    }
    
    # Define treatments
    treatments = {
        "common_cold": "Rest, drink plenty of fluids, over-the-counter pain relievers may help with symptoms.",
        "flu": "Rest, stay hydrated, take acetaminophen or ibuprofen for fever and aches. Antiviral medications if prescribed within 48 hours of symptoms.",
        "covid_19": "Isolate, rest, stay hydrated, monitor symptoms. Seek medical attention if experiencing severe symptoms. Follow local health guidelines.",
        "allergies": "Avoid allergens, take antihistamines, use nasal sprays. Consider allergy testing for long-term management.",
        "food_poisoning": "Stay hydrated, rest, ease back into eating with bland foods. Seek medical attention for severe symptoms or if not improving after 2 days.",
        "migraine": "Rest in a quiet, dark room, pain relievers, prescription medications for prevention and treatment.",
        "gastroenteritis": "Stay hydrated, rest, eat bland foods when returning to eating. Seek medical attention if symptoms are severe or persistent.",
        "pneumonia": "Antibiotics (for bacterial pneumonia), rest, increased fluid intake, medication for fever. Hospitalization may be required in severe cases."
    }
    results = []
    
    # Special case for common symptom combinations
    if len(selected_symptoms) <= 2:
        if "cough" in selected_symptoms and "body_ache" in selected_symptoms:
            results.append({
                "disease": "possible_flu",
                "treatment": "Rest, stay hydrated, and monitor for additional symptoms. If fever develops or symptoms worsen, consult a healthcare professional."
            })
            
    # Check each disease
    for disease, rule in disease_rules.items():
        required = rule.get("required", set())
        not_present = rule.get("not_present", set())
        any_of = rule.get("any_of", set())
        min_match = rule.get("min_match", 1)
        
        # Count matching required symptoms
        matches = len(selected_symptoms_set.intersection(required))
        
        # Check if any symptoms that should not be present are present
        has_forbidden = len(selected_symptoms_set.intersection(not_present)) > 0
        
        # Check if at least one from the any_of list is present (if applicable)
        any_of_match = any_of and len(selected_symptoms_set.intersection(any_of)) > 0
        
        # Determine if this disease is a match
        if (matches >= min_match and not has_forbidden and 
            (not any_of or any_of_match)):
            results.append({
                "disease": disease,
                "treatment": treatments.get(disease, "No specific treatment available.")
            })
    
    return results

def app():
    st.set_page_config(
        page_title="Medical Expert System",
        page_icon="🏥",
        layout="wide"
    )
    st.title("🏥 Medical Expert System for Disease Diagnosis")
    st.markdown("""
    This expert system uses knowledge representation and logical inference to diagnose
    common diseases based on symptoms. Select your symptoms below to get a diagnosis.
    
    **Disclaimer**: This is an educational project and not a replacement for professional medical advice.
    Always consult a healthcare professional for proper diagnosis and treatment.
    """)
    
    # Get all symptoms from the Prolog file
    all_symptoms = extract_symptoms_from_pl_file()
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Select Your Symptoms")
        selected_symptoms = st.multiselect(
            "Choose all symptoms you are experiencing:",
            all_symptoms,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if st.button("Get Diagnosis", type="primary"):
            if not selected_symptoms:
                st.warning("Please select at least one symptom.")
            else:
                st.session_state.run_diagnosis = True
                st.session_state.selected_symptoms = selected_symptoms
    
    with col2:
        st.subheader("Diagnosis Results")
        
        if st.session_state.get('run_diagnosis', False):
            with st.spinner("Analyzing symptoms..."):
                # Always use the fallback method
                results = fallback_diagnose(st.session_state.selected_symptoms)
            
            if results:
                st.success(f"Based on your symptoms, we found {len(results)} possible conditions.")
                
                for i, result in enumerate(results):
                    disease_name = result.get("disease", "Unknown").replace('_', ' ').title()
                    treatment = result.get("treatment", "No treatment information available.")
                    
                    with st.expander(f"Diagnosis {i+1}: {disease_name}", expanded=True):
                        st.markdown(f"**Possible Condition**: {disease_name}")
                        st.markdown(f"**Recommended Action**: {treatment}")
            else:
                st.warning("No specific diagnosis could be determined from the provided symptoms.")
                st.info("Please select more symptoms for a more accurate diagnosis. The system requires multiple symptoms to identify conditions with confidence.")
                st.info("Remember that this is an educational tool and not a replacement for professional medical advice.")
              # Display selected symptoms for reference
            with st.expander("Your Selected Symptoms", expanded=True):
                for symptom in st.session_state.selected_symptoms:
                    st.write(f"• {symptom.replace('_', ' ').title()}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center">
        <p>Medical Expert System | Developed with Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    # Initialize session state
    if 'run_diagnosis' not in st.session_state:
        st.session_state.run_diagnosis = False
    
    app()
