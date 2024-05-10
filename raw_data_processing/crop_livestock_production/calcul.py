
from make_years import make_valid_fao_year as mvy
import numpy as np

def calcul1(country,item_list, table_of_interest,relevant_years,parameters,col_years):

    df_copy=table_of_interest.copy()
    unit_list=table_of_interest['Unit'].unique()
    
    for code in country:
        print(code)
        for item in item_list:
            unit_ind=[]

            for a in unit_list:
                if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                    unit_ind.append(a)
            '''
            If the FAO item is represented by only one unit
            check how many different value there is 
            If there is only one value, we keep it constant all the years through
            '''
            if len(unit_ind)==1:
                for b in unit_ind:
                    if not (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),col_years].isnull().values.all()) :
                        diff_value_per_line = int(df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
                        nber_value_per_line = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),col_years].count(axis=1, numeric_only=True)
                        nber_value_per_line=nber_value_per_line.astype(int)
                        if  (diff_value_per_line == 1):
                            value = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),col_years].mean(axis=1,skipna=True) 
                            value = float(value.to_string(index=False, header=False)) 
                            for years in relevant_years :
                                if (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),[years]].isnull().values.any()):
                                    df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),[years]]=value


            else :
                if len(unit_ind)==2:
                    if not (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].isnull().values.all() and df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),col_years].isnull().values.all()) :
                        diff_value_per_line_1 = int(df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
                        nber_value_per_line1 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].count(axis=1, numeric_only=True)
                        nber_value_per_line1=nber_value_per_line1.astype(int)
                        diff_value_per_line_2 = int(df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
                        nber_value_per_line2 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),col_years].count(axis=1, numeric_only=True)
                        nber_value_per_line2=nber_value_per_line2.astype(int)
                        if  (diff_value_per_line_1 == 1 and diff_value_per_line_2==1):
                            value1 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].mean(axis=1,skipna=True) 
                            value1 = float(value1.to_string(index=False, header=False)) 
                            value2 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),col_years].mean(axis=1,skipna=True) 
                            value2 = float(value2.to_string(index=False, header=False)) 
                            if (value1 == 0.0 and value2==0):
                                for years in relevant_years :
                                    if (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),[years]].isnull().values.any()):
                                        df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),[years]]=value1
                                    if (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),[years]].isnull().values.any()):
                                        df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),[years]]=value2

                else :
                    if len(unit_ind)==3:
                        if not (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].isnull().values.all() and df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[2]),col_years].isnull().values.all()) :
                            diff_value_per_line_1 = int(df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
                            nber_value_per_line1 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].count(axis=1, numeric_only=True)
                            nber_value_per_line1=nber_value_per_line1.astype(int)
                            diff_value_per_line_2 = int(df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[2]),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
                            nber_value_per_line2 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[2]),col_years].count(axis=1, numeric_only=True)
                            nber_value_per_line2=nber_value_per_line2.astype(int)
                            if  (diff_value_per_line_1 == 1 and diff_value_per_line_2==1):
                                value1 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),col_years].mean(axis=1,skipna=True) 
                                value1 = float(value1.to_string(index=False, header=False)) 
                                value2 = df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[2]),col_years].mean(axis=1,skipna=True) 
                                value2 = float(value2.to_string(index=False, header=False)) 
                                if (value1 == 0.0 and value2==0):
                                    for years in relevant_years :

                                        if (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),[years]].isnull().values.any()):
                                            df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[0]),[years]]=value1
                                        if (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),[years]].isnull().values.any()):
                                            df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[1]),[years]]=value2
                                        if (df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[2]),[years]].isnull().values.any()):
                                            df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==unit_ind[2]),[years]]=value2
                        


    #df_copy.to_csv('crops_primary_zero_issue.csv',index = False)
                                
    table_of_interest = df_copy
    return table_of_interest  


def calcul2(country,item_list, table_of_interest,relevant_years,parameters,col_years):
    unit_list=table_of_interest['Unit'].unique()

    
    
    '''Here, we look at the first non empty cell. If value is 0, the previous years are assumed to be 0 too'''
    
    df_copy=table_of_interest.copy()
    unit_list=table_of_interest['Unit'].unique()
    for code in country:
        print(code)
        for item in item_list:
            unit_ind=[]
            for a in unit_list:
                if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                    unit_ind.append(a)
            '''
            If the FAO item is represented by only one unit
            check how many different value there is 
            If there is only one value, we keep it constant all the years through
            '''

            if len(unit_ind)==1:
                for b in unit_ind:
                    for years in relevant_years:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():                            
                            value =df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]]
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero))]
                                for years in year_zero :
                                    df_copy.loc[((df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b)),[years]]=0


            else :
                if len(unit_ind)==2:
                    value1=value2=0
                    for b in unit_ind:
                        for years in relevant_years:
                            if  not (df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]].isnull().values.all() and df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]].isnull().values.all()):                            
                                value1=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]
                                value1=float(value1.to_string(index=False, header=False)) 
                                value2=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]
                                value2=float(value2.to_string(index=False, header=False)) 
                                year_zero = int(years.replace("Y",""))
                                if (value1==0 and value2==0):
                                    year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero+1))]
                                    for years in year_zero :
                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
   
                                        
                else :
                    if len(unit_ind)==3:
                        for b in unit_ind:
                            for years in relevant_years:
                                if  not (df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]].isnull().values.all() and df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[2])),[years]].isnull().values.all() and not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]].isnull().values.all()):                            
                                    value_area=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]
                                    value_area=float(value_area.to_string(index=False, header=False)) 
                                    value_production=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[2])),[years]]
                                    value_production=float(value_production.to_string(index=False, header=False)) 
                                    value_yield=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]
                                    value_yield=float(value_yield.to_string(index=False, header=False)) 
                                    year_zero = int(years.replace("Y",""))
                                    if (value_area==0 and value_production==0 and np.isnan(value_yield)):
                                        year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero+1))]
                                        for years in year_zero :
                                            df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                            df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
                                            df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[2])),[years]]=0 


                            
    table_of_interest = df_copy.copy()
    return table_of_interest 

