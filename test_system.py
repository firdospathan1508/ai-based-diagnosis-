"""
=============================================================================
Project Title: Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : test_system.py
Description  : Automated verification script testing inference engine accuracy,
               emergency detection, dynamic thresholds, and HTML report output.
=============================================================================
"""

import os
import sys
from knowledge_base import DISEASE_RULES, ALL_SYMPTOMS
from inference_engine import InferenceEngine
from html_report import generate_html_report


def run_tests():
    print("=" * 68)
    print("  RUNNING AUTOMATED VERIFICATION TESTS FOR EXPERT SYSTEM")
    print("=" * 68)

    engine = InferenceEngine()
    passed = 0
    total = 0

    # Test 1: Verify Knowledge Base size
    total += 1
    if len(DISEASE_RULES) == 10:
        print("[PASS] Test 1: Knowledge Base contains exactly 10 diseases.")
        passed += 1
    else:
        print(f"[FAIL] Test 1: Expected 10 diseases, found {len(DISEASE_RULES)}")

    # Test 2: Verify Slide 7 Working Example (Flu 75%)
    total += 1
    slide_facts = ["fever", "cough", "body ache"]
    res = engine.diagnose(slide_facts)
    flu_match = next((d for d in res["fired_rules"] if d["disease"] == "Flu"), None)

    if flu_match and flu_match["match_percentage"] == 75.0:
        print("[PASS] Test 2: Slide 7 Example passed (Flu matched 3/4 = 75.0% and FIRED).")
        passed += 1
    else:
        print(f"[FAIL] Test 2: Slide 7 Example failed: {res.get('fired_rules')}")

    # Test 3: Verify Sub-threshold Rules do not fire
    total += 1
    non_fired = [d["disease"] for d in res["non_fired_rules"]]
    if "Common Cold" in non_fired and "Typhoid" in non_fired:
        print("[PASS] Test 3: Common Cold (25%) and Typhoid (25%) correctly DID NOT FIRE.")
        passed += 1
    else:
        print(f"[FAIL] Test 3: Sub-threshold check failed.")

    # Test 4: Verify Dengue 100% Match & Emergency Alert Trigger
    total += 1
    dengue_facts = ["high fever", "headache", "joint pain", "rash"]
    dengue_res = engine.diagnose(dengue_facts)
    if (
        dengue_res["top_diseases"]
        and dengue_res["top_diseases"][0]["disease"] == "Dengue"
        and dengue_res["top_diseases"][0]["match_percentage"] == 100.0
        and dengue_res["is_emergency"] is True
    ):
        print("[PASS] Test 4: Dengue 100% match & Emergency Alert Flag verified.")
        passed += 1
    else:
        print(f"[FAIL] Test 4: Dengue emergency test failed.")

    # Test 5: Verify Dynamic Threshold Slider Logic
    total += 1
    # Under 80% threshold, Flu (75%) should NOT fire
    strict_res = engine.diagnose(slide_facts, min_symptoms=2, min_percentage=80.0)
    if len(strict_res["fired_rules"]) == 0:
        print("[PASS] Test 5: Dynamic Threshold Slider verified (80% threshold blocked 75% match).")
        passed += 1
    else:
        print(f"[FAIL] Test 5: Dynamic threshold test failed.")

    # Test 6: Verify HTML Hospital Report Generator
    total += 1
    test_patient = {"name": "Test Patient", "age": "25", "gender": "Male", "city": "Delhi"}
    html_file = generate_html_report(test_patient, res, "test_report_temp.html")
    if os.path.exists(html_file) and os.path.getsize(html_file) > 1000:
        print("[PASS] Test 6: HTML Hospital Report generated successfully.")
        passed += 1
        try:
            os.remove(html_file)
        except OSError:
            pass
    else:
        print("[FAIL] Test 6: HTML Report generation failed.")

    print("=" * 68)
    print(f"TEST SUMMARY: {passed}/{total} tests passed successfully!")
    print("=" * 68)


if __name__ == "__main__":
    run_tests()
