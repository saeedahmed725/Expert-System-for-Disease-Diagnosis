% Expert System for Disease Diagnosis

% Symptoms facts
symptom(fever).
symptom(cough).
symptom(headache).
symptom(sore_throat).
symptom(fatigue).
symptom(body_ache).
symptom(runny_nose).
symptom(sneezing).
symptom(chills).
symptom(nausea).
symptom(vomiting).
symptom(diarrhea).
symptom(shortness_of_breath).
symptom(chest_pain).
symptom(loss_of_taste).
symptom(loss_of_smell).
symptom(rash).
symptom(joint_pain).
symptom(dizziness).
symptom(abdominal_pain).

% Disease definitions with their symptoms
disease(common_cold) :-
    has_symptom(cough),
    has_symptom(runny_nose),
    has_symptom(sneezing),
    has_symptom(sore_throat),
    not(has_symptom(high_fever)),
    not(has_symptom(severe_headache)).

disease(flu) :-
    has_symptom(fever),
    has_symptom(body_ache),
    has_symptom(fatigue),
    has_symptom(cough),
    has_symptom(headache).

disease(covid_19) :-
    has_symptom(fever),
    has_symptom(cough),
    has_symptom(fatigue),
    (has_symptom(loss_of_taste); has_symptom(loss_of_smell)),
    has_symptom(shortness_of_breath).

disease(allergies) :-
    has_symptom(sneezing),
    has_symptom(runny_nose),
    has_symptom(itchy_eyes),
    not(has_symptom(fever)).

disease(food_poisoning) :-
    has_symptom(nausea),
    has_symptom(vomiting),
    has_symptom(diarrhea),
    has_symptom(abdominal_pain).

disease(migraine) :-
    has_symptom(severe_headache),
    has_symptom(sensitivity_to_light),
    has_symptom(nausea),
    (has_symptom(dizziness); has_symptom(blurred_vision)).

disease(gastroenteritis) :-
    has_symptom(diarrhea),
    has_symptom(abdominal_pain),
    has_symptom(nausea),
    has_symptom(vomiting),
    has_symptom(fever).

disease(pneumonia) :-
    has_symptom(cough),
    has_symptom(fever),
    has_symptom(shortness_of_breath),
    has_symptom(chest_pain),
    has_symptom(fatigue).

% Treatment recommendations
treatment(common_cold, "Rest, drink plenty of fluids, over-the-counter pain relievers may help with symptoms.").
treatment(flu, "Rest, stay hydrated, take acetaminophen or ibuprofen for fever and aches. Antiviral medications if prescribed within 48 hours of symptoms.").
treatment(covid_19, "Isolate, rest, stay hydrated, monitor symptoms. Seek medical attention if experiencing severe symptoms. Follow local health guidelines.").
treatment(allergies, "Avoid allergens, take antihistamines, use nasal sprays. Consider allergy testing for long-term management.").
treatment(food_poisoning, "Stay hydrated, rest, ease back into eating with bland foods. Seek medical attention for severe symptoms or if not improving after 2 days.").
treatment(migraine, "Rest in a quiet, dark room, pain relievers, prescription medications for prevention and treatment.").
treatment(gastroenteritis, "Stay hydrated, rest, eat bland foods when returning to eating. Seek medical attention if symptoms are severe or persistent.").
treatment(pneumonia, "Antibiotics (for bacterial pneumonia), rest, increased fluid intake, medication for fever. Hospitalization may be required in severe cases.").

% Query predicates
diagnose(Disease, Treatment) :-
    disease(Disease),
    treatment(Disease, Treatment).

% Helper for checking multiple possible diseases
diagnose_all(Diseases, Treatments) :-
    findall(Disease-Treatment, diagnose(Disease, Treatment), Pairs),
    pairs_values(Pairs, Diseases, Treatments).

% Extract diseases and treatments from pairs
pairs_values([], [], []).
pairs_values([Disease-Treatment|Pairs], [Disease|Diseases], [Treatment|Treatments]) :-
    pairs_values(Pairs, Diseases, Treatments).