def calcul2_prim_livestock(country,item_list, table_of_interest,relevant_years,parameters,col_years):
    unit_list=table_of_interest['Unit'].unique()

    
    
    '''Here, we look at the first non empty cell. If value is 0, the previous years are assumed to be 0 too'''
    
    df_copy=table_of_interest.copy()
    unit_list=table_of_interest['Unit'].unique()
    for code in country:
        for item in item_list:
            unit_ind=[]
            for a in unit_list:
                if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                    unit_ind.append(a)
            '''
            If the FAO item is represented by only one unit
            check how many different value there is 
            If there is only one value, we keep it constant all the years through
            '''

            if len(unit_ind)==1:
                for b in unit_ind:
                    for years in relevant_years:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():                            
                            value =df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]]
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero))]
                                for years in year_zero :
                                    df_copy.loc[((df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b)),[years]]=0


            else :
                if len(unit_ind)==2:
                    value1=value2=0
                    for b in unit_ind:
                        for years in relevant_years:
                            if  not (df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]].isnull().values.all() and df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]].isnull().values.all()):                            
                                value1=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]
                                value1=float(value1.to_string(index=False, header=False)) 
                                value2=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]
                                value2=float(value2.to_string(index=False, header=False)) 
                                year_zero = int(years.replace("Y",""))
                                if (value1==0 and value2==0):
                                    year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero+1))]
                                    for years in year_zero :
                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
   
                                        
                else :
                    if len(unit_ind)==3:
                        for b in unit_ind:
                            if '100mg/An' in unit_ind:
                                for years in relevant_years:
                                    if  not (df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='tonnes')),[years]].isnull().values.all() and df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='1000 Head')),[years]].isnull().values.all() and not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='100mg/An')),[years]].isnull().values.all()):                            
                                        value_head=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='1000 Head')),[years]]
                                        value_head=float(value_head.to_string(index=False, header=False)) 
                                        value_production=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='tonnes')),[years]]
                                        value_production=float(value_production.to_string(index=False, header=False)) 
                                        value_yield=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='100mg/An')),[years]]
                                        value_yield=float(value_yield.to_string(index=False, header=False)) 
                                        year_zero = int(years.replace("Y",""))
                                        if (value_head==0 and value_production==0 and np.isnan(value_yield)):
                                            year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero+1))]
                                            for years in year_zero :
                                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
                                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[2])),[years]]=0 
                            else:
                                if 'hg/An' in unit_ind:
                                    for years in relevant_years:
                                        if  not (df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='tonnes')),[years]].isnull().values.all() and df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='Head')),[years]].isnull().values.all() and not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='hg/An')),[years]].isnull().values.all()):                            
                                            value_head=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='Head')),[years]]
                                            value_head=float(value_head.to_string(index=False, header=False)) 
                                            value_production=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='tonnes')),[years]]
                                            value_production=float(value_production.to_string(index=False, header=False)) 
                                            value_yield=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='hg/An')),[years]]
                                            value_yield=float(value_yield.to_string(index=False, header=False))
                                            year_zero = int(years.replace("Y",""))
                                            if (value_head==0 and value_production==0 and np.isnan(value_yield)):
                                                year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero+1))]
                                                for years in year_zero :
                                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
                                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[2])),[years]]=0 

                                else:
                                    if '0.1g/An' in unit_ind:
                                        for years in relevant_years:
                                            if  not (df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='tonnes')),[years]].isnull().values.all() and df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='1000 Head')),[years]].isnull().values.all() and not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='0.1g/An')),[years]].isnull().values.all()):                            
                                                value_head=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='1000 Head')),[years]]
                                                value_head=float(value_head.to_string(index=False, header=False)) 
                                                value_production=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='tonnes')),[years]]
                                                value_production=float(value_production.to_string(index=False, header=False)) 
                                                value_yield=df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']=='0.1g/An')),[years]]
                                                value_yield=float(value_yield.to_string(index=False, header=False))
                                                year_zero = int(years.replace("Y",""))
                                                if (value_head==0 and value_production==0 and np.isnan(value_yield)):
                                                    year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero+1))]
                                                    for years in year_zero :
                                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
                                                        df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[2])),[years]]=0 

                            
    table_of_interest = df_copy.copy()
    return table_of_interest 
            