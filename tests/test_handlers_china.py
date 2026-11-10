"""China (FAOSTAT area 351) net of Hong Kong, Macao and Taiwan in the
download handlers (download/handlers.py net_china, fao_area_to_iso3).

    .venv/Scripts/python.exe -m unittest discover -s tests
"""

import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "download"))
import handlers  # noqa: E402


def wide(rows):
    """FAOSTAT wide rows: (area, item, element, unit, Y1995, Y2019)."""
    return pd.DataFrame(rows, columns=["Area Code", "Item Code", "Element Code", "Unit",
                                       "Y1995", "Y2019"])


def row(df, area, item, element=5110):
    sel = df[(df["Area Code"] == area) & (df["Item Code"] == item) & (df["Element Code"] == element)]
    assert len(sel) == 1, sel
    return sel.iloc[0]


class NetChinaTest(unittest.TestCase):
    def test_mainland_row_replaces_351(self):
        df = wide([
            (351, 6620, 5110, "1000 ha", 130880.0, 128656.2),
            (41, 6620, 5110, "1000 ha", 130000.0, 127862.0),
            (214, 6620, 5110, "1000 ha", 873.0, 790.2),
            (96, 6620, 5110, "1000 ha", 7.0, 4.0),
        ])
        out = handlers.net_china(df)
        self.assertNotIn(41, set(out["Area Code"]))
        cn = row(out, 351, 6620)
        self.assertEqual(cn["Y1995"], 130000.0)
        self.assertEqual(cn["Y2019"], 127862.0)
        self.assertEqual(row(out, 214, 6620)["Y1995"], 873.0)
        self.assertEqual(len(out), 3)

    def test_mainland_only_series_is_kept_as_china(self):
        df = wide([(41, 6659, 5110, "1000 ha", np.nan, 371966.0)])
        out = handlers.net_china(df)
        self.assertEqual(row(out, 351, 6659)["Y2019"], 371966.0)

    def test_without_mainland_additive_is_netted_and_floored(self):
        df = wide([
            (351, 15, 5312, "ha", 100.0, 10.0),
            (214, 15, 5312, "ha", 20.0, 8.0),
            (96, 15, 5312, "ha", np.nan, 5.0),
            (351, 15, 5412, "kg/ha", 3000.0, 3100.0),
            (214, 15, 5412, "kg/ha", 2000.0, 2100.0),
        ])
        out = handlers.net_china(df)
        area = row(out, 351, 15, 5312)
        self.assertAlmostEqual(area["Y1995"], 80.0)
        self.assertEqual(area["Y2019"], 0.0)                  # 10 - 13 floored
        # a yield (rate) cannot be netted: left as reported
        self.assertEqual(row(out, 351, 15, 5412)["Y1995"], 3000.0)

    def test_empty_cell_stays_empty_and_others_untouched(self):
        df = wide([
            (351, 6640, 5110, "1000 ha", np.nan, 100.0),
            (214, 6640, 5110, "1000 ha", 5.0, 10.0),
            (4, 6640, 5110, "1000 ha", 1.0, 2.0),
        ])
        out = handlers.net_china(df)
        self.assertTrue(np.isnan(row(out, 351, 6640)["Y1995"]))
        self.assertAlmostEqual(row(out, 351, 6640)["Y2019"], 90.0)
        pd.testing.assert_series_equal(row(out, 4, 6640), row(df, 4, 6640), check_names=False)

    def test_no_china_is_a_no_op(self):
        df = wide([(4, 6620, 5110, "1000 ha", 1.0, 2.0)])
        pd.testing.assert_frame_equal(handlers.net_china(df), df)

    def test_fao_area_to_iso3_maps_netted_china_to_chn(self):
        df = wide([
            (351, 6620, 5110, "1000 ha", 130880.0, 128656.2),
            (41, 6620, 5110, "1000 ha", 130000.0, 127862.0),
            (214, 6620, 5110, "1000 ha", 873.0, 790.2),
        ])
        out = handlers.fao_area_to_iso3(df).set_index("ISO3")
        self.assertEqual(out.loc["CHN", "Y1995"], 130000.0)
        self.assertEqual(out.loc["TWN", "Y1995"], 873.0)


if __name__ == "__main__":
    unittest.main()
