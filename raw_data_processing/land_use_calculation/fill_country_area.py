from make_years import make_valid_fao_year as mvy
import ray

'''
This module is filling empty cells related to country area.
'''


def fill(landuse, code,col_years,relevant_years,parameters):
    relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
    if code in parameters.get("exeptions"):
        relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
    if not (landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==6600)&(landuse['Unit']=='1000 ha'),col_years].isnull().values.all()) :
        diff_value_per_line = int(landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==6600),col_years].nunique(axis=1,dropna=True).to_string(header=False, index=False))
        nber_value_per_line = landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==6600),col_years].count(axis=1, numeric_only=True)
        nber_value_per_line=nber_value_per_line.astype(int)
        if  (diff_value_per_line == 1):
            value = landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==6600),col_years].mean(axis=1,skipna=True) 
            value = value.to_string(index=False, header=False)
            for years in relevant_years :
                if (landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==6600),[years]].isnull().values.any()):
                    landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==6600),[years]]=value
    return landuse





