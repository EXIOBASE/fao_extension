import pandas as pd
import numpy as np


#def make_table_per_year(relevant_years):
'''REPRENDRE CECI AVEC MATRIX TRADE AND PROD FAO EXIOBASE version1'''


seed_cotton_p01e=0.63
seed_cotton_p01g=0.37

factor_beef_buffalo=20.0
factor_milk=1.0
factor_poultry=1.0
factor_pig=2.0
factor_sheep_goat=10.0


correspondance = pd.read_excel (r'Bridge_new_EXIO4.xlsx', sheet_name='Sheet1')
print (correspondance)
meta_col = [col for col in correspondance.columns if not col.startswith(("DESIRE","Un"))] 


#crops primary#
crops_primary = pd.read_csv('final_cropland_primary.csv', encoding="latin-1") 
crops_primary.insert(3, 'EXIOBASE product code', '')
crops_primary.insert(4, 'EXIOBASE product', '')


for i in crops_primary.index:
    #print(crops_primary.loc[index,['Item']].values[0])
    item_df=crops_primary.loc[i,['Item']].values[0]
    if item_df in correspondance['DESIRE products'].values:
        for column in meta_col:
            item = correspondance.loc[correspondance['DESIRE products']==item_df,column].values[0]
            #print(item)
            if(item==1):
                category_code=correspondance.loc[0,column]
                category=column
                
                print(category,category_code)
                crops_primary.loc[i,['EXIOBASE product code']]=category_code
                crops_primary.loc[i,['EXIOBASE product']]=category
                
                
                
crops_primary_area = crops_primary.loc[(crops_primary['Unit']=='ha')]
crops_primary_production = crops_primary.loc[(crops_primary['Unit']=='tonnes')]

#livestock primary#
livestock_primary = pd.read_csv('final_livestock_primary.csv', encoding="latin-1") 
livestock_primary.insert(3, 'EXIOBASE product code', '')
livestock_primary.insert(4, 'EXIOBASE product', '')


for i in livestock_primary.index:
    #print(crops_primary.loc[index,['Item']].values[0])
    item_df=livestock_primary.loc[i,['Item']].values[0]
    if item_df in correspondance['DESIRE products'].values:
        for column in meta_col:
            item = correspondance.loc[correspondance['DESIRE products']==item_df,column].values[0]
            #print(item)
            if(item==1):
                category_code=correspondance.loc[0,column]
                category=column
                
                print(category,category_code)
                livestock_primary.loc[i,['EXIOBASE product code']]=category_code
                livestock_primary.loc[i,['EXIOBASE product']]=category




livestock_primary_production = livestock_primary.loc[(crops_primary['Unit']=='tonnes')]

#correspondance.loc[correspondance['DESIRE products']=='Agave fibres nes']
#meta_col = [col for col in crop_livestock.columns if  col.startswith("Y")] 

#for index in crops_primary.index:


