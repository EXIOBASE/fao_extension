#import calcul_1_new as cal1
#import calcul_2_new as cal2
import calculation as cal
import calcul_3 as cal3
import adjustmentcase2 as adj2
import empty_cells_0706 as ec0706 
import make_table_pourcentage_case2 as mtpc2
import calcul_pourcent_case2 as cpc2
from make_years import make_valid_fao_year as mvy


def solve(landuse, dfs,code,relevant_years, diagram,key,country,missing,year3b,year3e,year2e,year2b,year1e,year1b,a,parameters):
    list3=[]
    list3 = ['minor1','minor2','minor3']    
    list2=[]
    list2=list3.copy()
    
    if year3b and (min(a)==year3b):
        relevant_years_adjust = [mvy(year) for year in list(range(year3b,year3e+1))]
        list3.remove('minor3')
        minor=str("minor3")

    if year1b and (min(a)==year1b):
        relevant_years_adjust = [mvy(year) for year in list(range(year1b,year1e+1))]
        list3.remove('minor1')
        minor=str("minor1")

    if year2b and (min(a)==year2b):
        relevant_years_adjust = [mvy(year) for year in list(range(year2b,year2e+1))]        
        list3.remove('minor2')
        minor=str("minor2")

    for years in relevant_years_adjust :         
        if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
            #cal1.calculation(landuse,code,key,years,diagram)
            #cal2.calculation(landuse,code,key,years,diagram)
            cal.calculation(landuse,code,key,years,diagram)
            cal.calculation2(landuse,code,key,years,diagram)
    
    relevant_years_adjust2 = [mvy(year) for year in range(parameters.get("year_of_interest").get("begin"),max(a))]
    

    for years in relevant_years_adjust2 :

        if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
            cal3.calculation(landuse,code,key,years,list2,list3,diagram)

    
    mtpc2.make_table(landuse, dfs,code,years, diagram,key,country, relevant_years_adjust2,relevant_years_adjust,list2,list3)
    file_name = str(key)+".csv"  
    dfs[key].to_csv(file_name, index=False) 
                
        
    missing = ec0706.check(landuse, code, years,key,missing,diagram,parameters)
    landuse.to_csv('land_use.csv',index = False) 
        
    if missing == 1 :
        cpc2.pourcentage(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust2,relevant_years_adjust,list3)
        landuse.to_csv('land_use.csv',index = False)

        adj2.adjust(landuse, dfs,code,years, diagram,key,country,relevant_years_adjust2,relevant_years_adjust,list2,list3) 
    landuse.to_csv('land_use.csv',index = False)
        

    
    return landuse,dfs
 