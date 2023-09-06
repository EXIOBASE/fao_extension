import numpy as np

def make_table(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust,list2):
    
    for years in relevant_years_adjust:
            value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
            if not value_major.isnull().values.all(): 
                value_major = float(value_major.to_string(index=False, header=False))
                if not value_major == 0 :
                    for i in list2:
                        if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                            if not (landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all()):
                                value_minor = landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]]
                                value_minor = float(value_minor.to_string(index=False, header=False))
                                p_minor=value_minor*100/value_major
                                dfs[key].loc[(dfs[key]['ISO3']==code)&(dfs[key]['item']==diagram.get(key).get(i)),[years]]=p_minor   

    
     

    col_years = [col for col in dfs[key].columns if  col.startswith("Y")] 
    dfs[key] = dfs[key].replace(0, np.NaN)


    dfs[key]['min_value'] = dfs[key][col_years].min(axis=1 )
    dfs[key]['max_value'] = dfs[key][col_years].max(axis=1)
    dfs[key]['mean_value'] = dfs[key][col_years].mean(axis = 1, skipna = True)
    dfs[key]['std_dev'] = dfs[key][col_years].std(axis = 1, skipna = True)
    dfs[key]['var'] = dfs[key][col_years].var(axis = 1, skipna = True) 


    for code in country: 
        for i in list2:
        
            if not  (dfs[key].loc[((dfs[key]['item']==diagram.get(key).get(i))&(dfs[key]['ISO3']==code)),['min_value']].isnull().values.all()) :
                mini = dfs[key].loc[((dfs[key]['item']==diagram.get(key).get(i))&(dfs[key]['ISO3']==code)),['min_value']]
                mini = float(mini.to_string(index=False, header=False))
            
                maxi = dfs[key].loc[((dfs[key]['item']==diagram.get(key).get(i))&(dfs[key]['ISO3']==code)),['max_value']]
                maxi = float(maxi.to_string(index=False, header=False))

                if mini == maxi :
                    dfs[key].loc[(dfs[key]['ISO3']==code)&(dfs[key]['item']==diagram.get(key).get(i)),['std_dev']]=0
       
    return dfs
    