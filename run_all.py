""" FAO land use processing

Note
-----

Runs the full sequence of FAO data downloading and processing:

1) Downloading the data 
2) Processing the raw data related to landuse
3) Processing the raw data related to crop and livestock (primary and processed)
4) Processing the classification of data related to crop and livestock (primary and processed)
5) Aggregate the data per EXIO3 region 
"""

from pathlib import Path
import sys
import os
from datetime import date
from datetime import datetime
today = date.today()

sys.path.insert(1, 'download')
sys.path.insert(2,'raw_data_processing/land_use_calculation')
sys.path.insert(3,'aux_data')
sys.path.insert(4,'raw_data_processing/crop_livestock_production')
sys.path.insert(5,'processig_classification')
sys.path.insert(6,'aggregation_region')

import download.main
import  raw_data_processing.land_use_calculation.landuse
import  raw_data_processing.crop_livestock_production.crop_livestock
import  processing_classification.landuse_calculation
import aggregation_region.aggregation
#All settings for running the script
DATAFOLDER: Path = Path('/home/candyd/tmp/FAO')

STARTYEAR: int = 1961
ENDYEAR: int = 2021
YEARS = range(STARTYEAR, ENDYEAR+1)
print(YEARS)
# Preperations
DATAFOLDER.mkdir(exist_ok=True, parents=True)

# Step 1 - downloading the data
download.main.get_all(years=YEARS, storage_path=DATAFOLDER)
# # Step 2 - processing the raw data related to landuse
landuse = raw_data_processing.land_use_calculation.landuse.whole_landuse_calculation(years=YEARS,storage_path=DATAFOLDER)
landuse.to_csv('landuse_final_runall.csv',index = False)
# # Step 3 - processing the raw data related to crop and livestock (primary and processed) 060524 18h05
crop = raw_data_processing.crop_livestock_production.crop_livestock.whole_production_calculation(years=YEARS,storage_path=DATAFOLDER)
# # Step 4 - processing the classification of data related to crop and livestock (primary and processed)
processing_classification.landuse_calculation.landuse_allocation(years=YEARS,storage_path=DATAFOLDER)
# #Step 5 - aggregation
aggregation_region.aggregation.table_aggregation()
