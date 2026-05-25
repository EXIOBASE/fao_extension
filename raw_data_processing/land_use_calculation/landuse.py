from pathlib import Path
import pandas as pd
import yaml
from make_years import make_valid_fao_year as mvy
from pipeline_config import apply_year_window, require_year_columns, year_columns
import fill_country_area as fca
import zero_assumption as za
from typing import List
#import ray
#import sys
import case1 
import case2
import case3
import case4
import case_small_diagrams as csd
import adjustment as adj
import regression_implant as reg
import regression_implant2 as reg2



#import regression_implant3 as reg3
#import fill_cells
#import adjustment2 as adj2



def whole_landuse_calculation(years: List[int], storage_path: Path):
    data_path = Path(storage_path / "data")
    #print(sys.path)
    with open(r'aux_data/parameters.yaml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    parameters = apply_year_window(parameters, years)
        
    with open(r'aux_data/items_primary.yaml') as file:
        items_primary = yaml.load(file, Loader=yaml.FullLoader)
        
    with open(r'aux_data/diagram.yaml') as file:
        diagram = yaml.load(file, Loader=yaml.FullLoader)


    with open(r'aux_data/unique_items.yaml') as file:
        unique_items = yaml.load(file, Loader=yaml.FullLoader)    
        
    with open(r'aux_data/small_diagrams.yaml') as file:
        small_diagrams = yaml.load(file, Loader=yaml.FullLoader) 

    with open(r'aux_data/items_small_diagrams.yaml') as file:
        items_small_diagrams = yaml.load(file, Loader=yaml.FullLoader) 
        
    with open(r'aux_data/country.yaml') as file:
        country = yaml.load(file, Loader=yaml.FullLoader) 

    relevant_years = year_columns(years)

    landcover = pd.read_csv(data_path/'refreshed_land_cover.csv', encoding="latin-1") 
    landcover = landcover[landcover['Element Code'] == 5008]
    meta_col = [
        col
        for col in landcover.columns
        if not col.startswith(("Y", "key", "Element","Area"))
    ]
    requested_landcover_years = [
        col
        for col in landcover.columns
        if col.startswith(("Y"))
        and int(col[1:]) in set(int(year) for year in years)
    ]
    missing_landcover_years = [
        col for col in relevant_years
        if int(col[1:]) >= 1992 and col not in landcover.columns
    ]
    if missing_landcover_years:
        raise KeyError(
            "refreshed_land_cover.csv is missing requested year columns: "
            f"{', '.join(missing_landcover_years)}"
        )
    
    landcover = landcover[meta_col + requested_landcover_years]
    first_column = landcover.pop('ISO3') 
    landcover.insert(0, 'ISO3', first_column) 

    landuse = pd.read_csv(data_path/'refreshed_land_use.csv', encoding="latin-1") 



    col_years = require_year_columns(landuse, years, "refreshed_land_use.csv")
    
    meta_col = ["ISO3", "Item Code", "Item","Unit"] 
            
    landuse=landuse[meta_col + relevant_years]
    landuse = landuse[landuse['Unit'] != 'million t']
    landuse = landuse[landuse['Unit'] != '%']
    landuse = landuse[landuse['Unit'] != 'ha/cap']
    landuse = landuse[landuse['Unit'] != 'USD_PPP/ha']

    landuse = landuse[landuse['ISO3'] != 'not found']
    
    units= landuse['Unit'].unique()
    
    
    
    if len(units)==1:
        if units[0]=='1000 ha':
            landuse[col_years]=(landuse[col_years]*10)
             
            landuse['Unit']='km2'
            
            
            
    landuse=landuse[landuse.ISO3.isin(country)]
    artificial_land = landcover.copy()
    artificial_land = artificial_land[artificial_land['Item Code'] == 6970]
    new=pd.concat([landuse,artificial_land])
    new = new.sort_values(['ISO3','Item Code'])
    landuse = new.copy()
    
    list_item_code = list(landuse['Item Code'])
    FAOitem = []
    for i in list_item_code:
        if i not in FAOitem:
            FAOitem.append(i)
            
            
            
    '''
        Here we make sure that the country area is available for the relevant years of
        each country
    '''
    print("country area")
    for code in country:
        landuse = fca.fill(landuse, code,col_years,relevant_years,parameters)
    
    '''
        Here, dictionnaries are created.
        We list for each major items the minor item corresponding
    '''
    print("create major / minor relation")

    dfs = dict()

    for key in diagram:
        df1 = pd.DataFrame(columns = ['ISO3','item'])
        for year in relevant_years:
            df1[year]=""
        for code in country :
            for item in list(diagram.get(key).values()) : 
                #df1 = df1.append(pd.Series([code,item,0], index=['ISO3','item',year]),ignore_index=True)
                new_row = pd.DataFrame({'ISO3':[code], 'item':[item], 'year':[0.0]})  
                df1 = pd.concat([df1,new_row])
        df1=df1.fillna(0.0)
        dfs[key] = df1.copy()

    for key in small_diagrams:
        df1 = pd.DataFrame(columns = ['ISO3','item'])
        for year in relevant_years:
            df1[year]=""
        for code in country :
            for item in list(small_diagrams.get(key).values()) : 
                new_row = pd.DataFrame({'ISO3':[code], 'item':[item], 'year':[0.0]})  
                df1 = pd.concat([df1,new_row])
                #df1 = df1.append(pd.Series([code,item,0], index=['ISO3','item',year]),ignore_index=True)
        df1=df1.fillna(0.0)
        dfs[key] = df1.copy() 
        
            
    print("zero assumption")

    landuse = za.assumption(country, FAOitem, parameters, landuse,col_years) #13:27 start - 13:55 end#
    
    print("calculation of minor as a funtion of major") 
    #8:40 ->
    
    

    for code in country :
        #15:16 begins - 17:04 end
        if not code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
        else:
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        
        for key in diagram:
            missing=0
            year1b=year2b=year3b=parameters.get("year_of_interest").get("begin")
            year1e=year2e=year3e=parameters.get("year_of_interest").get("end")
            a=[]
            if diagram.get(key).get("minor1") in parameters.get("exeptions"):
                exeption1=diagram.get(key).get("minor1")
                year1b=parameters.get("exeptions").get(exeption1).get("begin")
                year1e=parameters.get("exeptions").get(exeption1).get("end")
                a.append(year1b)
            if diagram.get(key).get("minor2") in parameters.get("exeptions"):
                exeption2=diagram.get(key).get("minor2")
                year2b=parameters.get("exeptions").get(exeption2).get("begin")
                year2e=parameters.get("exeptions").get(exeption2).get("end")
                a.append(year2b)
            if diagram.get(key).get("minor3") in parameters.get("exeptions"):
                exeption3=diagram.get(key).get("minor3")
                year3b=parameters.get("exeptions").get(exeption3).get("begin")
                year3e=parameters.get("exeptions").get(exeption3).get("end")
                a.append(year3b)
            
            #CASE1 which correspond to a case where neither the country or the FaoItem is in the exeption list
            if not a and not code in parameters.get("exeptions"):
                case1.solve(landuse, dfs,code,relevant_years, diagram,key,country,missing)
            
            #CASE2 which correspond to a case where only the country is in the exeption list
            if a and code not in parameters.get("exeptions"):
                case2.solve(landuse, dfs,code,relevant_years, diagram,key,country,missing,year3b,year3e,year2e,year2b,year1e,year1b,a,parameters)
            
            #CASE3 which correspond to a case where only the FaoItem is in the exeption list
            if not a and code in parameters.get("exeptions"):
                case3.solve(landuse, dfs,code,relevant_years, diagram,key,country,missing)
            
            #CASE4 which correspond to a case where the country and the FaoItem are in the exeption list
            if a and code in parameters.get("exeptions"):
                case4.solve(landuse, dfs,code,relevant_years, diagram,key,country,missing,year3b,year3e,year2e,year2b,year1e,year1b,a,parameters)

    landuse[col_years] = landuse[col_years].apply(pd.to_numeric)
    

    '''
        Linear interpolartion or primary items # 1min
    '''

    print("linear interpolation")
    landuse=landuse.reset_index().set_index(meta_col)
    for code in country :
        landuse_new=landuse[(landuse.index.get_level_values(0)==code)&(landuse.index.get_level_values(1).isin(items_primary))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in landuse_new.index:
            if item in landuse.index:
                landuse.loc[item,col_years]=landuse_new.loc[item, col_years]

    landuse=landuse.reset_index()

    '''
        adjust major = sum(minor) begin 17:19, end :17:41
    '''
    print("Adjustment major")

    for code in country :
        if not code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
        else:
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]

        for key in diagram:
            for years in relevant_years :
                adj.adjust(landuse, dfs,code,years, diagram,key,country)
                            
    '''
        regression begin : 17:43 end 17:51
    '''
    print("regression") 

    for code in country :
        reg.regression(code,parameters,landuse)
    # landuse.to_csv('regression_primary_items.csv',index = False)  
    
    '''
        Adjustment after regression   begin 17:55 end : 18:16
    '''
    print("adjustment after regression")

    for code in country :
        if not code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
        else:
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]

        for key in diagram:
            for years in relevant_years :
                adj.adjust(landuse, dfs,code,years, diagram,key,country)

                
                
    '''--------------------------------------------------------------------------------------------------------------'''  
    '''
    linear interpolation and regression for unique items
    This should be run in parallel of the first part of the script
    start 19:08 end : 19:20
    '''     
    print("interpolation unique items")

    landuse=landuse.reset_index().set_index(meta_col)
    for code in country :
        landuse_new=landuse[(landuse.index.get_level_values(0)==code)&(landuse.index.get_level_values(1).isin(unique_items))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in landuse_new.index:
            if item in landuse.index:
                landuse.loc[item,col_years]=landuse_new.loc[item, col_years]

    landuse=landuse.reset_index()
    
    print("regression minor")



    for code in country :
        reg2.regression(code,parameters,landuse,unique_items)

        
    '''--------------------------------------------------------------------------------------------------------------'''   
    '''
        This part deals with the small diagrams
        could be run in parallel of the 2 first parts

    ''' 

    '''
        20:16 begin calculation
    '''
    print("small disgram")

    for code in country :

        for key in small_diagrams:
            missing=0
            csd.solve(landuse, dfs,code,relevant_years, small_diagrams,key,country,missing,parameters)


    '''
        Interpolation small diagrams
    '''          
    print("small disgram interpolation")

    landuse=landuse.set_index(meta_col)
    for code in country :
        landuse_new=landuse[(landuse.index.get_level_values(0)==code)&(landuse.index.get_level_values(1).isin(items_small_diagrams))][col_years].interpolate(method ='linear',axis=1,limit_area ='inside')
        for item in landuse_new.index:
            if item in landuse.index:
                landuse.loc[item,col_years]=landuse_new.loc[item, col_years]

    landuse=landuse.reset_index()


    '''
        Adjust small diagrams
    '''
    print("adjustment small disgram")

    for code in country :
        if not code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
        else:
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]

        for key in small_diagrams:
            for years in relevant_years :
                adj.adjust(landuse,dfs,code,years, small_diagrams,key,country)

        #1min#  
    '''
        Regression small diagram
    '''
    print("regression small disgram")

    for code in country :
        reg2.regression(code,parameters,landuse,items_small_diagrams)

    '''
        Adjust after regression
    '''
    print("adjust after regression small disgram")

    for code in country :
        if not code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
        else:
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]

        for key in small_diagrams:
            for years in relevant_years :
                adj.adjust(landuse,dfs,code,years, small_diagrams,key,country)
            #landuse.to_csv('land_use_adjust4.csv',index = False)
            
        
    landuse.drop('index', inplace=True, axis=1, errors='ignore')
    col_years = [col for col in landuse.columns if  col.startswith("Y")]
    landuse[col_years] = landuse[col_years].round(2)
    landuse[col_years] = landuse[col_years].clip(lower=0)
    landuse = landuse.drop(['level_0', 'index'], axis=1, errors='ignore')


    
    
    for temp_file in [
        '6672.csv',
        '6671.csv',
        '6611.csv',
        '6616.csv',
        '6621.csv',
        '6620.csv',
        '6600.csv',
        '6601.csv',
        '6602.csv',
        '6610.csv',
        '6655.csv',
        'itemland_use_regression.csv',
        'itemland_use_regression2.csv',
        'land_use.csv',
    ]:
        Path(temp_file).unlink(missing_ok=True)


    # os.remove('landuse_cal_minor.csv')
    # os.remove('land_use_adjustmajor.csv')
    # os.remove('land_use_reg.csv')
    # os.remove('country_area.csv')
    # os.remove('landuse_zero assumption.csv')
    # os.remove('landuse_minor_major.csv')

    # os.remove('land_use.csv')
    # # os.remove('landuse_linear.csv')
    # os.remove('regression_primary_items.csv')

    return landuse
