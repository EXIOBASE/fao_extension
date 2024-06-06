from pathlib import Path
from typing import List

import pandas as pd
import yaml
from split_table import split
from split_table import split2
#from calcul import calcul1
from calcul_ray import calcul1

from calcul_ray import calcul2
from calcul_ray import calcul2_prim_livestock
from make_years import make_valid_fao_year as mvy
from regression import regression 
from adjustment_yield import adjust
from adjustment_yield import adjust_prim_livestock
import shutil
import os

def whole_production_calculation(years: List[int], storage_path: Path):
    data_path = Path(storage_path / "data")
    final_path = Path(str(storage_path) +"/final_tables")

    with open(r'aux_data/parameters.yaml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    
    with open(r'aux_data/country.yaml') as file:
        country = yaml.load(file, Loader=yaml.FullLoader) 
        
    
    relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

    """     storage_root = Path("../../land_use").absolute()
    download_path = storage_root / "download"
    data_path = storage_root / "data" """


    '''
    Read the table containing the data related to crop and livestock (primary and processed)
    '''
    

    crop_livestock = pd.read_csv(data_path/'refreshed_crop_livestock.csv', encoding="latin-1") 
    #crop_livestock = pd.read_csv('/home/candyd/tmp/FAO/data/refreshed_crop_livestock.csv', encoding="latin-1")
    col_years = [col for col in crop_livestock.columns if  col.startswith("Y")] 
    
    meta_col = ["ISO3", "Item Code", "Item","Unit"] 
        
    crop_livestock=crop_livestock[meta_col + relevant_years]
    crop_livestock = crop_livestock[crop_livestock['ISO3'] != 'not found']
    crop_livestock=crop_livestock[crop_livestock.ISO3.isin(country)]
    
    
    
    for row in crop_livestock.iterrows():
        if (crop_livestock.loc[row[0]]['Unit'] == 'ha'):
            crop_livestock.loc[row[0],'Unit']= 'km2'
            for year in col_years:
                value = (crop_livestock.loc[row[0],year])/100.0
                crop_livestock.loc[row[0],year] = value
        if (crop_livestock.loc[row[0]]['Unit'] == '100 g/ha'):
            crop_livestock.loc[row[0],'Unit']= '100 g/km2'
            for year in col_years:
                value = (crop_livestock.loc[row[0],year])*100.0
                crop_livestock.loc[row[0],year] = value
        else:
            continue
        
    table_crop_livestock = pd.read_csv('aux_data/itemGroup_crop_livestock.csv', encoding="UTF-8")

    '''
    Get the item as a funstion of the main category:
        crops primary
        crops processed
        live animal
        livestock primary
        livestock processed

    '''

    '''
    Get a list of the different FAO items as a function of the main category
    '''
    crops_primary=split(table_crop_livestock,'QC')
    crops_processed=split(table_crop_livestock,'QD')
    live_animal=split(table_crop_livestock,'QA')
    livestock_primary=split(table_crop_livestock,'QL')
    livestock_processed=split(table_crop_livestock,'QP')

    '''
    Split the main table unto 5 smaller tables, one for each main category
    '''
    crops_primary_table=split2(crop_livestock,crops_primary)
    crops_processed_table=split2(crop_livestock,crops_processed)
    live_animal_table=split2(crop_livestock,live_animal)
    livestock_primary_table=split2(crop_livestock,livestock_primary)
    livestock_processed_table=split2(crop_livestock,livestock_processed)


    '''
    Focus on crops_primary_table only.
    First, we fill up the table with the 0 assumption.
    If for exemple for a certain FAOitem, the area and the production are 0 as a first known value, 
    we consider the values to be 0 as well for the missing years which precede.
    '''
    

    crops_primary_list=crops_primary_table['Item Code'].unique()
    livestock_primary_list=livestock_primary_table['Item Code'].unique()
    crops_processed_list=crops_processed_table['Item Code'].unique()
    livestock_processed_list=livestock_processed_table['Item Code'].unique()
    live_animal_list=live_animal_table['Item Code'].unique() 

    '''
    calcul 1 : zero assumption. if area and production are 0 as the first value available, 
    we condidr the area, the production and the yield values to be zero for the previous missing years
    '''
    #20:27 ->20:51

    '''
    crops primary
    '''
#    crops_primary_table=calcul1(country,crops_primary_list,crops_primary_table,relevant_years,parameters,col_years)  
    crops_primary_table=calcul1(country,crops_primary_list,crops_primary_table,relevant_years,parameters,col_years)  

    '''
    crops processed
    '''

    crops_processed_table=calcul1(country,crops_processed_list,crops_processed_table,relevant_years,parameters,col_years)  

    '''
    livestock primary
    '''    


    livestock_primary_table=calcul1(country,livestock_primary_list,livestock_primary_table,relevant_years,parameters,col_years)  





    '''
    livestock processed
    '''

    livestock_processed_table=calcul1(country,livestock_processed_list,livestock_processed_table,relevant_years,parameters,col_years)  


    '''
    live animal
    '''
    '''ok'''
    live_animal_table=calcul1(country,live_animal_list,live_animal_table,relevant_years,parameters,col_years)  


    '''

    can we run this in parallel ? This takes ages to run.

    '''

    ''''ICI CA NE MARCHE PKUS -> live animal en premier ''' 
    crops_primary_table=calcul2(country,crops_primary_list,crops_primary_table,relevant_years,parameters,col_years)    
    crops_processed_table=calcul2(country,crops_processed_list,crops_processed_table,relevant_years,parameters,col_years)    
    
    livestock_primary_table=calcul2_prim_livestock(country,livestock_primary_list,livestock_primary_table,relevant_years,parameters,col_years)    
    
    livestock_processed_table=calcul2(country,livestock_processed_list,livestock_processed_table,relevant_years,parameters,col_years)    

    live_animal_table=calcul2(country,live_animal_list,live_animal_table,relevant_years,parameters,col_years)    


    '''linear interpolation'''

    crops_primary_table=crops_primary_table.set_index(meta_col)
    for code in country :
        print(code)
        crops_primary_table_new=crops_primary_table[(crops_primary_table.index.get_level_values(0)==code)&(crops_primary_table.index.get_level_values(1).isin(crops_primary_list))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in crops_primary_table_new.index:
            if item in crops_primary_table.index:
                crops_primary_table.loc[item,col_years]=crops_primary_table_new.loc[item, col_years]

    crops_primary_table=crops_primary_table.reset_index()

    livestock_primary_table=livestock_primary_table.set_index(meta_col)
    for code in country :
        print(code)
        livestock_primary_table_new=livestock_primary_table[(livestock_primary_table.index.get_level_values(0)==code)&(livestock_primary_table.index.get_level_values(1).isin(livestock_primary_list))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in livestock_primary_table_new.index:
            if item in livestock_primary_table.index:
                livestock_primary_table.loc[item,col_years]=livestock_primary_table_new.loc[item, col_years]

    livestock_primary_table=livestock_primary_table.reset_index()

    crops_processed_table=crops_processed_table.set_index(meta_col)
    for code in country :
        print(code)
        crops_processed_table_new=crops_processed_table[(crops_processed_table.index.get_level_values(0)==code)&(crops_processed_table.index.get_level_values(1).isin(crops_processed_list))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in crops_processed_table_new.index:
            if item in crops_processed_table.index:
                crops_processed_table.loc[item,col_years]=crops_processed_table_new.loc[item, col_years]

    crops_processed_table=crops_processed_table.reset_index()


    livestock_processed_table=livestock_processed_table.set_index(meta_col)
    for code in country :
        print(code)
        livestock_processed_table_new=livestock_processed_table[(livestock_processed_table.index.get_level_values(0)==code)&(livestock_processed_table.index.get_level_values(1).isin(livestock_processed_list))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in livestock_processed_table_new.index:
            if item in livestock_processed_table.index:
                livestock_processed_table.loc[item,col_years]=livestock_processed_table_new.loc[item, col_years]

    livestock_processed_table=livestock_processed_table.reset_index()


    live_animal_table=live_animal_table.set_index(meta_col)
    for code in country :
        print(code)
        live_animal_table_new=live_animal_table[(live_animal_table.index.get_level_values(0)==code)&(live_animal_table.index.get_level_values(1).isin(live_animal_list))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in live_animal_table_new.index:
            if item in live_animal_table.index:
                live_animal_table.loc[item,col_years]=live_animal_table_new.loc[item, col_years]

    live_animal_table=live_animal_table.reset_index()




    print('regression')
    '''Regression'''

    crops_primary_table=regression(country,parameters, crops_primary_table,crops_primary_list,col_years)    

    livestock_primary_table=regression(country,parameters, livestock_primary_table,livestock_primary_list,col_years)    

    crops_processed_table=regression(country,parameters, crops_processed_table,crops_processed_list,col_years)    

    livestock_processed_table=regression(country,parameters, livestock_processed_table,livestock_processed_list,col_years)    

    live_animal_table=regression(country,parameters, live_animal_table,live_animal_list,col_years)    
    
    # '''Adjust Yield'''
    

    # print('adjust')
    # crops_primary_list=crops_primary_table['Item Code'].unique()
    # livestock_primary_list=livestock_primary_table['Item Code'].unique()
    # crops_processed_list=crops_processed_table['Item Code'].unique()
    # livestock_processed_list=livestock_processed_table['Item Code'].unique()
    # live_animal_list=live_animal_table['Item Code'].unique()



    '''Final Cleaning'''
    print('cleaning')
    crops_primary_table=crops_primary_table.fillna(0)
    crops_primary_table[col_years] = crops_primary_table[col_years].round(2)
    crops_primary_table.to_csv(str(final_path)+'/final_crops_primary.csv', index = False) 

    livestock_primary_table=livestock_primary_table.fillna(0)
    livestock_primary_table[col_years] = livestock_primary_table[col_years].round(2)
    livestock_primary_table.to_csv(str(final_path)+'/final_livestock_primary.csv', index = False) 

    crops_processed_table=crops_processed_table.fillna(0)
    crops_processed_table[col_years] = crops_processed_table[col_years].round(2)
    crops_processed_table.to_csv(str(final_path)+'/final_crops_processed.csv', index = False) 

    livestock_processed_table=livestock_processed_table.fillna(0)
    livestock_processed_table[col_years] = livestock_processed_table[col_years].round(2)
    livestock_processed_table.to_csv(str(final_path)+'/final_livestock_processed.csv', index = False) 

    live_animal_table=live_animal_table.fillna(0)
    live_animal_table[col_years] = live_animal_table[col_years].round(2)
    live_animal_table.to_csv(str(final_path)+'/final_live_animal.csv', index = False) 
    

    
