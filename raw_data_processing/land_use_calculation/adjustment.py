def adjust(landuse, dfs,code,years, diagram,key,country):
    value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
    if not value_major.isnull().values.all(): 
        value_major = float(value_major.to_string(index=False, header=False))
        
        minor_value={}
        list = ['minor1','minor2','minor3']
        value_i=0
    
        value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
        if not value_major.isnull().values.all(): 
            value_major = float(value_major.to_string(index=False, header=False))
            for i in list:


                if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                    if  not landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                        value_i=landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]]
                        value_i = float(value_i.to_string(index=False, header=False))
                    else :
                        value_i=0
                    
                    minor_value[(i)]=value_i

        if not (sum(minor_value.values()))==0 : 

                if (diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and not minor_value[(i)]==0):                
                    minor_value[(i)]=minor_value[(i)]*value_major/sum(minor_value.values())

                    landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(i)),[years]]=minor_value[(i)]

    return landuse  
