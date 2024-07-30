#import calcul_1_new as cal1
#import calcul_2_new as cal2
import calculation as cal
import make_table_pourcentage as mtp
import empty_cells as ec
import calcul_pourcent_all as cpa
import adjustment as adj


def solve(landuse, dfs,code,relevant_years, diagram,key,country,missing):
    for years in relevant_years :
        if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
            #cal2.calculation(landuse,code,key,years,diagram)       
            #cal1.calculation(landuse,code,key,years,diagram)
            cal.calculation2(landuse,code,key,years,diagram)
            cal.calculation(landuse,code,key,years,diagram)
            
    mtp.make_table(landuse, dfs,code,relevant_years, diagram,key,country) 
    file_name = str(key)+".csv"  #Change the column name accordingly
    dfs[key].to_csv(file_name, index=False)
    missing = ec.check(landuse, code, relevant_years,key,missing,diagram)
    if missing == 1:
        for years in relevant_years : 
            cpa.pourcentage(landuse, dfs,code,years, diagram,key,country)
        for years in relevant_years : 
            cpa.pourcentage2(landuse, dfs,code,years, diagram,key,country)
        for years in relevant_years : 
            adj.adjust(landuse, dfs,code,years, diagram,key,country)
        
    
    return landuse,dfs

