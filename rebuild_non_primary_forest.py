"""Rebuild the per-year land workbook with the non-primary forest of countries
FAO gives no naturally regenerating forest split.

`processing_classification.landuse_calculation` used to insert a zero
"Naturally regenerating forest" (6717) row for a country FAOSTAT reports
forest land (6646) and primary forest (6714) for but no 6717, so its
"Naturally generating forest - Non primary forest" (6717 - 6714) came out
as minus its primary forest: Albania -848 km2 in every year, and Albania's
and North Macedonia's forest missing from the account. The rule is fixed
there (`derive_naturally_regenerating`: forest land minus planted forest).
A full rerun of the allocation needs the full-year land-use table, which is
not on disk (final_tables/landuse_final_runall.csv holds 2020 only since
2026-09-16), so this script applies the fixed rule to the existing
allocation workbook from the FAOSTAT Inputs_LandUse bulk file:

- the countries are those `derive_naturally_regenerating` returns for the
  bulk file (no 6717 row, forest land reported);
- their non-primary forest row of the 'final cropland' sheet becomes
  derived naturally regenerating forest minus primary forest (0 where FAO
  has none), floored at 0, for every year the bulk file has forest land;
- the sheet is summed to EXIO3 regions with
  `aggregation_region.aggregation.aggregate_final_cropland` and written one
  sheet per year, the layout `exiobase_land_extensions_final_format.py
  --source-xlsx` reads.

    python rebuild_non_primary_forest.py --output <dir>/aggregation_per_year.xlsx
"""

from __future__ import annotations

import argparse
from pathlib import Path

import country_converter as coco
import numpy as np
import pandas as pd

from aggregation_region.aggregation import aggregate_final_cropland, write_per_year
from processing_classification.landuse_calculation import (
    FOREST_LAND,
    NATURALLY_REGENERATING,
    PLANTED_FOREST,
    PRIMARY_FOREST,
    derive_naturally_regenerating,
)

ROW = "Naturally generating forest - Non primary forest"
ALLOCATION_XLSX = Path(__file__).parent / "EXIOBASE_allocation_FAO.xlsx"
FAOSTAT_LANDUSE = Path("D:/indecol/data/fao/data/Inputs_LandUse_E_All_Data_NOFLAG.csv")
AREA_ELEMENT = 5110          # "Area", 1000 ha
KM2_PER_1000HA = 10.0
#: M49 codes country_converter (1.3.2) has no UNcode for: 736 is FAOSTAT's
#: "Sudan (former)" (FAO area 206, 1961-2011); 729 "Sudan" (FAO 276, from
#: 2012) converts to SDN already. No year carries both, so the two rows of
#: an item are summed into one SDN series. Same rule as
#: download.handlers.FAO_CODE_PATCH.
M49_PATCH = {736: "SDN"}


def read_faostat_forest(path: Path) -> pd.DataFrame:
    """The four forest items of the FAOSTAT land-use bulk file, in km2, in the
    long layout of the allocation's land-use table (ISO3, Item Code, Item,
    Unit, Y<year>...). Countries from the M49 code via country_converter."""
    raw = pd.read_csv(path, encoding="latin-1")
    raw = raw[(raw["Area Code"] < 5000)            # FAOSTAT codes 5000+ are aggregates
              & (raw["Element Code"] == AREA_ELEMENT)
              & raw["Item Code"].isin([FOREST_LAND, PRIMARY_FOREST, PLANTED_FOREST,
                                       NATURALLY_REGENERATING])]
    m49 = raw["Area Code (M49)"].astype(str).str.lstrip("'").astype(int)
    patched = m49.map(M49_PATCH)
    iso3 = coco.convert(names=m49[patched.isna()].tolist(), src="UNcode", to="ISO3",
                        not_found=None)
    if not isinstance(iso3, list):
        iso3 = [iso3]
    patched[patched.isna()] = iso3
    years = [c for c in raw.columns if c.startswith("Y") and c[1:].isdigit()]
    out = raw[["Item Code", "Item"]].copy()
    out.insert(0, "ISO3", patched.to_numpy())
    out["Unit"] = "km2"
    out[years] = raw[years].astype(float) * KM2_PER_1000HA
    out = out[out["ISO3"].notna()].reset_index(drop=True)
    # One row per item for a patched country (its two FAO areas); every
    # other row is left as it was.
    hit = out["ISO3"].isin(set(M49_PATCH.values()))
    merged = (out[hit].groupby(["ISO3", "Item Code", "Item", "Unit"], sort=False)[years]
              .sum(min_count=1).reset_index())
    return pd.concat([out[~hit], merged[out.columns]], ignore_index=True)


def corrected_rows(landuse: pd.DataFrame) -> pd.DataFrame:
    """Non-primary forest (derived 6717 - 6714, floored at 0) of every country
    `derive_naturally_regenerating` covers, indexed by ISO3, Y<year> columns."""
    nrf = derive_naturally_regenerating(landuse).set_index("ISO3")
    years = [c for c in nrf.columns if str(c).startswith("Y")]
    code = pd.to_numeric(landuse["Item Code"], errors="coerce")
    primary = (landuse[code == PRIMARY_FOREST].drop_duplicates("ISO3")
               .set_index("ISO3")[years].reindex(nrf.index).astype(float).fillna(0.0))
    return (nrf[years].astype(float) - primary).clip(lower=0.0)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--allocation-xlsx", type=Path, default=ALLOCATION_XLSX)
    p.add_argument("--faostat-landuse", type=Path, default=FAOSTAT_LANDUSE)
    p.add_argument("--output", type=Path, required=True,
                   help="per-year workbook to write (never the tracked one in place)")
    p.add_argument("--allocation-output", type=Path, default=None,
                   help="also write the corrected 'final cropland' sheet, for "
                        "exiobase_land_extensions_axis.py --allocation-xlsx (rx2)")
    args = p.parse_args()
    if args.output.resolve().parent == Path(__file__).parent.resolve():
        raise SystemExit("write the rebuilt workbook outside the repository")

    sheet = pd.read_excel(args.allocation_xlsx, sheet_name="final cropland")
    fixed = corrected_rows(read_faostat_forest(args.faostat_landuse))
    is_row = sheet["EXIOBASE extension name"] == ROW
    for iso3, values in fixed.iterrows():
        hit = is_row & (sheet["ISO3"] == iso3)
        if not hit.any():
            print(f"{iso3}: not in the allocation workbook, skipped")
            continue
        cols = [c for c in values.index if c in sheet.columns and np.isfinite(values[c])]
        before = sheet.loc[hit, cols].iloc[0]
        sheet.loc[hit, cols] = values[cols].to_numpy()
        print(f"{iso3}: {ROW} {cols[0]}-{cols[-1]}: "
              f"{before.min():.1f}..{before.max():.1f} km2 -> "
              f"{values[cols].min():.1f}..{values[cols].max():.1f} km2")
    write_per_year(aggregate_final_cropland(sheet), args.output)
    print(f"wrote {args.output}")
    if args.allocation_output is not None:
        with pd.ExcelWriter(args.allocation_output) as writer:
            sheet.to_excel(writer, sheet_name="final cropland", index=False)
        print(f"wrote {args.allocation_output}")


if __name__ == "__main__":
    main()
