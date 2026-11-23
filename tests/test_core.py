import csv
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from triad.core import ITEMS,load_csv,validate,summarize,alpha,pearson

class ResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=load_csv(Path(__file__).resolve().parents[1]/"data/demo/synthetic_teacher_survey.csv")
    def test_schema_and_n(self):
        self.assertEqual(validate(self.rows),"synthetic")
        self.assertEqual(len(self.rows),120)
    def test_scale_range(self):
        report=summarize(self.rows,"synthetic")
        for scale in report["scales"].values():
            self.assertGreaterEqual(scale["mean"],1)
            self.assertLessEqual(scale["mean"],5)
    def test_reject_invalid_item(self):
        rows=[r.copy() for r in self.rows]
        rows[0]["ph1"]="6"
        with self.assertRaises(ValueError): validate(rows)
    def test_reject_status_mixing(self):
        rows=[r.copy() for r in self.rows]
        rows[0]["data_status"]="field_verified"
        with self.assertRaises(ValueError): validate(rows)
    def test_alpha_constant_is_undefined(self):
        self.assertIsNone(alpha([{"x":1,"y":1} for _ in range(4)],["x","y"]))
    def test_correlation(self):
        self.assertEqual(pearson([1,2,3],[2,4,6]),1.0)
if __name__=="__main__":unittest.main()
