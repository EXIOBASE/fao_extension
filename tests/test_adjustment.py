"""Rescaling of the parts of a land-use breakdown to their reported total.

    .venv/Scripts/python.exe -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "raw_data_processing" / "land_use_calculation"))
import adjustment  # noqa: E402

DIAGRAM = {
    6600: {"minor1": 6601, "minor2": 6680, "minor3": 6773},
    6646: {"minor1": 6716, "minor2": 6717},
}


def frame(rows):
    return pd.DataFrame(rows, columns=["ISO3", "Item Code", "Y2000"])


def value(df, code, item):
    return float(df.loc[(df["ISO3"] == code) & (df["Item Code"] == item), "Y2000"].iloc[0])


class AdjustTest(unittest.TestCase):
    def run_adjust(self, df, key):
        return adjustment.adjust(df, None, "AAA", "Y2000", DIAGRAM, key, None)

    def test_three_parts_scaled_with_the_sum_before_any_change(self):
        df = frame([
            ("AAA", 6600, 120.0),
            ("AAA", 6601, 50.0),
            ("AAA", 6680, 30.0),
            ("AAA", 6773, 20.0),
            ("BBB", 6601, 7.0),
        ])
        self.run_adjust(df, 6600)
        # sum(parts) = 100, factor 1.2 on every part
        self.assertAlmostEqual(value(df, "AAA", 6601), 60.0)
        self.assertAlmostEqual(value(df, "AAA", 6680), 36.0)
        self.assertAlmostEqual(value(df, "AAA", 6773), 24.0)
        self.assertAlmostEqual(value(df, "AAA", 6600), 120.0)
        self.assertAlmostEqual(value(df, "BBB", 6601), 7.0)

    def test_two_parts_are_scaled(self):
        df = frame([("AAA", 6646, 90.0), ("AAA", 6716, 10.0), ("AAA", 6717, 50.0)])
        self.run_adjust(df, 6646)
        self.assertAlmostEqual(value(df, "AAA", 6716), 15.0)
        self.assertAlmostEqual(value(df, "AAA", 6717), 75.0)

    def test_missing_part_takes_nothing(self):
        df = frame([
            ("AAA", 6600, 80.0),
            ("AAA", 6601, 30.0),
            ("AAA", 6680, np.nan),
            ("AAA", 6773, 10.0),
        ])
        self.run_adjust(df, 6600)
        self.assertAlmostEqual(value(df, "AAA", 6601), 60.0)
        self.assertTrue(np.isnan(value(df, "AAA", 6680)))
        self.assertAlmostEqual(value(df, "AAA", 6773), 20.0)

    def test_part_absent_from_the_country(self):
        df = frame([("AAA", 6600, 50.0), ("AAA", 6601, 20.0), ("AAA", 6680, 5.0)])
        self.run_adjust(df, 6600)
        self.assertAlmostEqual(value(df, "AAA", 6601), 40.0)
        self.assertAlmostEqual(value(df, "AAA", 6680), 10.0)

    def test_missing_total_or_zero_parts_change_nothing(self):
        df = frame([("AAA", 6646, np.nan), ("AAA", 6716, 10.0), ("AAA", 6717, 50.0)])
        self.run_adjust(df, 6646)
        self.assertAlmostEqual(value(df, "AAA", 6716), 10.0)
        self.assertAlmostEqual(value(df, "AAA", 6717), 50.0)

        df = frame([("AAA", 6646, 40.0), ("AAA", 6716, 0.0), ("AAA", 6717, np.nan)])
        self.run_adjust(df, 6646)
        self.assertAlmostEqual(value(df, "AAA", 6716), 0.0)
        self.assertTrue(np.isnan(value(df, "AAA", 6717)))


if __name__ == "__main__":
    unittest.main()
