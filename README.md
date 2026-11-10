# 🏥 AI Based Medical Diagnosis System

> **Mini Project | Department of Electronics and Telecommunication**  
> **Topic:** Medical Diagnosis System for Disease Detection by Symptoms  
> **Programming Language:** Python & Web Technologies  

---

## 📌 1. Project Overview & Problem Statement

In many areas across India and developing regions, medical practitioners are limited in number, leading to long queues and delayed care. Additionally, patients experiencing early or acute symptoms often feel anxious and uncertain about which medical specialist they should consult.

This project implements a **Rule-Based Expert System** that emulates how a physician performs an initial symptom assessment:
1. The user inputs observed symptoms (clinical facts).
2. The system checks these facts against an established medical knowledge base.
3. The inference engine applies **Forward Chaining** to infer candidate diseases.
4. The system calculates a **match percentage**, checks a **firing threshold** ($\ge 2$ symptoms and $\ge 50\%$ match), triages the patient to the right **medical specialist**, flags **critical emergencies**, and generates a **hospital-style printable diagnostic report**.

> **Important Medical Disclaimer:** This system is an educational decision-support prototype developed for the *Knowledge Representation and Reasoning* curriculum. It is intended for preliminary guidance and academic demonstration, **not** as a certified substitute for a licensed doctor.

---

## 🏗️ 2. System Architecture

An Expert System consists of three core components:

```
+---------------------------------------------------------------------------------+
|                                USER INTERFACE                                   |
|   (Desktop Tkinter GUI  /  Interactive Terminal CLI  /  Printable HTML Report)  |
+----------------------------------------+----------------------------------------+
                                         |
                            Observed Facts (Symptoms)
                                         v
+---------------------------------------------------------------------------------+
|                             INFERENCE ENGINE                                    |
|   - Forward Chaining Algorithm (Data-Driven Reasoning)                          |
|   - Evaluates Production Rules: IF <facts> THEN <disease>                       |
|   - Dynamic Viva Threshold Controls (Match % Slider & Min Symptoms Counter)     |
|   - Clinical Emergency Alert Detector (Severe conditions >= 75%)                |
|   - Doctor Specialization Triage (e.g. Pulmonologist, Neurologist, Urologist)   |
+----------------------------------------+----------------------------------------+
                                         |
                                Queries Rules & Facts
                                         v
+---------------------------------------------------------------------------------+
|                              KNOWLEDGE BASE                                     |
|   - 10 Disease Production Rules (Slide 5 of PPT)                                |
|   - Symptom Taxonomies & Severity Ratings                                       |
|   - Doctor Specialization Directory & Verified Clinical Advice                  |
|   - 10 Viva Test Presets (Instant 1-Click Evaluation)                           |
+---------------------------------------------------------------------------------+
```

---

## 📋 3. Knowledge Representation: Production Rules (10 Diseases)

Knowledge is encoded as **production rules** in the form:

$$\text{IF } \text{symptom}_1 \text{ AND } \text{symptom}_2 \dots \text{ THEN Disease is } X$$

| # | Disease Name | Symptoms in Rule (IF Part) | Severity | Consult Specialist | Emergency? |
|:---:|:---|:---|:---:|:---|:---:|
| 1 | **Common Cold** | runny nose, sneezing, sore throat, cough | Mild | General Physician | No |
| 2 | **Flu (Influenza)** | fever, cough, body ache, chills | Moderate | General Physician / Internal Med | No |
| 3 | **Dengue** | high fever, headache, joint pain, rash | Severe | Infectious Disease Specialist | **YES** |
| 4 | **Typhoid** | fever, stomach pain, loss of appetite, weakness | Moderate to Severe | Gastroenterologist / Physician | No |
| 5 | **Food Poisoning** | vomiting, diarrhea, stomach pain, weakness | Moderate | Gastroenterologist / Physician | No |
| 6 | **Migraine** | headache, vomiting, light sensitivity, nausea | Moderate | Neurologist | No |
| 7 | **Malaria** | high fever, chills, sweating, headache | Severe | Infectious Disease Specialist | **YES** |
| 8 | **Asthma** | breathlessness, wheezing, chest tightness, cough | Severe | Pulmonologist (Chest Specialist) | **YES** |
| 9 | **Eye Flu** | red eyes, watery eyes, itchy eyes, sticky eyes | Mild to Moderate | Ophthalmologist (Eye Specialist) | No |
| 10 | **Urinary Tract Infection**| burning urination, frequent urination, lower stomach pain, fever | Moderate | Urologist / Nephrologist | No |

