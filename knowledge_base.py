"""
=============================================================================
Project Title: Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : knowledge_base.py
Description  : Contains Knowledge Base (Facts, Rules, Doctor Specialties,
               and Clinical Advice) for 10 common diseases, plus presets
               and Indian patient demographics for viva demonstration.
=============================================================================
"""

# ---------------------------------------------------------------------------
# 1. KNOWLEDGE BASE: PRODUCTION RULES (10 DISEASES)
# ---------------------------------------------------------------------------
# Format:
# IF <symptom_1> AND <symptom_2> ... THEN <Disease>
DISEASE_RULES = {
    "Common Cold": {
        "symptoms": ["runny nose", "sneezing", "sore throat", "cough"],
        "severity": "Mild",
        "doctor_specialist": "General Physician",
        "emergency": False,
        "description": "A viral infectious disease of the upper respiratory tract.",
        "advice": (
            "1. Take adequate rest and stay warm.\n"
            "2. Drink warm fluids (tulsi-ginger tea, warm water, vegetable soup).\n"
            "3. Steam inhalation can help relieve nasal congestion.\n"
            "4. Consult a General Physician if fever develops or cough lasts over a week."
        )
    },
    "Flu": {
        "symptoms": ["fever", "cough", "body ache", "chills"],
        "severity": "Moderate",
        "doctor_specialist": "General Physician / Internal Medicine",
        "emergency": False,
        "description": "Influenza viral infection affecting the respiratory system.",
        "advice": (
            "1. Strict bed rest and high fluid intake are recommended.\n"
            "2. Over-the-counter paracetamol can help reduce fever and body ache (consult pharmacist).\n"
            "3. Keep warm and avoid cold drinks or drafts.\n"
            "4. Seek immediate medical attention if you experience breathing difficulty."
        )
    },
    "Dengue": {
        "symptoms": ["high fever", "headache", "joint pain", "rash"],
        "severity": "Severe",
        "doctor_specialist": "Infectious Disease Specialist / General Physician",
        "emergency": True,
        "description": "Mosquito-borne viral disease causing sudden high fever and severe body pain.",
        "advice": (
            "1. Visit a hospital or clinic immediately for a Complete Blood Count (CBC) test.\n"
            "2. Regularly monitor blood platelet counts as instructed by the doctor.\n"
            "3. Drink plenty of fluids (coconut water, ORS, fresh juices) to prevent dehydration.\n"
            "4. CRITICAL: Avoid aspirin or ibuprofen as they can trigger or worsen internal bleeding."
        )
    },
    "Typhoid": {
        "symptoms": ["fever", "stomach pain", "loss of appetite", "weakness"],
        "severity": "Moderate to Severe",
        "doctor_specialist": "Gastroenterologist / General Physician",
        "emergency": False,
        "description": "Bacterial infection caused by Salmonella typhi, spread through contaminated food/water.",
        "advice": (
            "1. Consult a doctor for a Widal or blood culture test.\n"
            "2. Complete the full course of prescribed antibiotics without skipping.\n"
            "3. Drink only boiled/purified water and eat light, easily digestible home-cooked food (khichdi, porridge).\n"
            "4. Maintain complete rest until body temperature normalizes."
        )
    },
    "Food Poisoning": {
        "symptoms": ["vomiting", "diarrhea", "stomach pain", "weakness"],
        "severity": "Moderate",
        "doctor_specialist": "Gastroenterologist / General Physician",
        "emergency": False,
        "description": "Illness caused by consuming contaminated, spoiled, or toxic food/water.",
        "advice": (
            "1. Stay hydrated by sipping Oral Rehydration Solution (ORS), coconut water, or electrolyte water.\n"
            "2. Avoid solid, spicy, greasy, or dairy foods for 24 hours.\n"
            "3. Gradually introduce bland foods (bananas, boiled rice, curd, plain toast).\n"
            "4. Seek emergency medical care if unable to retain any fluids or if blood appears in stool."
        )
    },
    "Migraine": {
        "symptoms": ["headache", "vomiting", "light sensitivity", "nausea"],
        "severity": "Moderate",
        "doctor_specialist": "Neurologist",
        "emergency": False,
        "description": "Neurological condition causing intense, throbbing unilateral headaches.",
        "advice": (
            "1. Rest in a dark, quiet, and cool room.\n"
            "2. Apply a cold compress or ice pack to your forehead or temples.\n"
            "3. Avoid screen time, bright lights, loud noises, and strong odors.\n"
            "4. Drink water and take prescribed migraine medication early in the attack."
        )
    },
    "Malaria": {
        "symptoms": ["high fever", "chills", "sweating", "headache"],
        "severity": "Severe",
        "doctor_specialist": "Infectious Disease Specialist / General Physician",
        "emergency": True,
        "description": "Life-threatening disease caused by Plasmodium parasites transmitted by Anopheles mosquitoes.",
        "advice": (
            "1. Get an urgent blood smear or rapid diagnostic test (RDT) for Malaria.\n"
            "2. Start doctor-prescribed anti-malarial medication immediately.\n"
            "3. Maintain hydration and manage high fever with cold water sponging.\n"
            "4. Use mosquito nets and repellent to prevent transmission to family members."
        )
    },
    "Asthma": {
        "symptoms": ["breathlessness", "wheezing", "chest tightness", "cough"],
        "severity": "Severe",
        "doctor_specialist": "Pulmonologist (Chest & Respiratory Specialist)",
        "emergency": True,
        "description": "Chronic respiratory condition where airways become inflamed, narrow, and swell.",
        "advice": (
            "1. Use your prescribed rescue inhaler (bronchodilator) immediately as directed.\n"
            "2. Sit upright comfortably and stay calm; do not lie down flat.\n"
            "3. Move away from known triggers (dust, smoke, cold air, pet dander).\n"
            "4. CALL EMERGENCY SERVICES IMMEDIATELY if lips/nails turn pale or inhaler gives no relief."
        )
    },
    "Eye Flu": {
        "symptoms": ["red eyes", "watery eyes", "itchy eyes", "sticky eyes"],
        "severity": "Mild to Moderate",
        "doctor_specialist": "Ophthalmologist (Eye Specialist)",
        "emergency": False,
        "description": "Viral or bacterial conjunctivitis causing inflammation of the eye's conjunctiva.",
        "advice": (
            "1. Clean eye discharge using a clean cotton pad soaked in cool boiled water.\n"
            "2. Wash your hands frequently with soap and DO NOT rub or touch your eyes.\n"
            "3. Avoid sharing towels, pillows, handkerchiefs, or eye makeup with others.\n"
            "4. Wear dark sunglasses to reduce light discomfort and consult an eye specialist."
        )
    },
    "Urinary Tract Infection": {
        "symptoms": ["burning urination", "frequent urination", "lower stomach pain", "fever"],
        "severity": "Moderate",
        "doctor_specialist": "Urologist / Nephrologist",
        "emergency": False,
        "description": "Bacterial infection in any part of the urinary system (kidneys, bladder, urethra).",
        "advice": (
            "1. Consult a physician for a routine urine analysis and antibiotic prescription.\n"
            "2. Drink plenty of water (2.5 to 3.5 liters daily) to flush bacteria out.\n"
            "3. Unsweetened cranberry juice or barley water may help prevent bacterial adherence.\n"
            "4. Do not hold urine for long periods; maintain good personal hygiene."
        )
    }
}

