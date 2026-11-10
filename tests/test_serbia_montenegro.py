"""Serbia and Montenegro before 2006 from the former union
(rebuild_non_primary_forest.fill_serbia_montenegro, option --fill-serbia-montenegro).

    .venv/Scripts/python.exe -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rebuild_non_primary_forest as rb  # noqa: E402

NAME = "EXIOBASE extension name"


def sheet():
    rows = [
        ("SRB", "Cropland - cropped area - Wheat", 0.0, 0.0, 60.0),
        ("SRB", "Cropland - fallowed area - Wheat", 0.0, 0.0, 20.0),
        ("MNE", "Cropland - cropped area - Wheat", 0.0, 0.0, 20.0),
        ("MNE", "Cropland - fallowed area - Wheat", 0.0, 0.0, 0.0),
        ("SRB", "Other land", 0.0, 0.0, 30.0),
        ("MNE", "Other land", 0.0, 0.0, 10.0),
        ("SRB", "Planted forest", 0.0, 0.0, 0.0),
        ("MNE", "Planted forest", 0.0, 0.0, 0.0),
        ("HRV", "Other land", 5.0, 6.0, 7.0),
    ]
    return pd.DataFrame(rows, columns=["ISO3", NAME, "Y2004", "Y2005", "Y2006"])


def union():
    return pd.DataFrame({"Y2004": [200.0, 80.0, 9.0], "Y2005": [100.0, np.nan, 9.0]},
                        index=pd.Index([6620, 6670, rb.PLANTED_FOREST], name="Item Code"))


class FillSerbiaMontenegroTest(unittest.TestCase):
    def test_rows_scaled_to_the_union_split_as_in_the_first_separate_year(self):
        s = sheet()
        rep = rb.fill_serbia_montenegro(s, union())
        crop = s[s[NAME].str.startswith("Cropland")]
        # 2006 cropland rows sum to 100; union 200 in 2004 -> factor 2
        self.assertEqual(list(crop["Y2004"]), [120.0, 40.0, 40.0, 0.0])
        self.assertEqual(list(crop["Y2005"]), [60.0, 20.0, 20.0, 0.0])
        other = s[(s[NAME] == "Other land") & s["ISO3"].isin(["SRB", "MNE"])]
        self.assertEqual(list(other["Y2004"]), [60.0, 20.0])
        # union item missing in 2005: left empty
        self.assertEqual(list(other["Y2005"]), [0.0, 0.0])
        # nothing to split on (planted forest zero in 2006): left empty
        self.assertTrue((s.loc[s[NAME] == "Planted forest", ["Y2004", "Y2005"]] == 0).all().all())
        # other countries and the first separate year untouched
        self.assertEqual(list(s.loc[s["ISO3"] == "HRV", ["Y2004", "Y2005", "Y2006"]].iloc[0]), [5.0, 6.0, 7.0])
        pd.testing.assert_series_equal(s["Y2006"], sheet()["Y2006"])
        self.assertAlmostEqual(rep.loc[(rep["group"] == "Cropland") & (rep["year"] == 2004),
                                       "filled_km2"].iloc[0], 200.0)

    def test_years_with_data_are_not_overwritten(self):
        s = sheet()
        s.loc[0, "Y2005"] = 1.0
        rb.fill_serbia_montenegro(s, union())
        self.assertEqual(s.loc[0, "Y2005"], 1.0)
        # 2005 is now the first year with separate data: 2004 is split as in 2005
        self.assertEqual(s.loc[0, "Y2004"], 200.0)
        self.assertEqual(s.loc[2, "Y2004"], 0.0)


if __name__ == "__main__":
    unittest.main()
