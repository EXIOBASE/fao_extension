from pathlib import Path
from typing import List, Union
import logging
import handlers



DOWNLOAD_TASKS = dict(
    landuse=dict(
        para=dict(
            src_url="http://fenixservices.fao.org/faostat/static/bulkdownloads/Inputs_LandUse_E_All_Data.zip",
            csv_name=Path("Inputs_LandUse_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_landuse,
    ),
    
    landcover=dict(
        para=dict(
            src_url="https://bulks-faostat.fao.org/production/Environment_LandCover_E_All_Data.zip",
            csv_name=Path("Environment_LandCover_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_landcover,
    ),
    
    crop_livestock=dict(
        para=dict(
            src_url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data.zip",
            csv_name = Path("Production_Crops_Livestock_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_crop_livestock,
    )    ,
    
    value_production=dict(
        para=dict(
            src_url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Value_of_Production_E_All_Data.zip",
            csv_name = Path("Value_of_Production_E_All_Data.csv"),
        ),
        processor=handlers.get_value_production,
    )
    
)


PARAMETERS_YAML = Path(__file__).resolve().parents[1] / "aux_data" / "parameters.yaml"


def configured_years(parameters_file: Path = PARAMETERS_YAML) -> range:
    """Years of interest from aux_data/parameters.yaml (year_of_interest).

    This is the one place the last year is set: steps 3 and 4
    (crop_livestock.py, value_production.py, landuse_calculation.py) read
    the same key, so the downloaded tables must not carry years past it.
    """
    import yaml

    with open(parameters_file) as file:
        window = yaml.safe_load(file)["year_of_interest"]
    return range(int(window["begin"]), int(window["end"]) + 1)


def get_all(years: List[int], storage_path: Path):
    """Download and process all FAO data

    Every task keeps the years in ``years`` (run_all passes the window of
    aux_data/parameters.yaml). Before 3.12.0 release 2 crop_livestock and
    value_production kept 1961-2024 while the later steps stop at the
    configured end year, which made step 3 fail with KeyError 'Y2024'.
    """
    years = list(years)

    download_path = Path(storage_path / "download")
    download_path.mkdir(exist_ok=True, parents=True)

    data_path = Path(storage_path / "data")
    data_path.mkdir(exist_ok=True, parents=True)

    for taskname, task in DOWNLOAD_TASKS.items():
        print(taskname)

        logging.info(f"Processing {taskname}")
        task["processor"](
            relevant_years=years,
            download_path=download_path,
            data_path=data_path,
            **task["para"]
        )
