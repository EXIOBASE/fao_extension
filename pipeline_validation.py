"""Validation checks for generated FAO pipeline tables."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd

from pipeline_config import require_year_columns


def validate_year_table(
    df: pd.DataFrame,
    *,
    years: Iterable[int],
    source: str,
    key_columns: Sequence[str] = (),
    require_non_negative: bool = True,
) -> None:
    year_cols = require_year_columns(df, years, source)

    missing_keys = [column for column in key_columns if column not in df.columns]
    if missing_keys:
        raise KeyError(f"{source} is missing key columns: {', '.join(missing_keys)}")

    if key_columns:
        duplicates = df.duplicated(list(key_columns))
        if duplicates.any():
            sample = df.loc[duplicates, list(key_columns)].head(5).to_dict("records")
            raise ValueError(f"{source} has duplicate key rows. Sample: {sample}")

    if require_non_negative:
        numeric_years = df[year_cols].apply(pd.to_numeric, errors="coerce")
        negative = numeric_years < 0
        if negative.any().any():
            rows, cols = negative.to_numpy().nonzero()
            examples = []
            for row_idx, col_idx in zip(rows[:5], cols[:5]):
                key = {
                    column: df.iloc[row_idx][column]
                    for column in key_columns
                    if column in df.columns
                }
                examples.append(
                    {
                        **key,
                        "year": year_cols[col_idx],
                        "value": numeric_years.iloc[row_idx, col_idx],
                    }
                )
            raise ValueError(f"{source} contains negative values. Sample: {examples}")


def validate_csv(
    path: Path,
    *,
    years: Iterable[int],
    key_columns: Sequence[str],
    require_non_negative: bool = True,
) -> None:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Expected output file not found: {path}")
    df = pd.read_csv(path, encoding="latin-1")
    validate_year_table(
        df,
        years=years,
        source=str(path),
        key_columns=key_columns,
        require_non_negative=require_non_negative,
    )


def validate_final_cropland_workbook(path: Path, *, years: Iterable[int]) -> None:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Expected allocation workbook not found: {path}")

    df = pd.read_excel(path, sheet_name="final cropland")
    validate_year_table(
        df,
        years=years,
        source=f"{path} [final cropland]",
        key_columns=[
            "ISO3",
            "EXIOBASE product code",
            "EXIOBASE extension name",
            "Unit",
        ],
    )

    labels = df["EXIOBASE extension name"]
    blank_labels = labels.isna() | labels.astype(str).str.strip().eq("")
    if blank_labels.any():
        sample = (
            df.loc[
                blank_labels,
                ["ISO3", "EXIOBASE product code", "EXIOBASE product", "Unit"],
            ]
            .head(5)
            .to_dict("records")
        )
        raise ValueError(
            f"{path} [final cropland] has blank EXIOBASE extension names. "
            f"Sample: {sample}"
        )
