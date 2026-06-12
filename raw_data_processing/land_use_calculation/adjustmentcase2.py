import yaml
def adjust(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust2,relevant_years_adjust,list2,list3):
    list_minor = ['minor1','minor2','minor3']
    minor_value={}
    with open(r'aux_data/parameters.yaml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    if not diagram.get(key).get("minor3") in parameters.get("exeptions"):  
    	list3 = ['minor1','minor2'] 
    	
    for years in relevant_years_adjust2:    
        print(years)
        value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
        print('value major adj2', value_major,'test',value_major.isnull().values.all())       
        if not value_major.isnull().values.all(): 
            value_major = float(value_major.to_string(index=False, header=False))
            #print('value MAJOR',value_major)
            for i in list3:
                #print('LISTE3',list3,'i',i,'diagram.get(key).get(i)',diagram.get(key).get(i))           
                if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                    if  not landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                        value_i=landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]]
                        value_i = float(value_i.to_string(index=False, header=False))
                        #print('i',i,"value_i =", value_i, "type:", type(value_i))
                    else :
                        #print("value_i = 0")                    
                        value_i=0
                    minor_value[(i)]=value_i

        if not (sum(minor_value.values()))==0 : 
            for i in list3:            

                #print("DEBUG line 21") 
                #print("diagram value:", diagram.get(key).get(i), type(diagram.get(key).get(i))) 
                #print("codes:", landuse.loc[landuse['ISO3'] == code, 'Item Code'].values[:10])
                #print("minor_value[i]:", minor_value[i], type(minor_value[i]))
                #print("i:", i, type(i))             
                #print("diagram keys sample:", list(diagram.get(key, {}).keys())[:10])            		
		

                if (diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and not minor_value[(i)]==0): 
                                                       
                    if minor_value[(i)] :
                        minor_value[(i)]=minor_value[(i)]*value_major/sum(minor_value.values())

                        landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(i)),[years]]=minor_value[(i)]
        
    for years in relevant_years_adjust:    
        value_major = landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]]
        if not value_major.isnull().values.all(): 
            value_major = float(value_major.to_string(index=False, header=False))
            
            for i in list_minor:
                if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                    if  not landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                        value_i=landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]]
                        value_i = float(value_i.to_string(index=False, header=False))
                    else :
                        value_i=0
                    
                    minor_value[(i)]=value_i
                    print('minor value',minor_value[(i)])
                    
                    
        if not (sum(minor_value.values()))==0 : 
            for i in list_minor:
                if (diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and not minor_value[(i)]==0): 
                    if minor_value[(i)] :
                        minor_value[(i)]=minor_value[(i)]*value_major/sum(minor_value.values())
                        landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==diagram.get(key).get(i)),[years]]=minor_value[(i)]     
                
    return landuse  

