"""
=============================================================================
Project Title: Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : cli_diagnosis.py
Description  : Enhanced Interactive Command-Line Interface (CLI).
               Supports Indian patient profiles, all 10 disease presets,
               dynamic thresholds, specialist recommendations, and emergency flags.
=============================================================================
"""

import sys
from knowledge_base import (
    ALL_SYMPTOMS,
    DISEASE_PRESETS,
    STUDENT_DETAILS,
    SAMPLE_INDIAN_PATIENTS,
    MEDICAL_DISCLAIMER
)
from inference_engine import InferenceEngine


def print_banner():
    print("=" * 72)
    print("      SANJEEVANI: MEDICAL DIAGNOSIS EXPERT SYSTEM (RULE-BASED)")
    print("      Unit III: Knowledge Representation and Reasoning (KRR)")
    print(f"      Project Team: {', '.join([m['name'] for m in STUDENT_DETAILS['team_members']])}")
    print(f"      Supervisor  : {STUDENT_DETAILS['guide_name']}")
    print("=" * 72)
    print("Inference Algorithm: Forward Chaining | Production Rules (IF-THEN)\n")


def display_symptom_menu():
    print("Available Symptoms in Knowledge Base:")
    print("-" * 72)
    for idx, symptom in enumerate(ALL_SYMPTOMS, 1):
        print(f"[{idx:2d}] {symptom.title():<28}", end="" if idx % 2 != 0 else "\n")
    if len(ALL_SYMPTOMS) % 2 != 0:
        print()
    print("-" * 72)


def display_results(result, patient_info=None):
    if patient_info:
        print("\n" + "-" * 72)
        print(f"PATIENT: {patient_info['name']} | Age: {patient_info['age']} | "
              f"Gender: {patient_info['gender']} | City: {patient_info['city']}")
        print("-" * 72)

    if result.get("is_emergency", False):
        print("\n" + "!" * 72)
        print("  ⚠️  CRITICAL EMERGENCY ALERT:")
        for r in result.get("emergency_reasons", []):
            print(f"     - {r}")
        print("     Immediate clinical attention at the nearest emergency ward is required!")
        print("!" * 72)

    print("\n" + "=" * 72)
    print("                  INFERENCE & REASONING LOG")
    print("=" * 72)
    for step in result["reasoning_steps"]:
        print(step)

    print("=" * 72)
    print("                     DIAGNOSIS RESULTS")
    print("=" * 72)

    top_diseases = result["top_diseases"]

    if not top_diseases:
        print("\n[!] NO DISEASE RULE FIRED.")
        print(f"Reason: No rule met the threshold of >= {result.get('min_symptoms_used', 2)} facts "
              f"and >= {result.get('min_percentage_used', 50.0)}% match rate.")
        print("Recommendation: Consult a General Physician for clinical evaluation.\n")
    else:
        print(f"\nTotal Rules Fired: {len(result['fired_rules'])}\n")
        print(f"{'Rank':<5} {'Disease':<24} {'Match %':<10} {'Specialist':<22}")
        print("-" * 72)
        for rank, d in enumerate(top_diseases, 1):
            print(f"#{rank:<4} {d['disease']:<24} {d['match_percentage']}%{'':<5} {d['doctor_specialist']:<22}")

        primary = top_diseases[0]
        print("\n" + "#" * 72)
        print(f" MOST LIKELY DIAGNOSIS : {primary['disease'].upper()} ({primary['match_percentage']}% Match)")
        print(f" Severity Level        : {primary['severity']}")
        print(f" Consult Specialist    : {primary['doctor_specialist']}")
        print(f" Overview              : {primary['description']}")
        print(f" Matched Symptoms      : {', '.join(primary['matched_symptoms'])}")
        print(f" Unobserved Symptoms   : {', '.join(primary['missing_symptoms']) if primary['missing_symptoms'] else 'None'}")
        print("#" * 72)
        print("\nRecommended Medical & Home Advice:")
        print(primary["advice"])
        print("-" * 72)

    print("\n" + MEDICAL_DISCLAIMER)
    print("=" * 72 + "\n")


