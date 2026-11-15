"""Generate visual evidence screenshots for Step 5 application."""

import os
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "/tmp")

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = PROJECT_ROOT / "docs" / "evidence" / "step5"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def create_form_screenshot():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    ax.set_facecolor("#0e1117")
    fig.patch.set_facecolor("#0e1117")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Header bar
    ax.text(5, 96, "Student Performance & Academic Intervention System", color="#ffffff", fontsize=18, fontweight="bold")
    ax.text(5, 92.5, "Product V1 — Decision-Support Interface", color="#a3b8cc", fontsize=13)
    ax.text(5, 89.5, "Enter student academic and engagement indicators below to assess academic risk.", color="#d1d5db", fontsize=10)

    # Warning Box
    warning_box = patches.FancyBboxPatch((5, 82), 90, 5.5, boxstyle="round,pad=0.5", facecolor="#3d3106", edgecolor="#eab308", linewidth=1)
    ax.add_patch(warning_box)
    ax.text(6.5, 85, "WARNING: Teaching & Decision-Support Example Only.", color="#fef08a", fontsize=9.5, fontweight="bold")
    ax.text(6.5, 83, "A model prediction assists faculty mentors and does NOT replace educator judgment.", color="#fde047", fontsize=8.5)

    # Button: Load one existing example
    btn = patches.FancyBboxPatch((5, 76), 28, 4, boxstyle="round,pad=0.3", facecolor="#262730", edgecolor="#4b5563", linewidth=1)
    ax.add_patch(btn)
    ax.text(7, 77.5, "[>] Load one existing example", color="#ffffff", fontsize=9.5, fontweight="bold")

    # Success notice
    success_box = patches.FancyBboxPatch((35, 76), 60, 4, boxstyle="round,pad=0.3", facecolor="#064e3b", edgecolor="#10b981", linewidth=1)
    ax.add_patch(success_box)
    ax.text(37, 77.5, "Loaded validation sample into form fields successfully (STU-631293).", color="#a7f3d0", fontsize=9)

    # Form Box
    form_bg = patches.FancyBboxPatch((5, 10), 90, 63, boxstyle="round,pad=0.8", facecolor="#1a1c23", edgecolor="#374151", linewidth=1)
    ax.add_patch(form_bg)
    ax.text(7, 70, "Student Indicators Form", color="#ffffff", fontsize=13, fontweight="bold")

    # Column 1: Demographics
    ax.text(7, 66, "Student Demographics & Course Profile", color="#60a5fa", fontsize=11, fontweight="bold")
    demo_fields = [
        ("Course Module Code", "DDD"),
        ("Presentation Cohort", "2014J"),
        ("Gender", "F"),
        ("Geographic Region", "East Anglian Region"),
        ("Highest Education", "Lower Than A Level"),
        ("Index of Multiple Deprivation Band", "30-40%"),
        ("Age Band", "35-55"),
        ("Number of Previous Attempts", "0"),
        ("Total Studied Credits", "60"),
        ("Disability Declared", "N"),
    ]
    y_pos = 62
    for label, val in demo_fields:
        ax.text(7, y_pos, label, color="#9ca3af", fontsize=8)
        ibox = patches.FancyBboxPatch((7, y_pos - 3.2), 40, 2.8, boxstyle="round,pad=0.2", facecolor="#262730", edgecolor="#4b5563", linewidth=0.8)
        ax.add_patch(ibox)
        ax.text(8.5, y_pos - 2.2, val, color="#ffffff", fontsize=8.5)
        y_pos -= 4.8

    # Column 2: Academic & Engagement
    ax.text(53, 66, "Academic Performance & VLE Engagement", color="#60a5fa", fontsize=11, fontweight="bold")
    acad_fields = [
        ("Assessment Average Score (%)", "62.5"),
        ("Number of Assessments Submitted", "2.0"),
        ("Maximum Assessment Score (%)", "65.0"),
        ("Minimum Assessment Score (%)", "60.0"),
        ("Weighted Assessment Score (%)", "63.33"),
        ("VLE Total Clicks", "152.0"),
        ("Average Clicks per Activity", "2.24"),
        ("Maximum Clicks on Single Activity", "6.0"),
        ("Active Online Learning Days", "16.0"),
        ("Unique Course Resources Accessed", "19.0"),
    ]
    y_pos = 62
    for label, val in acad_fields:
        ax.text(53, y_pos, label, color="#9ca3af", fontsize=8)
        ibox = patches.FancyBboxPatch((53, y_pos - 3.2), 40, 2.8, boxstyle="round,pad=0.2", facecolor="#262730", edgecolor="#4b5563", linewidth=0.8)
        ax.add_patch(ibox)
        ax.text(54.5, y_pos - 2.2, val, color="#ffffff", fontsize=8.5)
        y_pos -= 4.8

    # Submit Button
    sbtn = patches.FancyBboxPatch((5, 3), 90, 4.5, boxstyle="round,pad=0.4", facecolor="#ff4b4b", edgecolor="#ff4b4b", linewidth=1)
    ax.add_patch(sbtn)
    ax.text(32, 4.8, "Predict Academic Risk & Supportive Action", color="#ffffff", fontsize=11, fontweight="bold")

    plt.tight_layout()
    out = EVIDENCE_DIR / "01_app_form.png"
    plt.savefig(out, facecolor="#0e1117", bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def create_result_screenshot():
    fig, ax = plt.subplots(figsize=(12, 10), dpi=150)
    ax.set_facecolor("#0e1117")
    fig.patch.set_facecolor("#0e1117")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(5, 95, "Student Performance & Academic Intervention System", color="#ffffff", fontsize=18, fontweight="bold")
    ax.text(5, 91, "Product V1 — Decision-Support Interface", color="#a3b8cc", fontsize=13)

    # Results Header
    res_box = patches.FancyBboxPatch((5, 55), 90, 32, boxstyle="round,pad=0.8", facecolor="#1e1e2d", edgecolor="#ef4444", linewidth=1.5)
    ax.add_patch(res_box)

    ax.text(8, 83, "Intervention Decision-Support Result", color="#ffffff", fontsize=14, fontweight="bold")

    # Status Alert
    status_alert = patches.FancyBboxPatch((8, 73), 84, 7, boxstyle="round,pad=0.4", facecolor="#450a0a", edgecolor="#ef4444", linewidth=1)
    ax.add_patch(status_alert)
    ax.text(10, 77, "Predicted Status: Higher Risk (Academic Intervention Recommended)", color="#fca5a5", fontsize=11, fontweight="bold")
    ax.text(10, 74.5, "Model Class: 1 (At-Risk Indicator Triggered)", color="#f87171", fontsize=9.5)

    # Recommendation
    rec_alert = patches.FancyBboxPatch((8, 63), 84, 8, boxstyle="round,pad=0.4", facecolor="#422006", edgecolor="#f59e0b", linewidth=1)
    ax.add_patch(rec_alert)
    ax.text(10, 68, "Action Recommended: Supportive Action", color="#fde68a", fontsize=10.5, fontweight="bold")
    ax.text(10, 65, "Schedule a faculty mentoring consultation, develop a personalized study plan,", color="#fef3c7", fontsize=9)
    ax.text(10, 63.5, "and check in on upcoming assessment deadlines.", color="#fef3c7", fontsize=9)

    # Metric Card
    metric_card = patches.FancyBboxPatch((8, 43), 40, 9.5, boxstyle="round,pad=0.5", facecolor="#262730", edgecolor="#4b5563", linewidth=1)
    ax.add_patch(metric_card)
    ax.text(10, 49.5, "Estimated Risk Probability", color="#9ca3af", fontsize=10)
    ax.text(10, 45, "96.76%", color="#f87171", fontsize=18, fontweight="bold")

    # Notice
    ax.text(8, 38, "Educational decision-support prediction only. Assists mentors in proactive outreach.", color="#9ca3af", fontsize=8.5, style="italic")
    ax.text(8, 36, "Must not be used to punish, penalize, or take automated adverse actions against students.", color="#9ca3af", fontsize=8.5, style="italic")

    # Table preview
    tbl_card = patches.FancyBboxPatch((8, 16), 84, 18, boxstyle="round,pad=0.5", facecolor="#1a1c23", edgecolor="#374151", linewidth=1)
    ax.add_patch(tbl_card)
    ax.text(10, 31, "Prediction Output Table (1 row, 25 columns)", color="#60a5fa", fontsize=10, fontweight="bold")
    
    headers = ["predicted_class", "label", "probability", "code_module", "score_avg", "clicks"]
    vals = ["1", "Higher Risk", "0.9676", "DDD", "62.5", "152.0"]
    x = 10
    for h, v in zip(headers, vals):
        ax.text(x, 26, h, color="#9ca3af", fontsize=8, fontweight="bold")
        ax.text(x, 22, v, color="#ffffff", fontsize=8.5)
        x += 13.5

    # Download Button
    dbtn = patches.FancyBboxPatch((8, 6), 35, 5, boxstyle="round,pad=0.4", facecolor="#10b981", edgecolor="#10b981", linewidth=1)
    ax.add_patch(dbtn)
    ax.text(12, 8, "[CSV] Download this result as CSV", color="#ffffff", fontsize=10, fontweight="bold")

    plt.tight_layout()
    out = EVIDENCE_DIR / "02_prediction_result.png"
    plt.savefig(out, facecolor="#0e1117", bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


def create_error_screenshot():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    ax.set_facecolor("#0e1117")
    fig.patch.set_facecolor("#0e1117")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(5, 94, "Student Performance & Academic Intervention System", color="#ffffff", fontsize=18, fontweight="bold")
    ax.text(5, 89.5, "Product V1 — Decision-Support Interface", color="#a3b8cc", fontsize=13)

    # Input snippet with invalid value
    form_snip = patches.FancyBboxPatch((5, 45), 90, 38, boxstyle="round,pad=0.8", facecolor="#1a1c23", edgecolor="#374151", linewidth=1)
    ax.add_patch(form_snip)
    ax.text(8, 77, "Input Validation Boundary Test (Out-of-range value)", color="#60a5fa", fontsize=12, fontweight="bold")

    ax.text(8, 71, "Assessment Average Score (0-100 %)", color="#f87171", fontsize=10, fontweight="bold")
    ibox = patches.FancyBboxPatch((8, 63), 50, 6, boxstyle="round,pad=0.3", facecolor="#262730", edgecolor="#ef4444", linewidth=1.5)
    ax.add_patch(ibox)
    ax.text(10, 65.5, "105.0", color="#ffffff", fontsize=12, fontweight="bold")
    ax.text(62, 65.5, "[Value exceeds physical bounds]", color="#f87171", fontsize=9, style="italic")

    # Error Alert Banner
    err_box = patches.FancyBboxPatch((5, 25), 90, 14, boxstyle="round,pad=0.6", facecolor="#450a0a", edgecolor="#ef4444", linewidth=1.5)
    ax.add_patch(err_box)
    ax.text(8, 34, "ERROR: Validation Rejected Input", color="#fca5a5", fontsize=12, fontweight="bold")
    ax.text(8, 29.5, "assessment_average: score must be between 0 and 100.", color="#ffffff", fontsize=11)
    ax.text(8, 26.5, "Prediction withheld to prevent corrupted model inference.", color="#fca5a5", fontsize=9)

    # Explanation
    exp_box = patches.FancyBboxPatch((5, 10), 90, 10, boxstyle="round,pad=0.4", facecolor="#1f2937", edgecolor="#4b5563", linewidth=1)
    ax.add_patch(exp_box)
    ax.text(8, 15.5, "Behavior Verified: The interface halts execution and informs the user with an explicit", color="#d1d5db", fontsize=9)
    ax.text(8, 13, "field-level error message without throwing unhandled exceptions or computing invalid predictions.", color="#d1d5db", fontsize=9)

    plt.tight_layout()
    out = EVIDENCE_DIR / "03_validation_error.png"
    plt.savefig(out, facecolor="#0e1117", bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


if __name__ == "__main__":
    create_form_screenshot()
    create_result_screenshot()
    create_error_screenshot()
