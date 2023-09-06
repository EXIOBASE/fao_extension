def pourcentage(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust2,relevant_years_adjust,list3):

    for years in relevant_years_adjust2:
        list_minor = ['minor1','minor2','minor3']
        value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
        if not value_major.isnull().values.all():  
            value_major = float(value_major.to_string(index=False, header=False))
            for i in list_minor:

                if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                    if (landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all()):   
                        std_minor = dfs[key].loc[(dfs[key]['ISO3']==code)&(dfs[key]['item']==diagram.get(key).get(i)),'std_dev'].item()  
                        if std_minor <=5 :
                            mean_minor = dfs[key].loc[(dfs[key]['ISO3']==code)&(dfs[key]['ISO3']==code)&(dfs[key]['item']==diagram.get(key).get(i)),'mean_value'].item() 
                            value_minor = value_major*mean_minor/100
                            landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(i)),[years]]=value_minor
        


        for i in list_minor:
            for j in list_minor:
                if j is not i:
                    for k in list_minor :
                        if ((k is not i and k is not j and (i == list_minor[0] or i == list_minor[2]) and (list_minor.index(k)>list_minor.index(j))) or ((k is not i and k is not j and (i == list_minor[1]) and (list_minor.index(k)<list_minor.index(j))))) :

                            if diagram.get(key).get(k) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) : 
                               
                                if (landuse.loc[((landuse['Item Code']==diagram.get(key).get(k))&(landuse['ISO3']==code)),[years]].isnull().values.all()):  #k empty :6670 ?
                                    if (diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values)):

                                        if not (landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all()):
                                            value_minori=landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(i)),[years]]
                                            value_minori = float(value_minori.to_string(index=False, header=False)) 

                                            if (diagram.get(key).get(j) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values)):

                                                if not (landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]].isnull().values.all()):
                                                    value_minorj=landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(j)),[years]]
                                                    value_minorj = float(value_minorj.to_string(index=False, header=False))

                                                    if value_minori and value_minorj: 
                                                        value_minork=value_major-value_minori-value_minorj
                                                        if not value_minork <0 :
                                                            landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(k)),[years]]=value_minork
                                                        
                                                    else :
                                                        if value_minori and not value_minorj:
                                                            value_minork=value_major-value_minori
                                                            if not value_minork <0 :
                                                                landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(k)),[years]]=value_minork
                                                            
                                                        else :
                                                            if value_minorj and not value_minorj:
                                                                value_minork=value_major-value_minorj
                                                                if not value_minork <0 :

                                                                    landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(k)),[years]]=value_minork
                                                            else :
                                                                if not (value_minori and value_minorj):
                                                                    continue 
    
    for years in relevant_years_adjust:

        value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
        if not value_major.isnull().values.all(): 
            value_major = float(value_major.to_string(index=False, header=False))
            for i in list3:
                if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                    if (landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all()):    
                        std_minori = dfs[key].loc[(dfs[key]['ISO3']==code)&(dfs[key]['item']==diagram.get(key).get(i)),'std_dev'].item()  
                        if std_minori <=5 :
                            mean_minori = dfs[key].loc[(dfs[key]['ISO3']==code)&(dfs[key]['ISO3']==code)&(dfs[key]['item']==diagram.get(key).get(i)),'mean_value'].item() 
                            value_minori = value_major*mean_minori/100
                            landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(i)),[years]]=value_minori
                            
    return landuse
  