import calculation as cal
import calcul_3 as cal3
import adjustmentcase2 as adj2
import adjustment as adj
import make_table_pourcentage_case4 as mtpc4
import empty_cells as ec
import calcul_pourcent_case4 as cpc4
import calcul_pourcent_all as cpa
from make_years import make_valid_fao_year as mvy
 


def solve(landuse, dfs,code,relevant_years, diagram,key,country,missing,year3b,year3e,year2e,year2b,year1e,year1b,a,parameters):
    list3=[]
    list3 = ['minor1','minor2','minor3']    
    list2=[]
    list2=list3.copy()
    
    
    if (year3b and (min(a)==year3b) and year3b<parameters.get("exeptions").get(code).get("begin")):
        relevant_years_adjust = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
        list3.remove('minor3')
        minor=str("minor3")
    else:
        if (year1b and (min(a)==year1b) and year1b<parameters.get("exeptions").get(code).get("begin")):
            relevant_years_adjust = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
            list3.remove('minor1')
            minor=str("minor1")
        else :
            if year2b and (min(a)==year2b) and year2b<parameters.get("exeptions").get(code).get("begin"):
                relevant_years_adjust = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
                list3.remove('minor2')
                minor=str("minor2")
                
            
    if ((year3b and (min(a)==year3b) and year3b<parameters.get("exeptions").get(code).get("begin")) or (year1b and (min(a)==year1b) and year1b<parameters.get("exeptions").get(code).get("begin")) or (year2b and (min(a)==year2b) and year2b<parameters.get("exeptions").get(code).get("begin"))) :
        for years in relevant_years_adjust :             
            if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                cal.calculation(landuse,code,key,years,diagram)
                cal.calculation2(landuse,code,key,years,diagram)
        mtpc4.make_table(landuse, dfs,code,years, diagram,key,country,relevant_years,list2)
        file_name = str(key)+".csv"  #Change the column name accordingly
        dfs[key].to_csv(file_name, index=False) 
                       
        missing = ec.check(landuse, code, relevant_years_adjust,key,missing,diagram)

            
        if missing == 1 :            
            for years in relevant_years_adjust : 
                cpa.pourcentage(landuse, dfs,code,years, diagram,key,country)
            for years in relevant_years_adjust : 
                cpa.pourcentage2(landuse, dfs,code,years, diagram,key,country)
            for years in relevant_years_adjust : 
                adj.adjust(landuse, dfs,code,years, diagram,key,country)                
                
    
    if year3b and (min(a)==year3b) and year3b>parameters.get("exeptions").get(code).get("begin"):
        relevant_years_adjust = [mvy(year) for year in list(range(year3b,parameters.get("exeptions").get(code).get("end")+1))]
        relevant_years_adjust2= [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),year3b))]
        list3.remove('minor3')
        minor=str("minor3")
    else :
        if year1b and (min(a)==year1b) and year1b>parameters.get("exeptions").get(code).get("begin"):
            relevant_years_adjust = [mvy(year) for year in list(range(year1b,parameters.get("exeptions").get(code).get("end")+1))]
            relevant_years_adjust2= [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),year1b))]
            list3.remove('minor1')
            minor=str("minor1")
        else :
            if year2b and (min(a)==year2b) and year2b>parameters.get("exeptions").get(code).get("begin"):
                relevant_years_adjust = [mvy(year) for year in list(range(year2b,parameters.get("exeptions").get(code).get("end")+1))]      
                relevant_years_adjust2= [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),year2b))]
                list3.remove('minor2')
                minor=str("minor2")
    
    
    if ((year3b and (min(a)==year3b) and year3b>parameters.get("exeptions").get(code).get("begin")) or (year1b and (min(a)==year1b) and year1b>parameters.get("exeptions").get(code).get("begin")) or (year2b and (min(a)==year2b) and year2b>parameters.get("exeptions").get(code).get("begin"))):
        for years in relevant_years_adjust :             
            if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                
                cal.calculation(landuse,code,key,years,diagram)
                cal.calculation2(landuse,code,key,years,diagram)
        for years in relevant_years_adjust2:
            if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                cal3.calculation(landuse,code,key,years,list2,list3,diagram)
        mtpc4.make_table(landuse, dfs,code,years, diagram,key,country,relevant_years,list2)
        file_name = str(key)+".csv"  #Change the column name accordingly
        dfs[key].to_csv(file_name, index=False)     
    
    
        missing = ec.check(landuse, code, relevant_years,key,missing,diagram)
            
        if missing == 1 :
            if diagram.get(key).get(minor) in parameters.get("exeptions"):
                relevant_years_adjust = [mvy(year) for year in list(range(parameters.get("exeptions").get(diagram.get(key).get(minor)).get("begin"),parameters.get("exeptions").get(diagram.get(key).get(minor)).get("end")+1))]    
                relevant_years_adjust2 = [mvy(year) for year in range(parameters.get("year_of_interest").get("begin"),max(a))]
                cpc4.pourcentage(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust2,relevant_years_adjust,list3)
                
                adj2.adjust(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust2,relevant_years_adjust,list2,list3)
    
  
    return landuse,dfs
 