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

    KST-CD: What I did here are numpy-style docstrings. Please use these in this format for documenting the use of functions. There are more fields defined in the numpy docstrings, but at the very minimum use parameters.
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

    Parameters
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

        df["ISO3"] = converter.convert(names=country_code, src="FAOcode", to="ISO3")

        meta_col = [
            col
            for col in df.columns
            if not col.startswith(("Y", "key", "Element", "Area"))
        ]

        return df[meta_col + make_valid_fao_year(relevant_years)]

    else:
        return df

'''
The following function "deal_missing_data" allows us to know which are the missing values in the 
downloaded table from FAOSTAT
'''


'''
def deal_missing_data(df, relevant_years=None):
    """Reads the data and returns dataframe

    TODO CD: Please add a description what this actually does
    TODO CD: I also not sure why there is an if clause in there, this is not robust it seems

    Parameters
    ----------

    data_file: pandas DataFrame
        as downloaded

    relevant_years: list
        Relevant years defined in the main : relevant_years = list(range(1995,2021))
        Select the years of interest, in this case from 1995 to 2020

    """

    if relevant_years:

        relevant_years = make_valid_fao_year(relevant_years)

        country_code = list(df["Area Code"])
        converter = coco.country_converter

        df["ISO3"] = converter.convert(names=country_code, src="FAOcode", to="ISO3")
        filter_col = [col for col in df if col.startswith("Y")]
        df_modified = df.copy()

        df_modified["max_value"] = df_modified[filter_col].max(axis=1)
        df_modified["min_value"] = df_modified[filter_col].min(axis=1)
        df_modified["mean_value"] = df_modified[filter_col].mean(axis=1, skipna=True)
        df_modified["std_dev"] = df_modified[filter_col].std(axis=1, skipna=True)
        df_modified["Var"] = df_modified[filter_col].var(axis=1, skipna=True)

        # df['min_value'] = df.min(axis=1)
        # df['mean_value'] = df.mean(axis = 1, skipna = True)
        # df['std_dev'] = df.std(axis = 1, skipna = True)
        analysis_col = [
            col
            for col in df_modified.columns
            if col.startswith(
                ("max_value", "min_value", "mean_value", "std_dev", "Var")
            )
        ]
        meta_col = [
            col
            for col in df_modified.columns
            if not col.startswith(
                (
                    "Y",
                    "key",
                    "Element",
                    "Area",
                    "max_value",
                    "min_value",
                    "mean_value",
                    "std_dev",
                    "Var",
                )
            )
        ]

        # return df[meta_col + relevant_years]
        # print(df_modified.head(150))
        df_modified = df_modified[meta_col + relevant_years + analysis_col]
        print(df_modified.head(150))

        for index, row in df_modified.iterrows():
            for year in relevant_years:
                if (
                    row["std_dev"] == 0.0
                    and row["mean_value"] != 0
                    and pd.isnull(row[year])
                ):
                    print(year, row[year], row["std_dev"], row["mean_value"])
                    df_modified.loc[index, year] = row["mean_value"]

        return df_modified[meta_col + relevant_years + analysis_col]

    else:
        return df_modified
'''

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
    land_all.to_csv(data_path / "refreshed_land_use.csv", index=False)

    '''
    need to be uncomment if we are interested in knowing exacly which data are missing
    '''
    #land_missing = get_missing_data(land_all)
    # land_missing.to_csv(data_path / "missing_land_use.csv", index=False)
    
    #deal_land_all = deal_missing_data(land_all, relevant_years=relevant_years)
    #deal_land_all.to_csv(data_path / "deal_with_missing_data.csv", index=False)


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
    crop_livestock_all.to_csv(data_path / "refreshed_crop_livestock.csv", index=False)


    '''
    need to be uncomment if we are interested in knowing exacly which data are missing
    '''
    #crop_livestock_missing = get_missing_data(crop_livestock_all)    
    #crop_livestock_missing.to_csv(data_path / "missing_crop_livestock.csv", index=False)
    #deal_crop_livestock_all = deal_missing_data(crop_livestock_all, relevant_years=relevant_years)
    #deal_crop_livestock_all.to_csv(data_path / "deal_with_missing_data_crop_livestock.csv", index=False)
