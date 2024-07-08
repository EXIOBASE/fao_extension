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
    )
)


def get_all(years: List[int], storage_path: Path):
    """Download and process all FAO data

    Parameter
    ---------
    years: list[int],
        all years to process

    storage_path: pathlib.Path
        Location for storing the data

    """
    download_path = Path(storage_path / "download")
    download_path.mkdir(exist_ok=True, parents=True)
    data_path = Path(storage_path / "data")
    data_path.mkdir(exist_ok=True, parents=True)

    for taskname, task in DOWNLOAD_TASKS.items():
        logging.info(f"Processing {taskname}")
        task["processor"](
            relevant_years=years,
            download_path=download_path,
            data_path=data_path,
            **task["para"]
        )


