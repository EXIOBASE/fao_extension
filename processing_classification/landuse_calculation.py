import pandas as pd
import numpy as np
from pathlib import Path
from make_years import make_valid_fao_year as mvy 
import yaml
from typing import List

def landuse_allocation(years: List[int], storage_path: Path) : 

    with open(r'aux_data/parameters.yaml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    
    with open(r'aux_data/country.yaml') as file:
        country = yaml.load(file, Loader=yaml.FullLoader) 
        
        
    seed_cotton_p01e=0.63
    seed_cotton_p01g=0.37

    factor_beef_buffalo=20.0
    factor_milk=1.0
    factor_poultry=1.0
    factor_pig=2.0
    factor_sheep_goat=10.0

    '''Crops promary -> Crops primary area and crops primary production'''

    crops_primary = pd.read_csv('final_crops_primary.csv', encoding="latin-1") 
    crops_primary.insert(3, 'EXIOBASE product code', '')
    crops_primary.insert(4, 'EXIOBASE product', '')


    item_xlsx = Path("aux_data/List_Primary production_FAO-CPA-EXIOBASE.xlsx") 
    item_sheet = 'Correspondance_FAO-CPA-EXIOBASE' 

    correspondance = pd.read_excel(item_xlsx,item_sheet)
    meta_col = [col for col in correspondance.columns if not col.startswith(("DESIRE","Un"))] 

    for i in crops_primary.index:
        
        fao_code=crops_primary.loc[i,['Item Code']].values[0]
        if fao_code in correspondance['FAO item code'].values:
                    
            crops_primary.loc[i,['EXIOBASE product code']]=correspondance.loc[correspondance['FAO item code']==fao_code,['EXIOBASE product code']].values[0]
            crops_primary.loc[i,['EXIOBASE product']]=correspondance.loc[correspondance['FAO item code']==fao_code,['EXIOBASE product']].values[0]
        
                    
    crops_primary_area = crops_primary.loc[(crops_primary['Unit']=='ha')]
    crops_primary_production = crops_primary.loc[(crops_primary['Unit']=='tonnes')]



        
        
        
    '''crop production'''
    # new name is : crops_primary_production
    #called df before modification


    '''crop harvest'''
    #df2 = pd.read_csv('../Fill_4_tables/crop_harvest/crop_harvest.csv', encoding="latin-1")
    #new name is : crops_primary_area


    '''land use'''
    landuse = pd.read_csv('landuse_final_runall.csv', encoding="latin-1")
    #df3 = pd.read_csv('final_landuse.csv', encoding="latin-1")



    '''Livestock production'''

    #df_livestock_all = pd.read_csv('../Fill_4_tables/Livestock_prod/livestock_prod.csv', encoding="latin-1")
    livestock_primary_production = pd.read_csv('final_livestock_primary.csv', encoding="latin-1") 
    #livestock_primary.insert(3, 'EXIOBASE product code', '')
    #livestock_primary.insert(4, 'EXIOBASE product', '')



    #dfs = pd.read_csv('../aux_data/List_Primary_livestock_FAO-CPA-EXIOBASE.csv', encoding="latin-1")
        
        
        
        

    #land use#
    grazing_area = pd.read_csv('landuse_final_runall.csv', encoding="latin-1")
    forest_area = pd.read_csv('landuse_final_runall.csv', encoding="latin-1")
    final_demand_area = pd.read_csv('landuse_final_runall.csv', encoding="latin-1")
        

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


    grazing_area=grazing_area.fillna(0)  
    forest_area=forest_area.fillna(0)
    final_demand_area = final_demand_area.fillna(0)
        


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
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.e','Oil seeds','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        if not 'p01.g' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.g','Plant-based fibers','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])

        if not 'p01.a' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.a','Paddy rice','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])

        if not 'p01.b' in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.b','Wheat','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        

        if not 'p01.c'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.c','Cereal grains nec','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
    
        if not 'p01.d'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        
        if not 'p01.f'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        
        if not 'p01.h'  in (crops_primary_production_modified.loc[crops_primary_production_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_production_modified = crops_primary_production_modified.append(pd.Series([code,'p01.h','Crops nec','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'], 'Unit':['tonnes']})  
            crops_primary_production_modified = pd.concat([crops_primary_production_modified,new_row])
        

    crops_primary_production_modified=crops_primary_production_modified.fillna(0)   
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
    crops_primary_production_modified.to_csv('crops_primary_production_final1.csv', index=False)   



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



    #list_ISO3_2 = list(crops_primary_area_modified['ISO3'])
    #res = [] 
    #for i in list_ISO3_2: 
    #    if i not in res: 
    #        res.append(i) 


    list_exio = list(crops_primary_area_modified['EXIOBASE product code'])
    res2 = []
    for i in list_exio: 
        if i not in res2: 
            res2.append(i) 
    


    for code in country :
        if not 'p01.e' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.e','Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])
            
        if not 'p01.g' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.g','Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])
                    
        if not 'p01.a' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.a','Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])


        if not 'p01.b' in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.b','Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])
    
        if not 'p01.c'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.c','Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])    
        if not 'p01.d'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])    
        if not 'p01.f'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])    
        if not 'p01.h'  in (crops_primary_area_modified.loc[crops_primary_area_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            #crops_primary_area_modified = crops_primary_area_modified.append(pd.Series([code,'p01.h','Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
            new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'], 'Unit':['ha']})  
            crops_primary_area_modified = pd.concat([crops_primary_area_modified,new_row])

    crops_primary_area_modified=crops_primary_area_modified.fillna(0)   
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
        
    crops_primary_area_modified.to_csv('crops_primary_area_modified_final1.csv',index=False)
        
        
        
        
    """Get the harvest crop per ha per year per country"""

    harvested_per_country=crops_primary_area.groupby(['ISO3','Unit']).sum()

    '''select the total cropped land from FAOSTAT'''

    cropland_FAO = landuse[(landuse.ISO3 != 'not found')&(landuse['Item Code']==6620)]
        
    '''
    We can split permanent meadows and pastures (item 6655) unto
    FAO item 6659 : naturally growing 
    FAO item 6656 : cultivated

    '''


    nat_growing = grazing_area.copy()
    cultivated_area = grazing_area.copy()
    
    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6655 in (grazing_area.loc[grazing_area['ISO3']==code, ["Item Code"]].values) :
                #grazing_area = grazing_area.append(pd.Series([6655,'Land under perm. meadows and pastures','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                new_row = pd.DataFrame({'Item Code':[6655],'Item':['Land under perm. meadows and pastures'],'Unit':['1000ha'], 'ISO3':[code],year:[0]})  
                grazing_area = pd.concat([grazing_area,new_row])
            
    grazing_area = grazing_area[(grazing_area.ISO3 != 'not found')&(grazing_area['Item Code']==6655)]
    grazing_area=grazing_area.fillna(0)  

    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6659 in (nat_growing.loc[nat_growing['ISO3']==code, ["Item Code"]].values) :
                #nat_growing = nat_growing.append(pd.Series([6659,'Perm. meadows & pastures - Nat. growing','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                new_row = pd.DataFrame({'Item Code':[6659],'Item':['Perm. meadows & pastures - Nat. growing'],'Unit':['1000ha'], 'ISO3':[code],year:[0]})  
                nat_growing = pd.concat([nat_growing,new_row])            
    nat_growing = nat_growing[(nat_growing.ISO3 != 'not found')&(nat_growing['Item Code']==6659)]
    nat_growing = nat_growing.fillna(0)     

    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6656 in (cultivated_area.loc[cultivated_area['ISO3']==code, ["Item Code"]].values) :
                #cultivated_area = cultivated_area.append(pd.Series([6656,'Perm. meadows & pastures - Cultivated','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                new_row = pd.DataFrame({'Item Code':[6656],'Item':['Perm. meadows & pastures - Cultivated'],'Unit':['1000ha'], 'ISO3':[code],year:[0]})  
                cultivated_area = pd.concat([cultivated_area,new_row])            
    cultivated_area = cultivated_area[(cultivated_area.ISO3 != 'not found')&(cultivated_area['Item Code']==6656)]
    cultivated_area = cultivated_area.fillna(0)     





    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6670 in (final_demand_area.loc[final_demand_area['ISO3']==code, ["Item Code"]].values) :
                #final_demand_area = final_demand_area.append(pd.Series([6670,'Final Demand','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                new_row = pd.DataFrame({'Item Code':[6670],'Item':['Final Demand'],'Unit':['1000ha'], 'ISO3':[code],year:[0]})  
                final_demand_area = pd.concat([final_demand_area,new_row])             
    
    final_demand_area = final_demand_area[(final_demand_area.ISO3 != 'not found')&(final_demand_area['Item Code']==6670)]
    final_demand_area = final_demand_area.fillna(0) 


    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            if not 6646 in (forest_area.loc[forest_area['ISO3']==code, ["Item Code"]].values) :
                #forest_area = forest_area.append(pd.Series([6646,'Forest Land','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                new_row = pd.DataFrame({'Item Code':[6646],'Item':['Forest Land'],'Unit':['1000ha'], 'ISO3':[code],year:[0]})  
                forest_area = pd.concat([forest_area,new_row])             
                
    forest_area = forest_area[(forest_area.ISO3 != 'not found')&(forest_area.Unit != 'million tonnes')&(forest_area['Item Code']==6646)]
    forest_area = forest_area.fillna(0)    

    '''
    A PARTIR DE LA IL FAUT MODIFIER
    '''
    Unit='ha'

    cropland_total = []
    for code in country:
        for year in relevant_years:
            cropland = 1000*(cropland_FAO[cropland_FAO['ISO3'] == code][year]).astype(np.float32).values
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

    livestock_primary_production = pd.read_csv('final_livestock_primary.csv', encoding="latin-1") 
    livestock_primary_production = livestock_primary_production.loc[(livestock_primary_production['Unit']=='tonnes')]

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
                beef =0
            if 947 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                buffalo = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==947)),[year]].values[0]
            else :
                buffalo = 0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1806)),[year]] = beef + buffalo
            
            
            
            
            if 1089 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                bird = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1089)),[year]].values[0]
            else :
                bird =0
            if 1058 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                chicken = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1058)),[year]].values[0]
            else :
                chicken = 0
            if 1069 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                duck = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1069)),[year]].values[0]
            else :
                duck =0
            if 1073 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                goose = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1073)),[year]].values[0]
            else :
                goose = 0
            if 1080 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                turkey = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1080)),[year]].values[0]
            else :
                turkey = 0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1808)),[year]] = bird + chicken + duck + goose + turkey


            if 951 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_buffalo = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==951)),[year]].values[0]
            else :
                milk_buffalo =0
            if 1130 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_camel = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1130)),[year]].values[0]
            else :
                milk_camel = 0
            if 882 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_cow = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==882)),[year]].values[0]
            else :
                milk_cow =0
            if 1020 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_goat = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1020)),[year]].values[0]
            else :
                milk_goat = 0
            if 982 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                milk_sheep = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==982)),[year]].values[0]
            else :
                milk_sheep = 0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1780)),[year]] = milk_buffalo + milk_camel + milk_cow + milk_goat + milk_sheep


            if 1017 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                meat_goat = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1017)),[year]].values[0]
            else :
                meat_goat =0
            if 977 in livestock_primary_production.loc[livestock_primary_production['ISO3']==code,['Item Code']].values:
                meat_sheep = livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==977)),[year]].values[0]
            else :
                meat_sheep = 0
            livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['Item Code']==1807)),[year]] = meat_goat + meat_sheep
            
            

    #crops_primary = pd.read_csv('final_cropland_primary.csv', encoding="latin-1") 
    livestock_primary_production.insert(3, 'EXIOBASE product code', '')
    livestock_primary_production.insert(4, 'EXIOBASE product', '')

    correspondance2 = pd.read_csv('aux_data/List_Primary_livestock_FAO-CPA-EXIOBASE.csv', encoding="latin-1") 
    #meta_col = [col for col in correspondance2.columns if not col.startswith(("DESIRE","Un"))] 

    for i in livestock_primary_production.index:
        
        fao_code=livestock_primary_production.loc[i,['Item Code']].values[0]
        if fao_code in correspondance2['FAO item code'].values:
                    
            livestock_primary_production.loc[i,['EXIOBASE product code']]=correspondance2.loc[correspondance2['FAO item code']==fao_code,['EXIOBASE product code']].values[0]
            livestock_primary_production.loc[i,['EXIOBASE product']]=correspondance2.loc[correspondance2['FAO item code']==fao_code,['EXIOBASE product']].values[0]
        
                    
    #crops_primary_area = crops_primary.loc[(crops_primary['Unit']=='ha')]
    #crops_primary_production = crops_primary.loc[(crops_primary['Unit']=='tonnes')]
    #







    livestock_primary_production=livestock_primary_production.drop(columns=['Item Code'])
    livestock_primary_production=livestock_primary_production.drop(columns=['Item'])

    livestock_primary_production=livestock_primary_production.groupby(['ISO3','EXIOBASE product code','EXIOBASE product','Unit']).sum().reset_index()
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
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.i','Cropland - Fodder crops-Cattle','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cropland - Fodder crops-Cattle'], 'Unit':['tonnes']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
            
            if not 'p01.j' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.j','Cropland - Fodder crops-Pigs','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.j'],'EXIOBASE product':['Cropland - Fodder crops-Pigs'], 'Unit':['tonnes']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                    
            if not 'p01.k' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.k','Cropland - Fodder crops-Poultry','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.k'],'EXIOBASE product':['Cropland - Fodder crops-Poultry'], 'Unit':['tonnes']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                         
            if not 'p01.l' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.l','Cropland - Fodder crops-Meat animals nec','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Cropland - Fodder crops-Meat animals nec'], 'Unit':['tonnes']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                           
            if not 'p01.n' in (livestock_primary_production.loc[livestock_primary_production['ISO3']==code, ["EXIOBASE product code"]].values) :
                #livestock_primary_production = livestock_primary_production.append(pd.Series([code,'p01.n','Cropland - Fodder crops-Raw milk','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Cropland - Fodder crops-Raw milk'], 'Unit':['tonnes']})  
                livestock_primary_production = pd.concat([livestock_primary_production,new_row])  
                   

    livestock_primary_production=livestock_primary_production.fillna(0) 
    livestock_primary_production=livestock_primary_production.sort_values(by=['ISO3', 'EXIOBASE product code'])

        
    '''Calculation of fallowed crops and fodder crops + Grazing area'''


    df_fallow_crop = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','Unit'])
    df_fodder_crop = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','Unit'])
    df_grazzing = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','Unit'])
    df_harvested_corrected = pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','Unit'])
    df_cropland =pd.DataFrame(columns = ['ISO3', 'EXIOBASE product code','EXIOBASE product','Unit'])


    for year in relevant_years:
        df_fallow_crop[year]=""
        df_fodder_crop[year]=""
        df_grazzing[year]=""
        df_harvested_corrected[year]=""
        df_cropland[year]=""
        
    for code in country :
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.a','Cropland - fallowed area - Paddy rice','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.b','Cropland - fallowed area - Wheat','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.c','Cropland - fallowed area - Cereal grains nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.d','Cropland - fallowed area - Vegetables, fruit, nuts','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.e','Cropland - fallowed area - Oil seeds','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.f','Cropland - fallowed area - Sugar cane, sugar beet','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.g','Cropland - fallowed area - Plant-based fibers','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.h','Cropland - fallowed area - Crops nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.i','Cropland - Fodder crops-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.j','Cropland - Fodder crops-Pigs','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.k','Cropland - Fodder crops-Poultry','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.l','Cropland - Fodder crops-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.n','Cropland - Fodder crops-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)

        #df_grazzing = df_grazzing.append(pd.Series([code,'p01.i','Permanent pastures - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_grazzing = df_grazzing.append(pd.Series([code,'p01.l','Permanent pastures - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_grazzing = df_grazzing.append(pd.Series([code,'p01.n','Permanent pastures - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)

        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.a','Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.b','Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.c','Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.e','Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.g','Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.h','Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        #df_cropland = df_cropland.append(pd.Series([code,'p01.a','Cropland - cropped area - Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.a','Cropland - fallowed area - Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.b','Cropland - cropped area - Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.b','Cropland - fallowed area - Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.c','Cropland - cropped area - Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.c','Cropland - fallowed area - Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.d','Cropland - cropped area - Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.d','Cropland - fallowed area - Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.e','Cropland - cropped area - Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.e','Cropland - fallowed area - Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.f','Cropland - cropped area - Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.f','Cropland - fallowed area - Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.g','Cropland - cropped area - Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.g','Cropland - fallowed area - Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.h','Cropland - cropped area - Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.h','Cropland - fallowed area - Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.i','Cropland - fallowed area-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.j','Cropland - fallowed area-Pigs','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.k','Cropland - fallowed area-Poultry','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.l','Cropland - fallowed area-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.n','Cropland - fallowed area-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.i','Permanent pastures - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.i','Perm. meadows & pastures - Nat. growing - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.i','Perm. meadows & pastures - Cultivated - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.l','Permanent pastures - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.l','Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.l','Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.n','Permanent pastures - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.n','Perm. meadows & pastures - Nat. growing - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'p01.n','Perm. meadows & pastures - Cultivated - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)     
        #df_cropland = df_cropland.append(pd.Series([code,'','Forest area','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        #df_cropland = df_cropland.append(pd.Series([code,'','Final Demand','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
                                                                                             

        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Cropland - fallowed area - Paddy rice'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row])  
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Cropland - fallowed area - Wheat'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cropland - fallowed area - Cereal grains nec'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Cropland - fallowed area - Vegetables, fruit, nuts'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Cropland - fallowed area - Oil seeds'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Cropland - fallowed area - Sugar cane, sugar beet'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Cropland - fallowed area - Plant-based fibers'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Cropland - fallowed area - Crops nec'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 


        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cropland - Fodder crops-Cattle'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.j'],'EXIOBASE product':['Cropland - Fodder crops-Pigs'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.k'],'EXIOBASE product':['Cropland - Fodder crops-Poultry'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Cropland - Fodder crops-Meat animals nec'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Cropland - Fodder crops-Raw milk'], 'Unit':['ha'],year:[0]})  
        df_fallow_crop = pd.concat([df_fallow_crop,new_row]) 
            
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Permanent pastures - Grazing-Cattle'], 'Unit':['ha'],year:[0]})  
        df_grazzing = pd.concat([df_grazzing,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Permanent pastures - Grazing-Meat animals nec'], 'Unit':['ha'],year:[0]})  
        df_grazzing = pd.concat([df_grazzing,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Permanent pastures - Grazing-Raw milk'], 'Unit':['ha'],year:[0]})  
        df_grazzing = pd.concat([df_grazzing,new_row]) 
     
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Paddy rice'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row])  
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Wheat'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cereal grains nec'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Vegetables, fruit, nuts'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Oil seeds'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Sugar cane, sugar beet'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Plant-based fibers'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Crops nec'], 'Unit':['ha'],year:[0]})  
        df_harvested_corrected = pd.concat([df_harvested_corrected,new_row]) 

        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Cropland - cropped area - Paddy rice'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.a'],'EXIOBASE product':['Cropland - fallowed area - Paddy rice'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Cropland - cropped area - Wheat'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.b'],'EXIOBASE product':['Cropland - fallowed area - Wheat'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cropland - cropped area - Cereal grains nec'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.c'],'EXIOBASE product':['Cropland - fallowed area - Cereal grains nec'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Cropland - cropped area - Vegetables, fruit, nuts'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.d'],'EXIOBASE product':['Cropland - fallowed area - Vegetables, fruit, nuts'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Cropland - cropped area - Oil seeds'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.e'],'EXIOBASE product':['Cropland - fallowed area - Oil seeds'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Cropland - cropped area - Sugar cane, sugar beet'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.f'],'EXIOBASE product':['Cropland - fallowed area - Sugar cane, sugar beet'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Cropland - cropped area - Plant-based fibers'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.g'],'EXIOBASE product':['Cropland - fallowed area - Plant-based fibers'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Cropland - cropped area - Crops nec'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.h'],'EXIOBASE product':['Cropland - fallowed area - Crops nec'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Cropland - fallowed area-Cattle'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.j'],'EXIOBASE product':['Cropland - fallowed area-Pigs'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.k'],'EXIOBASE product':['Cropland - fallowed area-Poultry'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Cropland - fallowed area-Meat animals nec'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Cropland - fallowed area-Raw milk'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Permanent pastures - Grazing-Cattle'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Perm. meadows & pastures - Nat. growing - Grazing-Cattle'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.i'],'EXIOBASE product':['Perm. meadows & pastures - Cultivated - Grazing-Cattle'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Permanent pastures - Grazing-Meat animals nec'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.l'],'EXIOBASE product':['Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Permanent pastures - Grazing-Raw milk'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Perm. meadows & pastures - Nat. growing - Grazing-Raw milk'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':['p01.n'],'EXIOBASE product':['Perm. meadows & pastures - Cultivated - Grazing-Raw milk'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':[''],'EXIOBASE product':['Forest area'], 'Unit':['ha']})  
        df_cropland = pd.concat([df_cropland,new_row]) 
        new_row = pd.DataFrame({'ISO3':[code],'EXIOBASE product code':[''],'EXIOBASE product':['Final Demand'], 'Unit':['ha'],year:[0]})  
        df_cropland = pd.concat([df_cropland,new_row])



        
    df_fallow_crop=df_fallow_crop.fillna(0)    
    df_fodder_crop=df_fodder_crop.fillna(0)  
    df_grazzing=df_grazzing.fillna(0)  
    df_harvested_corrected=df_harvested_corrected.fillna(0) 
    df_cropland = df_cropland.fillna(0)

    for code in country:
        print(code)
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        else : 
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]

        for year in relevant_years:
            cropland_total_year_country.index = cropland_total_year_country.index.get_level_values('ISO3')
            harvested_per_country.index = harvested_per_country.index.get_level_values('ISO3')
            
            natgrowing = 1000 * nat_growing.loc[((nat_growing['ISO3']==code) & (nat_growing['Item Code'] == 6659)),[year]].astype(np.float32).values
            cultivated = 1000 * cultivated_area.loc[((cultivated_area['ISO3']==code) & (cultivated_area['Item Code'] == 6656)),[year]].astype(np.float32).values
            grazzing=1000 * grazing_area.loc[((grazing_area['ISO3']==code) & (grazing_area['Item Code'] == 6655)),[year]].astype(np.float32).values
            forest = 1000 * forest_area.loc[((forest_area['ISO3']==code) & (forest_area['Item Code'] == 6646)),[year]].astype(np.float32).values
            final_demand = 1000 * final_demand_area.loc[((final_demand_area['ISO3']==code) & (final_demand_area['Item Code'] == 6670)),[year]].astype(np.float32).values


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
            
                
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Paddy rice')),[year]] = p01a
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Wheat')),[year]] = p01b
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Cereal grains nec')),[year]] = p01c
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Vegetables, fruit, nuts')),[year]] = p01d
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Oil seeds')),[year]] = p01e
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Sugar cane, sugar beet')),[year]] = p01f
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Plant-based fibers')),[year]] = p01g
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Crops nec')),[year]] = p01h
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Forest area')),[year]] = forest
                    df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Final Demand')),[year]] = final_demand
                    
                    '''Values of Produced Livestock Products'''
                    livestock_primary_production.to_csv('pb_livestock.csv',index=False)
                    p01i=livestock_primary_production.loc[((livestock_primary_production['ISO3']==code) & (livestock_primary_production['EXIOBASE product code']=='p01.i')),[year]]
                    print(p01i)
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
                    
            
                    if not sumfodder == 0:
                        fodder_p01i = fodder_crop * (p01i * factor_beef_buffalo) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01j = fodder_crop * (p01j * factor_pig) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01k = fodder_crop * (p01k * factor_poultry) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01l = fodder_crop * (p01l * factor_sheep_goat) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        fodder_p01n = fodder_crop * (p01n * factor_milk) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.i')),[year]] = fodder_p01i
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.j')),[year]] = fodder_p01j
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.k')),[year]] = fodder_p01k
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.l')),[year]] = fodder_p01l
                        df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.n')),[year]] = fodder_p01n
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area-Cattle')),[year]] = fodder_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area-Pigs')),[year]] = fodder_p01j
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area-Poultry')),[year]] = fodder_p01k
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area-Meat animals nec')),[year]] = fodder_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area-Raw milk')),[year]] = fodder_p01n
                        
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
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Permanent pastures - Grazing-Cattle')),[year]] = grazzing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Permanent pastures - Grazing-Meat animals nec')),[year]] = grazzing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Permanent pastures - Grazing-Raw milk')),[year]] = grazzing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Nat. growing - Grazing-Cattle')),[year]] = natgrowing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec')),[year]] = natgrowing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Nat. growing - Grazing-Raw milk')),[year]] = natgrowing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Cultivated - Grazing-Cattle')),[year]] = cultivated_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec')),[year]] = cultivated_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Cultivated - Grazing-Raw milk')),[year]] = cultivated_p01n   
        
        
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
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Paddy rice')),[year]] = fallow_p01a
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Wheat')),[year]] = fallow_p01b
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Cereal grains nec')),[year]] = fallow_p01c
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Vegetables, fruit, nuts')),[year]] = fallow_p01d
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Oil seeds')),[year]] = fallow_p01e
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Sugar cane, sugar beet')),[year]] = fallow_p01f
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Plant-based fibers')),[year]] = fallow_p01g
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - fallowed area - Crops nec')),[year]] = fallow_p01h
                
                
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
                    
                    sumgrazzing = p01i * factor_beef_buffalo + p01l * factor_sheep_goat + p01n * factor_milk
                    
            
                    
                    if not sumgrazzing == 0:
                        grazzing_p01i = grazzing * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        grazzing_p01l = grazzing * (p01l * factor_sheep_goat) / (sumgrazzing)
                        grazzing_p01n = grazzing * (p01n * factor_milk) / (sumgrazzing)
                        
                        natgrowing_p01i = natgrowing * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        natgrowing_p01l = natgrowing * (p01l * factor_sheep_goat) / (sumgrazzing)
                        natgrowing_p01n = natgrowing * (p01n * factor_milk) / (sumgrazzing)
                                                
                    

                        
                    
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.i')),[year]] = grazzing_p01i
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.l')),[year]] = grazzing_p01l
                        df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.n')),[year]] = grazzing_p01n
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Permanent pastures - Grazing-Cattle')),[year]] = grazzing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Permanent pastures - Grazing-Meat animals nec')),[year]] = grazzing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Permanent pastures - Grazing-Raw milk')),[year]] = grazzing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Nat. growing - Grazing-Cattle')),[year]] = natgrowing_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec')),[year]] = natgrowing_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Nat. growing - Grazing-Raw milk')),[year]] = natgrowing_p01n                     
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Cultivated - Grazing-Cattle')),[year]] = cultivated_p01i
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec')),[year]] = cultivated_p01l
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Perm. meadows & pastures - Cultivated - Grazing-Raw milk')),[year]] = cultivated_p01n   
                        
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
                        
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Paddy rice')),[year]] = new_p01a
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Wheat')),[year]] = new_p01b
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Cereal grains nec')),[year]] = new_p01c
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Vegetables, fruit, nuts')),[year]] = new_p01d
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Oil seeds')),[year]] = new_p01e
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Sugar cane, sugar beet')),[year]] = new_p01f
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Plant-based fibers')),[year]] = new_p01g
                        df_cropland.loc[((df_cropland['ISO3']==code) & (df_cropland['EXIOBASE product']=='Cropland - cropped area - Crops nec')),[year]] = new_p01h
            
        
    with pd.ExcelWriter("Cropland.xlsx") as writer:    
    #writer = pd.ExcelWriter('Cropland.xlsx', engine='xlsxwriter')
        crops_primary_production.to_excel(writer, sheet_name='Production')
        crops_primary_production_modified.to_excel(writer, sheet_name='Production_noCotton')
        crops_primary_area.to_excel(writer, sheet_name='Harvested_per_product')
        crops_primary_area_modified.to_excel(writer, sheet_name='Harvested_per_product_noCotton')
        cropland_total_year_country.to_excel(writer, sheet_name='Cropped_total')
        harvested_per_country.to_excel(writer, sheet_name='Harvested_total')
        livestock_primary_production.to_excel(writer, sheet_name='Production_livestock')
        df_fallow_crop.to_excel(writer, sheet_name='Fallow crop')
        df_fodder_crop.to_excel(writer, sheet_name='Fodder crop')
        df_grazzing.to_excel(writer, sheet_name='Grazzing')
        df_harvested_corrected.to_excel(writer, sheet_name='harvested corrected')
        df_cropland.to_excel(writer, sheet_name='final cropland')
    writer