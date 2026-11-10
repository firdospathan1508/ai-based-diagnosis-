"""
=============================================================================
Project Title: Sanjeevani Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : web_server.py
Description  : Zero-dependency local web server built using Python's standard
               'http.server'. Serves the web interface and handles REST API
               requests for Forward Chaining diagnosis.
=============================================================================
"""

import os
import sys
import json
import socket
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from knowledge_base import (
    DISEASE_RULES,
    DISEASE_PRESETS,
    ALL_SYMPTOMS,
    STUDENT_DETAILS,
    SAMPLE_INDIAN_PATIENTS
)
from inference_engine import InferenceEngine

# Directory where web assets reside
WEB_DIR = os.path.dirname(os.path.abspath(__file__))


def get_local_ip():
    """Detects local machine's IP address on Wi-Fi/LAN for mobile testing."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


class MedicalDiagnosisApiHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/rules":
            self._send_json(200, DISEASE_RULES)
        elif parsed.path == "/api/presets":
            self._send_json(200, DISEASE_PRESETS)
        elif parsed.path == "/api/symptoms":
            self._send_json(200, ALL_SYMPTOMS)
        elif parsed.path == "/api/info":
            self._send_json(200, {
                "student_details": STUDENT_DETAILS,
                "sample_patients": SAMPLE_INDIAN_PATIENTS
            })
        elif parsed.path in ["/", "/index.html"]:
            self.path = "/index.html"
            return super().do_GET()
        else:
            return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/diagnose":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_body = self.rfile.read(content_length)
                data = json.loads(post_body.decode("utf-8"))

                facts = data.get("symptoms", [])
                min_symptoms = int(data.get("min_symptoms", 2))
                min_percentage = float(data.get("min_percentage", 50.0))

                engine = InferenceEngine()
                result = engine.diagnose(
                    facts,
                    min_symptoms=min_symptoms,
                    min_percentage=min_percentage
                )
                self._send_json(200, result)
            except Exception as e:
                self._send_json(400, {"error": str(e)})
        else:
            self._send_json(404, {"error": "API route not found"})

    def _send_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        # Clean terminal logging for students
        pass


def start_server(port=8000, auto_open=True):
    host = "0.0.0.0"
    local_ip = get_local_ip()

    # Find free port if 8000 is occupied
    while True:
        try:
            server = HTTPServer((host, port), MedicalDiagnosisApiHandler)
            break
        except OSError:
            port += 1

    print("=" * 72)
    print("      🏥 SANJEEVANI: AI MEDICAL EXPERT SYSTEM (WEB SERVER)")
    print("      Course Topic: Knowledge Representation & Reasoning (Unit III)")
    print(f"      Team: {', '.join([m['name'] for m in STUDENT_DETAILS['team_members']])}")
    print("=" * 72)
    print(f"\n[+] Local Access URL     : http://localhost:{port}")
    print(f"[+] Mobile/LAN Access URL : http://{local_ip}:{port}")
    print("\nAnyone connected to your Wi-Fi or Hotspot can open the Mobile URL!")
    print("Press CTRL + C to stop the web server.\n" + "-" * 72)

    if auto_open:
        webbrowser.open(f"http://localhost:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Web Server stopped successfully.")
        server.server_close()


if __name__ == "__main__":
    start_server()
