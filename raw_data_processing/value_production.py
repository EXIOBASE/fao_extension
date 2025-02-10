# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 13:23:02 2024

@author: richa
"""



from pathlib import Path
import sys
from datetime import date
import country_converter as coco
import shutil

from make_years import make_valid_fao_year as mvy 
today = date.today()

sys.path.insert(1, 'download')
sys.path.insert(2,'raw_data_processing/land_use_calculation')
sys.path.insert(3,'aux_data')
sys.path.insert(4,'raw_data_processing/value_production_production')
sys.path.insert(5,'processig_classification')
sys.path.insert(6,'aggregation_region')


# import raw_data_processing.land_use_calculation.landuse  # noqa 
# import raw_data_processing.value_production_production.value_production  # noqa
# import processing_classification.landuse_calculation  # noqa
# import aggregation_region.aggregation  # noqa
import yaml
import pandas as pd 

# RUN SETTINGS
# --------------

DATAFOLDER: Path = Path('d:/indecol/data/fao/')
DATAFOLDER.mkdir(exist_ok=True, parents=True)

final_path = Path(DATAFOLDER / "final_tables")
final_path.mkdir(exist_ok=True, parents=True)
STARTYEAR: int = 1961
ENDYEAR: int = 2021
YEARS = range(STARTYEAR, ENDYEAR+1)
STARTYEAR_cover: int = 1992
ENDYEAR: int = 2021
YEARS_cover = range(STARTYEAR_cover, ENDYEAR+1)


years=YEARS

storage_path=DATAFOLDER

classification_ind = pd.read_excel('../aux_data/exio3_mr_class.xlsx', sheet_name='ind')
ordered_columns_ind = pd.MultiIndex.from_arrays([
    classification_ind['Country'],
    classification_ind['CodeNr']
])
ordered_columns_ind2=classification_ind[['Country','CodeNr']]





    

data_path = Path(storage_path / "data")
final_path = Path(str(storage_path) +"/final_tables")

with open(r'../aux_data/parameters.yaml') as file:
    parameters = yaml.load(file, Loader=yaml.FullLoader)

with open(r'../aux_data/country.yaml') as file:
    country = yaml.load(file, Loader=yaml.FullLoader) 
    

relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

"""     storage_root = Path("../../land_use").absolute()
download_path = storage_root / "download"
data_path = storage_root / "data" """


'''
Read the table containing the data related to crop and livestock (primary and processed)
'''
value_production = pd.read_csv(data_path/'refreshed_value_production.csv', encoding="latin-1") 
    #value_production = pd.read_csv('/home/candyd/tmp/FAO/data/refreshed_value_production.csv', encoding="latin-1")
col_years = [col for col in value_production.columns if  col.startswith("Y")] 


meta_col = ["ISO3", "Item Code", "Item","Unit"] 
    
value_production=value_production[meta_col + relevant_years]
value_production = value_production[value_production['ISO3'] != 'not found']
value_production=value_production[value_production.ISO3.isin(country)]


value_production_usd=value_production[value_production.Unit=='1000 Int$']


item_xlsx = Path("../aux_data/List_Primary production_FAO-CPA-EXIOBASE.xlsx") 
item_sheet = 'Correspondance_FAO-CPA-EXIOBASE' 



correspondance = pd.read_excel(item_xlsx,item_sheet)

correspondance2 = pd.read_csv('../aux_data/List_Primary_livestock_FAO-CPA-EXIOBASE.csv', encoding="latin-1") 

correspondance_all=pd.concat([correspondance[['FAO item name', 'FAO item code','EXIOBASE product code','EXIOBASE product']]
                              ,correspondance2[['FAO item name', 'FAO item code','EXIOBASE product code','EXIOBASE product']]])



value_production_usd_exio_merge = value_production_usd.merge(correspondance_all, left_on='Item Code', right_on='FAO item code', how='left')

value_production_usd_exio_merge[value_production_usd_exio_merge.isna()]=0
value_production_usd_exio_merge_exio = value_production_usd_exio_merge.set_index(['ISO3', 'Item Code', 'Item', 'Unit','FAO item name', 'FAO item code', 'EXIOBASE product code','EXIOBASE product'])
value_production_usd_exio_merge_exio  = value_production_usd_exio_merge_exio.groupby(['ISO3','EXIOBASE product code'], sort=False).sum()

value_production_usd_exio_merge_exio = value_production_usd_exio_merge_exio.reset_index()
value_production_usd_exio_merge_exio = value_production_usd_exio_merge_exio[value_production_usd_exio_merge_exio['EXIOBASE product code'] != 0]
value_production_usd_exio_merge_exio = value_production_usd_exio_merge_exio[value_production_usd_exio_merge_exio['EXIOBASE product code'] != 'n.a.']
value_production_usd_exio_merge_exio = value_production_usd_exio_merge_exio.sort_values(by=['ISO3', 'EXIOBASE product code'])


cc = coco.CountryConverter()
cc.valid_class
cc.get_correspondence_dict('ISO3', 'EXIO3')

converter=coco.country_converter
country_code = list(value_production_usd_exio_merge_exio['ISO3'])
value_production_usd_exio_merge_exio.insert(1, 'EXIO3', converter.convert(names = country_code, to='EXIO3'))

group=value_production_usd_exio_merge_exio.groupby(['EXIO3','EXIOBASE product code'],dropna=False).sum()
group = group.drop(columns=['ISO3'])
group.index = group.index.rename(['Country', 'CodeNr'])
oc=ordered_columns_ind2.T.reindex(['Country', 'CodeNr'])
group2 = group.T.reindex_like(oc)

group.to_csv('exio_production_values_exio_class.csv')
