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

`--fill-serbia-montenegro` (default off) also fills Serbia and Montenegro
before 2006 from FAOSTAT's former union, see `fill_serbia_montenegro`.
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
FAOSTAT_LANDCOVER = Path("D:/indecol/data/fao/data/Environment_LandCover_E_All_Data_NOFLAG.csv")

# --- Serbia and Montenegro before 2006 (R-AGR-14, option, default off) -------
# FAOSTAT reports "Serbia and Montenegro" (area 186) for 1992-2005 and Serbia
# (272) and Montenegro (273) from 2006; country_converter knows only the two
# successors, so SRB and MNE are zero in every year before 2006. With
# --fill-serbia-montenegro each SRB and MNE row of 'final cropland' in a year
# where both countries are empty is set to its value in the first year with
# separate data, scaled by the union's FAOSTAT item in that year over the two
# countries' sum of the item's rows in the first separate year. The rows of an
# item then sum to the union's item, split between the two countries and
# across products as in the first separate year.
SERBIA_MONTENEGRO_AREA = 186
SERBIA_MONTENEGRO = ("SRB", "MNE")
LANDCOVER_ELEMENT = 5008         # the land cover element the allocation uses (6970)
#: 'final cropland' row (by name prefix) -> FAOSTAT item(s) it is built from;
#: non-primary forest is 6717 less 6714, artificial surfaces is land cover 6970.
UNION_ITEMS = (
    ("Cropland - ", (6620,), ()),
    ("Permanent pastures", (6655,), ()),
    ("Planted forest", (PLANTED_FOREST,), ()),
    (ROW, (NATURALLY_REGENERATING,), (PRIMARY_FOREST,)),
    ("Other land", (6670,), ()),
    ("Artificial Surfaces", (6970,), ()),
)
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


def read_union(landuse_path: Path, landcover_path: Path) -> pd.DataFrame:
    """Serbia and Montenegro (FAO area 186) by FAOSTAT item code, km2, Y<year>
    columns: the land-use items (element 5110) and land cover 6970."""
    out = []
    for path, element in ((landuse_path, AREA_ELEMENT), (landcover_path, LANDCOVER_ELEMENT)):
        raw = pd.read_csv(path, encoding="latin-1")
        raw = raw[(raw["Area Code"] == SERBIA_MONTENEGRO_AREA) & (raw["Element Code"] == element)]
        if path == landcover_path:
            raw = raw[raw["Item Code"] == 6970]
        years = [c for c in raw.columns if c.startswith("Y") and c[1:].isdigit()]
        out.append(raw.set_index("Item Code")[years].astype(float) * KM2_PER_1000HA)
    return pd.concat(out)


def fill_serbia_montenegro(sheet: pd.DataFrame, union: pd.DataFrame) -> pd.DataFrame:
    """SRB and MNE rows of 'final cropland' in the years both are empty, from
    the former union (see UNION_ITEMS). Returns one row per (item group, year)
    filled: group, year, union km2, filled km2."""
    years = [c for c in sheet.columns if str(c).startswith("Y") and str(c)[1:].isdigit()]
    names = sheet["EXIOBASE extension name"].astype(str)
    sm = sheet["ISO3"].isin(SERBIA_MONTENEGRO)
    per_year = sheet.loc[sm, years].fillna(0.0).abs().sum()
    nonzero = [y for y in years if per_year[y] > 0]
    if not nonzero:
        raise ValueError("SRB and MNE have no data in the allocation sheet")
    first = nonzero[0]
    empty = [y for y in years if y < first and per_year[y] == 0]
    report = []
    for prefix, plus, minus in UNION_ITEMS:
        rows = sm & names.str.startswith(prefix)
        base = float(sheet.loc[rows, first].fillna(0.0).sum())
        for y in empty:
            if y not in union.columns or any(i not in union.index for i in plus):
                continue
            u = sum(union.at[i, y] for i in plus) - sum(
                union.at[i, y] if i in union.index and np.isfinite(union.at[i, y]) else 0.0
                for i in minus)
            if not np.isfinite(u):
                continue
            u = max(u, 0.0)
            if base <= 0:
                if u > 0:
                    print(f"{prefix!r} {y}: union {u:.1f} km2 but SRB+MNE have none in {first}; not filled")
                continue
            sheet.loc[rows, y] = sheet.loc[rows, first].fillna(0.0) * (u / base)
            report.append({"group": prefix.strip(" -"), "year": int(y[1:]), "union_km2": u,
                           "filled_km2": float(sheet.loc[rows, y].sum())})
    return pd.DataFrame(report)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--allocation-xlsx", type=Path, default=ALLOCATION_XLSX)
    p.add_argument("--faostat-landuse", type=Path, default=FAOSTAT_LANDUSE)
    p.add_argument("--output", type=Path, required=True,
                   help="per-year workbook to write (never the tracked one in place)")
    p.add_argument("--allocation-output", type=Path, default=None,
                   help="also write the corrected 'final cropland' sheet, for "
                        "exiobase_land_extensions_axis.py --allocation-xlsx (rx2)")
    p.add_argument("--fill-serbia-montenegro", action="store_true",
                   help="fill SRB and MNE before 2006 from FAOSTAT 'Serbia and Montenegro' "
                        "(area 186), split as in 2006 (default off; R-AGR-14)")
    p.add_argument("--faostat-landcover", type=Path, default=FAOSTAT_LANDCOVER)
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
    if args.fill_serbia_montenegro:
        rep = fill_serbia_montenegro(sheet, read_union(args.faostat_landuse, args.faostat_landcover))
        if not rep.empty:
            tot = rep.groupby("year")["filled_km2"].sum()
            print(f"SRB+MNE filled from Serbia and Montenegro (FAO 186), {tot.index.min()}-"
                  f"{tot.index.max()}: {tot.iloc[0]:.1f} km2 ({tot.index[0]}) .. "
                  f"{tot.iloc[-1]:.1f} km2 ({tot.index[-1]})")
    write_per_year(aggregate_final_cropland(sheet), args.output)
    print(f"wrote {args.output}")
    if args.allocation_output is not None:
        with pd.ExcelWriter(args.allocation_output) as writer:
            sheet.to_excel(writer, sheet_name="final cropland", index=False)
        print(f"wrote {args.allocation_output}")


if __name__ == "__main__":
    main()
