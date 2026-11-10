"""
=============================================================================
Project Title: Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : html_report.py
Description  : Generates modern, printable hospital-style diagnostic reports
               in HTML format with responsive CSS and clean layout.
=============================================================================
"""

import os
import webbrowser
from datetime import datetime
from knowledge_base import MEDICAL_DISCLAIMER, STUDENT_DETAILS


def generate_html_report(patient_info, diagnosis_result, output_path=None):
    """
    Generates a beautifully styled, printable HTML clinical diagnosis report.
    
    Args:
        patient_info (dict): {'name': ..., 'age': ..., 'gender': ..., 'city': ...}
        diagnosis_result (dict): Output from InferenceEngine.diagnose()
        output_path (str, optional): Target file path. Defaults to a timestamped file.
        
    Returns:
        str: Absolute path of generated HTML file.
    """
    timestamp = datetime.now().strftime("%d-%b-%Y %I:%M %p")
    report_id = f"MED-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    patient_name = patient_info.get("name", "Rahul Verma")
    patient_age = patient_info.get("age", "24")
    patient_gender = patient_info.get("gender", "Male")
    patient_city = patient_info.get("city", "Delhi / NCR")

    top_diseases = diagnosis_result.get("top_diseases", [])
    primary = top_diseases[0] if top_diseases else None

    # Severity color mapping
    severity_colors = {
        "Mild": ("#27ae60", "#e8f8f5"),
        "Mild to Moderate": ("#2980b9", "#ebf5fb"),
        "Moderate": ("#d35400", "#fef5e7"),
        "Moderate to Severe": ("#c0392b", "#fdedec"),
        "Severe": ("#c0392b", "#fadbd8")
    }

    primary_color, primary_bg = severity_colors.get(
        primary["severity"] if primary else "Mild",
        ("#2c3e50", "#f4f6f7")
    )

    emergency_banner = ""
    if diagnosis_result.get("is_emergency", False):
        emergency_banner = f"""
        <div style="background: #fadbd8; border-left: 6px solid #c0392b; padding: 14px 18px; margin: 15px 0; border-radius: 4px;">
            <strong style="color: #900c3f; font-size: 15px;">⚠️ URGENT CLINICAL ALERT:</strong>
            <p style="margin: 4px 0 0 0; color: #78281f; font-size: 13px;">
                {' | '.join(diagnosis_result.get('emergency_reasons', []))}.
                Immediate medical consultation at an emergency center is advised.
            </p>
        </div>
        """

    # Build candidates table HTML
    candidates_rows = ""
    if top_diseases:
        for idx, d in enumerate(top_diseases, 1):
            s_color, s_bg = severity_colors.get(d["severity"], ("#333", "#eee"))
            matched_str = f"<b>{d['matched_count']}/{d['total_symptoms']}</b> ({', '.join(d['matched_symptoms'])})"
            candidates_rows += f"""
            <tr>
                <td style="text-align: center; font-weight: bold;">#{idx}</td>
                <td><b style="color: #174374;">{d['disease']}</b></td>
                <td style="text-align: center;">
                    <span style="background: {s_bg}; color: {s_color}; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">
                        {d['severity']}
                    </span>
                </td>
                <td style="text-align: center; font-weight: bold; color: #0e8388;">{d['match_percentage']}%</td>
                <td>{d['doctor_specialist']}</td>
                <td>{matched_str}</td>
            </tr>
            """
    else:
        candidates_rows = """
        <tr>
            <td colspan="6" style="text-align: center; color: #888; padding: 20px;">
                No rule fired with the given symptoms under current threshold settings.
            </td>
        </tr>
        """

    # Primary conclusion block
    if primary:
        primary_block = f"""
        <div class="result-box" style="border: 2px solid {primary_color}; background: #ffffff;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <span style="font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #7f8c8d;">Primary Predicted Diagnosis</span>
                    <h2 style="margin: 4px 0 6px 0; color: #174374; font-size: 24px;">{primary['disease']}</h2>
                    <p style="margin: 0; color: #555; font-size: 14px;">{primary['description']}</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 28px; font-weight: 800; color: {primary_color};">{primary['match_percentage']}%</div>
                    <span style="background: {primary_bg}; color: {primary_color}; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold;">
                        {primary['severity']} Condition
                    </span>
                </div>
            </div>

            <hr style="border: 0; border-top: 1px solid #ecf0f1; margin: 15px 0;">

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; margin-bottom: 15px;">
                <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border-left: 3px solid #0e8388;">
                    <small style="color: #7f8c8d; font-weight: bold;">RECOMMENDED SPECIALIST</small>
                    <div style="font-size: 14px; font-weight: bold; color: #2c3e50; margin-top: 4px;">👨‍⚕️ {primary['doctor_specialist']}</div>
                </div>
                <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border-left: 3px solid #3498db;">
                    <small style="color: #7f8c8d; font-weight: bold;">MATCHED FACTS</small>
                    <div style="font-size: 13px; color: #27ae60; margin-top: 4px;">✓ {', '.join(primary['matched_symptoms'])}</div>
                </div>
                <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border-left: 3px solid #e67e22;">
                    <small style="color: #7f8c8d; font-weight: bold;">UNOBSERVED RULE FACTS</small>
                    <div style="font-size: 13px; color: #e67e22; margin-top: 4px;">
                        {', '.join(primary['missing_symptoms']) if primary['missing_symptoms'] else 'None (All Rule Facts Present)'}
                    </div>
                </div>
            </div>

            <div style="background: #eef7fc; border-radius: 6px; padding: 14px 16px;">
                <h4 style="margin: 0 0 8px 0; color: #174374;">📋 Clinical & First-Aid Home Care Guidance:</h4>
                <div style="white-space: pre-line; line-height: 1.6; color: #2c3e50; font-size: 13px;">{primary['advice']}</div>
            </div>
        </div>
        """
    else:
        primary_block = """
        <div class="result-box" style="border: 2px solid #bdc3c7; background: #fafafa; padding: 20px; text-align: center;">
            <h3 style="color: #7f8c8d; margin-top: 0;">No Disease Rule Fired</h3>
            <p style="color: #555;">The reported symptoms did not meet the minimum firing criteria (at least 2 matching facts & >= 50% match rate).</p>
            <p><strong>Recommendation:</strong> Consult a General Physician for clinical evaluation.</p>
        </div>
        """

    # Student team list HTML
    students_html = ", ".join([f"<b>{m['name']}</b> ({m['roll_no']})" for m in STUDENT_DETAILS["team_members"]])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Medical Diagnostic Report - {patient_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            background-color: #f4f7f6;
            color: #333333;
            margin: 0;
            padding: 25px;
        }}
        .report-card {{
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #dcdde1;
        }}
        .header {{
            background: linear-gradient(135deg, #174374 0%, #0e8388 100%);
            color: #ffffff;
            padding: 24px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 22px;
            letter-spacing: 0.5px;
        }}
        .header p {{
            margin: 4px 0 0 0;
            font-size: 12px;
            color: #d1ecf1;
        }}
        .content {{
            padding: 25px 30px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            background: #f8f9fa;
            padding: 14px 18px;
            border-radius: 6px;
            border: 1px solid #e9ecef;
            margin-bottom: 20px;
        }}
        .info-item small {{
            display: block;
            font-size: 11px;
            color: #6c757d;
            text-transform: uppercase;
            font-weight: 600;
        }}
        .info-item span {{
            font-size: 14px;
            color: #2c3e50;
            font-weight: 600;
        }}
        .symptoms-bar {{
            background: #eef2f5;
            padding: 12px 16px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        .tag {{
            display: inline-block;
            background: #ffffff;
            color: #174374;
            border: 1px solid #b3cde0;
            border-radius: 12px;
            padding: 3px 10px;
            font-size: 12px;
            margin: 2px 4px;
            font-weight: 500;
        }}
        .result-box {{
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            margin: 15px 0;
        }}
        th {{
            background: #f1f3f5;
            color: #495057;
            padding: 10px;
            text-align: left;
            border-bottom: 2px solid #dee2e6;
            font-size: 12px;
            text-transform: uppercase;
        }}
        td {{
            padding: 10px;
            border-bottom: 1px solid #e9ecef;
        }}
        .footer {{
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
            padding: 16px 30px;
            font-size: 11px;
            color: #6c757d;
            line-height: 1.5;
        }}
        .print-btn {{
            background: #0e8388;
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
        }}
        @media print {{
            body {{ padding: 0; background: #fff; }}
            .report-card {{ box-shadow: none; border: none; max-width: 100%; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>

<div class="report-card">
    <div class="header">
        <div>
            <h1>🏥 SANJEEVANI HEALTHCARE NETWORK</h1>
            <p>Knowledge-Based Clinical Decision Support System | AI Unit III Project</p>
        </div>
        <div style="text-align: right;">
            <button class="print-btn no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
            <div style="font-size: 11px; margin-top: 6px; color: #e0f2f1;">Report ID: {report_id}</div>
        </div>
    </div>

    <div class="content">
        <!-- Patient Metadata -->
        <div class="info-grid">
            <div class="info-item">
                <small>Patient Name</small>
                <span>{patient_name}</span>
            </div>
            <div class="info-item">
                <small>Age / Gender</small>
                <span>{patient_age} Yrs / {patient_gender}</span>
            </div>
            <div class="info-item">
                <small>Location / City</small>
                <span>{patient_city}</span>
            </div>
            <div class="info-item">
                <small>Date & Time</small>
                <span>{timestamp}</span>
            </div>
        </div>

        {emergency_banner}

        <!-- Reported Facts / Symptoms -->
        <div class="symptoms-bar">
            <strong style="color: #174374; font-size: 13px;">Observed Clinical Facts (Reported Symptoms):</strong><br>
            <div style="margin-top: 6px;">
                {' '.join([f'<span class="tag">✓ {s.title()}</span>' for s in diagnosis_result.get('patient_facts', [])])}
            </div>
        </div>

        <!-- Primary Diagnosis Box -->
        {primary_block}

        <!-- Top 3 Candidates Differential Diagnosis -->
        <h3 style="color: #174374; margin: 20px 0 8px 0; font-size: 16px;">
            Differential Diagnosis Ranking (Top Fired Rules)
        </h3>
        <p style="margin: 0 0 10px 0; font-size: 12px; color: #6c757d;">
            Evaluated using Forward Chaining with threshold: Match Count &ge; {diagnosis_result.get('min_symptoms_used', 2)} facts and Match % &ge; {diagnosis_result.get('min_percentage_used', 50.0)}%.
        </p>

        <table>
            <thead>
                <tr>
                    <th style="width: 40px; text-align: center;">Rank</th>
                    <th>Disease</th>
                    <th style="width: 120px; text-align: center;">Severity</th>
                    <th style="width: 80px; text-align: center;">Match %</th>
                    <th style="width: 180px;">Specialist</th>
                    <th>Matched Facts</th>
                </tr>
            </thead>
            <tbody>
                {candidates_rows}
            </tbody>
        </table>
    </div>

    <!-- Academic & Medical Footer -->
    <div class="footer">
        <p style="margin: 0 0 6px 0;"><b>Academic Project Submission:</b> {STUDENT_DETAILS['course']} | {STUDENT_DETAILS['subject']}</p>
        <p style="margin: 0 0 8px 0;"><b>Student Project Team:</b> {students_html} | <b>Supervisor:</b> {STUDENT_DETAILS['guide_name']}</p>
        <p style="margin: 0; color: #888; font-style: italic;">{MEDICAL_DISCLAIMER}</p>
    </div>
</div>

</body>
</html>
"""

    if not output_path:
        filename = f"Diagnosis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        output_path = os.path.abspath(filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
