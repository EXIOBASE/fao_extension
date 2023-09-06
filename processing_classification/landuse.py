#import landuse_calculation as luc
import yaml
import pandas as pd

def make_valid_fao_year(year):
    """Make a valid fao year string from int year"""
    return "Y" + str(year)


with open(r'parameters.yaml') as file:
    parameters = yaml.load(file, Loader=yaml.FullLoader)
    
with open(r'country.yaml') as file:
    country = yaml.load(file, Loader=yaml.FullLoader)
    

crop_primary = pd.read_csv('final_cropland_primary.csv', encoding="latin-1") 
list_ISO3 = list(crop_primary['ISO3'])
country = [] 
for i in list_ISO3: 
    if i not in country: 
        country.append(i)


for code in country:
    if not code in parameters.get("exeptions"):
        relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
    else:
        relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
    print(code, relevant_years)
    table=luc.make_table_per_year(relevant_years)  