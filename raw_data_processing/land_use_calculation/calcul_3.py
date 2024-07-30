 
def calculation(landuse,code,key,years,list2,list3,diagram):
    if not landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]].isnull().values.all():
        value_major = landuse.loc[(landuse['Item Code']==key)&(landuse['ISO3']==code),[years]]
        value_major=float(value_major.to_string(index=False, header=False))
        for i in list3:
            for j in list3:
                if j is not i:
                    if not diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                        if diagram.get(key).get(j) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values  :
                            if landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]] = value_major
                    
                    if not diagram.get(key).get(j) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                        if diagram.get(key).get(i) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values  :
                            if landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]] = value_major
                                  
                    if (diagram.get(key).get(j) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and  diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) ):
                        if landuse.loc[(landuse['Item Code']==diagram.get(key).get(j)&(landuse['ISO3']==code)),[years]].isnull().values.all() :
                            if not landuse.loc[(landuse['Item Code']==diagram.get(key).get(i)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                value_i = landuse.loc[landuse['Item Code']==diagram.get(key).get(i)&(landuse['ISO3']==code),[years]]
                                value_i = float(value_i.to_string(index=False, header=False))
                                
                                landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]] = value_major - value_i
                            
                    if (diagram.get(key).get(j) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and  diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) ):
                        if landuse.loc[(landuse['Item Code']==diagram.get(key).get(i)&(landuse['ISO3']==code)),[years]].isnull().values.all() :
                            if not landuse.loc[(landuse['Item Code']==diagram.get(key).get(j)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                value_j = landuse.loc[landuse['Item Code']==diagram.get(key).get(j)&(landuse['ISO3']==code),[years]]
                                value_j = float(value_j.to_string(index=False, header=False))
                               
                                landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]] = value_major - value_j
                   
    
    return landuse