
def check(landuse, code, relevant_years,key,missing,diagram):
    list = ['minor1','minor2','minor3']
    for i in list:
    
        if diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
            for years in relevant_years:

                if  landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                    return 1
        

    return 0



