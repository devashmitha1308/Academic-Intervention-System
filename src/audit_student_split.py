"""Audit student overlap across training, validation, and test datasets.

This script directly verifies whether the same student (id_student) appears
in multiple dataset splits and explains the mechanism behind course-level vs
student-level partitioning for the OULAD dataset.
"""

from pathlib import Path
import json
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "data" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def audit_splits():
    train_df = pd.read_csv(DATA_DIR / "train.csv")
    val_df = pd.read_csv(DATA_DIR / "validation.csv")
    test_df = pd.read_csv(DATA_DIR / "test.csv")

    train_ids = set(train_df["id_student"].unique())
    val_ids = set(val_df["id_student"].unique())
    test_ids = set(test_df["id_student"].unique())

    all_ids = train_ids | val_ids | test_ids

    # Pairwise overlap checks
    overlap_train_test = train_ids & test_ids
    overlap_train_val = train_ids & val_ids
    overlap_val_test = val_ids & test_ids
    overlap_all_three = train_ids & val_ids & test_ids

    # Check multi-course registrations per student
    total_registrations = len(train_df) + len(val_df) + len(test_df)
    unique_students_total = len(all_ids)
    multi_module_students = (
        pd.concat([train_df, val_df, test_df])
        .groupby("id_student")
        .size()
    )
    multi_reg_count = (multi_module_students > 1).sum()

    report = {
        "dataset_name": "Open University Learning Analytics Dataset (OULAD)",
        "unit_of_analysis": "Student course-module registration (id_student, code_module, code_presentation)",
        "total_course_registrations": total_registrations,
        "unique_students_across_all_splits": unique_students_total,
        "students_with_multiple_module_registrations": int(multi_reg_count),
        "split_counts": {
            "train": {
                "rows": len(train_df),
                "unique_students": len(train_ids),
            },
            "validation": {
                "rows": len(val_df),
                "unique_students": len(val_ids),
            },
            "test": {
                "rows": len(test_df),
                "unique_students": len(test_ids),
            },
        },
        "student_id_overlaps": {
            "train_and_test": len(overlap_train_test),
            "train_and_validation": len(overlap_train_val),
            "validation_and_test": len(overlap_val_test),
            "across_all_three": len(overlap_all_three),
        },
        "overlap_percentage_of_test": round(len(overlap_train_test) / len(test_ids) * 100, 2),
        "explanation": (
            "Because OULAD records are structured per student-course registration "
            "(a single student can enroll in multiple distinct modules such as AAA, BBB, etc.), "
            "a standard stratified row-level split (train_test_split stratified on risk) "
            "evaluates model performance on course-level prediction. "
            "For strict student-level zero-overlap evaluation, GroupShuffleSplit(groups=id_student) "
            "can be used so that no student ID ever co-occurs in training and test splits."
        ),
    }

    report_path = REPORTS_DIR / "student_split_audit.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("=" * 70)
    print("NEURONEXUS DATASET SPLIT & STUDENT OVERLAP AUDIT REPORT")
    print("=" * 70)
    print(f"Total Course Registrations: {total_registrations:,}")
    print(f"Unique Individual Students: {unique_students_total:,}")
    print(f"Students Enrolled in >1 Module: {multi_reg_count:,} ({multi_reg_count/unique_students_total*100:.1f}%)")
    print("-" * 70)
    print("Split Sizes:")
    print(f"  - Training:   {len(train_df):,} rows | {len(train_ids):,} unique students")
    print(f"  - Validation: {len(val_df):,} rows | {len(val_ids):,} unique students")
    print(f"  - Test:       {len(test_df):,} rows | {len(test_ids):,} unique students")
    print("-" * 70)
    print("Student ID Overlap Check:")
    print(f"  - Train & Test Overlap:       {len(overlap_train_test):,} students ({report['overlap_percentage_of_test']}% of test students)")
    print(f"  - Train & Validation Overlap: {len(overlap_train_val):,} students")
    print(f"  - Validation & Test Overlap:  {len(overlap_val_test):,} students")
    print(f"  - Across All Three Splits:    {len(overlap_all_three):,} students")
    print("-" * 70)
    print(f"Report saved to: {report_path}")
    print("=" * 70)

    return report


if __name__ == "__main__":
    audit_splits()
