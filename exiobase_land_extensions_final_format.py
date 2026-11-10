"""Land extension in the release layout: pxp from the aggregated workbook, ixi
through a masked market share.

Reads one sheet per year of a per-year workbook (stressor rows, (region,
EXIOBASE code) columns) and writes raw/Extensions/land/{pxp,ixi}/<year>/ on
the release tree, in the layout every other account on the tree uses.

The release run (00-workflow scripts/run_clean_rebuild.py, land lane) does
not use the default workbook: it first writes the per-year workbook with
`rebuild_non_primary_forest.py --output <dir>/aggregation_per_year.xlsx`
(the tracked EXIOBASE_allocation_FAO.xlsx with the non-primary forest rule
applied, aggregated by aggregation_region/aggregation.py) and passes it
here with `--source-xlsx`. The default, aggregation_per_year.xlsx in the
repository root, is the tracked workbook of 2026-06-13, which predates the
non-primary forest and Sudan corrections; use it only to rerun that state.

The layout:

- product and industry codes become the ExioName labels of the `sector`
  header row, final-demand codes the `category` labels, both in
  classification order from io_utils.classification (exiobase_meta), the
  same table exio_incubator/definitions carries. Earlier versions wrote
  the codes and relied on the incubator to rename them; a rerun that
  skipped that step left the land account as the only one on the tree
  with codes, and every downstream reader matched its cells against the
  named core x as flows on zero output;
- ixi is `F_pxp @ T` with T the year's MarketShare matrix restricted to
  the agriculture and forestry industries (i01.*, i02). Land is a stock
  allocated to the industry that occupies it, not a flow that follows
  monetary secondary supply: the unrestricted market share put a share of
  a region's forest on whichever industry happened to sell forestry
  products (public administration, air transport, wood products). A
  product none of the land industries supplies in a region-year, or one
  the MarketShare file has no row for at all, falls back to its
  characteristic industry in the product-industry concordance, so no
  area is lost; every such region-product is printed;
- that matrix is then masked by the year's released ixi gross output
  (`raw/IOT_txt/IOT_<year>_ixi/x.txt`) through
  io_utils.extension_convert.zero_output, the mask every product-native
  account applies: an industry the core gave x = 0 receives nothing, the
  product's remaining industries take its area, and a product left with
  no industry keeps its concordance row (printed, area conserved). A year
  whose ixi x.txt is missing is refused before anything is written;
- files go through io_utils.extension_io, which checks the layout.

    python exiobase_land_extensions_final_format.py
    python exiobase_land_extensions_final_format.py --years 2019 --output-root <tmp>
    python rebuild_non_primary_forest.py --output <dir>/aggregation_per_year.xlsx
    python exiobase_land_extensions_final_format.py --source-xlsx <dir>/aggregation_per_year.xlsx

With no arguments it reads the tracked aggregation_per_year.xlsx and rewrites 1995-2023 on the EXIOBASE_3_12_0_r2 tree (3.12.0 release 2;
release 1, EXIOBASE_3_12_0, is frozen). `--release-root` is where MarketShare is read from and where the
default output goes; `--output-root` writes the pxp/ and ixi/ folders
elsewhere without touching the tree. The 2024-2028 tail is filled
afterwards with io_utils.extension_nowcast (`--ixi independent` holds
the 2023 ixi flat, so it carries this mask forward).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from exiobase_meta import read_exio3_classification
from io_utils.classification import (
    final_demand_layout,
    ind_multiindex,
    pro_multiindex,
    region_codes,
    sector_layout,
)
from io_utils.extension_convert.concordance import load_pi_concordance_mr
from io_utils.extension_convert.mask_overlay import apply_mask
from io_utils.extension_convert.zero_output import (
    mask_zero_output_columns,
    release_gross_output,
)
from io_utils.extension_io import write_extension_folder
from io_utils.sut.load_conversion_matrices import load_market_share

#: The tracked per-year workbook (renamed from aggregation_per_year_120626.xlsx
#: in ed55405). The release run passes its own with --source-xlsx.
SOURCE_XLSX = Path(__file__).parent / "aggregation_per_year.xlsx"
#: 3.12.0 release 2 (Richard 2026-11-10); release 1 (EXIOBASE_3_12_0) is frozen.
RELEASE_ROOT = Path("D:/indecol/Projects/MRIOs/EXIOBASE3/EXIOBASE_3_12_0_r2")
AXIS = "exiobase3"
EXTENSION = "land"
UNIT = "km2"
YEARS = range(1995, 2024)
#: ISIC divisions whose industries may carry land: 01 agriculture (every
#: i01 sub-industry, i01.w.1 and i01.w.2 included) and 02 forestry.
LAND_INDUSTRIES = ("i01", "i02")
#: Relative tolerance of the per-region mass check between pxp and ixi.
MASS_RTOL = 1e-9
#: Relative tolerance of the workbook total against what was laid out
#: (the check the script has always made).
LAYOUT_RTOL = 1e-3


def final_demand_codes() -> pd.MultiIndex:
    """(region, final-demand code) columns, as the workbook labels them.

    Position by position the same as `final_demand_layout`, which carries
    the names; io_utils exposes only the names for final demand.
    """
    fd = read_exio3_classification().tables["final_demand"]
    return pd.MultiIndex.from_product(
        [list(region_codes(AXIS)), fd.sort_values("Number")["CodeNr"].tolist()],
        names=["region", "category"],
    )


def year_frames(year: int, source: Path) -> tuple[pd.DataFrame, pd.DataFrame, float]:
    """pxp F on (region, product code), F_Y on (region, category name), workbook total.

    A workbook column with no EXIOBASE code is dropped by the reindexes,
    as it always was; any such column carrying area is printed.
    """
    exten = pd.read_excel(source, sheet_name=str(year), header=[0, 1], index_col=[0])
    F = exten.reindex(columns=pro_multiindex(AXIS)).fillna(0.0)
    F_Y = exten.reindex(columns=final_demand_codes()).fillna(0.0)
    F_Y.columns = final_demand_layout(AXIS)
    kept = set(map(tuple, F.columns)) | set(map(tuple, final_demand_codes()))
    dropped = [c for c in exten.columns if tuple(c) not in kept and exten[c].abs().sum() > 0]
    if dropped:
        print(f"  {year}: workbook columns without an EXIOBASE code dropped: "
              f"{[(c, float(exten[c].sum())) for c in dropped]}")
    return F, F_Y, float(exten.sum().sum())


def land_mask(like: pd.DataFrame) -> pd.DataFrame:
    """0/1 mask on `like`'s (region, product) x (region, industry) grid.

    Land is a stock allocated to the industry that occupies it. The
    market share spreads a product over every industry that sells it, so
    it would hand forest to public administration or air transport where
    those report secondary forestry output; only i01.* and i02 may
    receive land.
    """
    industries = like.columns.get_level_values("industry")
    allowed = np.array(
        [code.split(".")[0] in LAND_INDUSTRIES for code in industries], dtype=float
    )
    return pd.DataFrame(
        np.broadcast_to(allowed, like.shape).copy(), index=like.index, columns=like.columns
    )


def ixi_output_on_codes(release_root: Path, year: int) -> pd.Series:
    """Released ixi gross output of `year` on the (region, industry code)
    labels the transfer matrix carries.

    io_utils reads x.txt on the names the file carries; the release ixi
    layout and the code axis are aligned position by position, which is
    checked before the relabel. Raises FileNotFoundError naming the path
    when the core has not written the year.
    """
    x = release_gross_output(release_root, year, "ixi")
    if not x.index.equals(sector_layout(AXIS, "ixi")):
        raise ValueError(f"{year}: {x.name} is not in the release ixi layout order")
    return pd.Series(x.to_numpy(), index=ind_multiindex(AXIS), name=x.name)


def land_transfer(
    year: int, market_share_dir: Path, F: pd.DataFrame, x: pd.Series
) -> pd.DataFrame:
    """Row-stochastic (region, product) x (region, industry) matrix for `F_pxp @ T`.

    The year's market share under `land_mask`, rows renormalised. A row
    the mask empties (the product is supplied, but not by a land
    industry) is replaced by apply_mask with the product's characteristic
    industry from the concordance. A row with no supply at all stays
    empty under apply_mask and would lose its area (MarketShare_1995 has
    such rows), so those take the concordance as well. Every fallback row
    that carries land is printed.

    The result is then masked by `x`, the released ixi gross output on
    the code axis (`ixi_output_on_codes`): no share stays on an industry
    with x = 0, the product's other industries take it, and a product
    left with none takes its concordance row (which may itself be a
    zero-output industry: then the area stays there, conserved, and the
    product is printed).
    """
    D = load_market_share(year, market_share_dir)
    C = load_pi_concordance_mr()
    mask = land_mask(D)
    T = apply_mask(D, mask, fallback=C, label=f"{year} land mask").to_numpy(copy=True)
    supplied = D.to_numpy().sum(axis=1) > 0
    survived = (D.to_numpy() * mask.to_numpy()).sum(axis=1) > 0
    T[~survived] = C.to_numpy()[~survived]

    area = F.to_numpy().sum(axis=0)
    used = ~survived & (area > 0)
    if used.any():
        rows = pd.DataFrame({
            "area_km2": area[used],
            "reason": np.where(
                supplied[used], "no land industry supplies it", "no supply row"
            ),
        }, index=D.index[used])
        print(
            f"  {year}: {int(used.sum())} region-products with land took the "
            f"concordance fallback ({rows['reason'].value_counts().to_dict()}), "
            f"{rows['area_km2'].sum():.6g} km2"
        )
        print(rows.sort_values("area_km2", ascending=False).to_string())

    T_before = pd.DataFrame(T, index=D.index, columns=D.columns)
    T, report = mask_zero_output_columns(
        T_before, x, fallback=C, label=f"{year} land ixi x",
    )
    zero = x.reindex(T.columns).to_numpy() == 0
    on_zero_before = float((F.to_numpy() @ T_before.to_numpy()[:, zero]).sum())
    on_zero_after = float((F.to_numpy() @ T.to_numpy()[:, zero]).sum())
    del T_before
    print(f"  {year}: ixi x mask: {report.n_zero_columns} zero-output industries; "
          f"{len(report.rows_touched)} region-products had a share on one, "
          f"{len(report.rows_fallback)} of them nowhere else and keep their row; "
          f"area on zero-output industries {on_zero_before:.6g} km2 before the mask, "
          f"{on_zero_after:.6g} km2 after ({on_zero_before - on_zero_after:.6g} km2 moved)")
    kept = [p for p in report.rows_fallback if area[D.index.get_loc(p)] > 0]
    if kept:
        print(f"  {year}: {len(kept)} region-products with land stay on a "
              f"zero-output industry (no industry that could take them has "
              f"output): {kept}")
    return T


def check_region_mass(F: pd.DataFrame, F_ixi: pd.DataFrame, year: int) -> None:
    """Raise unless every region's area is the same in pxp and ixi, per stressor."""
    pxp = F.T.groupby(level="region", sort=False).sum().T
    ixi = F_ixi.T.groupby(level="region", sort=False).sum().T
    ixi = ixi.reindex(columns=pxp.columns)
    err = np.abs(ixi.to_numpy() - pxp.to_numpy())
    bad = err > MASS_RTOL * np.abs(pxp.to_numpy())
    if bad.any():
        where = pxp.where(bad).stack().index[:10].tolist()
        raise ValueError(f"{year}: ixi does not conserve the pxp area in {where}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--years", type=int, nargs="*", default=None)
    p.add_argument("--release-root", type=Path, default=RELEASE_ROOT)
    p.add_argument("--output-root", type=Path, default=None,
                   help="folder receiving pxp/<year> and ixi/<year>; "
                        "default <release-root>/raw/Extensions/land")
    p.add_argument("--source-xlsx", type=Path, default=SOURCE_XLSX,
                   help="per-year workbook (aggregation_region output, or "
                        "rebuild_non_primary_forest.py output); default "
                        f"{SOURCE_XLSX.name}")
    p.add_argument("--no-overwrite", dest="overwrite", action="store_false",
                   help="refuse to replace year folders that already exist")
    args = p.parse_args()

    out_root = args.output_root or args.release_root / "raw" / "Extensions" / EXTENSION
    market_share_dir = args.release_root / "raw" / "MarketShare"
    years = [y for y in YEARS if args.years is None or y in args.years]
    for year in years:
        print(f"Processing year: {year}")
        F, F_Y, total = year_frames(year, args.source_xlsx)
        laid_out = F.to_numpy().sum() + F_Y.to_numpy().sum()
        if not np.isclose(laid_out, total, rtol=LAYOUT_RTOL):
            raise ValueError(f"{year}: {total} in the workbook, {laid_out} laid out as pxp")

        x = ixi_output_on_codes(args.release_root, year)
        T = land_transfer(year, market_share_dir, F, x)
        F_ixi = F @ T
        del T
        check_region_mass(F, F_ixi, year)
        laid_out = F_ixi.to_numpy().sum() + F_Y.to_numpy().sum()
        if not np.isclose(laid_out, total, rtol=LAYOUT_RTOL):
            raise ValueError(f"{year}: {total} in the workbook, {laid_out} laid out as ixi")

        unit = pd.DataFrame({"unit": UNIT}, index=F.index)
        for system, frame in (("pxp", F), ("ixi", F_ixi)):
            write_extension_folder(
                out_root / system / str(year), EXTENSION, system,
                frame.set_axis(sector_layout(AXIS, system), axis=1), F_Y, unit,
                axis=AXIS, overwrite=args.overwrite,
            )
        print(f"{year}: F {F.to_numpy().sum():.6g} km2, F_Y {F_Y.to_numpy().sum():.6g} km2")


if __name__ == "__main__":
    main()
