"""Land extension on another country axis (rx2), from the per-country allocation.

The 49-region account is built in two steps: aggregation_region/
aggregation.py sums the `final cropland` sheet of
EXIOBASE_allocation_FAO.xlsx (per ISO3) onto EXIO3 regions with
country_converter and writes aggregation_per_year.xlsx, then
exiobase_land_extensions_final_format.py lays that out as pxp and turns it
into ixi with the release tree's MarketShare matrices. This script does
the same for the 159-region rx2 axis in one pass:

- each ISO3 goes to its rx2 region through io_utils (an rx2 country is
  its own region, every other code its W bucket);
- product codes become pxp `F`, the final-demand code (y01, artificial
  surfaces used by households) becomes `F_Y`, exactly as the reindexes
  of the final-format script split them. The workbook's one stressor
  with no product code is dropped by that same reindex on e3 and is
  dropped here too;
- ixi is `F_pxp @ D`, with D the market share built per region from the
  rx2 per-country SUT export (rx2 has no MarketShare folder), sparse;
  a product a country does not supply falls back to its characteristic
  industry, so no area is lost;
- files are written in the release layout (names, file_parameters.json)
  through io_utils, which checks it.

    python exiobase_land_extensions_axis.py --axis rx2
    python exiobase_land_extensions_axis.py --axis rx2 --years 2019 --output-root <tmp>

Years 1995-2023, as the 49-region account. The 2024-2028 tail is filled
afterwards with io_utils.extension_nowcast, as on the e3 tree.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from io_utils.classification import (
    final_demand_layout,
    iso3_to_region,
    pro_multiindex,
    region_codes,
    sector_layout,
)
from io_utils.extension_io import write_extension_folder
from io_utils.sut.per_country_supply import market_share

ALLOCATION_XLSX = Path(__file__).parent / "EXIOBASE_allocation_FAO.xlsx"
SHEET = "final cropland"
RELEASE_ROOT = Path("D:/indecol/Projects/MRIOs/EXIOBASE3/EXIOBASE_3_12_0")
EXTENSION = "land"
UNIT = "km2"
FD_CODE = "y01"
YEARS = range(1995, 2024)


def read_allocation(axis: str, path: Path = ALLOCATION_XLSX) -> pd.DataFrame:
    """The per-ISO3 allocation with an rx2 `region` column."""
    df = pd.read_excel(path, sheet_name=SHEET)
    to_region = iso3_to_region(axis)
    unknown = sorted(set(df["ISO3"].astype(str)) - set(to_region))
    if unknown:
        raise ValueError(f"ISO3 codes with no {axis} region: {unknown}")
    df["region"] = df["ISO3"].map(to_region)
    return df


def year_frames(
    df: pd.DataFrame, year: int, axis: str
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """pxp F on (region, product code) and F_Y on (region, category name)."""
    col = f"Y{year}"
    coded = df.dropna(subset=["EXIOBASE product code"])
    pivot = coded.pivot_table(
        index="EXIOBASE extension name",
        columns=["region", "EXIOBASE product code"],
        values=col,
        aggfunc="sum",
        fill_value=0.0,
    )
    F = pivot.reindex(columns=pro_multiindex(axis), fill_value=0.0)
    fd_cols = pd.MultiIndex.from_product([list(region_codes(axis)), [FD_CODE]])
    F_Y = pivot.reindex(columns=fd_cols, fill_value=0.0)
    # y01 is the first final-demand category; the rest of F_Y is zero.
    full = pd.DataFrame(0.0, index=pivot.index, columns=final_demand_layout(axis))
    full.iloc[:, ::7] = F_Y.to_numpy()
    covered = F.to_numpy().sum() + full.to_numpy().sum()
    if not np.isclose(covered, coded[col].sum(), rtol=1e-12):
        raise ValueError(f"{year}: {coded[col].sum()} coded in, {covered} laid out")
    return F, full


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--axis", required=True, choices=["rx2"])
    p.add_argument("--years", type=int, nargs="*", default=None)
    p.add_argument("--output-root", type=Path, default=None)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--allocation-xlsx", type=Path, default=ALLOCATION_XLSX,
                   help="workbook with the 'final cropland' sheet (default the "
                        "tracked one; rebuild_non_primary_forest.py "
                        "--allocation-output writes a corrected one)")
    args = p.parse_args()

    axis = args.axis
    out_root = args.output_root or (
        RELEASE_ROOT.with_name(f"{RELEASE_ROOT.name}_{axis}") / "raw" / "Extensions" / EXTENSION
    )
    sut_root = RELEASE_ROOT.with_name(f"{RELEASE_ROOT.name}_{axis}") / "raw" / "sut" / "current"
    df = read_allocation(axis, args.allocation_xlsx)
    years = [y for y in YEARS if args.years is None or y in args.years]
    for year in years:
        F, F_Y = year_frames(df, year, axis)
        D = market_share(sut_root, year, axis)
        F_ixi = pd.DataFrame(np.asarray((D.T @ F.to_numpy().T).T), index=F.index)
        if not np.isclose(F_ixi.to_numpy().sum(), F.to_numpy().sum(), rtol=1e-9):
            raise ValueError(f"{year}: ixi does not conserve the pxp area")
        unit = pd.DataFrame({"unit": UNIT}, index=F.index)
        for system, frame in (("pxp", F), ("ixi", F_ixi)):
            write_extension_folder(
                out_root / system / str(year), EXTENSION, system,
                frame.set_axis(sector_layout(axis, system), axis=1), F_Y, unit,
                axis=axis, overwrite=args.overwrite,
            )
        print(f"{year}: F {F.to_numpy().sum():.6g} km2, F_Y {F_Y.to_numpy().sum():.6g} km2")


if __name__ == "__main__":
    main()
