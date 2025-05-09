# Expert System for Disease Diagnosis

This project implements a simple Expert System capable of diagnosing common diseases based on user-input symptoms. The core logic is implemented using Prolog, which handles rule-based reasoning, while a Streamlit interface in Python allows users to interact with the system easily.

## Project Structure

- `expert_system.pl`: Prolog knowledge base containing facts and rules for disease diagnosis
- `app.py`: Streamlit application for the user interface
- `requirements.txt`: Dependencies for the project

## Prerequisites

To run this project, you need to have the following installed:

1. Python 3.7+

## Installation

1. Clone or download this repository
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Application

To start the Streamlit application:

```bash
streamlit run app.py
```

This will open the application in your default web browser.

## How to Use

1. Select the symptoms you are experiencing from the dropdown menu
2. Click on "Get Diagnosis" to see the possible diseases and recommended treatments
3. View the results in the expandable sections on the right

## Project Features

- Knowledge representation using logical rules
- Rule-based inference for disease diagnosis
- Interactive user interface built with Streamlit
- Treatment recommendations for diagnosed conditions
- Support for multiple possible diagnoses

## Disclaimer

This is an educational project and not a replacement for professional medical advice. Always consult a healthcare professional for proper diagnosis and treatment.

## Extensions

To extend this project, you can:

1. Add more diseases and symptoms to the Prolog knowledge base
2. Implement certainty factors to rank diagnoses
3. Include more detailed treatment information
4. Add disease descriptions and risk factors
5. Implement a feature to save diagnosis history
