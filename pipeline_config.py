"""Shared year-window helpers for the FAO pipeline."""

from __future__ import annotations

from copy import deepcopy
from typing import Iterable

import pandas as pd


def normalize_years(years: Iterable[int]) -> list[int]:
    normalized = sorted({int(year) for year in years})
    if not normalized:
        raise ValueError("At least one processing year is required")
    return normalized


def year_columns(years: Iterable[int]) -> list[str]:
    return [f"Y{year}" for year in normalize_years(years)]


def apply_year_window(parameters: dict, years: Iterable[int]) -> dict:
    """Return parameters with year ranges clipped to the requested years."""
    years = normalize_years(years)
    start_year, end_year = min(years), max(years)
    clipped = deepcopy(parameters)
    clipped.setdefault("year_of_interest", {})
    clipped["year_of_interest"]["begin"] = start_year
    clipped["year_of_interest"]["end"] = end_year

    exceptions = clipped.get("exeptions") or {}
    for exception in exceptions.values():
        if not isinstance(exception, dict):
            continue
        exception["begin"] = max(int(exception.get("begin", start_year)), start_year)
        exception["end"] = min(int(exception.get("end", end_year)), end_year)
    return clipped


def require_year_columns(df: pd.DataFrame, years: Iterable[int], source: str) -> list[str]:
    columns = year_columns(years)
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise KeyError(
            f"{source} is missing requested year columns: {', '.join(missing)}"
        )
    return columns
