""" FAO land use processing

Note
-----

Runs the full sequence of FAO data downloading and processing:

1) Downloading the data
2) Processing the raw data related to landuse
3) Processing the raw data related to crop and livestock (primary and processed)
4) Processing the raw data related to fishery production (FishStat)
5) Processing the classification of data related to crop and livestock (primary and processed)
6) Aggregate the data per EXIO3 region
"""

from pathlib import Path
import sys
from datetime import date
today = date.today()

sys.path.insert(1, 'download')
sys.path.insert(2,'raw_data_processing/land_use_calculation')
sys.path.insert(3,'aux_data')
sys.path.insert(4,'raw_data_processing/crop_livestock_production')
sys.path.insert(5,'processig_classification')
sys.path.insert(6,'aggregation_region')
sys.path.insert(7,'raw_data_processing/fishery_production')
sys.path.insert(8,'raw_data_processing/forestry_production')

import download.main   # noqa
import raw_data_processing.land_use_calculation.landuse  # noqa
import raw_data_processing.crop_livestock_production.crop_livestock  # noqa
import raw_data_processing.fishery_production.fishery  # noqa
import raw_data_processing.forestry_production.forestry  # noqa
import processing_classification.landuse_calculation  # noqa
import aggregation_region.aggregation  # noqa

# RUN SETTINGS
# --------------

DATAFOLDER: Path = Path('d:/indecol/data/fao/')
#DATAFOLDER: Path = Path('/home/candyd/tmp/FAO')
DATAFOLDER.mkdir(exist_ok=True, parents=True)

final_path = Path(DATAFOLDER / "final_tables")
final_path.mkdir(exist_ok=True, parents=True)
STARTYEAR: int = 1961
ENDYEAR: int = 2022
YEARS = range(STARTYEAR, ENDYEAR+1)
STARTYEAR_cover: int = 1992
ENDYEAR: int = 2022
YEARS_cover = range(STARTYEAR_cover, ENDYEAR+1)


# Preperations

# Step 1 - downloading the data  14:24 ->16:50
print("download files")
download.main.get_all(years=YEARS, storage_path=DATAFOLDER)

# # Step 2 - processing the raw data related to landuse
print("processing the raw data related to landuse")
landuse = raw_data_processing.land_use_calculation.landuse.whole_landuse_calculation(years=YEARS,storage_path=DATAFOLDER)
landuse.to_csv(str(final_path)+"/landuse_final_runall.csv",index = False) 

# # Step 3 - processing the raw data related to crop and livestock (primary and processed) 
print("processing the raw data related to crop and livestock")
crop = raw_data_processing.crop_livestock_production.crop_livestock.whole_production_calculation(years=YEARS,storage_path=DATAFOLDER)
import crop_livestock
# ray.shutdown()
crop = crop_livestock.whole_production_calculation(years=YEARS,storage_path=DATAFOLDER)


# # Step 4 - processing the raw data related to fishery (FishStat)
# Skipped automatically when the FishStat bulk export is not present
# under DATAFOLDER/data; see raw_data_processing/fishery_production/README.md.
print("processing the raw data related to fishery (FishStat)")
try:
    fishery = raw_data_processing.fishery_production.fishery.whole_fishery_calculation(
        years=YEARS, storage_path=DATAFOLDER
    )
    fishery.to_csv(str(final_path) + "/fishery_final_runall.csv", index=False)
except FileNotFoundError as exc:
    print(f"  -> skipping fishery step ({exc}). "
          f"Drop the FishStat release CSVs into {DATAFOLDER}/data/ and re-run.")

# # Step 4b - processing the raw data related to forestry (FAOSTAT FO)
print("processing the raw data related to forestry (FAOSTAT FO)")
try:
    forestry = raw_data_processing.forestry_production.forestry.whole_forestry_calculation(
        years=YEARS, storage_path=DATAFOLDER
    )
    forestry.to_csv(str(final_path) + "/forestry_final_runall.csv", index=False)
except FileNotFoundError as exc:
    print(f"  -> skipping forestry step ({exc}). "
          f"Run the download step or check {DATAFOLDER}/data/.")

# # Step 5 - processing the classification of data related to crop and livestock (primary and processed)
print("processing classification of data (crop and livestock, primary and processed")
processing_classification.landuse_calculation.landuse_allocation(years=YEARS,storage_path=DATAFOLDER)

# #Step 6 - aggregation
print("aggregation EXIO regions, EXIO  product code")
aggregation_region.aggregation.table_aggregation(final_tables = final_path)

