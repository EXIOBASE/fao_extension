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
    return df[df.isnull().any(axis=1)]


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

    if relevant_years is None:
        year_cols = [
            col
            for col in df.columns
            if col.startswith("Y") and col[1:].isdigit()
        ]
    else:
        year_cols = make_valid_fao_year(relevant_years)
        missing_years = [col for col in year_cols if col not in df.columns]
        if missing_years:
            raise KeyError(
                f"{data_file} is missing requested year columns: "
                f"{', '.join(missing_years)}"
            )

    return df[meta_col + year_cols]




def get_landuse(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
    force_download: bool = False,
):
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """
    land_zip = download_fao_data(
        src_url=src_url, storage_path=download_path, force_download=force_download
    )
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
    force_download: bool = False,
):
    
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """
    land_zip = download_fao_data(
        src_url=src_url, storage_path=download_path, force_download=force_download
    )

    extract_archive(zip_archive=land_zip, store_to=data_path)
    if relevant_years is not None:
        relevant_years = [
            year for year in relevant_years if int(str(year).lstrip("Y")) >= 1992
        ]

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
    if relevant_years is None:
        year_cols = [
            col
            for col in land_cover_all.columns
            if col.startswith("Y") and col[1:].isdigit()
        ]
    else:
        year_cols = make_valid_fao_year(relevant_years)
        missing_years = [col for col in year_cols if col not in land_cover_all.columns]
        if missing_years:
            raise KeyError(
                f"{data_path / csv_name} is missing requested year columns: "
                f"{', '.join(missing_years)}"
            )

    land_cover_all = land_cover_all[meta_col + year_cols]

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
    force_download: bool = False,
):
    
    
    
    """
    Get the FAO landuse data for futher processing

    This downloads the data and deals with missing values
    """

    crop_livestock_zip = download_fao_data(
        src_url=src_url, storage_path=download_path, force_download=force_download
    )
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
    force_download: bool = False,
):
    
    
    
    """
    Get the FAO value of production for futher processing

    This downloads the data and deals with missing values
    """

    value_production_zip = download_fao_data(
        src_url=src_url, storage_path=download_path, force_download=force_download
    )
    extract_archive(zip_archive=value_production_zip, store_to=data_path)

    value_production_all = read_land_data(data_path / csv_name, relevant_years=relevant_years)
    value_production_all = value_production_all[value_production_all['ISO3'] != 'not found']
    value_production_all.to_csv(data_path / "refreshed_value_production.csv", index=False)


def get_forestry(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
    force_download: bool = False,
):
    """Download and prep FAOSTAT Forestry Production data.

    Same pattern as get_crop_livestock / get_value_production but with
    one extra step: the Forestry bulk publishes Production, Import,
    and Export rows for each item, all sharing Item Code. ``read_land_data``
    strips the Element column without filtering, which would let
    Imports + Exports get summed alongside Production downstream.
    Filter to Element = Production here so only one row per
    (country, item) survives.
    """
    forestry_zip = download_fao_data(
        src_url=src_url, storage_path=download_path, force_download=force_download
    )
    extract_archive(zip_archive=forestry_zip, store_to=data_path)

    # Read once with Element preserved, filter, then call read_land_data
    # logic on the filtered subset. We do the filter via raw pandas read
    # and then run read_land_data on a temp file to keep the country
    # converter behaviour identical to the rest of the pipeline.
    raw = pd.read_csv(data_path / csv_name, encoding="latin-1")
    if "Element Code" in raw.columns:
        # Element codes 5510 (Production) and 5516 (Production tonnes)
        # are the production series; 56xx are import, 59xx are export.
        production_mask = raw["Element Code"].astype(int).between(5500, 5519)
        raw = raw[production_mask]
    elif "Element" in raw.columns:
        raw = raw[raw["Element"].astype(str).str.strip() == "Production"]

    filtered_csv = data_path / "_forestry_production_only.csv"
    raw.to_csv(filtered_csv, index=False)
    forestry_all = read_land_data(filtered_csv, relevant_years=relevant_years)
    forestry_all = forestry_all[forestry_all["ISO3"] != "not found"]
    forestry_all.to_csv(data_path / "refreshed_forestry.csv", index=False)
    filtered_csv.unlink(missing_ok=True)


def _get_fishery_zip(
    download_path: Path,
    data_path: Path,
    src_url: str,
    marker_csv: Path,
    force_download: bool = False,
):
    """Download and unpack one FishStat bulk zip (Aquaculture or Capture).

    FishStat bulks are at https://www.fao.org/fishery/static/Data/.
    The zip extracts a flat set of CSVs that downstream processing
    expects under ``<data_path>/fishstat/``. We extract there directly,
    so reference tables (CL_FI_*) from both Aquaculture and Capture
    zips merge into the same directory (they are identical between
    zips of the same release).
    """
    import logging
    target_dir = data_path / "fishstat"
    target_dir.mkdir(parents=True, exist_ok=True)
    zip_name = Path(src_url.split("/")[-1]).name
    source_marker = target_dir / f".{marker_csv.stem}_source_zip"
    marker_matches = (
        source_marker.exists()
        and source_marker.read_text(encoding="utf-8").strip() == zip_name
    )
    if (
        (target_dir / marker_csv.name).exists()
        and not force_download
        and marker_matches
    ):
        return  # already extracted for this kind

    try:
        zip_path = download_fao_data(
            src_url=src_url,
            storage_path=download_path,
            force_download=force_download,
        )
        extract_archive(zip_archive=zip_path, store_to=target_dir)
        source_marker.write_text(zip_name, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        logging.warning(
            "FishStat bulk download failed for %s (%s). Drop the zip "
            "into %s manually (FAO directory: "
            "https://www.fao.org/fishery/static/Data/) and re-run.",
            src_url, exc, download_path,
        )


def get_fishery_aquaculture(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
    force_download: bool = False,
):
    """Download and unpack the FAO Aquaculture bulk zip."""
    _get_fishery_zip(
        download_path=download_path,
        data_path=data_path,
        src_url=src_url,
        marker_csv=Path("Aquaculture_Quantity.csv"),
        force_download=force_download,
    )


def get_fishery_capture(
    download_path: Path,
    data_path: Path,
    src_url: str,
    csv_name: Union[str, Path],
    relevant_years: List[int],
    force_download: bool = False,
):
    """Download and unpack the FAO Capture bulk zip."""
    _get_fishery_zip(
        download_path=download_path,
        data_path=data_path,
        src_url=src_url,
        marker_csv=Path("Capture_Quantity.csv"),
        force_download=force_download,
    )

