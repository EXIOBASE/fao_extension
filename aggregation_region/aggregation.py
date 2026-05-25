from pathlib import Path
from typing import Iterable

import country_converter as coco
import pandas as pd


def table_aggregation(final_tables: Path, years: Iterable[int] | None = None):
    final_tables = Path(final_tables)
    xls = pd.ExcelFile(final_tables / "EXIOBASE_allocation_FAO.xlsx")
    df1 = pd.read_excel(xls, "final cropland")
    blank_extension = (
        df1["EXIOBASE extension name"].isna()
        | df1["EXIOBASE extension name"].astype(str).str.strip().eq("")
    )
    if blank_extension.any():
        sample = df1.loc[
            blank_extension,
            ["ISO3", "EXIOBASE product code", "EXIOBASE product", "Unit"],
        ].head(5).to_dict("records")
        raise ValueError(
            "EXIOBASE_allocation_FAO.xlsx [final cropland] has blank "
            f"EXIOBASE extension names. Sample: {sample}"
        )

    converter = coco.country_converter
    country_code = list(df1["ISO3"])
    df1.insert(1, "EXIO3", converter.convert(names=country_code, to="EXIO3"))

    year_cols = [col for col in df1.columns if str(col).startswith("Y")]
    if years is None:
        selected_year_cols = year_cols
    else:
        selected_year_cols = [f"Y{year}" for year in years]
        missing_years = [col for col in selected_year_cols if col not in year_cols]
        if missing_years:
            raise KeyError(
                "EXIOBASE_allocation_FAO.xlsx is missing requested year columns: "
                f"{', '.join(missing_years)}"
            )

    index_cols = [
        "EXIO3",
        "EXIOBASE product code",
        "EXIOBASE product",
        "EXIOBASE extension name",
    ]
    group = df1.groupby(index_cols, dropna=False)[selected_year_cols].sum()
    table_pivot = group.pivot_table(
        index="EXIOBASE extension name",
        columns=["EXIO3", "EXIOBASE product code"],
        fill_value=0,
    )

    output_file = final_tables / "aggregation_per_year_new.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        for year_col in selected_year_cols:
            table_pivot.loc[:, year_col].to_excel(
                writer, sheet_name=year_col.removeprefix("Y")
            )

    return output_file
