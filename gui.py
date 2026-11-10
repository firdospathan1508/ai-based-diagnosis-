"""
=============================================================================
Project Title: Medical Diagnosis Expert System
Course Topic : Knowledge Representation and Reasoning (Unit III)
File Name    : gui.py
Description  : Enhanced Desktop Graphical User Interface (GUI) with:
               - Student credentials & Indian patient profiles
               - 1-click test presets for all 10 diseases (including Slide 7)
               - Dynamic Forward Chaining threshold controls (slider & spinbox)
               - Emergency critical alert banner
               - Doctor specialization triage
               - Hospital-style HTML report export with browser preview
=============================================================================
"""

import os
import random
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from knowledge_base import (
    DISEASE_RULES,
    SYMPTOM_CATEGORIES,
    ALL_SYMPTOMS,
    DISEASE_PRESETS,
    STUDENT_DETAILS,
    SAMPLE_INDIAN_PATIENTS,
    MEDICAL_DISCLAIMER
)
from inference_engine import InferenceEngine
from html_report import generate_html_report


class MedicalDiagnosisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Diagnosis Expert System | AI & Knowledge Reasoning (Unit III)")
        self.root.geometry("1160x820")
        self.root.minsize(1020, 720)

        # Initialize Inference Engine
        self.engine = InferenceEngine()

        # Dictionary to store BooleanVar for each symptom checkbox
        self.symptom_vars = {symptom: tk.BooleanVar(value=False) for symptom in ALL_SYMPTOMS}

        # Cache of last diagnosis
        self.last_result = None

        # Setup modern styles
        self._configure_styles()

        # Build Main Layout
        self._build_header()
        self._build_viva_toolbar()
        self._build_body()
        self._build_footer()

    def _configure_styles(self):
        """Configure ttk styles for a clean, student-crafted medical aesthetic."""
        style = ttk.Style()
        style.theme_use("clam")

        # Color palette
        self.c_primary = "#174374"      # Medical Navy Blue
        self.c_secondary = "#0e8388"    # Teal Accent
        self.c_bg_light = "#f4f7f9"     # Crisp background
        self.c_card_bg = "#ffffff"      # Card background
        self.c_text = "#2c3e50"         # Dark slate text
        self.c_border = "#d0dbe5"       # Light border

        self.root.configure(bg=self.c_bg_light)

        style.configure("TFrame", background=self.c_bg_light)
        style.configure("Card.TFrame", background=self.c_card_bg, relief="solid", borderwidth=1)
        style.configure("Header.TLabel", background=self.c_primary, foreground="#ffffff", font=("Segoe UI", 15, "bold"))
        style.configure("SubHeader.TLabel", background=self.c_primary, foreground="#cce3f5", font=("Segoe UI", 8))
        
        style.configure("TCheckbutton", background=self.c_card_bg, font=("Segoe UI", 9), foreground=self.c_text)
        style.map("TCheckbutton", background=[("active", self.c_card_bg)])

        style.configure("TNotebook", background=self.c_bg_light)
        style.configure("TNotebook.Tab", font=("Segoe UI", 9, "bold"), padding=[12, 5])

        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), foreground=self.c_primary)
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)

    def _build_header(self):
        """Top banner with project title, course details, and student names."""
        header_frame = tk.Frame(self.root, bg=self.c_primary, height=82)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        top_row = tk.Frame(header_frame, bg=self.c_primary)
        top_row.pack(fill=tk.X, padx=18, pady=(8, 2))

        title_lbl = tk.Label(
            top_row,
            text="🏥 Medical Diagnosis Expert System",
            bg=self.c_primary,
            fg="#ffffff",
            font=("Segoe UI", 15, "bold")
        )
        title_lbl.pack(side=tk.LEFT)

        team_str = "Team: " + " | ".join([f"{m['name']} ({m['roll_no']})" for m in STUDENT_DETAILS["team_members"][:2]])
        team_lbl = tk.Label(
            top_row,
            text=team_str,
            bg=self.c_primary,
            fg="#e0f2fe",
            font=("Segoe UI", 9, "bold")
        )
        team_lbl.pack(side=tk.RIGHT)

        sub_row = tk.Frame(header_frame, bg=self.c_primary)
        sub_row.pack(fill=tk.X, padx=18, pady=(0, 8))

        sub_lbl = tk.Label(
            sub_row,
            text="Unit III: Knowledge Representation & Reasoning  |  Forward Chaining Rule-Based Architecture",
            bg=self.c_primary,
            fg="#c2d9ee",
            font=("Segoe UI", 8)
        )
        sub_lbl.pack(side=tk.LEFT)

        course_lbl = tk.Label(
            sub_row,
            text=f"{STUDENT_DETAILS['course']} | Supervisor: {STUDENT_DETAILS['guide_name']}",
            bg=self.c_primary,
            fg="#a5c8e4",
            font=("Segoe UI", 8)
        )
        course_lbl.pack(side=tk.RIGHT)

    def _build_viva_toolbar(self):
        """Toolbar with dynamic threshold sliders and 1-click preset selector for viva demos."""
        toolbar = tk.Frame(self.root, bg="#e2ecf5", bd=1, relief="solid")
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=12, pady=(6, 0), ipady=4)

        # Preset Dropdown Section
        tk.Label(
            toolbar,
            text="⚡ Viva Test Preset:",
            bg="#e2ecf5",
            fg=self.c_primary,
            font=("Segoe UI", 9, "bold")
        ).pack(side=tk.LEFT, padx=(10, 4))

        self.preset_combo = ttk.Combobox(
            toolbar,
            values=list(DISEASE_PRESETS.keys()),
            width=30,
            state="readonly"
        )
        self.preset_combo.current(0)
        self.preset_combo.pack(side=tk.LEFT, padx=4)

        load_preset_btn = tk.Button(
            toolbar,
            text="Load Preset",
            bg=self.c_primary,
            fg="#ffffff",
            font=("Segoe UI", 8, "bold"),
            relief="groove",
            command=self._apply_selected_preset
        )
        load_preset_btn.pack(side=tk.LEFT, padx=4)

        # Separator
        ttk.Separator(toolbar, orient="vertical").pack(side=tk.LEFT, fill=tk.Y, padx=12, pady=2)

        # Threshold controls (Live demonstration for examiner)
        tk.Label(
            toolbar,
            text="⚙️ Min Match %:",
            bg="#e2ecf5",
            font=("Segoe UI", 8, "bold"),
            fg=self.c_text
        ).pack(side=tk.LEFT, padx=(4, 2))

        self.threshold_slider = tk.Scale(
            toolbar,
            from_=25,
            to=80,
            orient=tk.HORIZONTAL,
            resolution=5,
            bg="#e2ecf5",
            highlightthickness=0,
            length=110,
            font=("Segoe UI", 8)
        )
        self.threshold_slider.set(50)  # PPT default: 50%
        self.threshold_slider.pack(side=tk.LEFT, padx=2)

        tk.Label(
            toolbar,
            text="Min Symptoms:",
            bg="#e2ecf5",
            font=("Segoe UI", 8, "bold"),
            fg=self.c_text
        ).pack(side=tk.LEFT, padx=(8, 2))

        self.min_symptoms_spin = ttk.Spinbox(toolbar, from_=1, to=4, width=3)
        self.min_symptoms_spin.set(2)  # PPT default: 2 symptoms
        self.min_symptoms_spin.pack(side=tk.LEFT, padx=2)

        reset_btn = tk.Button(
            toolbar,
            text="Default Thresholds",
            font=("Segoe UI", 8),
            bg="#ffffff",
            relief="groove",
            command=self._reset_thresholds
        )
        reset_btn.pack(side=tk.LEFT, padx=8)

        # Launch Web Version Button
        web_btn = tk.Button(
            toolbar,
            text="🌐 Open Web Version",
            font=("Segoe UI", 8, "bold"),
            bg="#0e8388",
            fg="#ffffff",
            relief="groove",
            cursor="hand2",
            command=self._launch_web_in_browser
        )
        web_btn.pack(side=tk.RIGHT, padx=8)

    def _build_footer(self):
        """Bottom status bar with medical disclaimer."""
        footer_frame = tk.Frame(self.root, bg="#e9ecef", height=28)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

        disclaimer_lbl = tk.Label(
            footer_frame,
            text="⚠️ Student Prototype: For educational & viva demonstration only. Does not replace professional medical judgment.",
            bg="#e9ecef",
            fg="#5a6268",
            font=("Segoe UI", 8, "italic")
        )
        disclaimer_lbl.pack(side=tk.LEFT, padx=15, pady=4)

        credits_lbl = tk.Label(
            footer_frame,
            text="KRR Unit III Mini-Project | Python 3 Expert System",
            bg="#e9ecef",
            fg="#6c757d",
            font=("Segoe UI", 8)
        )
        credits_lbl.pack(side=tk.RIGHT, padx=15, pady=4)

    def _build_body(self):
        """Main body with left input column and right results column."""
        main_container = tk.Frame(self.root, bg=self.c_bg_light)
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=12, pady=8)

        # ----------------- LEFT PANEL: PATIENT & SYMPTOMS -----------------
        left_panel = tk.Frame(main_container, bg=self.c_bg_light, width=480)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 8))
        left_panel.pack_propagate(False)

        # Card 1: Patient Information (Indian Demographics)
        patient_card = tk.LabelFrame(
            left_panel,
            text=" 1. Patient Profile (Indian Context) ",
            bg=self.c_card_bg,
            fg=self.c_primary,
            font=("Segoe UI", 9, "bold"),
            relief="solid",
            bd=1
        )
        patient_card.pack(side=tk.TOP, fill=tk.X, pady=(0, 6))

        p_row1 = tk.Frame(patient_card, bg=self.c_card_bg)
        p_row1.pack(fill=tk.X, padx=10, pady=(4, 2))

        tk.Label(p_row1, text="Name:", bg=self.c_card_bg, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.patient_name_entry = tk.Entry(p_row1, font=("Segoe UI", 9), width=16)
        self.patient_name_entry.pack(side=tk.LEFT, padx=(4, 10))
        self.patient_name_entry.insert(0, "Rahul Verma")

        tk.Label(p_row1, text="Age:", bg=self.c_card_bg, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.patient_age_entry = tk.Entry(p_row1, font=("Segoe UI", 9), width=4)
        self.patient_age_entry.pack(side=tk.LEFT, padx=(4, 10))
        self.patient_age_entry.insert(0, "24")

        tk.Label(p_row1, text="Gender:", bg=self.c_card_bg, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.gender_combo = ttk.Combobox(p_row1, values=["Male", "Female", "Other"], width=7, state="readonly")
        self.gender_combo.current(0)
        self.gender_combo.pack(side=tk.LEFT, padx=4)

        p_row2 = tk.Frame(patient_card, bg=self.c_card_bg)
        p_row2.pack(fill=tk.X, padx=10, pady=(2, 6))

        tk.Label(p_row2, text="City:", bg=self.c_card_bg, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.patient_city_entry = tk.Entry(p_row2, font=("Segoe UI", 9), width=16)
        self.patient_city_entry.pack(side=tk.LEFT, padx=(14, 10))
        self.patient_city_entry.insert(0, "Delhi")

        random_p_btn = tk.Button(
            p_row2,
            text="🎲 Random Patient",
            font=("Segoe UI", 8),
            bg="#f1f5f9",
            fg=self.c_primary,
            relief="groove",
            command=self._load_random_indian_patient
        )
        random_p_btn.pack(side=tk.RIGHT)

        # Card 2: Symptom Selection
        symptom_card = tk.LabelFrame(
            left_panel,
            text=" 2. Select Patient Symptoms (Knowledge Facts) ",
            bg=self.c_card_bg,
            fg=self.c_primary,
            font=("Segoe UI", 9, "bold"),
            relief="solid",
            bd=1
        )
        symptom_card.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Search Bar
        search_frame = tk.Frame(symptom_card, bg=self.c_card_bg)
        search_frame.pack(fill=tk.X, padx=10, pady=(6, 4))

        tk.Label(search_frame, text="🔍 Search:", bg=self.c_card_bg, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_filter_changed)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Segoe UI", 9))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)

        # Categorized Tab Notebook for Symptoms
        self.notebook = ttk.Notebook(symptom_card)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        self.tab_frames = {}
        for category, cat_symptoms in SYMPTOM_CATEGORIES.items():
            tab_frame = self._create_symptom_tab(self.notebook, cat_symptoms)
            self.notebook.add(tab_frame, text=category)
            self.tab_frames[category] = tab_frame

        # Action Buttons under symptoms
        btn_bar = tk.Frame(symptom_card, bg=self.c_card_bg)
        btn_bar.pack(fill=tk.X, padx=10, pady=6)

        slide7_btn = tk.Button(
            btn_bar,
            text="⚡ Slide 7 (Flu)",
            font=("Segoe UI", 8, "bold"),
            bg="#eaf2f8",
            fg=self.c_primary,
            relief="groove",
            command=lambda: self._apply_preset_by_name("Slide 7 Example (Flu - 75%)")
        )
        slide7_btn.pack(side=tk.LEFT, padx=2)

        clear_btn = tk.Button(
            btn_bar,
            text="Clear All",
            font=("Segoe UI", 8),
            bg="#fff0f0",
            fg="#c0392b",
            relief="groove",
            command=self._clear_all_symptoms
        )
        clear_btn.pack(side=tk.RIGHT, padx=2)

        # Big Diagnose Button
        diagnose_btn = tk.Button(
            left_panel,
            text="🔬 RUN FORWARD CHAINING DIAGNOSIS",
            bg=self.c_secondary,
            fg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            relief="raised",
            bd=2,
            pady=7,
            cursor="hand2",
            command=self._run_diagnosis
        )
        diagnose_btn.pack(fill=tk.X, pady=(6, 0))

        # ----------------- RIGHT PANEL: RESULTS & REASONING -----------------
        right_panel = tk.Frame(main_container, bg=self.c_bg_light)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.result_notebook = ttk.Notebook(right_panel)
        self.result_notebook.pack(fill=tk.BOTH, expand=True)

        self.diagnosis_tab = tk.Frame(self.result_notebook, bg=self.c_card_bg)
        self.reasoning_tab = tk.Frame(self.result_notebook, bg=self.c_card_bg)

        self.result_notebook.add(self.diagnosis_tab, text="📋 Clinical Diagnosis & Advice")
        self.result_notebook.add(self.reasoning_tab, text="🧠 Forward Chaining Reasoning Trace")

        self._build_diagnosis_tab()
        self._build_reasoning_tab()

    def _create_symptom_tab(self, notebook, symptoms):
        """Creates a scrollable tab for a category of symptoms."""
        tab_container = tk.Frame(notebook, bg=self.c_card_bg)

        canvas = tk.Canvas(tab_container, bg=self.c_card_bg, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.c_card_bg)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for idx, symptom in enumerate(symptoms):
            cb = ttk.Checkbutton(
                scrollable_frame,
                text=symptom.title(),
                variable=self.symptom_vars[symptom]
            )
            r = idx // 2
            c = idx % 2
            cb.grid(row=r, column=c, sticky="w", padx=10, pady=4)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return tab_container

    def _build_diagnosis_tab(self):
        """Build the primary diagnosis card, emergency alert, and advice view."""
        self.diag_container = tk.Frame(self.diagnosis_tab, bg=self.c_card_bg)
        self.diag_container.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

        # Welcome message initially
        self.welcome_label = tk.Label(
            self.diag_container,
            text=(
                "👋 Welcome to the Medical Diagnosis Expert System Prototype\n\n"
                "Designed for Unit III: Knowledge Representation and Reasoning\n\n"
                "Quick Start for Presentation:\n"
                "1. Select a preset from 'Viva Test Preset' at top (e.g., Slide 7 Flu, Dengue, Malaria).\n"
                "2. Or manually check symptoms from the categories on the left.\n"
                "3. Click 'RUN FORWARD CHAINING DIAGNOSIS'.\n"
                "4. View the fired rules, specialist triage, and export official reports!"
            ),
            bg=self.c_card_bg,
            fg="#5a6268",
            font=("Segoe UI", 10),
            justify="center"
        )
        self.welcome_label.pack(expand=True)

        self.result_display_frame = tk.Frame(self.diag_container, bg=self.c_card_bg)

        # Emergency Critical Banner (Initially Hidden)
        self.emergency_banner = tk.Frame(self.result_display_frame, bg="#fadbd8", bd=1, relief="solid")
        self.emergency_lbl = tk.Label(
            self.emergency_banner,
            text="",
            bg="#fadbd8",
            fg="#78281f",
            font=("Segoe UI", 9, "bold"),
            wraplength=550,
            justify="left"
        )
        self.emergency_lbl.pack(fill=tk.X, padx=10, pady=6)

        # Disease Header Card
        self.disease_badge_frame = tk.Frame(self.result_display_frame, bg="#eef5fc", bd=1, relief="solid")
        self.disease_badge_frame.pack(fill=tk.X, pady=(0, 8), ipady=6, ipadx=10)

        self.res_disease_lbl = tk.Label(
            self.disease_badge_frame,
            text="",
            bg="#eef5fc",
            fg=self.c_primary,
            font=("Segoe UI", 15, "bold")
        )
        self.res_disease_lbl.pack(anchor="w")

        self.res_meta_lbl = tk.Label(
            self.disease_badge_frame,
            text="",
            bg="#eef5fc",
            fg="#495057",
            font=("Segoe UI", 9)
        )
        self.res_meta_lbl.pack(anchor="w", pady=(2, 0))

        # Specialist & Progress Bar Row
        spec_row = tk.Frame(self.result_display_frame, bg=self.c_card_bg)
        spec_row.pack(fill=tk.X, pady=(0, 8))

        self.specialist_badge = tk.Label(
            spec_row,
            text="👨‍⚕️ Specialist: -",
            bg="#e8f8f5",
            fg="#0e8388",
            font=("Segoe UI", 9, "bold"),
            relief="solid",
            bd=1,
            padx=8,
            pady=3
        )
        self.specialist_badge.pack(side=tk.LEFT)

        self.bar_label = tk.Label(
            spec_row,
            text="Confidence: 0%",
            bg=self.c_card_bg,
            font=("Segoe UI", 9, "bold"),
            fg=self.c_primary
        )
        self.bar_label.pack(side=tk.RIGHT)

        self.progress_bar = ttk.Progressbar(self.result_display_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=(0, 8))

        # Differential Diagnosis Candidates (Top 3)
        cand_frame = tk.LabelFrame(
            self.result_display_frame,
            text=" Ranked Differential Diagnoses (Top Fired Rules) ",
            bg=self.c_card_bg,
            fg=self.c_primary,
            font=("Segoe UI", 9, "bold")
        )
        cand_frame.pack(fill=tk.X, pady=(0, 8))

        self.tree_candidates = ttk.Treeview(
            cand_frame,
            columns=("rank", "disease", "severity", "match", "specialist"),
            show="headings",
            height=3
        )
        self.tree_candidates.heading("rank", text="Rank")
        self.tree_candidates.heading("disease", text="Predicted Disease")
        self.tree_candidates.heading("severity", text="Severity")
        self.tree_candidates.heading("match", text="Match %")
        self.tree_candidates.heading("specialist", text="Consult Specialist")

        self.tree_candidates.column("rank", width=45, anchor="center")
        self.tree_candidates.column("disease", width=150)
        self.tree_candidates.column("severity", width=110, anchor="center")
        self.tree_candidates.column("match", width=75, anchor="center")
        self.tree_candidates.column("specialist", width=190)
        self.tree_candidates.pack(fill=tk.X, padx=6, pady=4)

        # Advice & Recommendations
        advice_group = tk.LabelFrame(
            self.result_display_frame,
            text=" Clinical & First-Aid Home Care Guidance ",
            bg=self.c_card_bg,
            fg=self.c_primary,
            font=("Segoe UI", 9, "bold")
        )
        advice_group.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self.advice_text = tk.Text(
            advice_group,
            wrap="word",
            height=5,
            bg="#fdfefe",
            font=("Segoe UI", 9),
            relief="solid",
            bd=1
        )
        self.advice_text.pack(fill=tk.BOTH, expand=True, padx=6, pady=4)

        # Dual Report Export Buttons
        export_bar = tk.Frame(self.result_display_frame, bg=self.c_card_bg)
        export_bar.pack(fill=tk.X)

        self.html_export_btn = tk.Button(
            export_bar,
            text="🌐 Open Printable Hospital HTML Report",
            bg="#0e8388",
            fg="#ffffff",
            font=("Segoe UI", 9, "bold"),
            relief="raised",
            cursor="hand2",
            padx=10,
            command=self._export_html_report
        )
        self.html_export_btn.pack(side=tk.RIGHT, padx=(4, 0))

        self.txt_export_btn = tk.Button(
            export_bar,
            text="📄 Save Text Report (.txt)",
            bg="#eef2f5",
            fg=self.c_primary,
            font=("Segoe UI", 9),
            relief="groove",
            command=self._export_text_report
        )
        self.txt_export_btn.pack(side=tk.RIGHT)

    def _build_reasoning_tab(self):
        """Displays the step-by-step forward chaining execution trace."""
        container = tk.Frame(self.reasoning_tab, bg=self.c_card_bg)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        info_lbl = tk.Label(
            container,
            text="Forward Chaining Evaluation Trace (Knowledge Base Rules checked sequentially):",
            bg=self.c_card_bg,
            fg="#495057",
            font=("Segoe UI", 9)
        )
        info_lbl.pack(anchor="w", pady=(0, 6))

        scroll = ttk.Scrollbar(container, orient="vertical")
        self.reasoning_text = tk.Text(
            container,
            wrap="word",
            font=("Consolas", 9),
            bg="#212529",
            fg="#f8f9fa",
            relief="solid",
            bd=1,
            yscrollcommand=scroll.set
        )
        scroll.config(command=self.reasoning_text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.reasoning_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.reasoning_text.tag_config("fired", foreground="#4cd137", font=("Consolas", 9, "bold"))
        self.reasoning_text.tag_config("not_fired", foreground="#e84118")
        self.reasoning_text.tag_config("step_header", foreground="#00d2d3", font=("Consolas", 9, "bold"))

    def _load_random_indian_patient(self):
        """Randomly cycles through Indian patient demographics."""
        p = random.choice(SAMPLE_INDIAN_PATIENTS)
        self.patient_name_entry.delete(0, tk.END)
        self.patient_name_entry.insert(0, p["name"])
        self.patient_age_entry.delete(0, tk.END)
        self.patient_age_entry.insert(0, str(p["age"]))
        self.gender_combo.set(p["gender"])
        self.patient_city_entry.delete(0, tk.END)
        self.patient_city_entry.insert(0, p["city"])

    def _reset_thresholds(self):
        """Resets to PPT default thresholds (50% and 2 symptoms)."""
        self.threshold_slider.set(50)
        self.min_symptoms_spin.set(2)

    def _apply_selected_preset(self):
        """Loads the selected preset from dropdown and runs diagnosis."""
        preset_name = self.preset_combo.get()
        self._apply_preset_by_name(preset_name)

    def _apply_preset_by_name(self, preset_name):
        """Loads symptoms corresponding to a named preset."""
        symptoms = DISEASE_PRESETS.get(preset_name, [])
        if not symptoms:
            return
        self._clear_all_symptoms()
        for s in symptoms:
            if s in self.symptom_vars:
                self.symptom_vars[s].set(True)
        self._run_diagnosis()

    def _clear_all_symptoms(self):
        """Unchecks all symptoms."""
        for var in self.symptom_vars.values():
            var.set(False)
        self.search_var.set("")

    def _get_selected_symptoms(self):
        """Returns list of checked symptoms."""
        return [symptom for symptom, var in self.symptom_vars.items() if var.get()]

    def _on_filter_changed(self, *args):
        """Live search filter for symptoms."""
        query = self.search_var.get().strip().lower()
        if not query:
            return
        for cat_name, symptoms in SYMPTOM_CATEGORIES.items():
            for s in symptoms:
                if query in s:
                    tab_frame = self.tab_frames[cat_name]
                    self.notebook.select(tab_frame)
                    return

    def _run_diagnosis(self):
        """Executes forward chaining with dynamic thresholds."""
        selected_symptoms = self._get_selected_symptoms()
        if not selected_symptoms:
            messagebox.showwarning(
                "No Symptoms Selected",
                "Please select at least one symptom or choose a Viva Test Preset."
            )
            return

        min_pct = float(self.threshold_slider.get())
        try:
            min_symp = int(self.min_symptoms_spin.get())
        except ValueError:
            min_symp = 2

        result = self.engine.diagnose(
            selected_symptoms,
            min_symptoms=min_symp,
            min_percentage=min_pct
        )
        self.last_result = result

        # Switch view
        self.welcome_label.pack_forget()
        self.result_display_frame.pack(fill=tk.BOTH, expand=True)

        # 1. Update Reasoning Log
        self.reasoning_text.delete("1.0", tk.END)
        self.reasoning_text.insert(
            tk.END,
            "======================================================================\n"
            "             FORWARD CHAINING INFERENCE EXECUTION TRACE\n"
            "======================================================================\n"
            f"Observed Patient Facts : {', '.join(selected_symptoms)}\n"
            f"Active Firing Criteria : Min Symptoms >= {min_symp} | Match % >= {min_pct}%\n"
            "----------------------------------------------------------------------\n\n"
        )

        for step in result["reasoning_steps"]:
            for line in step.split("\n"):
                if "Step" in line and "Evaluating Rule" in line:
                    self.reasoning_text.insert(tk.END, line + "\n", "step_header")
                elif "STATUS: [FIRED]" in line:
                    self.reasoning_text.insert(tk.END, line + "\n", "fired")
                elif "STATUS: [NOT FIRED]" in line:
                    self.reasoning_text.insert(tk.END, line + "\n", "not_fired")
                else:
                    self.reasoning_text.insert(tk.END, line + "\n")

        # 2. Update Emergency Alert Banner
        if result["is_emergency"]:
            self.emergency_lbl.config(
                text="⚠️ URGENT CLINICAL ALERT: " + " | ".join(result["emergency_reasons"]) +
                     ". Immediate hospital consultation advised."
            )
            self.emergency_banner.pack(fill=tk.X, pady=(0, 8), before=self.disease_badge_frame)
        else:
            self.emergency_banner.pack_forget()

        # 3. Update Diagnosis Tab
        top_diseases = result["top_diseases"]

        for item in self.tree_candidates.get_children():
            self.tree_candidates.delete(item)

        if not top_diseases:
            self.res_disease_lbl.config(
                text="❌ No Disease Rule Fired",
                fg="#c0392b"
            )
            self.res_meta_lbl.config(
                text=f"No disease satisfied the current criteria (>= {min_symp} facts & >= {min_pct}% match)."
            )
            self.specialist_badge.config(text="👨‍⚕️ Specialist: General Physician")
            self.progress_bar["value"] = 0
            self.bar_label.config(text="Confidence: 0%")

            self.advice_text.delete("1.0", tk.END)
            self.advice_text.insert(
                tk.END,
                "• The selected symptoms did not reach the threshold for any of the 10 diseases.\n"
                "• In viva demonstrations: Try lowering the 'Min Match %' slider or 'Min Symptoms' counter above!\n"
                "• Clinical Guidance: Consult a General Physician for comprehensive medical examination."
            )
            return

        primary = top_diseases[0]
        self.res_disease_lbl.config(
            text=f"🎯 Primary Match: {primary['disease']}",
            fg=self.c_primary
        )
        self.res_meta_lbl.config(
            text=f"Severity: {primary['severity']}  |  Matched: {primary['matched_count']} of {primary['total_symptoms']} symptoms  |  {primary['description']}"
        )

        self.specialist_badge.config(
            text=f"👨‍⚕️ Specialist: {primary['doctor_specialist']}"
        )

        match_pct = primary["match_percentage"]
        self.progress_bar["value"] = match_pct
        self.bar_label.config(text=f"Confidence: {match_pct}% (Rule Fired)")

        for rank, d in enumerate(top_diseases, 1):
            self.tree_candidates.insert(
                "",
                "end",
                values=(f"#{rank}", d["disease"], d["severity"], f"{d['match_percentage']}%", d["doctor_specialist"])
            )

        self.advice_text.delete("1.0", tk.END)
        self.advice_text.insert(
            tk.END,
            f"Diagnosis: {primary['disease']} ({primary['severity']} Severity)\n"
            f"Consult: {primary['doctor_specialist']}\n\n"
            f"{primary['advice']}\n\n"
            f"Unobserved Rule Symptoms: {', '.join(primary['missing_symptoms']) if primary['missing_symptoms'] else 'None (Complete Rule Match)'}."
        )

        self.result_notebook.select(self.diagnosis_tab)

    def _get_current_patient_info(self):
        """Collects patient info from the UI fields."""
        return {
            "name": self.patient_name_entry.get().strip() or "Rahul Verma",
            "age": self.patient_age_entry.get().strip() or "24",
            "gender": self.gender_combo.get(),
            "city": self.patient_city_entry.get().strip() or "Delhi"
        }

    def _export_html_report(self):
        """Exports styled hospital HTML report and opens in browser."""
        if not self.last_result:
            messagebox.showinfo("Export Report", "Please run a diagnosis first.")
            return

        patient_info = self._get_current_patient_info()
        filename = f"Diagnosis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        save_path = os.path.abspath(filename)

        try:
            generate_html_report(patient_info, self.last_result, save_path)
            webbrowser.open(f"file://{save_path}")
            messagebox.showinfo(
                "Hospital Report Generated",
                f"HTML Medical Report created and opened in your web browser:\n{save_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate HTML report: {e}")

    def _launch_web_in_browser(self):
        """Opens the web application prototype in default web browser."""
        index_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
        if os.path.exists(index_file):
            webbrowser.open(f"file://{index_file}")
        else:
            messagebox.showwarning("Web App", "index.html not found in project folder.")

    def _export_text_report(self):
        """Exports standard text report."""
        if not self.last_result:
            messagebox.showinfo("Export Report", "Please run a diagnosis first.")
            return

        patient_info = self._get_current_patient_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report_lines = [
            "=" * 70,
            "       SANJEEVANI HEALTHCARE NETWORK - DIAGNOSTIC REPORT",
            "       Unit III: Knowledge Representation and Reasoning",
            "=" * 70,
            f"Date & Time  : {timestamp}",
            f"Patient Name : {patient_info['name']}",
            f"Age / Gender : {patient_info['age']} Yrs / {patient_info['gender']}",
            f"City         : {patient_info['city']}",
            "-" * 70,
            f"Observed Facts (Symptoms):\n  {', '.join(self.last_result['patient_facts'])}",
            "-" * 70,
            "FORWARD CHAINING DIAGNOSIS RESULTS:",
        ]

        if not self.last_result["top_diseases"]:
            report_lines.append("  No disease rule fired under current threshold criteria.")
        else:
            primary = self.last_result["top_diseases"][0]
            report_lines.append(f"  Primary Diagnosis   : {primary['disease']} ({primary['match_percentage']}% Match)")
            report_lines.append(f"  Severity            : {primary['severity']}")
            report_lines.append(f"  Consult Specialist  : {primary['doctor_specialist']}")
            report_lines.append(f"  Matched Symptoms    : {', '.join(primary['matched_symptoms'])}")
            report_lines.append(f"  Missing Symptoms    : {', '.join(primary['missing_symptoms']) if primary['missing_symptoms'] else 'None'}")
            report_lines.append(f"\n  Clinical Advice:\n{primary['advice']}")

        report_lines.extend([
            "-" * 70,
            f"Project Team : {', '.join([m['name'] for m in STUDENT_DETAILS['team_members']])}",
            f"Course       : {STUDENT_DETAILS['course']}",
            "-" * 70,
            MEDICAL_DISCLAIMER,
            "=" * 70
        ])

        filename = f"Diagnosis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=filename,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(report_lines))
                messagebox.showinfo("Report Saved", f"Medical report saved at:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save report: {e}")


def launch_gui():
    root = tk.Tk()
    app = MedicalDiagnosisGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
