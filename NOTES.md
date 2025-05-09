# Technical Notes

## About the Diagnosis Engine

This project implements a rule-based diagnosis engine directly in Python:

### Rule-Based Engine

This engine is implemented directly in Python and doesn't require any external dependencies. It uses rule-based matching to diagnose diseases based on symptoms. The rules are defined in the application and follow logical inference patterns for medical diagnosis.

Benefits:
- Works without installing SWI-Prolog
- Runs on any system that supports Python
- Fast and reliable

## Technical Implementation Details

1. **Rule Extraction**
   The application extracts symptom and disease information directly from the Prolog file using regular expressions. This allows us to maintain a single source of truth for the knowledge base.

2. **Pattern Matching**
   The engine uses set operations to perform pattern matching, checking if the user's symptoms match the disease criteria.

3. **Streamlit User Interface**
   The UI provides a simple and intuitive interface for selecting symptoms and viewing diagnoses.