def interactive_cli():
    print_banner()
    engine = InferenceEngine()

    current_patient = SAMPLE_INDIAN_PATIENTS[0]

    while True:
        print("\nSelect an Option:")
        print(f"1. Diagnose Patient [{current_patient['name']}, {current_patient['age']}/{current_patient['gender']}]")
        print("2. Run Viva Preset Test Case (Slide 7 Flu, Dengue, Malaria, etc.)")
        print("3. Switch Patient Profile (Indian Names)")
        print("4. View All 10 Production Rules in Knowledge Base")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            display_symptom_menu()
            print("\nEnter symptom numbers separated by comma (e.g., 2, 8, 14)")
            print("OR type symptom names separated by comma:")
            user_input = input(">> ").strip()

            if not user_input:
                print("No symptoms entered. Please try again.")
                continue

            selected = []
            for token in [t.strip() for t in user_input.split(",") if t.strip()]:
                if token.isdigit():
                    num = int(token)
                    if 1 <= num <= len(ALL_SYMPTOMS):
                        selected.append(ALL_SYMPTOMS[num - 1])
                else:
                    t_lower = token.lower()
                    if t_lower in ALL_SYMPTOMS:
                        selected.append(t_lower)
                    else:
                        matches = [s for s in ALL_SYMPTOMS if t_lower in s]
                        if matches:
                            selected.append(matches[0])
                            print(f"Note: Matched '{token}' -> '{matches[0]}'")

            if not selected:
                print("No valid symptoms recognized.")
                continue

            print(f"\nAnalyzing Facts for {current_patient['name']}: {', '.join(selected)}")
            res = engine.diagnose(selected)
            display_results(res, current_patient)

        elif choice == "2":
            print("\nSelect a Viva Preset Case:")
            preset_keys = list(DISEASE_PRESETS.keys())
            for idx, key in enumerate(preset_keys, 1):
                print(f"  [{idx:2d}] {key}")

            p_choice = input(f"\nEnter preset number (1-{len(preset_keys)}): ").strip()
            if p_choice.isdigit() and 1 <= int(p_choice) <= len(preset_keys):
                selected_preset = preset_keys[int(p_choice) - 1]
                facts = DISEASE_PRESETS[selected_preset]
                print(f"\n>>> Running Preset: {selected_preset}")
                print(f"Symptoms: {', '.join(facts)}")
                res = engine.diagnose(facts)
                display_results(res, current_patient)
            else:
                print("Invalid preset choice.")

        elif choice == "3":
            print("\nSelect an Indian Patient Profile:")
            for idx, p in enumerate(SAMPLE_INDIAN_PATIENTS, 1):
                print(f"  [{idx}] {p['name']} ({p['age']} Yrs, {p['gender']}, {p['city']})")
            p_idx = input("Enter choice (1-5): ").strip()
            if p_idx.isdigit() and 1 <= int(p_idx) <= len(SAMPLE_INDIAN_PATIENTS):
                current_patient = SAMPLE_INDIAN_PATIENTS[int(p_idx) - 1]
                print(f"Switched active patient to: {current_patient['name']}")
            else:
                print("Invalid patient selection.")

        elif choice == "4":
            print("\n" + "=" * 72)
            print("                 KNOWLEDGE BASE: 10 PRODUCTION RULES")
            print("=" * 72)
            from knowledge_base import DISEASE_RULES
            for disease, info in DISEASE_RULES.items():
                symptoms_str = " AND ".join(info["symptoms"])
                print(f"RULE: IF {symptoms_str}")
                print(f"      THEN Disease is [{disease}]")
                print(f"      Severity: {info['severity']} | Specialist: {info['doctor_specialist']}\n")

        elif choice == "5":
            print("\nThank you for using the Medical Diagnosis Expert System.")
            break
        else:
            print("Invalid selection. Please choose 1 to 5.")


if __name__ == "__main__":
    interactive_cli()
