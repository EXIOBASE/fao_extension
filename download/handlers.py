from pathlib import Path
import zipfile
import pandas as pd
import requests
from typing import List, Union
import country_converter as coco
#from pathlib import Path


def make_valid_fao_year(year):
    """Return valid fao year(s)

    This works on lists or single str/int
    and is robust for repetetive calls (calling on 'Y1932' will return 'Y1932')
    on single values and lists
    """

    def make_single_year(single_year):
        if type(single_year) is str:
            if single_year[0] == "Y":
                return single_year
            else:
                return "Y" + single_year
        else:
            return "Y" + str(single_year)

    if type(year) in (str, int):
        return make_single_year(year)
    else:
        return [make_single_year(y) for y in year]


def get_missing_data(df):
    """Make a summary table with all missing data

    Any row with a nan is included in the resulting table

    fao_df: pandas DataFrame
        Based on raw csv read

    """
    return df[df.isnull().any(1)]


def extract_archive(zip_archive, store_to):
    """Extract zip archive (pathlib.Path) to store_to (pathlib.Path)"""
    with zipfile.ZipFile(zip_archive, "r") as zf:
        zf.extractall(path=store_to)


def download_fao_data(src_url, storage_path, force_download=False):
    """Store the fao dataset at storage path

    Parameters
    ----------

    src_url: str
        Url of the source data

    storage_path: pathlib.Path
        Location for storing the data

    force_download: boolean, optional
        If True, downloads the data even if it is already present in storage_path.
        If False (default), only downloads the data if is is not available locally.

    Returns
    -------
        Downloaded File: pathlib.Path

    """
    filename = Path(src_url.split("/")[-1])

    # Making the storage path if should not exisit
    storage_path.mkdir(parents=True, exist_ok=True)
    storage_file = storage_path / filename
    if storage_file.exists() and (force_download is False):
        return storage_file

    download = requests.get(src_url)

    # Raise exception if the file is not available
    download.raise_for_status()
    with open(storage_file, "wb") as sf:
        sf.write(download.content)

    return storage_file


def read_land_data(data_file: Path, relevant_years: list = None):
    """Reads the data and returns dataframe

    Parameter
    ----------

    data_file: pathlib.Path
        Extracted fao csv file

    relevant_years: list
        Years to process

    """

    df = pd.read_csv(data_file, encoding="latin-1")

    if relevant_years:

        country_code = list(df["Area Code"])
        converter = coco.country_converter

        '''
        Remove from the df all "Area Code" which arenot of interest
        '''
        cc = coco.CountryConverter()
        unique_FAO_code = cc.FAOcode['FAOcode'].astype('int64').to_list()

        df=df[df['Area Code'].isin(unique_FAO_code)]
        country_code = list(df["Area Code"])

        df["ISO3"] = converter.convert(names=country_code, src="FAOcode", to="ISO3")

        meta_col = [
            col
            for col in df.columns
            if not col.startswith(("Y", "key", "Element", "Area"))
        ]

        return df[meta_col + make_valid_fao_year(relevant_years)]

    else:
        return df




def get_landuse(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
):
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """
    land_zip = download_fao_data(src_url=src_url, storage_path=download_path)
    extract_archive(zip_archive=land_zip, store_to=data_path)

    land_all = read_land_data(data_path / csv_name, relevant_years=relevant_years)   
    land_all = land_all[land_all['ISO3'] != 'not found']
    land_all.to_csv(data_path / "refreshed_land_use.csv", index=False)



def get_landcover(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
):
    
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """
    land_zip = download_fao_data(src_url=src_url, storage_path=download_path)

    extract_archive(zip_archive=land_zip, store_to=data_path)
    relevant_years = relevant_years[relevant_years.index(1991)+1:]

    land_cover_all = pd.read_csv(data_path / csv_name, encoding="latin-1")

    country_code = list(land_cover_all["Area Code"])
    converter = coco.country_converter


    cc = coco.CountryConverter()
    unique_FAO_code = cc.FAOcode['FAOcode'].astype('int64').to_list()

    land_cover_all=land_cover_all[land_cover_all['Area Code'].isin(unique_FAO_code)]
    country_code = list(land_cover_all["Area Code"])


    land_cover_all["ISO3"] = converter.convert(names=country_code, src="FAOcode", to="ISO3")

    meta_col = [
        col
        for col in land_cover_all.columns
        if not col.startswith(("Y", "key", "Area"))
        ]
    land_cover_all = land_cover_all[meta_col + make_valid_fao_year(relevant_years)]

    col_year = [
        col
        for col in land_cover_all.columns
        if  col.startswith(("Y"))
    ]
    
    
    units= land_cover_all['Unit'].unique()

    if len(units)==1:
        
        if units[0]=='1000 ha':
            land_cover_all[col_year]=(land_cover_all[col_year]/10)
            
            land_cover_all['Unit']='km2'
    
    land_cover_all = land_cover_all[land_cover_all['ISO3'] != 'not found']
    land_cover_all.to_csv(data_path / "refreshed_land_cover.csv", index=False)

                                

def get_crop_livestock(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
):
    
    
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """

    crop_livestock_zip = download_fao_data(src_url=src_url, storage_path=download_path)
    extract_archive(zip_archive=crop_livestock_zip, store_to=data_path)

    crop_livestock_all = read_land_data(data_path / csv_name, relevant_years=relevant_years)
    crop_livestock_all = crop_livestock_all[crop_livestock_all['ISO3'] != 'not found']
    crop_livestock_all.to_csv(data_path / "refreshed_crop_livestock.csv", index=False)

