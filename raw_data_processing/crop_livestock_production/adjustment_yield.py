from make_years import make_valid_fao_year as mvy

def adjust(country,parameters, table_of_interest,item_list,col_years) :
    
    '''
    value_yield = value_production*10000/value_area
    '''
    df_copy=table_of_interest.copy()
    unit_list=table_of_interest['Unit'].unique()
    
    relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
    
    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
                   
        print(code)
        for item in item_list:
            print(item)
            unit_ind=[]
            for a in unit_list:
                if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                    unit_ind.append(a)

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
                            if (value_area==0 or value_production ==0):
                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=0
                            else:
                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[1])),[years]]=value_production*10000/value_area

        df_copy[col_years] = df_copy[col_years].round(2)

                
                           
    table_of_interest = df_copy.copy()
    return table_of_interest 

def adjust_prim_livestock(country,parameters, table_of_interest,item_list,col_years) :
    
    '''
    value_yield = value_production*10000/value_area
    '''
    df_copy=table_of_interest.copy()
    unit_list=table_of_interest['Unit'].unique()
    
    relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
    
    for code in country:
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
                   
        print(code)
        for item in item_list:
            print(item)
            unit_ind=[]
            for a in unit_list:
                if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                    unit_ind.append(a)

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
                                if (value_head==0 or value_production ==0):
                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                else:
                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=value_production*10000/value_head
                                        
           
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
                                            if (value_head==0 or value_production ==0):
                                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                            else:
                                                df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=value_production*10000/value_head
                               
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
                                                if (value_head==0 or value_production ==0):
                                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=0
                                                else:
                                                    df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==unit_ind[0])),[years]]=value_production*10000/value_head
                               

                    
        df_copy[col_years] = df_copy[col_years].round(2)

                
                           
    table_of_interest = df_copy.copy()
    return table_of_interest 