#            else :
#                
#                crops_primary.loc[i,crops_primary['EXIOBASE product code']]=''
#                crops_primary.loc[i,crops_primary['EXIOBASE product']]=''
#    for column in meta_col:
#        item = correspondance.loc[correspondance['DESIRE products']=='Agave fibres nes',column].values[0]
#        if(item==1):
#            category=correspondance.loc[0,column]
#            print(category)
            
    
    
    
    
    
    
    
    #crop harvest#
    df2 = pd.read_csv('../Fill_4_tables/crop_harvest/crop_harvest.csv', encoding="latin-1")
    #land use#
    df3 = pd.read_csv('final_landuse.csv', encoding="latin-1")
    #Livestock production#
    df_livestock_all = pd.read_csv('../Fill_4_tables/Livestock_prod/livestock_prod.csv', encoding="latin-1")
    dfs = pd.read_csv('../Of_interest/List_Primary_livestock_FAO-CPA-EXIOBASE.csv', encoding="latin-1")
    #land use#
    df_graz = pd.read_csv('final_landuse.csv', encoding="latin-1")
    df_forest = pd.read_csv('final_landuse.csv', encoding="latin-1")
    df_final_demand = pd.read_csv('final_landuse.csv', encoding="latin-1")
    

    list_ISO3 = list(df['ISO3'])
    df=df.drop(columns=['Item Code'])
    df2=df2.drop(columns=['Item Code'])
    
    df=df.groupby(['ISO3','EXIOBASE product code','EXIOBASE product','Unit']).sum().reset_index()
    df_modified=df.copy()

    
    df_graz=df_graz.fillna(0)  
    df_forest=df_forest.fillna(0)
    df_final_demand = df_final_demand.fillna(0)
    
    """
    allocate the seed cotton harvested area to p01.e oil crops and p01.g fibre
    """
    
    list_ISO3_2 = list(df_modified['ISO3'])
    res = [] 
    for i in list_ISO3: 
        if i not in res: 
            res.append(i) 
    
    
    
    list_exio = list(df_modified['EXIOBASE product code'])
    res2 = []
    for i in list_exio: 
        if i not in res2: 
            res2.append(i) 
 
    

    for code in res :
        if not 'p01.e' in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.e','Oil seeds','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)

        if not 'p01.g' in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.g','Plant-based fibers','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.a' in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.a','Paddy rice','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        if not 'p01.b' in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.b','Wheat','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        if not 'p01.c'  in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.c','Cereal grains nec','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        if not 'p01.d'  in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        if not 'p01.f'  in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.h'  in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified = df_modified.append(pd.Series([code,'p01.h','Crops nec','tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
 
    
    df_modified=df_modified.fillna(0)   
    df_modified=df_modified.sort_values(by=['ISO3', 'EXIOBASE product code'])
         
       
    for code in res :
        for year in relevant_years:
            if 'n.a.' in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
                
                value_seed_cotton=df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='n.a.')),[year]]
                seed_cotton=value_seed_cotton.to_string(index=False, header=False)
                
                cotton_to_p01e=float(seed_cotton_p01e*float(seed_cotton))
                cotton_to_p01g=float(seed_cotton_p01g*float(seed_cotton))
       
                value_p01e=df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.e')),[year]]
                value_p01g=df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.g')),[year]]                
                p01e=float(value_p01e.to_string(index=False, header=False))
                p01g=float(value_p01g.to_string(index=False, header=False))
                
                new_p01e=p01e+cotton_to_p01e
                new_p01g=p01g+cotton_to_p01g
         
                
                '''Replace old value p01.e and p01.g with new vales in dataframe'''
                
                df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
                df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.g')),[year]] = new_p01g
                
    df_modified=df_modified[~df_modified['EXIOBASE product code'].str.contains("n.a.")]
                
    df2=df2.groupby(['ISO3','EXIOBASE product code','EXIOBASE product','Unit']).sum().reset_index()

    df_modified2=df2.copy()
    
        
    """
    allocate the seed cotton harvested area to p01.e oil crops and p01.g fibre
    """



    list_ISO3_2 = list(df_modified2['ISO3'])
    res = [] 
    for i in list_ISO3_2: 
        if i not in res: 
            res.append(i) 
    
    
    list_exio = list(df_modified2['EXIOBASE product code'])
    res2 = []
    for i in list_exio: 
        if i not in res2: 
            res2.append(i) 
  
    

    for code in res :
        if not 'p01.e' in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.e','Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.g' in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.g','Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        if not 'p01.a' in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.a','Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.b' in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.b','Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.c'  in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.c','Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.d'  in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
       
        if not 'p01.f'  in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
      
        if not 'p01.h'  in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
            df_modified2 = df_modified2.append(pd.Series([code,'p01.h','Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)


    df_modified2=df_modified2.fillna(0)   
    df_modified2=df_modified2.sort_values(by=['ISO3', 'EXIOBASE product code'])
    
       
    for code in res :
        for year in relevant_years:
            if 'n.a.' in (df_modified2.loc[df_modified2['ISO3']==code, ["EXIOBASE product code"]].values) :
                value_seed_cotton=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='n.a.')),[year]]
                seed_cotton=value_seed_cotton.to_string(index=False, header=False)
                cotton_to_p01e=float(seed_cotton_p01e*float(seed_cotton))
                cotton_to_p01g=float(seed_cotton_p01g*float(seed_cotton))
                value_p01e=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.e')),[year]]
                value_p01g=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.g')),[year]]                
                p01e=float(value_p01e.to_string(index=False, header=False))
                p01g=float(value_p01g.to_string(index=False, header=False))
                new_p01e=p01e+cotton_to_p01e
                new_p01g=p01g+cotton_to_p01g
                
                '''Replace old value p01.e and p01.g with new vales in dataframe'''     
                
                df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
                df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.g')),[year]] = new_p01g
                
    df_modified2=df_modified2[~df_modified2['EXIOBASE product code'].str.contains("n.a.")]
    

    
    
    
    
    """Get the harvest crop per ha per year per country"""
    
    df2_2=df2.groupby(['ISO3','Unit']).sum()

    '''select the total cropped land from FAOSTAT'''
    
    df3 = df3[(df3.ISO3 != 'not found')&(df3['Item Code']==6620)]
    
    '''
    We can split permanent meadows and pastures (item 6655) unto
    FAO item 6659 : naturally growing 
    FAO item 6656 : cultivated
    
    '''
    
    
    df_natgrowing = df_graz.copy()
    df_cultivated = df_graz.copy()
   
    for code in res:
       for year in relevant_years:
          if not 6655 in (df_graz.loc[df_graz['ISO3']==code, ["Item Code"]].values) :
             df_graz = df_graz.append(pd.Series([6655,'Land under perm. meadows and pastures','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                
    df_graz = df_graz[(df_graz.ISO3 != 'not found')&(df_graz['Item Code']==6655)]
    df_graz=df_graz.fillna(0)  

    for code in res:
       for year in relevant_years:
          if not 6659 in (df_natgrowing.loc[df_natgrowing['ISO3']==code, ["Item Code"]].values) :
             df_natgrowing = df_natgrowing.append(pd.Series([6659,'Perm. meadows & pastures - Nat. growing','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                
    df_natgrowing = df_natgrowing[(df_natgrowing.ISO3 != 'not found')&(df_natgrowing['Item Code']==6659)]
    df_natgrowing = df_natgrowing.fillna(0)     

    for code in res:
       for year in relevant_years:
          if not 6656 in (df_cultivated.loc[df_cultivated['ISO3']==code, ["Item Code"]].values) :
             df_cultivated = df_cultivated.append(pd.Series([6656,'Perm. meadows & pastures - Cultivated','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                
    df_cultivated = df_cultivated[(df_cultivated.ISO3 != 'not found')&(df_cultivated['Item Code']==6656)]
    df_cultivated = df_cultivated.fillna(0)     





    for code in res:
       for year in relevant_years:
          if not 6670 in (df_final_demand.loc[df_final_demand['ISO3']==code, ["Item Code"]].values) :
             df_final_demand = df_final_demand.append(pd.Series([6670,'Final Demand','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                
    df_final_demand = df_final_demand[(df_final_demand.ISO3 != 'not found')&(df_final_demand['Item Code']==6670)]
    df_final_demand = df_final_demand.fillna(0) 

    
    for code in res:
       for year in relevant_years:
          if not 6646 in (df_forest.loc[df_forest['ISO3']==code, ["Item Code"]].values) :
             df_forest = df_forest.append(pd.Series([6646,'Forest Land','1000ha',code,0], index=['Item Code','Item','Unit','ISO3',year]),ignore_index=True)
                
    df_forest = df_forest[(df_forest.ISO3 != 'not found')&(df_forest.Unit != 'million tonnes')&(df_forest['Item Code']==6646)]
    df_forest = df_forest.fillna(0)    

    
    Unit='ha'
    
    cropland_total = []
    for ISO3 in list_ISO3:
        for year in relevant_years:
            cropland = 1000*(df3[df3['ISO3'] == ISO3][year]).astype(np.float32).values
            cropland_total.append((ISO3,Unit,year,*cropland))
            
   

    df4=pd.DataFrame(cropland_total,columns=["ISO3","Unit","YEAR","cropland total"])


    df5=df4.pivot_table(index=['ISO3','Unit'],columns=['YEAR'], values="cropland total")

    
    df5.to_csv('cropland_total.csv',index = False)
    
    '''
    Extract data for fodder crops


        Select FAOSTAT Item codes related to 
        1806	Beef and Buffalo Meat
        1808	Meat, Poultry
        1780	Milk, Total
        1807	Sheep and Goat Meat
        1035	Meat, pig

    '''

    df_livestock = df_livestock_all[(df_livestock_all.ISO3 != 'not found')&(df_livestock_all['Item Code'].isin([1035,1807,1780,1808,1806]))] 
    df_livestock = pd.merge(df_livestock,dfs[['EXIOBASE product code','EXIOBASE product']],left_on=df_livestock['Item Code'], right_on = dfs['FAO item code'],how = 'left')
    df_livestock = df_livestock.drop(columns=['key_0','Item Code'])  

            
    meta_col = ['ISO3', 'EXIOBASE product code', 'EXIOBASE product','Unit']
    meta_col2 = [col for col in df_livestock.columns if  col.startswith("Y")] 
    df_livestock = df_livestock[meta_col + meta_col2]   
    
    
    
    for code in res:
        for year in relevant_years:
            if not 'p01.i' in (df_livestock.loc[df_livestock['ISO3']==code, ["EXIOBASE product code"]].values) :
                df_livestock = df_livestock.append(pd.Series([code,'p01.i','Cropland - Fodder crops-Cattle','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
          
            if not 'p01.j' in (df_livestock.loc[df_livestock['ISO3']==code, ["EXIOBASE product code"]].values) :
                df_livestock = df_livestock.append(pd.Series([code,'p01.j','Cropland - Fodder crops-Pigs','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
         
            if not 'p01.k' in (df_livestock.loc[df_livestock['ISO3']==code, ["EXIOBASE product code"]].values) :
                df_livestock = df_livestock.append(pd.Series([code,'p01.k','Cropland - Fodder crops-Poultry','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
           
            if not 'p01.l' in (df_livestock.loc[df_livestock['ISO3']==code, ["EXIOBASE product code"]].values) :
                df_livestock = df_livestock.append(pd.Series([code,'p01.l','Cropland - Fodder crops-Meat animals nec','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
         
            if not 'p01.n' in (df_livestock.loc[df_livestock['ISO3']==code, ["EXIOBASE product code"]].values) :
                df_livestock = df_livestock.append(pd.Series([code,'p01.n','Cropland - Fodder crops-Raw milk','Tonnes'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)


    df_livestock=df_livestock.fillna(0) 
    
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
        
    for code in res :
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.a','Cropland - fallowed area - Paddy rice','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.b','Cropland - fallowed area - Wheat','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.c','Cropland - fallowed area - Cereal grains nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.d','Cropland - fallowed area - Vegetables, fruit, nuts','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.e','Cropland - fallowed area - Oil seeds','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.f','Cropland - fallowed area - Sugar cane, sugar beet','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.g','Cropland - fallowed area - Plant-based fibers','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fallow_crop = df_fallow_crop.append(pd.Series([code,'p01.h','Cropland - fallowed area - Crops nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        
        df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.i','Cropland - Fodder crops-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.j','Cropland - Fodder crops-Pigs','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.k','Cropland - Fodder crops-Poultry','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.l','Cropland - Fodder crops-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_fodder_crop = df_fodder_crop.append(pd.Series([code,'p01.n','Cropland - Fodder crops-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
    
        df_grazzing = df_grazzing.append(pd.Series([code,'p01.i','Permanent pastures - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_grazzing = df_grazzing.append(pd.Series([code,'p01.l','Permanent pastures - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_grazzing = df_grazzing.append(pd.Series([code,'p01.n','Permanent pastures - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.a','Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.b','Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.c','Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.d','Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.e','Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.f','Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.g','Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_harvested_corrected = df_harvested_corrected.append(pd.Series([code,'p01.h','Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        
        df_cropland = df_cropland.append(pd.Series([code,'p01.a','Cropland - cropped area - Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.a','Cropland - fallowed area - Paddy rice','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.b','Cropland - cropped area - Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.b','Cropland - fallowed area - Wheat','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.c','Cropland - cropped area - Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.c','Cropland - fallowed area - Cereal grains nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.d','Cropland - cropped area - Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.d','Cropland - fallowed area - Vegetables, fruit, nuts','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.e','Cropland - cropped area - Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.e','Cropland - fallowed area - Oil seeds','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.f','Cropland - cropped area - Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.f','Cropland - fallowed area - Sugar cane, sugar beet','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.g','Cropland - cropped area - Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.g','Cropland - fallowed area - Plant-based fibers','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.h','Cropland - cropped area - Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.h','Cropland - fallowed area - Crops nec','ha'], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit']),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.i','Cropland - fallowed area-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.j','Cropland - fallowed area-Pigs','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.k','Cropland - fallowed area-Poultry','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.l','Cropland - fallowed area-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.n','Cropland - fallowed area-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.i','Permanent pastures - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.i','Perm. meadows & pastures - Nat. growing - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.i','Perm. meadows & pastures - Cultivated - Grazing-Cattle','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.l','Permanent pastures - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.l','Perm. meadows & pastures - Nat. growing - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.l','Perm. meadows & pastures - Cultivated - Grazing-Meat animals nec','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.n','Permanent pastures - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.n','Perm. meadows & pastures - Nat. growing - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'p01.n','Perm. meadows & pastures - Cultivated - Grazing-Raw milk','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)     
        df_cropland = df_cropland.append(pd.Series([code,'','Forest area','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
        df_cropland = df_cropland.append(pd.Series([code,'','Final Demand','ha',0], index=['ISO3','EXIOBASE product code','EXIOBASE product','Unit',year]),ignore_index=True)
         
         
    df_fallow_crop=df_fallow_crop.fillna(0)    
    df_fodder_crop=df_fodder_crop.fillna(0)  
    df_grazzing=df_grazzing.fillna(0)  
    df_harvested_corrected=df_harvested_corrected.fillna(0) 
    df_cropland = df_cropland.fillna(0)
    
    for code in res:
        for year in relevant_years:
            df5.index = df5.index.get_level_values('ISO3')
            df2_2.index = df2_2.index.get_level_values('ISO3')
            
            natgrowing = 1000 * df_natgrowing.loc[((df_natgrowing['ISO3']==code) & (df_natgrowing['Item Code'] == 6659)),[year]].astype(np.float32).values
            cultivated = 1000 * df_cultivated.loc[((df_cultivated['ISO3']==code) & (df_cultivated['Item Code'] == 6656)),[year]].astype(np.float32).values
            grazzing=1000 * df_graz.loc[((df_graz['ISO3']==code) & (df_graz['Item Code'] == 6655)),[year]].astype(np.float32).values
            forest = 1000 * df_forest.loc[((df_forest['ISO3']==code) & (df_forest['Item Code'] == 6646)),[year]].astype(np.float32).values
            final_demand = 1000 * df_final_demand.loc[((df_final_demand['ISO3']==code) & (df_final_demand['Item Code'] == 6670)),[year]].astype(np.float32).values


            if code in (df5.index.values) and code in (df2_2.index.values) and code in (df_graz.ISO3.values):
                cropped=df5.loc[code,year]
                harvested=df2_2.loc[code,year]
                fallowed=cropped-harvested
                
                
                if fallowed>0 :
                    fallowed_crop = fallowed/2
                    fodder_crop = fallowed/2

                    '''Values of Harvested area'''
                    
                    p01a=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.a')),[year]]
                    p01a=float(p01a.to_string(index=False, header=False))
                    p01b=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.b')),[year]]
                    p01b=float(p01b.to_string(index=False, header=False))
                    p01c=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.c')),[year]]
                    p01c=float(p01c.to_string(index=False, header=False))
                    p01d=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.d')),[year]]
                    p01d=float(p01d.to_string(index=False, header=False))
                    p01e=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.e')),[year]]
                    p01e=float(p01e.to_string(index=False, header=False))
                    p01f=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.f')),[year]]
                    p01f=float(p01f.to_string(index=False, header=False))
                    p01g=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.g')),[year]]
                    p01g=float(p01g.to_string(index=False, header=False))
                    p01h=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.h')),[year]]
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
            
                    p01i=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.i')),[year]]
                    p01i=float(p01i.to_string(index=False, header=False))
                    p01j=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.j')),[year]]
                    p01j=float(p01j.to_string(index=False, header=False))
                    p01k=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.k')),[year]]
                    p01k=float(p01k.to_string(index=False, header=False))
                    p01l=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.l')),[year]]
                    p01l=float(p01l.to_string(index=False, header=False))
                    p01n=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.n')),[year]]
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
                    
                    p01a=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.a')),[year]]
                    p01a=float(p01a.to_string(index=False, header=False))
                    p01b=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.b')),[year]]
                    p01b=float(p01b.to_string(index=False, header=False))
                    p01c=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.c')),[year]]
                    p01c=float(p01c.to_string(index=False, header=False))
                    p01d=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.d')),[year]]
                    p01d=float(p01d.to_string(index=False, header=False))
                    p01e=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.e')),[year]]
                    p01e=float(p01e.to_string(index=False, header=False))
                    p01f=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.f')),[year]]
                    p01f=float(p01f.to_string(index=False, header=False))
                    p01g=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.g')),[year]]
                    p01g=float(p01g.to_string(index=False, header=False))
                    p01h=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.h')),[year]]
                    p01h=float(p01h.to_string(index=False, header=False))
                    sum_all=p01a+p01b+p01c+p01d+p01e+p01f+p01g+p01h
               
                    
                    '''Values of Produced Livestock Products'''
            
                    p01i=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.i')),[year]]
                    p01i=float(p01i.to_string(index=False, header=False))
                    p01l=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.l')),[year]]
                    p01l=float(p01l.to_string(index=False, header=False))
                    p01n=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.n')),[year]]
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
           
    
    
    writer = pd.ExcelWriter('Cropland.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Production')
    df_modified.to_excel(writer, sheet_name='Production_noCotton')
    df2.to_excel(writer, sheet_name='Harvested_per_product')
    df_modified2.to_excel(writer, sheet_name='Harvested_per_product_noCotton')
    df5.to_excel(writer, sheet_name='Cropped_total')
    df2_2.to_excel(writer, sheet_name='Harvested_total')
    df_livestock.to_excel(writer, sheet_name='Production_livestock')
    df_fallow_crop.to_excel(writer, sheet_name='Fallow crop')
    df_fodder_crop.to_excel(writer, sheet_name='Fodder crop')
    df_grazzing.to_excel(writer, sheet_name='Grazzing')
    df_harvested_corrected.to_excel(writer, sheet_name='harvested corrected')
    df_cropland.to_excel(writer, sheet_name='final cropland')
    writer.save()    