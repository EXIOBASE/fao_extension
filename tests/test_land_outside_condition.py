"""Land of countries outside the allocation's data condition (R-AGR-04):
landuse_calculation.write_rows / first_value, and the release-route fill
rebuild_non_primary_forest.fill_no_land / no_land_rows.

    .venv/Scripts/python.exe -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import rebuild_non_primary_forest as rb  # noqa: E402
from processing_classification import landuse_calculation as lc  # noqa: E402

NAME = "EXIOBASE extension name"


class WriteRowsTest(unittest.TestCase):
    def test_writes_reported_values_and_skips_missing(self):
        df = pd.DataFrame({"ISO3": ["GRL"] * 4, "EXIOBASE product": list(lc.NON_AGRICULTURAL_PRODUCTS),
                           "Y2019": [0.0] * 4})
        vals = dict(zip(lc.NON_AGRICULTURAL_PRODUCTS,
                        (np.array([[2.0]]), np.array([[3.5]]), np.empty((0, 1)), np.array([[1.0]]))))
        lc.write_rows(df, "GRL", "Y2019", vals)
        self.assertEqual(df["Y2019"].tolist(), [2.0, 3.5, 0.0, 1.0])
        self.assertTrue(np.isnan(lc.first_value(np.empty((0, 1)))))

    def test_switch_is_on(self):
        self.assertTrue(lc.WRITE_LAND_OUTSIDE_DATA_CONDITION)


def landuse_long():
    rows = [("GRL", 6646, 2.0, 2.0), ("GRL", 6716, 0.5, 0.5), ("GRL", 6670, 400.0, 410.0),
            ("ALB", 6646, 9.0, 9.0), ("ALB", 6717, 8.0, 8.0), ("ALB", 6714, 1.0, 1.0),
            ("ALB", 6716, 1.0, 1.0)]
    df = pd.DataFrame(rows, columns=["ISO3", "Item Code", "Y2018", "Y2019"])
    df.insert(2, "Item", "")
    df.insert(3, "Unit", "km2")
    return df


def landcover_long():
    return pd.DataFrame({"ISO3": ["GRL"], "Item Code": [6970], "Item": [""], "Unit": ["km2"],
                         "Y2018": [0.3], "Y2019": [0.4]})


def sheet():
    names = ["Planted forest", rb.ROW, "Other land", "Artificial Surfaces",
             "Cropland - cropped area - Wheat"]
    rows = [("GRL", n, 0.0, 0.0) for n in names] + [("ALB", n, 1.0, 1.0) for n in names]
    rows[0] = ("GRL", "Planted forest", 7.0, 0.0)          # GRL has land in 2018, not in 2019
    return pd.DataFrame(rows, columns=["ISO3", NAME, "Y2018", "Y2019"])


class FillNoLandTest(unittest.TestCase):
    def test_fills_only_country_years_with_no_land(self):
        s = sheet()
        rows = rb.no_land_rows(landuse_long(), landcover_long())
        rep = rb.fill_no_land(s, rows)
        grl = s[s["ISO3"] == "GRL"].set_index(NAME)
        # 2019 is empty: filled from FAOSTAT (non-primary = forest - planted - primary)
        self.assertEqual(grl.at["Planted forest", "Y2019"], 0.5)
        self.assertEqual(grl.at[rb.ROW, "Y2019"], 1.5)
        self.assertEqual(grl.at["Other land", "Y2019"], 410.0)
        self.assertAlmostEqual(grl.at["Artificial Surfaces", "Y2019"], 0.4)
        # cropland is never filled; 2018 had land, so it is left as it was
        self.assertEqual(grl.at["Cropland - cropped area - Wheat", "Y2019"], 0.0)
        self.assertEqual(grl.at["Planted forest", "Y2018"], 7.0)
        self.assertEqual(grl.at["Other land", "Y2018"], 0.0)
        # a country with land is untouched
        self.assertTrue((s[s["ISO3"] == "ALB"][["Y2018", "Y2019"]] == 1.0).all().all())
        self.assertEqual(rep[["ISO3", "year"]].values.tolist(), [["GRL", 2019]])


if __name__ == "__main__":
    unittest.main()
