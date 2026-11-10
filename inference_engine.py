"""
=============================================================================
Project Title: Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : inference_engine.py
Description  : Implements Forward Chaining with dynamic threshold controls,
               doctor specialization triage, and emergency alert detection.
=============================================================================
"""

from knowledge_base import DISEASE_RULES


class InferenceEngine:
    """
    Forward Chaining Inference Engine for Rule-Based Medical Diagnosis.
    
    Forward Chaining Reasoning Steps:
    1. Input Facts: Observed patient symptoms.
    2. Check production rules in Knowledge Base sequentially.
    3. Compute Match Rate = (Matched Symptoms / Total Rule Symptoms) * 100.
    4. Fire Rule if:
       - Matched Count >= min_symptoms_threshold (Default = 2)
       - AND Match % >= min_percentage_threshold (Default = 50.0%)
    5. Detect Emergency Conditions (e.g., Dengue/Malaria/Asthma with high confidence).
    6. Triage to Doctor Specialization (e.g., Pulmonologist, Neurologist).
    """

    def __init__(self, rules=None):
        self.rules = rules if rules is not None else DISEASE_RULES

    def diagnose(self, patient_facts, min_symptoms=2, min_percentage=50.0):
        """
        Executes Forward Chaining diagnosis with configurable thresholds.
        
        Args:
            patient_facts (list or set): Symptoms reported by the patient.
            min_symptoms (int): Minimum matching symptoms required to fire (default: 2).
            min_percentage (float): Minimum match percentage required to fire (default: 50.0).
            
        Returns:
            dict with fired rules, reasoning logs, emergency flags, and doctor recommendations.
        """
        facts_set = {s.strip().lower() for s in patient_facts}

        fired_rules = []
        non_fired_rules = []
        reasoning_steps = []

        is_emergency = False
        emergency_reasons = []

        step_counter = 1

        for disease, rule_data in self.rules.items():
            rule_symptoms = rule_data["symptoms"]
            total_rule_symptoms = len(rule_symptoms)

            # Match facts against rule premise
            matched = [s for s in rule_symptoms if s.lower() in facts_set]
            missing = [s for s in rule_symptoms if s.lower() not in facts_set]

            matched_count = len(matched)
            match_percentage = round((matched_count / total_rule_symptoms) * 100, 1)

            # Check rule firing conditions
            rule_fired = (
                matched_count >= min_symptoms
                and match_percentage >= min_percentage
            )

            rule_summary = {
                "disease": disease,
                "total_symptoms": total_rule_symptoms,
                "matched_count": matched_count,
                "match_percentage": match_percentage,
                "matched_symptoms": matched,
                "missing_symptoms": missing,
                "rule_fired": rule_fired,
                "severity": rule_data["severity"],
                "doctor_specialist": rule_data.get("doctor_specialist", "General Physician"),
                "is_emergency_type": rule_data.get("emergency", False),
                "description": rule_data["description"],
                "advice": rule_data["advice"]
            }

            # Detailed reasoning log for students to explain during viva
            step_log = (
                f"Step {step_counter}: Evaluating Rule for [{disease}]\n"
                f"  • Premise (IF): {', '.join(rule_symptoms)}\n"
                f"  • Matched Facts: {matched_count}/{total_rule_symptoms} "
                f"({', '.join(matched) if matched else 'None'})\n"
                f"  • Calculated Match Rate: {match_percentage}%\n"
            )

            if rule_fired:
                step_log += (
                    f"  => STATUS: [FIRED] (Satisfies >= {min_symptoms} facts "
                    f"& >= {min_percentage}% match criteria)\n"
                )
                fired_rules.append(rule_summary)

                # Check if this high-confidence fired rule warrants an emergency alert
                if rule_data.get("emergency", False) and match_percentage >= 75.0:
                    is_emergency = True
                    emergency_reasons.append(
                        f"High match ({match_percentage}%) for critical condition: {disease}"
                    )
            else:
                reasons = []
                if matched_count < min_symptoms:
                    reasons.append(f"matched {matched_count} < {min_symptoms} required facts")
                if match_percentage < min_percentage:
                    reasons.append(f"{match_percentage}% < {min_percentage}% threshold")
                reason_str = " and ".join(reasons)
                step_log += f"  => STATUS: [NOT FIRED] ({reason_str})\n"
                non_fired_rules.append(rule_summary)

            reasoning_steps.append(step_log)
            step_counter += 1

        # Sort fired rules by match percentage descending, then by matched_count
        fired_rules.sort(
            key=lambda r: (r["match_percentage"], r["matched_count"]),
            reverse=True
        )

        top_diseases = fired_rules[:3]

        return {
            "patient_facts": list(facts_set),
            "min_symptoms_used": min_symptoms,
            "min_percentage_used": min_percentage,
            "fired_rules": fired_rules,
            "non_fired_rules": non_fired_rules,
            "reasoning_steps": reasoning_steps,
            "top_diseases": top_diseases,
            "is_emergency": is_emergency,
            "emergency_reasons": emergency_reasons
        }