---

## ⚙️ 4. Reasoning Mechanism: Forward Chaining

Forward Chaining is a **data-driven reasoning approach** that starts from known facts (symptoms) and works forward to conclude matching diseases.

### Step-by-Step Reasoning Cycle:
1. **Fact Acquisition:** Patient selects symptoms from GUI or CLI.
2. **Rule Evaluation:** Inference engine checks each rule in Knowledge Base one by one.
3. **Match Calculation:**
   $$\text{Match Percentage} = \left(\frac{\text{Matched Symptoms}}{\text{Total Symptoms in Rule}}\right) \times 100$$
4. **Rule Firing Condition (PPT Slide 6):**
   A rule fires if:
   - **Matched Symptoms $\ge 2$**
   - **AND Match Percentage $\ge 50\%$** *(Adjustable via the Viva slider)*
5. **Ranking & Triage:** Fired rules are ranked by match percentage. Top 3 diseases are displayed with doctor specialization, severity badge, and home care advice.

### 🧪 Working Example (from PPT Slide 7):
* **Input Facts:** `Fever`, `Cough`, `Body ache`
* **Rule Checks:**
  * **Flu:** 3 of 4 match $\rightarrow 75\%$ $\rightarrow$ **FIRED** (Meets $\ge 2$ facts and $\ge 50\%$)
  * **Common Cold:** 1 of 4 match $\rightarrow 25\%$ $\rightarrow$ **NOT FIRED** ($< 2$ facts and $< 50\%$)
  * **Typhoid:** 1 of 4 match $\rightarrow 25\%$ $\rightarrow$ **NOT FIRED** ($< 2$ facts and $< 50\%$)
* **Diagnosis:** **Flu (75% Match)** $\rightarrow$ Consult **General Physician**.

---

## 📂 5. Project File Structure

```
medical-diagnosis/
│
├── index.html              # Standalone Web Application (Host online or open locally)
├── web_server.py           # Local Python web server with REST API endpoints
├── run_web.bat             # 1-click Windows launcher for Web Application
├── DEPLOYMENT_GUIDE.md     # Step-by-step guide to get a free live public website link
│
├── main.py                 # Master entry point (supports GUI, Web, and CLI)
├── gui.py                  # Modern Desktop GUI with student credentials & sliders
├── html_report.py          # Hospital-style printable HTML report generator
├── cli_diagnosis.py        # Terminal / Command-line interface for viva demos
├── inference_engine.py     # Forward Chaining inference engine implementation
├── knowledge_base.py       # Knowledge base (10 diseases, advice, presets, Indian names)
├── test_system.py          # Automated verification test script
├── run_project.bat         # 1-click Windows launcher for Desktop GUI
├── run_cli.bat             # 1-click Windows launcher for CLI
└── README.md               # Complete project documentation & viva guide
```

---

## 🚀 6. How to Run the Project

### Prerequisites:
- Python 3.8+ installed.
- Pure Python standard libraries — **zero `pip install` required!**

### Option A: 1-Click Launch (Windows)
- Double-click **`run_project.bat`** to launch the Desktop Tkinter GUI.
- Double-click **`run_web.bat`** to launch the Web Application in your browser.
- Double-click **`index.html`** to open the web version directly without Python!

### Option B: Terminal / Command Prompt
```bash
# Navigate to project folder
cd "c:\Users\patha\OneDrive\Desktop\medical diagnosis"

# 1. Launch the Desktop GUI
python main.py

# 2. Launch the Web Application (Local Server)
python main.py --web
# or:
python web_server.py

# 3. Launch the terminal CLI version
python main.py --cli

# 4. Run automated viva tests
python test_system.py
```

