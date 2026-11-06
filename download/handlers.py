from pathlib import Path
import zipfile
import pandas as pd
import requests
from typing import List, Union
import country_converter as coco
#from pathlib import Path

#: FAOSTAT area codes country_converter (1.3.2) has no FAOcode for. Sudan is
#: 206 "Sudan (former)" for 1961-2011 (South Sudan included) and 276 "Sudan"
#: from 2012; no year carries both, so both map to SDN and their rows are
#: merged into one series (see `fao_area_to_iso3`, `merge_patched_rows`).
FAO_CODE_PATCH = {206: "SDN", 276: "SDN"}


def fao_area_to_iso3(df: pd.DataFrame) -> pd.DataFrame:
    """Keep the country rows of a FAOSTAT table and add an ISO3 column.

    Country rows are the "Area Code"s country_converter knows as FAOcode plus
    those of FAO_CODE_PATCH; the ISO3 comes from country_converter, then
    FAO_CODE_PATCH overrides it.
    """
    cc = coco.CountryConverter()
    valid = set(cc.FAOcode["FAOcode"].astype("int64").to_list()) | set(FAO_CODE_PATCH)
    df = df[df["Area Code"].isin(valid)].copy()
    patched = df["Area Code"].map(FAO_CODE_PATCH)
    known = patched.isna()
    iso3 = coco.country_converter.convert(
        names=list(df.loc[known, "Area Code"]), src="FAOcode", to="ISO3"
    )
    if isinstance(iso3, str):  # convert returns a bare string for a single name
        iso3 = [iso3]
    df["ISO3"] = patched
    df.loc[known, "ISO3"] = iso3
    return df


def merge_patched_rows(df: pd.DataFrame) -> pd.DataFrame:
    """One row per series for the FAO_CODE_PATCH countries.

    After `fao_area_to_iso3` and the column selection, a patched country can
    have two rows for the same item (one per FAO area code, on disjoint
    years). They are summed year by year (all-empty stays empty); every
    other row is untouched and keeps its order, the merged rows take the
    position of their first row.
    """
    hit = df["ISO3"].isin(set(FAO_CODE_PATCH.values()))
    if not hit.any():
        return df
    years = [c for c in df.columns if str(c).startswith("Y") and str(c)[1:].isdigit()]
    keys = [c for c in df.columns if c not in years]
    df = df.assign(_pos=range(len(df)))
    sub = df[hit.to_numpy()]
    merged = sub.groupby(keys, dropna=False, sort=False)[years].sum(min_count=1)
    merged["_pos"] = sub.groupby(keys, dropna=False, sort=False)["_pos"].min()
    out = pd.concat([df[~hit.to_numpy()], merged.reset_index()[df.columns]], ignore_index=True)
    return out.sort_values("_pos", kind="stable").drop(columns="_pos").reset_index(drop=True)


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


    Comment - RW - IS THIS NAMED APPROPRIATELY? IT READS OTHER DATA NOT JUST LAND RIGHT?
    """

    df = pd.read_csv(data_file, encoding="latin-1")

    if relevant_years:

        '''
        Remove from the df all "Area Code" which arenot of interest
        (country_converter FAOcodes plus FAO_CODE_PATCH)
        '''
        df = fao_area_to_iso3(df)

        meta_col = [
            col
            for col in df.columns
            if not col.startswith(("Y", "key", "Element", "Area"))
        ]

        return merge_patched_rows(df[meta_col + make_valid_fao_year(relevant_years)])

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
    print('in handler', relevant_years)
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """
    land_zip = download_fao_data(src_url=src_url, storage_path=download_path)

    extract_archive(zip_archive=land_zip, store_to=data_path)
    relevant_years = relevant_years[relevant_years.index(1991)+1:]

    land_cover_all = pd.read_csv(data_path / csv_name, encoding="latin-1")

    land_cover_all = fao_area_to_iso3(land_cover_all)

    meta_col = [
        col
        for col in land_cover_all.columns
        if not col.startswith(("Y", "key", "Area"))
        ]
    land_cover_all = merge_patched_rows(land_cover_all[meta_col + make_valid_fao_year(relevant_years)])

    col_year = [
        col
        for col in land_cover_all.columns
        if  col.startswith(("Y"))
    ]
    
    
    units= land_cover_all['Unit'].unique()

    if len(units)==1:
        
        if units[0]=='1000 ha':
            land_cover_all[col_year]=(land_cover_all[col_year]*10)
            
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



def get_value_production(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
):
    
    
    
    """
    Get the FAO value of production for futher processing

    This downloads the data and deals with missing values
    """

    value_production_zip = download_fao_data(src_url=src_url, storage_path=download_path)
    extract_archive(zip_archive=value_production_zip, store_to=data_path)

    value_production_all = read_land_data(data_path / csv_name, relevant_years=relevant_years)
    value_production_all = value_production_all[value_production_all['ISO3'] != 'not found']
    value_production_all.to_csv(data_path / "refreshed_value_production.csv", index=False)

