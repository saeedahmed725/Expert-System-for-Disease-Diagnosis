from pyswip import Prolog
import subprocess
import os
import re
import tempfile
import platform
import json

# Get the path to the Prolog knowledge base
def get_prolog_kb_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, "expert_system.pl")


# Load disease rules from the Prolog file using pyswip
def load_disease_rules_from_prolog():

    try:
        prolog = Prolog()
        prolog.consult(get_prolog_kb_path())
        
        # Extract disease rules from Prolog file
        disease_rules = {}
        
        # # Get all disease predicates
        # for disease_query in list(prolog.query("clause(disease(X), Body)")):
        #     disease_name = disease_query["X"]
        #     disease_rules[disease_name] = {
        #         "required": set(),
        #         "not_present": set(),
        #         "any_of": set()
        #     }
            
        #     # Parse the disease body to extract rules
        #     body_str = str(disease_query["Body"])
            
        #     # Extract positive symptoms (has_symptom)
        #     has_symptoms = re.findall(r'has_symptom\((\w+)\)', body_str)
        #     disease_rules[disease_name]["required"].update(has_symptoms)
            
        #     # Extract negative symptoms (not has_symptom)
        #     not_symptoms = re.findall(r'not\(has_symptom\((\w+)\)\)', body_str)
        #     disease_rules[disease_name]["not_present"].update(not_symptoms)
            
        #     # Extract any_of conditions (symptom1; symptom2)
        #     or_conditions = re.findall(r'\(has_symptom\((\w+)\);\s*has_symptom\((\w+)\)\)', body_str)
        #     for or_cond in or_conditions:
        #         # Remove these from required since they're in any_of
        #         for symptom in or_cond:
        #             if symptom in disease_rules[disease_name]["required"]:
        #                 disease_rules[disease_name]["required"].remove(symptom)
        #         disease_rules[disease_name]["any_of"].update(or_cond)
            
        #     # Set minimum match requirements (default to 1 if very few symptoms, else 2)
        #     required_count = len(disease_rules[disease_name]["required"])
        #     disease_rules[disease_name]["min_match"] = 1 if required_count <= 2 else 2
            
        return disease_rules
    
    except Exception as e:
        return {
            "error" : e
        }

print(load_disease_rules_from_prolog())