---

## 🌟 7. Special Prototype Features Built for Presentation

1. **Indian Demographics & Random Patient:** Includes realistic Indian patient profiles (Rahul Verma, Ananya Sharma, Amit Kumar, Pooja Deshmukh) with a 1-click `🎲 Random Patient` button.
2. **1-Click Viva Presets:** A dropdown selector lets you load any of the 10 diseases with 1 click (e.g. Slide 7 Flu, Dengue Outbreak, Malaria Fever, Asthma Attack) to demonstrate during viva without manual checking.
3. **Dynamic Threshold Slider:** Demonstrates the sensitivity of the forward chaining engine live: sliding the threshold from $50\%$ to $80\%$ blocks lower-matching rules in real time!
4. **Emergency Critical Alert:** Automatically triggers a red emergency banner if severe conditions (Dengue, Malaria, Asthma) match with $\ge 75\%$ confidence.
5. **Doctor Specialization Triage:** Recommends the exact specialist (Pulmonologist, Neurologist, Ophthalmologist, Urologist, Gastroenterologist).
6. **Printable Hospital HTML Report:** Generates an official-looking diagnostic report with CSS styling and patient barcode that opens directly in any web browser and can be printed or saved to PDF.

---

## ⚖️ 8. Advantages & Limitations (from PPT Slide 8)

### Advantages:
- **Human-Readable:** Production rules closely mirror medical diagnostic guidelines.
- **Instant Response:** Evaluates all rules within milliseconds.
- **Explainability:** Fully transparent forward chaining execution log (no black box).
- **Maintainable:** Easy to add new disease rules in `knowledge_base.py`.
- **Healthcare Reach:** Valuable for rural health centers and triage stations.

### Limitations:
- **Static Knowledge:** Limited to 10 diseases unless manually updated.
- **No Blood Test Values:** Only evaluates qualitative symptoms, not numeric lab parameters (e.g. platelet count, hemoglobin).
- **Binary Matching:** Does not use fuzzy uncertainty or probabilistic Bayesian weights.
- **Not a Doctor Replacement:** Cannot perform physical stethoscope or imaging examinations.

---

## 🔮 9. Future Scope & Conclusion (from PPT Slide 9)

### Future Scope:
1. Expand to 50+ diseases covering chronic, pediatric, and geriatric conditions.
2. Integrate Machine Learning (Random Forest / Naive Bayes) for hybrid reasoning.
3. Accept numerical laboratory inputs (blood glucose, WBC count, SpO2).
4. Launch as a cross-platform mobile application.

### Conclusion:
Knowledge representation using production rules coupled with Forward Chaining provides a robust, interpretable, and practical foundation for primary medical triage and diagnosis support.

---

## 🎓 10. Viva / Interview Questions & Answers

**Q1: What is an Expert System?**  
*Answer:* An expert system is an AI application that captures the knowledge of human domain experts in a Knowledge Base and uses an Inference Engine to reason and deduce conclusions.

**Q2: What is Forward Chaining? Why use it here?**  
*Answer:* Forward Chaining is a bottom-up, data-driven reasoning strategy starting from known facts (patient symptoms) and applying rules to reach conclusions (diseases). Since medical consultation starts with patient symptoms, forward chaining is the natural choice.

**Q3: What is the rule firing condition in your system?**  
*Answer:* A rule fires if $\text{matched symptoms} \ge 2$ AND $\text{match percentage} \ge 50\%$. This avoids false positives from isolated symptoms like general weakness.

**Q4: What happens if you slide the threshold to 80%?**  
*Answer:* The engine becomes stricter. For example, the Slide 7 Flu case (3 of 4 = 75%) will no longer fire at an 80% threshold, demonstrating how rule firing is governed by the confidence cutoff.

**Q5: What is Doctor Specialization Triage?**  
*Answer:* Rather than just predicting the illness, the system routes the patient to the appropriate medical branch (e.g. Asthma $\rightarrow$ Pulmonologist, Migraine $\rightarrow$ Neurologist), preventing clinic misdirection.
