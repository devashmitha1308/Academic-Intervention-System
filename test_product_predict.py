"""Automated validation unit tests for SC03 Product V1."""

import unittest
from src.product_predict import FEATURES, validate_inputs


class ValidationTests(unittest.TestCase):
    """Unit tests for student indicator schema and range validation."""

    def setUp(self):
        """Prepare a baseline valid input dictionary before each test."""
        self.values = {
            "code_module": "DDD",
            "code_presentation": "2014J",
            "gender": "F",
            "region": "East Anglian Region",
            "highest_education": "Lower Than A Level",
            "imd_band": "30-40%",
            "age_band": "35-55",
            "num_of_prev_attempts": "0",
            "studied_credits": "60",
            "disability": "N",
            "assessment_average": "62.5",
            "assessment_count": "2.0",
            "assessment_max": "65.0",
            "assessment_min": "60.0",
            "assessment_weighted_average": "63.33",
            "total_clicks": "152.0",
            "average_clicks": "2.24",
            "maximum_clicks": "6.0",
            "active_days": "16.0",
            "unique_resources": "19.0",
        }

    def test_normal(self):
        """Verify that a valid normal student record passes validation."""
        clean = validate_inputs(self.values)
        self.assertEqual(clean["assessment_average"], 62.5)
        self.assertEqual(clean["code_module"], "DDD")
        self.assertEqual(clean["studied_credits"], 60.0)
        self.assertEqual(clean["active_days"], 16.0)

    def test_assessment_boundaries(self):
        """Verify boundary inputs at exactly 0% and 100% for academic scores."""
        for boundary_val in ("0", "100", 0.0, 100.0):
            self.values["assessment_average"] = boundary_val
            clean = validate_inputs(self.values)
            self.assertEqual(clean["assessment_average"], float(boundary_val))

    def test_invalid_assessment_scores(self):
        """Verify rejection of out-of-range, blank, non-numeric, and non-finite scores."""
        for invalid_val in ("-1", "101", "150", "", "   ", "abc", "nan", "inf"):
            self.values["assessment_average"] = invalid_val
            with self.assertRaises(ValueError):
                validate_inputs(self.values)

    def test_negative_measurements(self):
        """Verify rejection of negative values for counts, attempts, credits, and engagement."""
        for field in ("num_of_prev_attempts", "studied_credits", "total_clicks", "active_days"):
            with self.subTest(field=field):
                original = self.values[field]
                self.values[field] = "-5"
                with self.assertRaises(ValueError):
                    validate_inputs(self.values)
                self.values[field] = original

    def test_missing_feature(self):
        """Verify that omitting a mandatory input feature raises ValueError."""
        self.values.pop("assessment_average")
        with self.assertRaises(ValueError):
            validate_inputs(self.values)


if __name__ == "__main__":
    unittest.main()
