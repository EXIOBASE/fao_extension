from make_years import make_valid_fao_year as mvy

def check(landuse, code, years,key,missing,diagram,parameters):
    if diagram.get(key).get("minor1") in parameters.get("exeptions"):
        exeption1=diagram.get(key).get("minor1")

        year1b=parameters.get("exeptions").get(exeption1).get("begin")
        year1e=parameters.get("exeptions").get(exeption1).get("end")
    else :
        year1b=parameters.get("year_of_interest").get("begin")
        year1e=parameters.get("year_of_interest").get("end")
        
        
    if diagram.get(key).get("minor2") in parameters.get("exeptions"):
        exeption2=diagram.get(key).get("minor2")

        year2b=parameters.get("exeptions").get(exeption2).get("begin")
        year2e=parameters.get("exeptions").get(exeption2).get("end")
    else :
        year2b=parameters.get("year_of_interest").get("begin")
        year2e=parameters.get("year_of_interest").get("end")
        
    if diagram.get(key).get("minor3") in parameters.get("exeptions"):
        exeption3=diagram.get(key).get("minor3")

        year3b=parameters.get("exeptions").get(exeption3).get("begin")
        year3e=parameters.get("exeptions").get(exeption3).get("end")
    else :
        year3b=parameters.get("year_of_interest").get("begin")
        year3e=parameters.get("year_of_interest").get("end")

    if diagram.get(key).get("minor1") in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
        relevant_years_1 = [mvy(year) for year in range(year1b,year1e+1)]
        for years in relevant_years_1:
            if  landuse.loc[((landuse['Item Code']==diagram.get(key).get("minor1"))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                return 1
            
                
    if diagram.get(key).get("minor2") in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
        relevant_years_2 = [mvy(year) for year in range(year2b,year2e+1)]
        for years in relevant_years_2 :
            if  landuse.loc[((landuse['Item Code']==diagram.get(key).get("minor2"))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                return 1
                      
    if diagram.get(key).get("minor3") in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
        relevant_years_3 = [mvy(year) for year in range(year3b,year3e+1)]
        for years in relevant_years_3 :
            if  landuse.loc[((landuse['Item Code']==diagram.get(key).get("minor3"))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                return 1
            
    return 0