# ---------------------------------------------------------------------------
# 2. SYMPTOM CATEGORIZATION (For UI layout & tabs)
# ---------------------------------------------------------------------------
SYMPTOM_CATEGORIES = {
    "Fever & General": [
        "fever",
        "high fever",
        "chills",
        "sweating",
        "weakness",
        "body ache",
        "joint pain",
        "loss of appetite"
    ],
    "Respiratory & Throat": [
        "cough",
        "runny nose",
        "sneezing",
        "sore throat",
        "breathlessness",
        "wheezing",
        "chest tightness"
    ],
    "Digestive & Stomach": [
        "stomach pain",
        "lower stomach pain",
        "nausea",
        "vomiting",
        "diarrhea"
    ],
    "Head & Eyes": [
        "headache",
        "light sensitivity",
        "red eyes",
        "watery eyes",
        "itchy eyes",
        "sticky eyes"
    ],
    "Other Symptoms": [
        "rash",
        "burning urination",
        "frequent urination"
    ]
}

# Flat list of all unique symptoms sorted alphabetically
ALL_SYMPTOMS = sorted(list({
    symptom
    for rule in DISEASE_RULES.values()
    for symptom in rule["symptoms"]
}))

# ---------------------------------------------------------------------------
# 3. 1-CLICK DEMO PRESETS (For quick viva/presentation demos)
# ---------------------------------------------------------------------------
DISEASE_PRESETS = {
    "Slide 7 Example (Flu - 75%)": ["fever", "cough", "body ache"],
    "Dengue Outbreak Case (100%)": ["high fever", "headache", "joint pain", "rash"],
    "Malaria Fever Cycle (100%)": ["high fever", "chills", "sweating", "headache"],
    "Asthma Respiratory Attack (100%)": ["breathlessness", "wheezing", "chest tightness", "cough"],
    "Food Poisoning Triage (100%)": ["vomiting", "diarrhea", "stomach pain", "weakness"],
    "Migraine Episode (100%)": ["headache", "vomiting", "light sensitivity", "nausea"],
    "Typhoid Fever Case (100%)": ["fever", "stomach pain", "loss of appetite", "weakness"],
    "Common Cold Case (100%)": ["runny nose", "sneezing", "sore throat", "cough"],
    "Eye Flu / Conjunctivitis (100%)": ["red eyes", "watery eyes", "itchy eyes", "sticky eyes"],
    "Urinary Tract Infection (100%)": ["burning urination", "frequent urination", "lower stomach pain", "fever"]
}

# ---------------------------------------------------------------------------
# 4. STUDENT & INDIAN PATIENT SAMPLE DATA (Authentic project touch)
# ---------------------------------------------------------------------------
STUDENT_DETAILS = {
    "project_title": "AI Based Medical Diagnosis System",
    "course": "Mini Project",
    "department": "Department of Electronics and Telecommunication",
    "team_members": [],
    "guide_name": "Department of Electronics and Telecommunication"
}

SAMPLE_INDIAN_PATIENTS = [
    {"name": "Rahul Verma", "age": 24, "gender": "Male", "city": "Delhi"},
    {"name": "Ananya Sharma", "age": 21, "gender": "Female", "city": "Mumbai"},
    {"name": "Amit Kumar", "age": 29, "gender": "Male", "city": "Bengaluru"},
    {"name": "Pooja Deshmukh", "age": 22, "gender": "Female", "city": "Pune"},
    {"name": "Vikram Singh", "age": 35, "gender": "Male", "city": "Jaipur"}
]

# System-wide medical disclaimer
MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This expert system is an academic software prototype developed by students "
    "for educational evaluation in Knowledge Representation and Reasoning (Unit III). "
    "It is NOT a medical device and CANNOT replace clinical judgment. In case of emergency, "
    "please visit the nearest hospital or consult a licensed medical doctor immediately."
)
