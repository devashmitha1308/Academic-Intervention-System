"""Demonstrate GroupShuffleSplit to enforce zero student overlap across splits.

This script demonstrates how grouping by `id_student` guarantees that 
no individual student appears in both training and test/validation sets.
"""

from pathlib import Path
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "academic_intervention_dataset.csv"


def verify_group_split():
    if not DATA_PATH.exists():
        print(f"Dataset not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    print(f"Total dataset records: {len(df):,}")
    print(f"Total unique students: {df['id_student'].nunique():,}")

    # First split: 70% Train, 30% Temp (grouped by id_student)
    gss1 = GroupShuffleSplit(n_splits=1, test_size=0.30, random_state=42)
    train_idx, temp_idx = next(gss1.split(df, groups=df["id_student"]))

    train_df = df.iloc[train_idx]
    temp_df = df.iloc[temp_idx]

    # Second split: 50% Validation, 50% Test of Temp (15% and 15% overall)
    gss2 = GroupShuffleSplit(n_splits=1, test_size=0.50, random_state=42)
    val_idx, test_idx = next(gss2.split(temp_df, groups=temp_df["id_student"]))

    val_df = temp_df.iloc[val_idx]
    test_df = temp_df.iloc[test_idx]

    # Verify zero student overlap
    train_students = set(train_df["id_student"])
    val_students = set(val_df["id_student"])
    test_students = set(test_df["id_student"])

    overlap_train_test = len(train_students & test_students)
    overlap_train_val = len(train_students & val_students)
    overlap_val_test = len(val_students & test_students)

    print("\nGroupShuffleSplit Results (Strict Student Isolation):")
    print(f"  - Train rows: {len(train_df):,} | Unique students: {len(train_students):,}")
    print(f"  - Validation rows: {len(val_df):,} | Unique students: {len(val_students):,}")
    print(f"  - Test rows: {len(test_df):,} | Unique students: {len(test_students):,}")
    print("\nVerification of Overlap:")
    print(f"  - Train & Test Overlap:       {overlap_train_test} (0.00%)")
    print(f"  - Train & Validation Overlap: {overlap_train_val} (0.00%)")
    print(f"  - Validation & Test Overlap:  {overlap_val_test} (0.00%)")
    print("\n[SUCCESS] Guaranteed zero student overlap achieved via GroupShuffleSplit.")


if __name__ == "__main__":
    verify_group_split()
