'''
In this module, we fill empty cells which we consider should be 0.
For exemple, if 0 is the only value available for one Faoitem, we consider that
we can fill the empty cell corresponding to this FAOitem with a 0 value
'''

from make_years import make_valid_fao_year as mvy

def assumption(country, FAOitem, parameters, landuse,col_years):

    for code in country:
        for item in FAOitem :
            '''
            We determine the years of interest.
            For some country or for some FaoItem, the whole range is not necessary 1961 to 2018
            '''
            
            if not (item  in parameters.get("exeptions") and code in parameters.get("exeptions")):
                relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
                backward = [mvy(year) for year in list(reversed(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1)))]
                begin=parameters.get("year_of_interest").get("begin")
            if not item  in parameters.get("exeptions") and  code in parameters.get("exeptions"):
                relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
                backward = [mvy(year) for year in list(reversed(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1)))]
                begin=parameters.get("exeptions").get(code).get("begin")
            if item  in parameters.get("exeptions") and  not code in parameters.get("exeptions"):
                relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(item).get("begin"),parameters.get("exeptions").get(item).get("end")+1))]
                backward = [mvy(year) for year in list(reversed(range(parameters.get("exeptions").get(item).get("begin"),parameters.get("exeptions").get(item).get("end")+1)))]
                begin=parameters.get("exeptions").get(item).get("begin")
            if item  in parameters.get("exeptions") and  code in parameters.get("exeptions"):
                relevant_years = [mvy(year) for year in list(range(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")),parameters.get("exeptions").get(code).get("end")+1))]
                backward = [mvy(year) for year in list(reversed(range(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")),parameters.get("exeptions").get(code).get("end")+1)))]
                begin=max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))
            
            '''
            The first step to fill out the table is to check if for some item, only a zero value is available. No matter the number of corresponding years.
            '''
           
            if not (landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item)&(landuse['Unit']=='1000 ha'),col_years].isnull().values.all()) :
                diff_value_per_line = int(landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
                #diff_value_per_line=int(diff_value_per_line)
                nber_value_per_line = landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),col_years].count(axis=1, numeric_only=True)
                nber_value_per_line=nber_value_per_line.astype(int)
                if  (diff_value_per_line == 1):
                    value = landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),col_years].mean(axis=1,skipna=True) 
                    value = float(value.to_string(index=False, header=False)) 
                    if (value == 0.0):
                        for years in relevant_years :
                            if (landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),[years]].isnull().values.any()):
                                landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),[years]]=0
        
        '''
        For each FAOitem, if there is 3 consecutive years with a zero value, and if there is empty cell before these years, we consider the reported value to be 0 for these first years.
        '''
        for item in FAOitem :
            for years in relevant_years:

                if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                    value =landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] 
                    value=float(value.to_string(index=False, header=False))
                    year_zero = int(years.replace("Y",""))
                    if value == 0 and  year_zero < 2016:
                        years_consecutives = [mvy(year) for year in list(range(year_zero,year_zero+3))]
                        if all(float(landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].to_string(index=False, header=False)) == 0 for years in years_consecutives):
                            year_zero= [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),year_zero))]
                            for years in year_zero :
                                landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),[years]]=0
    return landuse
