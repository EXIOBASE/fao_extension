import pandas as pd
import numpy as np
from pathlib import Path
from make_years import make_valid_fao_year as mvy 
import yaml
from typing import List
import shutil
import os

def landuse_allocation(years: List[int], storage_path: Path) : 

    with open(r'aux_data/parameters.yaml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    
    with open(r'aux_data/country.yaml') as file:
        country = yaml.load(file, Loader=yaml.FullLoader) 
        
    final_path = Path(str(storage_path) +"/final_tables")
    
    seed_cotton_p01e=0.63
    seed_cotton_p01g=0.37

    factor_beef_buffalo=20.0
    factor_milk=1.0
    factor_poultry=1.0
    factor_pig=2.0
    factor_sheep_goat=10.0

    '''Crops promary -> Crops primary area and crops primary production'''

    crops_primary = pd.read_csv(final_path / 'final_crops_primary.csv', encoding="latin-1") 
    crops_primary.insert(3, 'EXIOBASE product code', '')
    crops_primary.insert(4, 'EXIOBASE product', '')


    '''revove total from list so some items are not counted twice'''
    
    FAO_items = pd.read_csv("aux_data/FAOSTAT_items.csv")
    item_group_unique = FAO_items['Item Group Code'].unique().tolist()
    item_group_unique = [ x for x in item_group_unique if x.isdigit() ]
    item_group_unique = [eval(i) for i in item_group_unique]
    

    '''we removed the total values in order to remove duplicate'''
    
    crops_primary = crops_primary[~crops_primary['Item Code'].isin(item_group_unique)]
    

    
    item_xlsx = Path("aux_data/List_Primary production_FAO-CPA-EXIOBASE.xlsx") 
    item_sheet = 'Correspondance_FAO-CPA-EXIOBASE' 

    correspondance = pd.read_excel(item_xlsx,item_sheet)
    meta_col = [col for col in correspondance.columns if not col.startswith(("DESIRE","Un"))] 

    for i in crops_primary.index:
        
        fao_code=crops_primary.loc[i,['Item Code']].values[0]
        if fao_code in correspondance['FAO item code'].values:
                    
            crops_primary.loc[i,['EXIOBASE product code']]=correspondance.loc[correspondance['FAO item code']==fao_code,['EXIOBASE product code']].values[0]
            crops_primary.loc[i,['EXIOBASE product']]=correspondance.loc[correspondance['FAO item code']==fao_code,['EXIOBASE product']].values[0]
        
                    
    crops_primary_area = crops_primary.loc[(crops_primary['Unit']=='km2')]
    crops_primary_production = crops_primary.loc[(crops_primary['Unit']=='t')]



        
        
        
    '''crop production'''
    # new name is : crops_primary_production
    #called df before modification


    '''crop harvest'''
    #df2 = pd.read_csv('../Fill_4_tables/crop_harvest/crop_harvest.csv', encoding="latin-1")
    #new name is : crops_primary_area


    '''land use'''
    landuse = pd.read_csv(final_path / 'landuse_final_runall.csv', encoding="latin-1")
    #df3 = pd.read_csv('final_landuse.csv', encoding="latin-1")



    '''Livestock production'''

    #df_livestock_all = pd.read_csv('../Fill_4_tables/Livestock_prod/livestock_prod.csv', encoding="latin-1")
    livestock_primary_production = pd.read_csv(final_path /'final_livestock_primary.csv', encoding="latin-1") 
    
    '''remove duplicates'''
    
    livestock_primary_production = livestock_primary_production[~livestock_primary_production['Item Code'].isin(item_group_unique)]


    item_csv = pd.read_csv("aux_data/List_Primary_livestock_FAO-CPA-EXIOBASE.csv") 
    
    meta_col = [col for col in correspondance.columns if not col.startswith(("DESIRE","Un"))] 


    livestock_primary_production.insert(3, 'EXIOBASE product code', '')
    livestock_primary_production.insert(4, 'EXIOBASE product', '')

    for i in livestock_primary_production.index:
        
        fao_code=livestock_primary_production.loc[i,['Item Code']].values[0]
        if fao_code in item_csv['FAO item code'].values:
                    
            livestock_primary_production.loc[i,['EXIOBASE product code']]=item_csv.loc[item_csv['FAO item code']==fao_code,['EXIOBASE product code']].values[0]
            livestock_primary_production.loc[i,['EXIOBASE product']]=item_csv.loc[item_csv['FAO item code']==fao_code,['EXIOBASE product']].values[0]
        
                    
    # livestock_primary_production_area = livestock_primary_production.loc[(livestock_primary_production['Unit']=='km2')]
    livestock_primary_production = livestock_primary_production.loc[(livestock_primary_production['Unit']=='t')]



    #dfs = pd.read_csv('../aux_data/List_Primary_livestock_FAO-CPA-EXIOBASE.csv', encoding="latin-1")
        
        
        
        

    #land use#
    grazing_area = pd.read_csv(final_path /'landuse_final_runall.csv', encoding="latin-1")
    forest_area = pd.read_csv(final_path /'landuse_final_runall.csv', encoding="latin-1")
    final_demand_area = pd.read_csv(final_path /'landuse_final_runall.csv', encoding="latin-1")
        

    #list_ISO3 = list(df['ISO3'])
    list_ISO3 = list(crops_primary_production['ISO3'])

    crops_primary_production=crops_primary_production.drop(columns=['Item Code'])
    crops_primary_production=crops_primary_production.drop(columns=['Item'])

    crops_primary_area=crops_primary_area.drop(columns=['Item Code'])
    crops_primary_area=crops_primary_area.drop(columns=['Item'])

    crops_primary_production['EXIOBASE product code'].replace('',np.nan, inplace=True)
    crops_primary_production.dropna(subset=['EXIOBASE product code'], inplace=True)  



    crops_primary_production=crops_primary_production.groupby(['ISO3','EXIOBASE product code','EXIOBASE product','Unit']).sum().reset_index()
    crops_primary_production_modified=crops_primary_production.copy()
    crops_primary_production_modified['EXIOBASE product code'].replace('',np.nan, inplace=True)
    crops_primary_production_modified.dropna(subset=['EXIOBASE product code'], inplace=True)  


    grazing_area=grazing_area.fillna(0.0)  
    forest_area=forest_area.fillna(0.0)
    final_demand_area = final_demand_area.fillna(0.0)
        


    #list_ISO3_2 = list(crops_primary_production_modified['ISO3'])
    #res = [] 
    #for i in list_ISO3: 
    #    if i not in res: 
    #        res.append(i) 



    list_exio = list(crops_primary_production_modified['EXIOBASE product code'])
    res2 = []
    for i in list_exio: 
        if i not in res2: 
            res2.append(i) 
    

    '''
    Make sure that all the categories from p01.a to p01.h are in the table for each country
    '''
    for code in country :
        if not 'p01.e' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.e','Oil seeds','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        if not 'p01.g' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.g','Plant-based fibers','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])

        if not 'p01.a' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.a','Paddy rice','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])

        if not 'p01.b' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.b','Wheat','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        

        if not 'p01.c'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.c','Cereal grains nec','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
    
        if not 'p01.d'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        
        if not 'p01.f'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        
        if not 'p01.h'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.h','Crops nec','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'], 'Unit':['t']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        

    crops_primary_production_modified=crops_primary_production_modified.fillna(0.0)   
    crops_primary_production_modified=crops_primary_production_modified.sort_values(by=['ISO3', 'EXIOBASE product code'])
    """
    allocate the seed cotton harvested area to p01.e oil crops and p01.g fibre
    """       
    for code in country :
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if 'n.a.' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
                
                value_seed_cotton=crops_primary_production_modified.loc[((crops_primary_production_modified['ISO3']==code) & (crops_primary_production_modified['EXIOBASE product code']=='n.a.')),[year]]
                seed_cotton=value_seed_cotton.to_string(index=False, header=False)
                
                cotton_to_p01e=float(seed_cotton_p01e*float(seed_cotton))
                cotton_to_p01g=float(seed_cotton_p01g*float(seed_cotton))
    
                value_p01e=crops_primary_production_modified.loc[((crops_primary_production_modified['ISO3']==code) & (crops_primary_production_modified['EXIOBASE product code']=='p01.e')),[year]]
                value_p01g=crops_primary_production_modified.loc[((crops_primary_production_modified['ISO3']==code) & (crops_primary_production_modified['EXIOBASE product code']=='p01.g')),[year]]                
                p01e=float(value_p01e.to_string(index=False, header=False))
                p01g=float(value_p01g.to_string(index=False, header=False))
                
                new_p01e=p01e+cotton_to_p01e
                new_p01g=p01g+cotton_to_p01g
        
                
                '''Replace old value p01.e and p01.g with new vales in dataframe'''
                
                crops_primary_production_modified.loc[((crops_primary_production_modified['ISO3']==code) & (crops_primary_production_modified['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
                crops_primary_production_modified.loc[((crops_primary_production_modified['ISO3']==code) & (crops_primary_production_modified['EXIOBASE product code']=='p01.g')),[year]] = new_p01g




    '''
    This df is the crops primary production revised (the seed cotton has been allocated to p01.e ad p01.g)
    '''
                
    crops_primary_production_modified=crops_primary_production_modified[~crops_primary_production_modified['EXIOBASE product code'].str.contains("n.a.")]



    '''
    We have to do the same now with the harvested area
    '''

                
    crops_primary_area=crops_primary_area.groupby(['ISO3','EXIOBASE product code','EXIOBASE product','Unit']).sum().reset_index()
    crops_primary_area['EXIOBASE product code'].replace('',np.nan, inplace=True)
    crops_primary_area.dropna(subset=['EXIOBASE product code'], inplace=True)  


    crops_primary_area_modified=crops_primary_area.copy()







    #df_modified2 avt modif
            
    """
    allocate the seed cotton harvested area to p01.e oil crops and p01.g fibre
    """




    list_exio = list(crops_primary_area_modified['EXIOBASE product code'])
    res2 = []
    for i in list_exio: 
        if i not in res2: 
            res2.append(i) 
    


    for code in country :
        if not 'p01.e' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])
            
        if not 'p01.g' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])
                    
        if not 'p01.a' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])


        if not 'p01.b' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])
    
        if not 'p01.c'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])    
        if not 'p01.d'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])    
        if not 'p01.f'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])    
        if not 'p01.h'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'], 'Unit':['km2']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])

    crops_primary_area_modified=crops_primary_area_modified.fillna(0.0)   
    crops_primary_area_modified.sort_values(by=['ISO3', 'EXIOBASE product code'])

        
    for code in country :
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if 'n.a.' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
                value_seed_cotton=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='n.a.')),[year]]
                seed_cotton=value_seed_cotton.to_string(index=False, header=False)
                cotton_to_p01e=float(seed_cotton_p01e*float(seed_cotton))
                cotton_to_p01g=float(seed_cotton_p01g*float(seed_cotton))
                value_p01e=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.e')),[year]]
                value_p01g=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.g')),[year]]                
                p01e=float(value_p01e.to_string(index=False, header=False))
                p01g=float(value_p01g.to_string(index=False, header=False))
                new_p01e=p01e+cotton_to_p01e
                new_p01g=p01g+cotton_to_p01g
                
                '''Replace old value p01.e and p01.g with new vales in dataframe'''     
                
                crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
                crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.g')),[year]] = new_p01g

    '''
    This df is the crops primary area revised (the seed cotton has been allocated to p01.e ad p01.g)
    '''

    crops_primary_area_modified=crops_primary_area_modified[~crops_primary_area_modified['EXIOBASE product code'].str.contains("n.a.")]
        
        
        
        
        
    """Get the harvest crop per ha per year per country"""

    harvested_per_country=crops_primary_area.groupby(['ISO3','Unit']).sum()

    '''select the total cropped land from FAOSTAT'''

    cropland_FAO = landuse[(landuse.ISO3 != 'not found')&(landuse['Item Code']==6620)]
        
    '''We can split permanent meadows and pastures (item 6655) unto FAO item 6659 : naturally growing FAO item 6656 : cultivated'''

    nat_growing = grazing_area.copy()
    cultivated_area = grazing_area.copy()
    
    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6655 in (grazing_area.loc[grazing_area['ISO3']==code, ["Item Code"]].values) :
                new_row = pd.DataFrame({'Item Code':[6655],'Item':['Land under perm. meadows and pastures'],'Unit':['km2'], 'ISO3':[code],year:[0]})  
                grazing_area = pd.concat([grazing_area,new_row])
            
    grazing_area = grazing_area[(grazing_area.ISO3 != 'not found')&(grazing_area['Item Code']==6655)]
    grazing_area=grazing_area.fillna(0.0)     

    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6659 in (nat_growing.loc[nat_growing['ISO3']==code, ["Item Code"]].values) :
                new_row = pd.DataFrame({'Item Code':[6659],'Item':['Perm. meadows & pastures - Nat. growing'],'Unit':['km2'], 'ISO3':[code],year:[0]})  
                nat_growing = pd.concat([nat_growing,new_row])            
    nat_growing = nat_growing[(nat_growing.ISO3 != 'not found')&(nat_growing['Item Code']==6659)]
    nat_growing = nat_growing.fillna(0.0)        

    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6656 in (cultivated_area.loc[cultivated_area['ISO3']==code, ["Item Code"]].values) :
                new_row = pd.DataFrame({'Item Code':[6656],'Item':['Perm. meadows & pastures - Cultivated'],'Unit':['km2'], 'ISO3':[code],year:[0]})  
                cultivated_area = pd.concat([cultivated_area,new_row])            
    cultivated_area = cultivated_area[(cultivated_area.ISO3 != 'not found')&(cultivated_area['Item Code']==6656)]
    cultivated_area = cultivated_area.fillna(0.0)       





    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6670 in (final_demand_area.loc[final_demand_area['ISO3']==code, ["Item Code"]].values) :
                new_row = pd.DataFrame({'Item Code':[6670],'Item':['Final Demand'],'Unit':['km2'], 'ISO3':[code],year:[0]})  
                final_demand_area = pd.concat([final_demand_area,new_row])             
    
    final_demand_area = final_demand_area[(final_demand_area.ISO3 != 'not found')&(final_demand_area['Item Code']==6670)]
    final_demand_area = final_demand_area.fillna(0.0) 


    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6646 in (forest_area.loc[forest_area['ISO3']==code, ["Item Code"]].values) :
                new_row = pd.DataFrame({'Item Code':[6646],'Item':['Forest Land'],'Unit':['km2'], 'ISO3':[code],year:[0]})  
                forest_area = pd.concat([forest_area,new_row])             
                
    forest_area = forest_area[(forest_area.ISO3 != 'not found')&(forest_area['Item Code']==6646)]
    forest_area = forest_area.fillna(0.0)    


    Unit='km2'

    cropland_total = []
    for code in country:
        for year in relevant_years:
            cropland = (cropland_FAO[cropland_FAO['ISO3'] == code][year]).astype(np.float32).values
            cropland_total.append((code,Unit,year,*cropland))
            
    

    cropland_total_year=pd.DataFrame(cropland_total,columns=["ISO3","Unit","YEAR","cropland total"])


    cropland_total_year_country=cropland_total_year.pivot_table(index=['ISO3','Unit'],columns=['YEAR'], values="cropland total")


    #cropland_total_year_country.to_csv('cropland_total.csv',index = False)

    '''
        Extract data for fodder crops


            Select FAOSTAT Item codes related to 
            1806	Beef and Buffalo Meat
            1808	Meat, Poultry
            1780	Milk, Total
            1807	Sheep and Goat Meat
            1035	Meat, pig

    '''

    livestock_primary_production = pd.read_csv(final_path /'final_livestock_primary.csv', encoding="latin-1") 

    livestock_primary_production = livestock_primary_production.loc[(livestock_primary_production['Unit']=='t')]

    '''
    Check if 1806 = 947 + 867
            1808 = 1089+ 1058 + 1069 + 1073 + 1080
            1780 = 951 + 1130 + 882 + 1020 + 982
            1807 = 1017 + 977
            1035 = 1035
    '''
    for code in country:
        print(code)
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if 867 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                beef = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==867)),[year]].values[0]
            else :
                beef =0.0
            if 947 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                buffalo = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==947)),[year]].values[0]
            else :
                buffalo = 0.0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1806)),[year]] = beef + buffalo
            
            
            
            
            if 1089 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                bird = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1089)),[year]].values[0]
            else :
                bird =0.0
            if 1058 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                chicken = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1058)),[year]].values[0]
            else :
                chicken = 0.0
            if 1069 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                duck = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1069)),[year]].values[0]
            else :
                duck =0.0
            if 1073 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                goose = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1073)),[year]].values[0]
            else :
                goose = 0.0
            if 1080 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                turkey = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1080)),[year]].values[0]
            else :
                turkey = 0.0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1808)),[year]] = bird + chicken + duck + goose + turkey


            if 951 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_buffalo = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==951)),[year]].values[0]
            else :
                milk_buffalo =0.0
            if 1130 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_camel = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1130)),[year]].values[0]
            else :
                milk_camel = 0.0
            if 882 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_cow = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==882)),[year]].values[0]
            else :
                milk_cow =0.0
            if 1020 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_goat = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1020)),[year]].values[0]
            else :
                milk_goat = 0.0
            if 982 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_sheep = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==982)),[year]].values[0]
            else :
                milk_sheep = 0.0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1780)),[year]] = milk_buffalo + milk_camel + milk_cow + milk_goat + milk_sheep


            if 1017 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                meat_goat = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1017)),[year]].values[0]
            else :
                meat_goat =0.0
            if 977 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                meat_sheep = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==977)),[year]].values[0]
            else :
                meat_sheep = 0.0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1807)),[year]] = meat_goat + meat_sheep
            
            
    livestock_primary_production = livestock_primary_production[~livestock_primary_production['Item Code'].isin(item_group_unique)]

    #crops_primary = pd.read_csv('final_cropland_primary.csv', encoding="latin-1") 
    '''RAJOUTER EXIOBASE EXTENSION NAME AND EXIOBASE PRODUCT''' 
    '''8 of MAY'''
    
    livestock_primary_production.insert(3, 'EXIOBASE product code', '')
    livestock_primary_production.insert(4, 'EXIOBASE product', '')
    livestock_primary_production.insert(5, 'EXIOBASE extension name', '')

    correspondance2 = pd.read_csv('aux_data/List_Primary_livestock_FAO-CPA-EXIOBASE.csv', encoding="latin-1") 
    #meta_col = [col for col in correspondance2.columns if not col.startswith(("DESIRE","Un"))] 

    for i in livestock_primary_production.index:
        
        fao_code=livestock_primary_production.loc[i,['Item Code']].values[0]
        if fao_code in correspondance2['FAO item code'].values:
                    
            livestock_primary_production.loc[i,['EXIOBASE product code']]=correspondance2.loc[correspondance2['FAO item code']==fao_code,['EXIOBASE product code']].values[0]
            livestock_primary_production.loc[i,['EXIOBASE product']]=correspondance2.loc[correspondance2['FAO item code']==fao_code,['EXIOBASE product']].values[0]
            livestock_primary_production.loc[i,['EXIOBASE extension name']]=correspondance2.loc[correspondance2['FAO item code']==fao_code,['EXIOBASE extension name']].values[0]

                    
    #crops_primary_area = crops_primary.loc[(crops_primary['Unit']=='ha')]
    #crops_primary_production = crops_primary.loc[(crops_primary['Unit']=='t')]
    #







    livestock_primary_production=livestock_primary_production.drop(columns=['Item Code'])
    livestock_primary_production=livestock_primary_production.drop(columns=['Item'])

    livestock_primary_production=livestock_primary_production.groupby(['ISO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit']).sum().reset_index()
    livestock_primary_production['EXIOBASE product code'].replace('',np.nan, inplace=True)
    livestock_primary_production.dropna(subset=['EXIOBASE product code'], inplace=True)  



    
    #livestock_primary_production = livestock_primary_production[(livestock_primary_production.ISO3 != 'not found')&(livestock_primary_production['Item Code'].isin([1035,1807,1780,1808,1806]))] 
    #livestock_primary_production = pd.merge(livestock_primary_production,dfs[['EXIOBASE product code','EXIOBASE product']],left_on=livestock_primary_production['Item Code'], right_on = dfs['FAO item code'],how = 'left')
    #livestock_primary_production = livestock_primary_production.drop(columns=['key_0','Item Code'])  
    #
    #            
    #    meta_col = ['ISO3', 'EXIOBASE product code', 'EXIOBASE product','Unit']
    #    meta_col2 = [col for col in livestock_primary_production.columns if  col.startswith("Y")] 
    #    livestock_primary_production = livestock_primary_production[meta_col + meta_col2]   
        
        
        
    for code in country:
        
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 'p01.i' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.i','Cropland - Fodder crops-Cattle','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Cropland - Fodder crops-Cattle'], 'Unit':['t']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
            
            if not 'p01.j' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.j','Cropland - Fodder crops-Pigs','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.j'],'EXIOBASE product':['Pigs'],'EXIOBASE extension name':['Cropland - Fodder crops-Pigs'], 'Unit':['t']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                    
            if not 'p01.k' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.k','Cropland - Fodder crops-Poultry','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.k'],'EXIOBASE product':['Poultry'],'EXIOBASE extension name':['Cropland - Fodder crops-Poultry'], 'Unit':['t']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                         
            if not 'p01.l' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.l','Cropland - Fodder crops-Meat animals nec','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Cropland - Fodder crops-Meat animals nec'], 'Unit':['t']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                           
            if not 'p01.n' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.n','Cropland - Fodder crops-Raw milk','t'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Cropland - Fodder crops-Raw milk'], 'Unit':['t']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                   

    livestock_primary_production=livestock_primary_production.fillna(0.0) 
    livestock_primary_production=livestock_primary_production.sort_values(by=['ISO3', 'EXIOBASE product code'])

        
    '''Calculation of fallowed crops and fodder crops + Grazing area'''


    df_fallow_crop = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit'])
    df_fodder_crop = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit'])
    df_grazzing = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit'])
    df_harvested_corrected = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit'])
    df_cropland =pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit'])


    for year in relevant_years:
        df_fallow_crop[year]=""
        df_fodder_crop[year]=""
        df_grazzing[year]=""
        df_harvested_corrected[year]=""
        df_cropland[year]=""
        
    for code in country :


        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'],'EXIOBASE extension name':['Cropland - fallowed area - Paddy rice'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row])  
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'],'EXIOBASE extension name':['Cropland - fallowed area - Wheat'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'],'EXIOBASE extension name':['Cropland - fallowed area - Cereal grains nec'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'],'EXIOBASE extension name':['Cropland - fallowed area - Vegetables, fruit, nuts'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'],'EXIOBASE extension name':['Cropland - fallowed area - Oil seeds'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'],'EXIOBASE extension name':['Cropland - fallowed area - Sugar cane, sugar beet'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'],'EXIOBASE extension name':['Cropland - fallowed area - Plant-based fibers'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'],'EXIOBASE extension name':['Cropland - fallowed area - Crops nec'], 'Unit':['km2'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 


        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Cropland - Fodder crops-Cattle'], 'Unit':['km2'],year:[0]})  
        df_fodder_crop = pd.concat([df_fodder_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.j'],'EXIOBASE product':['Pigs'],'EXIOBASE extension name':['Cropland - Fodder crops-Pigs'], 'Unit':['km2'],year:[0]})  
        df_fodder_crop = pd.concat([df_fodder_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.k'],'EXIOBASE product':['Poultry'],'EXIOBASE extension name':['Cropland - Fodder crops-Poultry'], 'Unit':['km2'],year:[0]})  
        df_fodder_crop = pd.concat([df_fodder_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Cropland - Fodder crops-Meat animals nec'], 'Unit':['km2'],year:[0]})  
        df_fodder_crop = pd.concat([df_fodder_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Cropland - Fodder crops-Raw milk'], 'Unit':['km2'],year:[0]})  
        df_fodder_crop = pd.concat([df_fodder_crop,new_row]) 
            
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Permanent pastures - Grazing-Cattle'], 'Unit':['km2'],year:[0]})  
        df_grazzing = pd.concat([df_grazzing,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Permanent pastures - Grazing-Meat animals nec'], 'Unit':['km2'],year:[0]})  
        df_grazzing = pd.concat([df_grazzing,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Permanent pastures - Grazing-Raw milk'], 'Unit':['km2'],year:[0]})  
        df_grazzing = pd.concat([df_grazzing,new_row]) 
     
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row])  
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'], 'Unit':['km2'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 


        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'],'EXIOBASE extension name':['Cropland - cropped area - Paddy rice'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'],'EXIOBASE extension name':['Cropland - fallowed area - Paddy rice'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'],'EXIOBASE extension name':['Cropland - cropped area - Wheat'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'],'EXIOBASE extension name':['Cropland - fallowed area - Wheat'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'],'EXIOBASE extension name':['Cropland - cropped area - Cereal grains nec'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'],'EXIOBASE extension name':['Cropland - fallowed area - Cereal grains nec'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'],'EXIOBASE extension name':['Cropland - cropped area - Vegetables, fruit, nuts'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'],'EXIOBASE extension name':['Cropland - fallowed area - Vegetables, fruit, nuts'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'],'EXIOBASE extension name':['Cropland - cropped area - Oil seeds'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'],'EXIOBASE extension name':['Cropland - fallowed area - Oil seeds'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'],'EXIOBASE extension name':['Cropland - cropped area - Sugar cane, sugar beet'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'],'EXIOBASE extension name':['Cropland - fallowed area - Sugar cane, sugar beet'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'],'EXIOBASE extension name':['Cropland - cropped area - Plant-based fibers'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'],'EXIOBASE extension name':['Cropland - fallowed area - Plant-based fibers'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'],'EXIOBASE extension name':['Cropland - cropped area - Crops nec'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'],'EXIOBASE extension name':['Cropland - fallowed area - Crops nec'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Cropland - fallowed area-Cattle'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.j'],'EXIOBASE product':['Pigs'],'EXIOBASE extension name':['Cropland - fallowed area-Pigs'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.k'],'EXIOBASE product':['Poultry'],'EXIOBASE extension name':['Cropland - fallowed area-Poultry'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Cropland - fallowed area-Meat animals nec'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Cropland - fallowed area-Raw milk'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Permanent pastures - Grazing-Cattle'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Perm. meadows & pastures - Nat. growing - Grazing-Cattle'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cattle'],'EXIOBASE extension name':['Perm. meadows & pastures - Cultivated - Grazing-Cattle'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Permanent pastures - Grazing-Meat animals nec'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Meat animals nec'],'EXIOBASE extension name':['Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Permanent pastures - Grazing-Raw milk'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Perm. meadows & pastures - Nat. growing - Grazing-Raw milk'], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Raw milk'],'EXIOBASE extension name':['Perm. meadows & pastures - Cultivated - Grazing-Raw milk'], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['y01'],'EXIOBASE product':['Forest area'],'EXIOBASE extension name':[''], 'Unit':['km2']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p02'],'EXIOBASE product':['Final Demand'],'EXIOBASE extension name':[''], 'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':[''],'EXIOBASE product':['Artificial Surfaces'], 'EXIOBASE extension name':[''],'Unit':['km2'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])


    
    df_fallow_crop=df_fallow_crop.fillna(0.0)    
    df_fodder_crop=df_fodder_crop.fillna(0.0)  
    df_grazzing=df_grazzing.fillna(0.0)  
    df_harvested_corrected=df_harvested_corrected.fillna(0.0) 
    df_cropland = df_cropland.fillna(0.0)
    

    df_fallow_crop.iloc[:,-1:] =0.0
    df_fodder_crop.iloc[:,-1:] =0.0
    df_grazzing.iloc[:,-1:] =0.0
    df_harvested_corrected.iloc[:,-1:] =0.0
    df_cropland.iloc[:,-1:] =0.0


    FAO_items = Path("aux_data/FAOSTAT_items.csv") 
    # crops_primary_area = crops_primary.loc[(crops_primary['Unit']=='km2')]
    
    for code in country:
        # print(code)
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            cropland_total_year_country.index = cropland_total_year_country.index.get_level_values('ISO3')
            harvested_per_country.index = harvested_per_country.index.get_level_values('ISO3')
            
            natgrowing =  nat_growing.loc[((nat_growing['ISO3']==code) & (nat_growing['Item Code'] == 6659)),[year]].astype(np.float32).values
            
            
            # if cultivated_area.loc[((cultivated_area['ISO3']==code) & (cultivated_area['Item Code'] == 6656)),[year]].astype(np.float32).values:
            cultivated = cultivated_area.loc[((cultivated_area['ISO3']==code) & (cultivated_area['Item Code'] == 6656)),[year]].astype(np.float32).values
            # else :
            #     cultivated = 0
                
            grazzing= grazing_area.loc[((grazing_area['ISO3']==code) & (grazing_area['Item Code'] == 6655)),[year]].astype(np.float32).values
            forest =  forest_area.loc[((forest_area['ISO3']==code) & (forest_area['Item Code'] == 6646)),[year]].astype(np.float32).values
            final_demand =  final_demand_area.loc[((final_demand_area['ISO3']==code) & (final_demand_area['Item Code'] == 6670)),[year]].astype(np.float32).values
            artificial = landuse.loc[((landuse['ISO3']==code) & (landuse['Item Code'] == 6970)),[year]].astype(np.float32).values


            if code in (cropland_total_year_country.index.values) and code in (harvested_per_country.index.values) and code in (grazing_area.ISO3.values):
                cropped=cropland_total_year_country.loc[code,year]
                harvested=harvested_per_country.loc[code,year]
                fallowed=cropped-harvested
                if fallowed>0 :

                    fallowed_crop = fallowed/2
                    fodder_crop = fallowed/2
                    '''Values of Harvested area'''
                    
                    p01a=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.a')),[year]]
                    p01a=float(p01a.to_string(index=False, header=False))
                    p01b=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.b')),[year]]
                    p01b=float(p01b.to_string(index=False, header=False))
                    p01c=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.c')),[year]]
                    p01c=float(p01c.to_string(index=False, header=False))
                    p01d=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.d')),[year]]
                    p01d=float(p01d.to_string(index=False, header=False))
                    p01e=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.e')),[year]]
                    p01e=float(p01e.to_string(index=False, header=False))
                    p01f=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.f')),[year]]
                    p01f=float(p01f.to_string(index=False, header=False))
                    p01g=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.g')),[year]]
                    p01g=float(p01g.to_string(index=False, header=False))
                    p01h=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.h')),[year]]
                    p01h=float(p01h.to_string(index=False, header=False))
                    sum_all=p01a+p01b+p01c+p01d+p01e+p01f+p01g+p01h
            
                
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Paddy rice')),[year]] = p01a
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Wheat')),[year]] = p01b
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Cereal grains nec')),[year]] = p01c
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Vegetables, fruit, nuts')),[year]] = p01d
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Oil seeds')),[year]] = p01e
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Sugar cane, sugar beet')),[year]] = p01f
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Plant-based fibers')),[year]] = p01g
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Crops nec')),[year]] = p01h
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Forest area')),[year]] = forest
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Final Demand')),[year]] = final_demand
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Artificial Surfaces')),[year]] = artificial

                    
                    '''Values of Produced Livestock Products'''
                    p01i=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.i')),[year]]
                    p01i=float(p01i.to_string(index=False, header=False))
                    p01j=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.j')),[year]]
                    p01j=float(p01j.to_string(index=False, header=False))
                    p01k=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.k')),[year]]
                    p01k=float(p01k.to_string(index=False, header=False))
                    p01l=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.l')),[year]]
                    p01l=float(p01l.to_string(index=False, header=False))
                    p01n=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.n')),[year]]
                    p01n=float(p01n.to_string(index=False, header=False))
                    
                    sumfodder = p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk
                    sumgrazzing = p01i * factor_beef_buffalo + p01l * factor_sheep_goat + p01n * factor_milk
                    # print(code, year,sumgrazzing)
                    if not sumfodder == 0:

                        fodder_p01i = fodder_crop * (p01i * factor_beef_buffalo) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01j = fodder_crop * (p01j * factor_pig) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01k = fodder_crop * (p01k * factor_poultry) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01l = fodder_crop * (p01l * factor_sheep_goat) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01n = fodder_crop * (p01n * factor_milk) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        (code , fodder_p01i,fodder_p01j,fodder_p01k,fodder_p01l,fodder_p01n)
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.i')),[year]] = fodder_p01i
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.j')),[year]] = fodder_p01j
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.k')),[year]] = fodder_p01k
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.l')),[year]] = fodder_p01l
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.n')),[year]] = fodder_p01n
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area-Cattle')),[year]] = fodder_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area-Pigs')),[year]] = fodder_p01j
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area-Poultry')),[year]] = fodder_p01k
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area-Meat animals nec')),[year]] = fodder_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area-Raw milk')),[year]] = fodder_p01n
                        
                    if not sumgrazzing == 0:
                        grazzing_p01i = grazzing * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        grazzing_p01l = grazzing * (p01l * factor_sheep_goat) / (sumgrazzing)
                        grazzing_p01n = grazzing * (p01n * factor_milk) / (sumgrazzing)
                        
                        natgrowing_p01i = natgrowing * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        natgrowing_p01l = natgrowing * (p01l * factor_sheep_goat) / (sumgrazzing)
                        natgrowing_p01n = natgrowing * (p01n * factor_milk) / (sumgrazzing)
                
                        cultivated_p01i = cultivated * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        cultivated_p01l = cultivated * (p01l * factor_sheep_goat) / (sumgrazzing)
                        cultivated_p01n = cultivated * (p01n * factor_milk) / (sumgrazzing)
                        
                    
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.i')),[year]] = grazzing_p01i
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.l')),[year]] = grazzing_p01l
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.n')),[year]] = grazzing_p01n
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Permanent pastures - Grazing-Cattle')),[year]] = grazzing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Permanent pastures - Grazing-Meat animals nec')),[year]] = grazzing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Permanent pastures - Grazing-Raw milk')),[year]] = grazzing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Nat. growing - Grazing-Cattle')),[year]] = natgrowing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec')),[year]] = natgrowing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Nat. growing - Grazing-Raw milk')),[year]] = natgrowing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Cultivated - Grazing-Cattle')),[year]] = cultivated_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec')),[year]] = cultivated_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Cultivated - Grazing-Raw milk')),[year]] = cultivated_p01n   
        
        
                    if not sum_all == 0:
                
                        '''Values of Fallowed crops'''
        
                        fallow_p01a=fallowed_crop*p01a/sum_all
                        fallow_p01b=fallowed_crop*p01b/sum_all
                        fallow_p01c=fallowed_crop*p01c/sum_all
                        fallow_p01d=fallowed_crop*p01d/sum_all
                        fallow_p01e=fallowed_crop*p01e/sum_all
                        fallow_p01f=fallowed_crop*p01f/sum_all
                        fallow_p01g=fallowed_crop*p01g/sum_all
                        fallow_p01h=fallowed_crop*p01h/sum_all
                        
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.a')),[year]] = fallow_p01a
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.b')),[year]] = fallow_p01b
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.c')),[year]] = fallow_p01c
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.d')),[year]] = fallow_p01d
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.e')),[year]] = fallow_p01e
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.f')),[year]] = fallow_p01f
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.g')),[year]] = fallow_p01g
                        df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.h')),[year]] = fallow_p01h
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Paddy rice')),[year]] = fallow_p01a
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Wheat')),[year]] = fallow_p01b
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Cereal grains nec')),[year]] = fallow_p01c
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Vegetables, fruit, nuts')),[year]] = fallow_p01d
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Oil seeds')),[year]] = fallow_p01e
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Sugar cane, sugar beet')),[year]] = fallow_p01f
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Plant-based fibers')),[year]] = fallow_p01g
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - fallowed area - Crops nec')),[year]] = fallow_p01h
                
                
                if fallowed<0 :
                    fallowed_crop = fallowed/2
                    '''Values of Harvested area'''
                    
                    p01a=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.a')),[year]]
                    p01a=float(p01a.to_string(index=False, header=False))
                    p01b=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.b')),[year]]
                    p01b=float(p01b.to_string(index=False, header=False))
                    p01c=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.c')),[year]]
                    p01c=float(p01c.to_string(index=False, header=False))
                    p01d=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.d')),[year]]
                    p01d=float(p01d.to_string(index=False, header=False))
                    p01e=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.e')),[year]]
                    p01e=float(p01e.to_string(index=False, header=False))
                    p01f=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.f')),[year]]
                    p01f=float(p01f.to_string(index=False, header=False))
                    p01g=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.g')),[year]]
                    p01g=float(p01g.to_string(index=False, header=False))
                    p01h=crops_primary_area_modified.loc[((crops_primary_area_modified['ISO3']==code) & (crops_primary_area_modified['EXIOBASE product code']=='p01.h')),[year]]
                    p01h=float(p01h.to_string(index=False, header=False))
                    sum_all=p01a+p01b+p01c+p01d+p01e+p01f+p01g+p01h
            
                    
                    '''Values of Produced Livestock Products'''
                    
                    p01i=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.i')),[year]]
                    p01i=float(p01i.to_string(index=False, header=False))
                    p01l=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.l')),[year]]
                    p01l=float(p01l.to_string(index=False, header=False))
                    p01n=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.n')),[year]]
                    p01n=float(p01n.to_string(index=False, header=False))
                    
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Forest area')),[year]] = forest
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Final Demand')),[year]] = final_demand
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Artificial Surfaces')),[year]] = artificial

                    sumgrazzing = p01i * factor_beef_buffalo + p01l * factor_sheep_goat + p01n * factor_milk
            
                    
                    if not sumgrazzing == 0:
                        grazzing_p01i = grazzing * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        grazzing_p01l = grazzing * (p01l * factor_sheep_goat) / (sumgrazzing)
                        grazzing_p01n = grazzing * (p01n * factor_milk) / (sumgrazzing)
                        
                        natgrowing_p01i = natgrowing * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        natgrowing_p01l = natgrowing * (p01l * factor_sheep_goat) / (sumgrazzing)
                        natgrowing_p01n = natgrowing * (p01n * factor_milk) / (sumgrazzing)
                                                
                        cultivated_p01i = cultivated * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        cultivated_p01l = cultivated * (p01l * factor_sheep_goat) / (sumgrazzing)
                        cultivated_p01n = cultivated * (p01n * factor_milk) / (sumgrazzing)

                        
                    
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.i')),[year]] = grazzing_p01i
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.l')),[year]] = grazzing_p01l
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.n')),[year]] = grazzing_p01n
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Permanent pastures - Grazing-Cattle')),[year]] = grazzing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Permanent pastures - Grazing-Meat animals nec')),[year]] = grazzing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Permanent pastures - Grazing-Raw milk')),[year]] = grazzing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Nat. growing - Grazing-Cattle')),[year]] = natgrowing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec')),[year]] = natgrowing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Nat. growing - Grazing-Raw milk')),[year]] = natgrowing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Cultivated - Grazing-Cattle')),[year]] = cultivated_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec')),[year]] = cultivated_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Perm. meadows & pastures - Cultivated - Grazing-Raw milk')),[year]] = cultivated_p01n   
                        
                    if not sum_all == 0:
                
                        '''Values of Fallowed crops'''
                        
                        new_p01a=cropped*p01a/sum_all
                        new_p01b=cropped*p01b/sum_all
                        new_p01c=cropped*p01c/sum_all
                        new_p01d=cropped*p01d/sum_all
                        new_p01e=cropped*p01e/sum_all
                        new_p01f=cropped*p01f/sum_all
                        new_p01g=cropped*p01g/sum_all
                        new_p01h=cropped*p01h/sum_all
                        
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.a')),[year]] = new_p01a
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.b')),[year]] = new_p01b
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.c')),[year]] = new_p01c
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.d')),[year]] = new_p01d
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.f')),[year]] = new_p01f
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.g')),[year]] = new_p01g
                        df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.h')),[year]] = new_p01h
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Paddy rice')),[year]] = new_p01a
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Wheat')),[year]] = new_p01b
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Cereal grains nec')),[year]] = new_p01c
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Vegetables, fruit, nuts')),[year]] = new_p01d
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Oil seeds')),[year]] = new_p01e
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Sugar cane, sugar beet')),[year]] = new_p01f
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Plant-based fibers')),[year]] = new_p01g
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE extension name']=='Cropland - cropped area - Crops nec')),[year]] = new_p01h
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'' : 'ar'})
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'p02' : ''})
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'y01' : 'p02'})
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'ar' : 'y01'})

    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'' : 'Y01','y01' : 'ar','p02' : 'for'})
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'p02' : ''})
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'y01' : 'p02'})
    df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'Y01' : 'y01'})

    df_cropland.reset_index(drop=True, inplace=True)

    for row in df_cropland.iterrows():
       if (df_cropland.loc[row[0]]['EXIOBASE product code'] == 'p02'):
           df_cropland.loc[row[0],'EXIOBASE product']= 'Products of forestry, logging and related services (02)'
           df_cropland.loc[row[0],'EXIOBASE extension name']= 'Forest'
           
       if (df_cropland.loc[row[0]]['EXIOBASE product code'] == 'y01'):
           df_cropland.loc[row[0],'EXIOBASE product']= 'Final consumption expenditure by households'         
           df_cropland.loc[row[0],'EXIOBASE extension name']= 'Artificial Surfaces'         

       if (df_cropland.loc[row[0]]['EXIOBASE product code'] == ''):
           df_cropland.loc[row[0],'EXIOBASE product']= 'Not Assigned'         
           df_cropland.loc[row[0],'EXIOBASE extension name']= 'Other land'   


    # df_cropland['EXIOBASE product code'] = df_cropland['EXIOBASE product code'].replace({'Y01' : 'y01','p02' : '','y01' : 'p02'})

    # df_cropland['EXIOBASE product'] = df_cropland['EXIOBASE product'].replace({'Forest area' : 'Products of forestry, logging and related services (02)' ,'Final Demand' : 'Final consumption expenditure by households'})
    #df_harvested_corrected = df_harvested_corrected.drop('EXIOBASE extension name',axis=1)  
    with pd.ExcelWriter("EXIOBASE_allocation_FAO.xlsx") as writer:    
    #writer = pd.ExcelWriter('Cropland.xlsx', engine='xlsxwriter')
        crops_primary_production.to_excel(writer, sheet_name='Production',index = False)
        crops_primary_production_modified.to_excel(writer, sheet_name='Production_noCotton',index = False)
        crops_primary_area.to_excel(writer, sheet_name='Harvested_per_product',index = False)
        crops_primary_area_modified.to_excel(writer, sheet_name='Harvested_per_product_noCotton',index = False)
        cropland_total_year_country.to_excel(writer, sheet_name='Cropped_total')
        harvested_per_country.to_excel(writer, sheet_name='Harvested_total')
        livestock_primary_production.to_excel(writer, sheet_name='Production_livestock',index = False)
        df_fallow_crop.to_excel(writer, sheet_name='Fallow crop',index = False)
        df_fodder_crop.to_excel(writer, sheet_name='Fodder crop')
        df_grazzing.to_excel(writer, sheet_name='Grazzing',index = False)
        #df_harvested_corrected.to_excel(writer, sheet_name='harvested corrected',index = False)
        df_cropland.to_excel(writer, sheet_name='final cropland',index = False)
    writer
    
    shutil.copy("EXIOBASE_allocation_FAO.xlsx", str(final_path) + "/EXIOBASE_allocation_FAO.xlsx")
    os.remove("EXIOBASE_allocation_FAO.xlsx")

