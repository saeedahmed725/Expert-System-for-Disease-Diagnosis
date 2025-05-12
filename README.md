# Expert System for Disease Diagnosis

This project implements a rule-based Expert System for diagnosing common diseases based on user-input symptoms. The core logic is implemented using Prolog, which handles rule-based reasoning, with a Python interface using pyswip to directly interact with the Prolog knowledge base. The Streamlit interface allows users to interact with the system easily.

## Project Structure

- `expert_system.pl`: Prolog knowledge base containing facts and rules for disease diagnosis
- `app.py`: Streamlit application with pyswip integration for the user interface
- `requirements.txt`: Dependencies for the project
- `setup.bat`: Windows batch file to help set up the environment
- `run_app.bat`: Windows batch file to run the application

## Prerequisites

To run this project, you need to have the following installed:

1. Python 3.7+
2. SWI-Prolog (must be in your system PATH)

## Installation

1. Clone or download this repository
2. Run the setup script:

```bash
setup.bat
```

Or install the dependencies manually:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the application:

```bash
run_app.bat
```

Or run it directly:

```bash
streamlit run app.py
```

This will open the application in your default web browser.

## How to Use

1. Select the symptoms you are experiencing from the checkboxes
2. Click on "Diagnose" to see the possible diseases and recommended treatments
3. View the results in the expandable sections

## Technical Implementation

- **Knowledge Base**: The Prolog file contains a set of facts (symptoms) and rules (diseases with their associated symptoms and treatments)
- **Interface**: Python communicates directly with the Prolog engine using pyswip
- **Reasoning**: The system uses logical inference to determine which diseases match the user's symptoms
- **User Experience**: Streamlit provides an easy-to-use interface for symptom selection and diagnostic results

## Project Features

- Knowledge representation using Prolog predicates
- Direct integration with SWI-Prolog via pyswip
- Rule-based inference for disease diagnosis
- Interactive user interface built with Streamlit
- Treatment recommendations for diagnosed conditions
- Support for multiple possible diagnoses
- Proper handling of negative conditions (symptoms that should NOT be present)
- Support for OR conditions in disease rules

## Disclaimer

This is an educational project and not a replacement for professional medical advice. Always consult a healthcare professional for proper diagnosis and treatment.

## Future Enhancements

To extend this project, you can:

1. Add more diseases and symptoms to the Prolog knowledge base
2. Implement certainty factors to provide confidence levels for diagnoses
3. Add explanation capabilities to show why a particular diagnosis was made
4. Implement a feature to save diagnosis history
5. Expand the knowledge base with more sophisticated rules
