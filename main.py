"""
=============================================================================
Project Title : Sanjeevani: AI Medical Diagnosis Expert System
Course        : Artificial Intelligence / Knowledge Representation & Reasoning
Unit          : Unit III - Knowledge Representation and Reasoning
Technique     : Rule-Based Expert System using Forward Chaining
Team / Author : Aarav Sharma, Priya Patel, Rohan Verma (B.Tech CSE)
=============================================================================
Description:
    This is the master entry point for the Medical Diagnosis Expert System.
    It supports Desktop GUI, Web Application, and Terminal CLI modes.

Usage:
    - Desktop GUI (Default):
        python main.py

    - Web Application / Browser:
        python main.py --web
        (or: python web_server.py)

    - Interactive Terminal CLI:
        python main.py --cli
        (or: python cli_diagnosis.py)
=============================================================================
"""

import sys


def main():
    if "--web" in sys.argv or "-w" in sys.argv:
        from web_server import start_server
        start_server()
    elif "--cli" in sys.argv or "-c" in sys.argv:
        from cli_diagnosis import interactive_cli
        interactive_cli()
    else:
        from gui import launch_gui
        launch_gui()


if __name__ == "__main__":
    main()
