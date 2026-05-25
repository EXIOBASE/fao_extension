"""Run the FAO land-use extension pipeline.

The default settings match the historical local workflow, while command-line
options make the data folder, years, and in-development extension steps explicit.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from pipeline_config import normalize_years
from pipeline_validation import (
    validate_csv,
    validate_final_cropland_workbook,
    validate_year_table,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_DATAFOLDER = Path("d:/indecol/data/fao")
DEFAULT_STARTYEAR = 1961
DEFAULT_ENDYEAR = "latest"
LATEST_ENDYEAR = "latest"
YEAR_COLUMN_RE = re.compile(r"^Y(\d{4})$")


@dataclass(frozen=True)
class SourceSpec:
    name: str
    path: Path
    kind: str


@dataclass(frozen=True)
class SourceAvailability:
    name: str
    path: Path
    years: list[int]

    @property
    def first_year(self) -> int:
        return min(self.years)

    @property
    def last_year(self) -> int:
        return max(self.years)


def _configure_module_paths() -> None:
    """Keep legacy local imports working while modules are being packaged."""
    paths = [
        ROOT,
        ROOT / "download",
        ROOT / "raw_data_processing" / "land_use_calculation",
        ROOT / "aux_data",
        ROOT / "raw_data_processing" / "crop_livestock_production",
        ROOT / "processing_classification",
        ROOT / "aggregation_region",
        ROOT / "raw_data_processing" / "fishery_production",
        ROOT / "raw_data_processing" / "forestry_production",
        ROOT / "raw_data_processing" / "livestock_stocks",
    ]
    for path in reversed(paths):
        path_str = str(path)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-folder",
        type=Path,
        default=DEFAULT_DATAFOLDER,
        help=f"Folder containing download, data, and final_tables (default: {DEFAULT_DATAFOLDER}).",
    )
    parser.add_argument("--start-year", type=int, default=DEFAULT_STARTYEAR)
    parser.add_argument(
        "--end-year",
        type=_parse_end_year,
        default=DEFAULT_ENDYEAR,
        help=(
            "Last year to process, or 'latest' to use the newest year present "
            "in every selected source table (default: latest)."
        ),
    )
    parser.add_argument(
        "--refresh-downloads",
        action="store_true",
        help=(
            "Re-download source archives even when cached zips exist. Use this "
            "with --end-year latest to pick up FAO updates behind stable URLs."
        ),
    )
    parser.add_argument(
        "--fishstat-release",
        default="latest",
        help=(
            "FishStat release to download, e.g. 2026.1.0, or 'latest' to "
            "discover the newest matching Aquaculture/Capture release."
        ),
    )
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-landuse", action="store_true")
    parser.add_argument("--skip-crop-livestock", action="store_true")
    parser.add_argument("--skip-fishery", action="store_true")
    parser.add_argument("--skip-forestry", action="store_true")
    parser.add_argument("--skip-livestock-stocks", action="store_true")
    parser.add_argument("--skip-classification", action="store_true")
    parser.add_argument("--skip-aggregation", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    return parser.parse_args(argv)


def _parse_end_year(value: str) -> int | str:
    normalized = str(value).strip().lower()
    if normalized in {"latest", "auto"}:
        return LATEST_ENDYEAR
    try:
        return int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "--end-year must be an integer year or 'latest'"
        ) from exc


def _download_tasks(*, skip_fishery: bool, skip_forestry: bool) -> list[str]:
    tasks = ["landuse", "landcover", "crop_livestock", "value_production"]
    if not skip_forestry:
        tasks.append("forestry")
    if not skip_fishery:
        tasks.extend(["fishery_aquaculture", "fishery_capture"])
    return tasks


def _source_specs_for_pipeline(
    data_folder: Path,
    *,
    skip_landuse: bool,
    skip_crop_livestock: bool,
    skip_fishery: bool,
    skip_forestry: bool,
    skip_livestock_stocks: bool,
) -> list[SourceSpec]:
    data_path = data_folder / "data"
    specs: list[SourceSpec] = []
    if not skip_landuse:
        specs.extend(
            [
                SourceSpec(
                    "FAOSTAT land use",
                    data_path / "refreshed_land_use.csv",
                    "wide",
                ),
                SourceSpec(
                    "FAOSTAT land cover",
                    data_path / "refreshed_land_cover.csv",
                    "wide",
                ),
            ]
        )
    if not skip_crop_livestock or not skip_livestock_stocks:
        specs.append(
            SourceSpec(
                "FAOSTAT crops/livestock",
                data_path / "refreshed_crop_livestock.csv",
                "wide",
            )
        )
    if not skip_forestry:
        specs.append(
            SourceSpec(
                "FAOSTAT forestry",
                data_path / "refreshed_forestry.csv",
                "wide",
            )
        )
    if not skip_fishery:
        specs.extend(
            [
                SourceSpec(
                    "FishStat aquaculture",
                    data_path / "fishstat" / "Aquaculture_Quantity.csv",
                    "period",
                ),
                SourceSpec(
                    "FishStat capture",
                    data_path / "fishstat" / "Capture_Quantity.csv",
                    "period",
                ),
            ]
        )
    return specs


def _wide_csv_years(path: Path) -> list[int]:
    if not path.exists():
        raise FileNotFoundError(f"Expected source table not found: {path}")
    with path.open("r", encoding="latin-1", newline="") as fh:
        header = next(csv.reader(fh))
    years = sorted(
        {
            int(match.group(1))
            for column in header
            if (match := YEAR_COLUMN_RE.match(column))
        }
    )
    if not years:
        raise ValueError(f"{path} has no YYYYY year columns")
    return years


def _period_csv_years(path: Path) -> list[int]:
    if not path.exists():
        raise FileNotFoundError(f"Expected source table not found: {path}")

    import pandas as pd

    years: set[int] = set()
    for chunk in pd.read_csv(path, usecols=["PERIOD"], chunksize=250_000):
        periods = pd.to_numeric(chunk["PERIOD"], errors="coerce").dropna()
        years.update(periods.astype(int).tolist())
    if not years:
        raise ValueError(f"{path} has no usable PERIOD years")
    return sorted(years)


def _availability_for_spec(spec: SourceSpec) -> SourceAvailability:
    if spec.kind == "wide":
        years = _wide_csv_years(spec.path)
    elif spec.kind == "period":
        years = _period_csv_years(spec.path)
    else:
        raise ValueError(f"Unknown source availability kind: {spec.kind}")
    return SourceAvailability(name=spec.name, path=spec.path, years=years)


def _year_span(years: list[int]) -> str:
    first_year, last_year = min(years), max(years)
    expected_count = last_year - first_year + 1
    if len(years) == expected_count:
        return f"{first_year}-{last_year}"
    return f"{first_year}-{last_year} ({len(years)} reported years)"


def _resolve_latest_full_year(specs: list[SourceSpec]) -> tuple[int, list[SourceAvailability]]:
    if not specs:
        raise ValueError(
            "Cannot resolve --end-year latest because all source-producing "
            "steps were skipped. Provide --end-year explicitly."
        )
    availability = [_availability_for_spec(spec) for spec in specs]
    common_years = set(availability[0].years)
    for source in availability[1:]:
        common_years &= set(source.years)
    if not common_years:
        names = ", ".join(source.name for source in availability)
        raise ValueError(f"No common available years across selected sources: {names}")
    return max(common_years), availability


def _print_availability_report(
    *,
    latest_year: int,
    availability: list[SourceAvailability],
) -> None:
    print("source year availability (full means the year exists in every selected source)")
    for source in availability:
        print(f"  - {source.name}: {_year_span(source.years)}")
    limiting_sources = [
        source.name for source in availability if source.last_year == latest_year
    ]
    if limiting_sources:
        limited_by = "; limited by " + ", ".join(limiting_sources)
    else:
        limited_by = ""
    print(f"last available year with full selected-source data: {latest_year}{limited_by}")


def _print_download_info(download_info: dict | None) -> None:
    if not download_info:
        return
    fishstat_release = download_info.get("fishstat_release")
    if fishstat_release:
        print(f"FishStat release: {fishstat_release}")


def run_pipeline(
    *,
    data_folder: Path,
    years: Iterable[int],
    refresh_downloads: bool = False,
    fishstat_release: str = "latest",
    skip_download: bool = False,
    skip_landuse: bool = False,
    skip_crop_livestock: bool = False,
    skip_fishery: bool = False,
    skip_forestry: bool = False,
    skip_livestock_stocks: bool = False,
    skip_classification: bool = False,
    skip_aggregation: bool = False,
    skip_validation: bool = False,
) -> None:
    _configure_module_paths()

    years = normalize_years(years)
    data_folder.mkdir(exist_ok=True, parents=True)
    final_path = data_folder / "final_tables"
    final_path.mkdir(exist_ok=True, parents=True)

    if not skip_download:
        import download.main as download_main

        print("download files")
        download_info = download_main.get_all(
            years=years,
            storage_path=data_folder,
            tasks=_download_tasks(
                skip_fishery=skip_fishery,
                skip_forestry=skip_forestry,
            ),
            force_download=refresh_downloads,
            fishstat_release=fishstat_release,
        )
        _print_download_info(download_info)

    if not skip_landuse:
        from raw_data_processing.land_use_calculation import landuse as landuse_module

        print("processing the raw data related to landuse")
        landuse = landuse_module.whole_landuse_calculation(
            years=years, storage_path=data_folder
        )
        if not skip_validation:
            validate_year_table(
                landuse,
                years=years,
                source="landuse_final_runall",
                key_columns=["ISO3", "Item Code", "Item", "Unit"],
            )
        landuse.to_csv(final_path / "landuse_final_runall.csv", index=False)

    if not skip_crop_livestock:
        from raw_data_processing.crop_livestock_production import (
            crop_livestock as crop_livestock_module,
        )

        print("processing the raw data related to crop and livestock")
        crop_livestock_module.whole_production_calculation(
            years=years, storage_path=data_folder
        )
        if not skip_validation:
            for name in [
                "final_crops_primary.csv",
                "final_livestock_primary.csv",
                "final_crops_processed.csv",
                "final_livestock_processed.csv",
                "final_live_animal.csv",
            ]:
                validate_csv(
                    final_path / name,
                    years=years,
                    key_columns=["ISO3", "Item Code", "Item", "Unit"],
                )

    if not skip_fishery:
        from raw_data_processing.fishery_production import fishery as fishery_module

        print("processing the raw data related to fishery (FishStat)")
        try:
            fishery = fishery_module.whole_fishery_calculation(
                years=years, storage_path=data_folder
            )
            if not skip_validation:
                validate_year_table(
                    fishery,
                    years=years,
                    source="fishery_final_runall",
                    key_columns=[
                        "ISO3",
                        "EXIOBASE product code",
                        "EXIOBASE sub-product",
                        "source_category",
                        "Unit",
                    ],
                )
            fishery.to_csv(final_path / "fishery_final_runall.csv", index=False)
        except FileNotFoundError as exc:
            print(
                f"  -> skipping fishery step ({exc}). "
                f"Run the download step or check {data_folder / 'data'}."
            )

    if not skip_forestry:
        from raw_data_processing.forestry_production import forestry as forestry_module

        print("processing the raw data related to forestry (FAOSTAT FO)")
        try:
            forestry = forestry_module.whole_forestry_calculation(
                years=years, storage_path=data_folder
            )
            if not skip_validation:
                validate_year_table(
                    forestry,
                    years=years,
                    source="forestry_final_runall",
                    key_columns=[
                        "ISO3",
                        "EXIOBASE product code",
                        "EXIOBASE sub-product",
                        "Unit",
                    ],
                )
            forestry.to_csv(final_path / "forestry_final_runall.csv", index=False)
        except FileNotFoundError as exc:
            print(
                f"  -> skipping forestry step ({exc}). "
                f"Run the download step or check {data_folder / 'data'}."
            )

    if not skip_livestock_stocks:
        from raw_data_processing.livestock_stocks import (
            livestock_stocks as livestock_stocks_module,
        )

        print("processing FAOSTAT livestock stocks (head counts)")
        try:
            stocks = livestock_stocks_module.whole_livestock_stocks_calculation(
                years=years, storage_path=data_folder
            )
            if not skip_validation:
                validate_year_table(
                    stocks,
                    years=years,
                    source="livestock_stocks_runall",
                    key_columns=["ISO3", "water_species", "Unit"],
                )
            stocks.to_csv(final_path / "livestock_stocks_runall.csv", index=False)
        except FileNotFoundError as exc:
            print(
                f"  -> skipping livestock_stocks step ({exc}). "
                f"Run the crop_livestock download/processing first."
            )

    if not skip_classification:
        import processing_classification.landuse_calculation as classification_module

        print("processing classification of data (crop and livestock, primary and processed)")
        classification_module.landuse_allocation(years=years, storage_path=data_folder)
        if not skip_validation:
            validate_final_cropland_workbook(
                final_path / "EXIOBASE_allocation_FAO.xlsx", years=years
            )

    if not skip_aggregation:
        import aggregation_region.aggregation as aggregation_module

        print("aggregation EXIO regions, EXIO product code")
        aggregation_module.table_aggregation(final_tables=final_path, years=years)


def main(argv: Sequence[str] | None = None) -> None:
    args = _parse_args(argv)
    end_year = args.end_year
    download_already_done = False

    if end_year == LATEST_ENDYEAR:
        if not args.skip_download:
            _configure_module_paths()
            import download.main as download_main

            print("download files")
            if not args.refresh_downloads:
                print(
                    "  -> using cached source zips where present; pass "
                    "--refresh-downloads to force a fresh FAO check"
                )
            download_info = download_main.get_all(
                years=None,
                storage_path=args.data_folder,
                tasks=_download_tasks(
                    skip_fishery=args.skip_fishery,
                    skip_forestry=args.skip_forestry,
                ),
                force_download=args.refresh_downloads,
                fishstat_release=args.fishstat_release,
            )
            _print_download_info(download_info)
            download_already_done = True

        latest_year, availability = _resolve_latest_full_year(
            _source_specs_for_pipeline(
                args.data_folder,
                skip_landuse=args.skip_landuse,
                skip_crop_livestock=args.skip_crop_livestock,
                skip_fishery=args.skip_fishery,
                skip_forestry=args.skip_forestry,
                skip_livestock_stocks=args.skip_livestock_stocks,
            )
        )
        _print_availability_report(
            latest_year=latest_year,
            availability=availability,
        )
        end_year = latest_year

    if end_year < args.start_year:
        raise ValueError("--end-year must be greater than or equal to --start-year")

    run_pipeline(
        data_folder=args.data_folder,
        years=range(args.start_year, end_year + 1),
        refresh_downloads=args.refresh_downloads,
        fishstat_release=args.fishstat_release,
        skip_download=args.skip_download or download_already_done,
        skip_landuse=args.skip_landuse,
        skip_crop_livestock=args.skip_crop_livestock,
        skip_fishery=args.skip_fishery,
        skip_forestry=args.skip_forestry,
        skip_livestock_stocks=args.skip_livestock_stocks,
        skip_classification=args.skip_classification,
        skip_aggregation=args.skip_aggregation,
        skip_validation=args.skip_validation,
    )


if __name__ == "__main__":
    main()
