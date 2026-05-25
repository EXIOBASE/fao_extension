# -*- coding: utf-8 -*-
"""FAOSTAT Live Animals (Stocks) processing.

Reads the FAOSTAT Production_Crops_Livestock bulk and emits a tidy
long table of live animal head counts per (ISO3, water-account
species, year), in heads. Used by the water-extension livestock
adapter to refine the within-EXIOBASE-product species split with
country-year specific weights, replacing global defaults.

This is the lightweight, free, public alternative to GLEAM v3 for the
within-product species split. It does not give per-head water-use
intensity (M-H 2012 factors do that), only relative population, which
is what we need for the within-product partition.

Data source
-----------

FAOSTAT Production_Crops_Livestock (domain QCL):
https://www.fao.org/faostat/en/#data/QCL

The Production_Crops_Livestock bulk is already downloaded by
download/main.py; this module reads the same refreshed CSV.

Output
------

pandas.DataFrame with columns

    ISO3, water_species, Y1995, Y1996, ..., YYYYY

water_species values:
    nondairy cattle, dairy cattle, buffaloes, pigs, sheep, goats,
    chicken, turkeys, ducks, geese, camels, horses

The dairy/nondairy cattle split uses the FAOSTAT 'Milk Animals'
element (count of milking cattle) - dairy = milk animals,
nondairy = stocks - milk animals.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml


def _make_valid_fao_year(year: int) -> str:
    return f"Y{int(year)}"


def _normalise_units(value: float, unit: str) -> float:
    """Convert all stocks measurements to head counts (An)."""
    if pd.isna(value):
        return 0.0
    u = str(unit).strip().lower()
    if u in ("an", ""):
        return float(value)
    if u == "1000 an":
        return float(value) * 1000.0
    if u == "no":
        return float(value)
    return float(value)


def whole_livestock_stocks_calculation(
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

    src = data_path / params["source_csv"]
    if not src.exists():
        raise FileNotFoundError(
            f"Source CSV not found: {src}. Run the crop_livestock "
            f"download step first (download.main.get_all)."
        )

    df = pd.read_csv(src, encoding="latin-1", low_memory=False)
    df = df[df["ISO3"].astype(str) != "not found"]
    df = df[df["ISO3"].isin(country_filter)]

    yrs = list(years)
    year_cols = [c for c in df.columns
                 if isinstance(c, str) and c.startswith("Y")
                 and c[1:].isdigit() and int(c[1:]) in yrs]

    species_map = params["species_map"]
    stocks_el = params["stocks_element"]
    milk_el = params["milk_animals_element"]

    # Stocks rows: live animal head counts
    stocks = df[df["Element"] == stocks_el].copy() if "Element" in df.columns else df.copy()
    stocks = stocks[stocks["Item"].isin(species_map.keys())].copy()
    stocks["water_species"] = stocks["Item"].map(species_map)

    # Normalise units to head counts before melting
    for ycol in year_cols:
        stocks[ycol] = pd.to_numeric(stocks[ycol], errors="coerce")
        stocks[ycol] = stocks.apply(
            lambda r: _normalise_units(r[ycol], r.get("Unit", "An")), axis=1
        )

    cattle_total = stocks[stocks["water_species"] == "cattle_total"].copy()
    other = stocks[stocks["water_species"] != "cattle_total"].copy()

    # Split cattle_total into dairy + nondairy using Milk Animals
    if "Element" in df.columns:
        milk = df[(df["Element"] == milk_el) & (df["Item"] == "Cattle")].copy()
    else:
        milk = pd.DataFrame()

    for ycol in year_cols:
        if not milk.empty:
            milk[ycol] = pd.to_numeric(milk[ycol], errors="coerce")
            milk[ycol] = milk.apply(
                lambda r: _normalise_units(r[ycol], r.get("Unit", "An")), axis=1
            )

    if not cattle_total.empty:
        if not milk.empty:
            cattle_merge = cattle_total[["ISO3"] + year_cols].merge(
                milk[["ISO3"] + year_cols].rename(
                    columns={c: f"{c}_milk" for c in year_cols}
                ),
                on="ISO3", how="left",
            )
            for ycol in year_cols:
                milk_col = f"{ycol}_milk"
                cattle_merge[milk_col] = cattle_merge[milk_col].fillna(0.0)
            dairy = cattle_merge[["ISO3"]].copy()
            for ycol in year_cols:
                dairy[ycol] = cattle_merge[f"{ycol}_milk"]
            dairy["water_species"] = "dairy cattle"

            nondairy = cattle_merge[["ISO3"]].copy()
            for ycol in year_cols:
                nondairy[ycol] = (cattle_merge[ycol] - cattle_merge[f"{ycol}_milk"]).clip(lower=0)
            nondairy["water_species"] = "nondairy cattle"

            cattle_split = pd.concat([dairy, nondairy], ignore_index=True)
        else:
            # No Milk Animals series available: assume 35% dairy / 65% nondairy global default
            dairy = cattle_total[["ISO3"]].copy()
            for ycol in year_cols:
                dairy[ycol] = cattle_total[ycol] * 0.35
            dairy["water_species"] = "dairy cattle"
            nondairy = cattle_total[["ISO3"]].copy()
            for ycol in year_cols:
                nondairy[ycol] = cattle_total[ycol] * 0.65
            nondairy["water_species"] = "nondairy cattle"
            cattle_split = pd.concat([dairy, nondairy], ignore_index=True)
    else:
        cattle_split = pd.DataFrame()

    other_cols = ["ISO3", "water_species"] + year_cols
    other = other[other_cols] if not other.empty else other
    final = pd.concat(
        [other, cattle_split[other_cols] if not cattle_split.empty else cattle_split],
        ignore_index=True,
    )

    # Aggregate over duplicate (ISO3, water_species) rows (some FAO files
    # have multiple entries per country/item due to historical entity
    # changes); sum heads.
    final = (final
             .groupby(["ISO3", "water_species"], as_index=False)
             [year_cols].sum())

    final["Unit"] = "head"
    front = ["ISO3", "water_species", "Unit"]
    return final[front + sorted(year_cols)]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storage-path", type=Path, required=True)
    parser.add_argument("--start-year", type=int, default=1995)
    parser.add_argument("--end-year", type=int, default=2022)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    df = whole_livestock_stocks_calculation(
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
