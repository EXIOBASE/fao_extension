#import calcul_1_new as cal1
#import calcul_2_new as cal2
import calculation as cal
import make_table_pourcentage as mtp
from make_years import make_valid_fao_year as mvy
import empty_cells as ec
import calcul_pourcent_all as cpa
import adjustment as adj


def solve(landuse, dfs,code,relevant_years, diagram,key,country,missing,parameters):
    for years in relevant_years :
        if key in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
            if  not landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                first_year = int(years.replace("Y",""))
                relevant_years_2 = [mvy(year) for year in list(range(first_year,parameters.get("year_of_interest").get("end")+1))]
        
                for years in relevant_years_2:
                    cal.calculation2(landuse,code,key,years,diagram)       
                    cal.calculation(landuse,code,key,years,diagram)
            
        
                mtp.make_table(landuse, dfs,code,relevant_years_2, diagram,key,country) 
                file_name = str(key)+".csv"  #Change the column name accordingly
                dfs[key].to_csv(file_name, index=False)
                #landuse.to_csv('land_use3.csv',index = False)
   
                missing = ec.check(landuse, code, relevant_years_2,key,missing,diagram)
                if missing == 1:
                    for years in relevant_years_2 : 
                        cpa.pourcentage(landuse, dfs,code,years, diagram,key,country)  
                    for years in relevant_years_2 :  
                        cpa.pourcentage2(landuse, dfs,code,years, diagram,key,country)
                    for years in relevant_years_2 :  
                        adj.adjust(landuse, dfs,code,years, diagram,key,country)
                    #landuse.to_csv('land_use3.csv',index = False)
        
    
    return landuse,dfs

