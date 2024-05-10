from pathlib import Path
from typing import List, Union
# import landuse_download as lud
# import prodcrop_download as pcd
# import prodlivestock_download as pld
import logging
import handlers


# TODO CD: LANDUSE IS DONE, ALSO PUT THE OTHERS IN THE DICT BELOW
# src_landuse = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Inputs_LandUse_E_All_Data.zip"
# csv_name_landuse = Path("Inputs_LandUse_E_All_Data_NOFLAG.csv")

# src_prod_crops = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_E_All_Data.zip"
# csv_name_prod_crops = Path("Production_Crops_E_All_Data.csv")

# src_prod_lifestock = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Production_LivestockPrimary_E_All_Data.zip"
# csv_name_prod_lifestock = Path("Production_LivestockPrimary_E_All_Data.csv")

DOWNLOAD_TASKS = dict(
    landuse=dict(
        para=dict(
            src_url="http://fenixservices.fao.org/faostat/static/bulkdownloads/Inputs_LandUse_E_All_Data.zip",
            csv_name=Path("Inputs_LandUse_E_All_Data_NOFLAG.csv"),
        ),
        processor=handlers.get_landuse,
    ),
    
    crop_livestock=dict(
        para=dict(
            src_url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data.zip",
            csv_name = Path("Production_Crops_Livestock_E_All_Data.csv"),
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

# THIS IS JUST FOR DEBUGING
# storage_path = Path("/home/konstans/tmp/fao_test")
# storage_path.mkdir(exist_ok=True)
# years = [2000, 2001]
# get_all(years=years, storage_path=storage_path)
