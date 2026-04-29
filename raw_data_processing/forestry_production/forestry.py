# -*- coding: utf-8 -*-
"""FAO Forestry primary production processing.

Mirrors the ``crop_livestock_production`` and ``fishery_production``
modules: produces a tidy long table of primary forestry production
(roundwood) per (ISO3, EXIOBASE product code, EXIOBASE sub-product,
year) in m^3.

Data source
-----------

FAOSTAT Forestry Production and Trade domain (``FO``):
https://www.fao.org/faostat/en/#data/FO

Downloaded by ``download/handlers.get_forestry`` from the standard
FAOSTAT bulk URL. Annual updates from FAO (typically December for the
previous calendar year).

Inputs
------

``<storage_path>/data/refreshed_forestry.csv`` produced by the
download handler. The same FAOSTAT 'Area Code' and 'Item Code'
schema as crop/livestock.

Output
------

pandas.DataFrame with columns

    ISO3, EXIOBASE product code (=p02), EXIOBASE product,
    EXIOBASE sub-product, Unit (=m3), Y1995, ... YYYYY

EXIOBASE has a single forestry product (p02 = "Forestry and logging").
Below that we keep two sub-products to allow downstream extensions to
weight green vs blue water:

    plantation_industrial - industrial roundwood
                            (sawn-wood, pulp, plywood feedstock)
    plantation_fuelwood   - wood fuel (firewood, charcoal feedstock)

The water extension applies green-water footprints
(Schyns & Hoekstra 2014) to both, with industrial roundwood given the
plantation-management coefficient and fuelwood treated separately.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml


# FAO item code -> EXIOBASE sub-product. We use only the two
# mutually-exclusive aggregates that together cover total roundwood:
#   1865 = Industrial roundwood
#   1864 = Wood fuel
# Together: 1864 + 1865 = 1861 (Roundwood total). Coniferous /
# non-coniferous splits (1862/1863, 1866/1867) exist in FAOSTAT but
# are subsets and would double-count if added.
ITEM_TO_SUBPRODUCT: dict[int, str] = {
    1865: "plantation industrial",
    1864: "plantation fuelwood",
}


def _make_valid_fao_year(year: int) -> str:
    return f"Y{int(year)}"


def whole_forestry_calculation(
    years: Iterable[int],
    storage_path: Path,
) -> pd.DataFrame:
    storage_path = Path(storage_path)
    data_path = storage_path / "data"

    here = Path(__file__).resolve().parent
    with open(here / "parameters.yaml") as fh:
        params = yaml.safe_load(fh)
    with open(here / "country.yaml") as fh:
        country_filter = yaml.safe_load(fh)

    refreshed = data_path / "refreshed_forestry.csv"
    if not refreshed.exists():
        raise FileNotFoundError(
            f"Refreshed forestry CSV not found at {refreshed}. Run the "
            f"download handler first (download.main.get_all)."
        )

    df = pd.read_csv(refreshed, encoding="latin-1")

    # FAOSTAT bulks: keep only the Production element and m^3 unit.
    if "Element" in df.columns:
        df = df[df["Element"].astype(str).str.strip() == params["faostat_element"]]
    if "Unit" in df.columns:
        df = df[df["Unit"].astype(str).str.strip() == params["faostat_unit"]]

    df = df[df["Item Code"].isin(set(params["primary_items"]))]

    # Drop ISO3 = 'not found' (handler uses country_converter.convert(...)
    # so unmatched FAO codes show up as 'not found').
    if "ISO3" in df.columns:
        df = df[df["ISO3"].astype(str) != "not found"]
        df = df[df["ISO3"].isin(country_filter)]
    else:
        raise ValueError(
            "Refreshed forestry CSV is missing an ISO3 column - the "
            "download handler is expected to populate it."
        )

    # Keep year columns within the requested window
    yrs = list(years)
    year_cols = [c for c in df.columns if isinstance(c, str)
                 and c.startswith("Y") and c[1:].isdigit()
                 and int(c[1:]) in yrs]
    keep = ["ISO3", "Item Code"] + year_cols
    df = df[keep].copy()

    # Map item code -> sub-product (only the four leaf items survive).
    df["sub_product"] = df["Item Code"].map(ITEM_TO_SUBPRODUCT)
    df = df.dropna(subset=["sub_product"]).copy()

    # Aggregate to (ISO3, sub_product), summing across granular item codes
    out = (df
           .groupby(["ISO3", "sub_product"], as_index=False)
           [year_cols].sum())

    out.insert(1, "EXIOBASE product code", "p02")
    out.insert(2, "EXIOBASE product", "Forestry and logging")
    out = out.rename(columns={"sub_product": "EXIOBASE sub-product"})
    out["Unit"] = "m3"

    front = ["ISO3", "EXIOBASE product code", "EXIOBASE product",
             "EXIOBASE sub-product", "Unit"]
    return out[front + sorted(year_cols)]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storage-path", type=Path, required=True)
    parser.add_argument("--start-year", type=int, default=1995)
    parser.add_argument("--end-year", type=int, default=2022)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    df = whole_forestry_calculation(
        years=range(args.start_year, args.end_year + 1),
        storage_path=args.storage_path,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(args.output, index=False)
        print(f"Wrote {len(df)} rows to {args.output}")
    else:
        print(df.head())
        print(f"... ({len(df)} rows)")
