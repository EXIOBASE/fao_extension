# -*- coding: utf-8 -*-
"""FAO FishStat fishery production processing.

Mirrors the ``crop_livestock_production`` module: produces a tidy long
table with one row per (ISO3, EXIOBASE product code, EXIOBASE
sub-product, source_category, year) and a Quantity (tonnes) column.

Data source
-----------

FAO bulk download at https://www.fao.org/fishery/static/Data/. The
directory listing publishes annual release zips with stable naming:

    Aquaculture_<release>.zip
    Capture_<release>.zip

Each zip contains the production CSV plus the matching reference
tables (species, country, water-area, environment). This is the
authoritative FAO source - the same data the FishStatJ desktop tool
and the fishstat R package on CRAN consume. The FAO directory pattern
has been stable since the 2017 release.

For full pipeline runs, ``download.main`` can discover the latest
matching Aquaculture/Capture release before processing. ``fishstat_release``
in ``parameters.yaml`` is retained as documentation/fallback for direct
module use.

Inputs (fetched and unpacked by ``download/handlers.get_fishery_production``):

    <storage_path>/data/fishstat/Aquaculture_Quantity.csv
    <storage_path>/data/fishstat/Capture_Quantity.csv
    <storage_path>/data/fishstat/CL_FI_SPECIES_GROUPS.csv
    <storage_path>/data/fishstat/CL_FI_COUNTRY_GROUPS.csv
    <storage_path>/data/fishstat/CL_FI_PRODENVIRONMENT.csv
    <storage_path>/data/fishstat/CL_FI_WATERAREA_GROUPS.csv

Output
------

pandas.DataFrame with columns

    ISO3, EXIOBASE product code (=p05), EXIOBASE product,
    EXIOBASE sub-product, source_category, Unit (=t),
    Y1995, Y1996, ... YYYYY

The ``source_category`` column carries the freshwater-relevance flag:
    aquaculture inland   - inland freshwater aquaculture
    aquaculture brackish - coastal/brackish aquaculture
    aquaculture marine   - marine aquaculture
    capture inland       - inland capture fisheries (rivers, lakes)
    capture marine       - marine capture fisheries
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import yaml


# ---------------------------------------------------------------------------
# ISSCAAP group name -> EXIOBASE sub-product mapping
# ---------------------------------------------------------------------------

ISSCAAP_TO_SUBPRODUCT: dict[str, str] = {
    # Freshwater + diadromous finfish
    "Carps, barbels and other cyprinids":   "inland fish",
    "Tilapias and other cichlids":          "inland fish",
    "Miscellaneous freshwater fishes":      "inland fish",
    "Sturgeons, paddlefishes":              "inland fish",
    "River eels":                           "inland fish",
    "Salmons, trouts, smelts":              "inland fish",
    "Shads":                                "inland fish",
    "Miscellaneous diadromous fishes":      "inland fish",
    # Marine finfish
    "Flounders, halibuts, soles":           "marine fish",
    "Cods, hakes, haddocks":                "marine fish",
    "Miscellaneous coastal fishes":         "marine fish",
    "Miscellaneous demersal fishes":        "marine fish",
    "Herrings, sardines, anchovies":        "marine fish",
    "Tunas, bonitos, billfishes":           "marine fish",
    "Miscellaneous pelagic fishes":         "marine fish",
    "Sharks, rays, chimaeras":              "marine fish",
    "Marine fishes not identified":         "marine fish",
    # Crustaceans
    "Freshwater crustaceans":               "crustaceans",
    "Crabs, sea-spiders":                   "crustaceans",
    "Lobsters, spiny-rock lobsters":        "crustaceans",
    "King crabs, squat-lobsters":           "crustaceans",
    "Shrimps, prawns":                      "crustaceans",
    "Krill, planktonic crustaceans":        "crustaceans",
    "Miscellaneous marine crustaceans":     "crustaceans",
    "Horseshoe crabs and other arachnoids": "crustaceans",
    # Molluscs
    "Freshwater molluscs":                  "molluscs",
    "Abalones, winkles, conchs":            "molluscs",
    "Oysters":                              "molluscs",
    "Mussels":                              "molluscs",
    "Scallops, pectens":                    "molluscs",
    "Clams, cockles, arkshells":            "molluscs",
    "Squids, cuttlefishes, octopuses":      "molluscs",
    "Miscellaneous marine molluscs":        "molluscs",
    # Other aquatic animals + plants
    "Blue-whales, fin-whales":              "other aquatic",
    "Sperm-whales, pilot-whales":           "other aquatic",
    "Eared seals, hair seals, walruses":    "other aquatic",
    "Miscellaneous aquatic mammals":        "other aquatic",
    "Turtles":                              "other aquatic",
    "Crocodiles and alligators":            "other aquatic",
    "Frogs and other amphibians":           "other aquatic",
    "Sea-urchins and other echinoderms":    "other aquatic",
    "Sea-squirts and other tunicates":      "other aquatic",
    "Miscellaneous aquatic invertebrates":  "other aquatic",
    "Sponges":                              "other aquatic",
    "Corals":                               "other aquatic",
    "Pearls, mother-of-pearl, shells":      "other aquatic",
    "Brown seaweeds":                       "other aquatic",
    "Red seaweeds":                         "other aquatic",
    "Green seaweeds":                       "other aquatic",
    "Miscellaneous aquatic plants":         "other aquatic",
}


# Aquaculture environment code -> source_category
ENVIRONMENT_TO_CATEGORY: dict[str, str] = {
    "IN": "aquaculture inland",
    "BW": "aquaculture brackish",
    "MA": "aquaculture marine",
    "AL": "aquaculture marine",
}


# Mass measure codes (live weight tonnes). The MEASURE column also
# carries effort and value codes; we drop those here.
MASS_MEASURES = {"Q_tlw", "Q_t", "Q_t_1"}


def _make_valid_fao_year(year: int) -> str:
    return f"Y{int(year)}"


def whole_fishery_calculation(
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

    fao_root = data_path / params["fishstat_data_subdir"]
    aquaculture_csv = fao_root / params["fishstat_aquaculture_quantity"]
    capture_csv = fao_root / params["fishstat_capture_quantity"]
    species_csv = fao_root / params["fishstat_species_groups"]
    country_csv = fao_root / params["fishstat_country_groups"]
    waterarea_csv = fao_root / params["fishstat_waterarea"]

    for path in (aquaculture_csv, capture_csv, species_csv, country_csv, waterarea_csv):
        if not path.exists():
            raise FileNotFoundError(
                f"Expected FishStat input not found: {path}. "
                f"Drop the FAO Aquaculture_<release>.zip and Capture_<release>.zip "
                f"into <storage_path>/download/ and let the download handler "
                f"unpack them, or unpack manually into {fao_root}."
            )

    yrs = list(years)
    year_min, year_max = min(yrs), max(yrs)

    # ---- Reference tables ----------------------------------------------
    species = pd.read_csv(species_csv, encoding="utf-8")
    species = species[["3A_Code", "ISSCAAP_Group_En"]].rename(
        columns={"3A_Code": "species", "ISSCAAP_Group_En": "isscaap"}
    )
    species["isscaap"] = species["isscaap"].astype(str).str.strip()
    species["sub_product"] = species["isscaap"].map(ISSCAAP_TO_SUBPRODUCT).fillna("other aquatic")

    country = pd.read_csv(country_csv, encoding="utf-8", dtype=str)
    cols = {c.lower(): c for c in country.columns}
    un_col = cols.get("un_code") or cols.get("country.un_code") or cols.get("code")
    iso3_col = cols.get("iso3_code") or cols.get("iso3")
    if un_col is None or iso3_col is None:
        raise ValueError(
            f"Country file {country_csv} missing UN_Code or ISO3_Code; "
            f"got columns: {list(country.columns)}"
        )
    country = country[[un_col, iso3_col]].rename(columns={un_col: "country_un", iso3_col: "ISO3"})
    country["country_un"] = country["country_un"].astype(str).str.zfill(3)

    waterarea = pd.read_csv(waterarea_csv, encoding="utf-8", dtype=str)
    wcols = {c.lower(): c for c in waterarea.columns}
    waterarea = waterarea[[wcols["code"], wcols["inlandmarine_group_en"]]].rename(
        columns={wcols["code"]: "area_code",
                 wcols["inlandmarine_group_en"]: "inland_marine"}
    )
    waterarea["area_code"] = waterarea["area_code"].astype(str).str.zfill(2)
    waterarea["is_inland"] = (
        waterarea["inland_marine"].astype(str).str.contains("Inland", case=False, na=False)
    )

    # ---- Aquaculture ---------------------------------------------------
    aq = pd.read_csv(aquaculture_csv, encoding="utf-8", dtype=str)
    aq.columns = [c.upper().replace(".", "_") for c in aq.columns]
    aq = aq.rename(columns={
        "COUNTRY_UN_CODE": "country_un",
        "SPECIES_ALPHA_3_CODE": "species",
        "ENVIRONMENT_ALPHA_2_CODE": "environment",
    })
    aq["country_un"] = aq["country_un"].astype(str).str.zfill(3)
    aq["VALUE"] = pd.to_numeric(aq["VALUE"], errors="coerce").fillna(0.0)
    aq["PERIOD"] = pd.to_numeric(aq["PERIOD"], errors="coerce").astype("Int64")
    aq = aq[aq["MEASURE"].isin(MASS_MEASURES)]
    aq = aq[aq["PERIOD"].between(year_min, year_max)]
    aq["source_category"] = aq["environment"].map(ENVIRONMENT_TO_CATEGORY).fillna("aquaculture marine")
    aq = aq[["country_un", "species", "PERIOD", "VALUE", "source_category"]].rename(
        columns={"PERIOD": "year", "VALUE": "value"}
    )

    # ---- Capture -------------------------------------------------------
    cap = pd.read_csv(capture_csv, encoding="utf-8", dtype=str)
    cap.columns = [c.upper().replace(".", "_") for c in cap.columns]
    cap = cap.rename(columns={
        "COUNTRY_UN_CODE": "country_un",
        "SPECIES_ALPHA_3_CODE": "species",
        "AREA_CODE": "area_code",
    })
    cap["country_un"] = cap["country_un"].astype(str).str.zfill(3)
    cap["area_code"] = cap["area_code"].astype(str).str.zfill(2)
    cap["VALUE"] = pd.to_numeric(cap["VALUE"], errors="coerce").fillna(0.0)
    cap["PERIOD"] = pd.to_numeric(cap["PERIOD"], errors="coerce").astype("Int64")
    cap = cap[cap["MEASURE"].isin(MASS_MEASURES)]
    cap = cap[cap["PERIOD"].between(year_min, year_max)]
    cap = cap.merge(waterarea[["area_code", "is_inland"]], on="area_code", how="left")
    cap["source_category"] = cap["is_inland"].map(
        {True: "capture inland", False: "capture marine"}
    ).fillna("capture marine")
    cap = cap[["country_un", "species", "PERIOD", "VALUE", "source_category"]].rename(
        columns={"PERIOD": "year", "VALUE": "value"}
    )

    # ---- Combine, attach ISO3 and sub_product --------------------------
    long = pd.concat([aq, cap], ignore_index=True)
    long = long.merge(country, on="country_un", how="left")
    long = long.merge(species[["species", "sub_product"]], on="species", how="left")
    long = long.dropna(subset=["ISO3"]).copy()
    long = long[long["ISO3"].isin(country_filter)]
    long["sub_product"] = long["sub_product"].fillna("other aquatic")

    agg = (long.groupby(["ISO3", "sub_product", "source_category", "year"],
                        as_index=False)["value"].sum())

    wide = agg.pivot_table(
        index=["ISO3", "sub_product", "source_category"],
        columns="year", values="value", aggfunc="sum", fill_value=0.0,
    ).reset_index()
    wide.columns = [
        _make_valid_fao_year(int(c))
        if isinstance(c, (int, float)) and not pd.isna(c) else c
        for c in wide.columns
    ]

    wide.insert(1, "EXIOBASE product code", "p05")
    wide.insert(2, "EXIOBASE product", "Fish and other fishing products")
    wide = wide.rename(columns={"sub_product": "EXIOBASE sub-product"})
    wide["Unit"] = "t"

    front = ["ISO3", "EXIOBASE product code", "EXIOBASE product",
             "EXIOBASE sub-product", "source_category", "Unit"]
    year_cols = sorted(c for c in wide.columns
                       if isinstance(c, str) and c.startswith("Y") and c[1:].isdigit())
    return wide[front + year_cols]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--storage-path", type=Path, required=True)
    parser.add_argument("--start-year", type=int, default=1995)
    parser.add_argument("--end-year", type=int, default=2022)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    df = whole_fishery_calculation(
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
