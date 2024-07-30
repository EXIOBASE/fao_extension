# Import the packages and classes needed in this example:
import numpy as np
from sklearn.linear_model import LinearRegression
import yaml
import statistics


def regression(code,parameters,landuse,diagram):
    
 
    
    def make_valid_fao_year(year):
        """Make a valid fao year string from int year"""
        return "Y" + str(year)


    first_consecutive_values={}
    last_consecutive_values={}
    first_values =[1,2,3]   
    last_values = [4,5,6]  

    
    for item in diagram:
        relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
        backward = [make_valid_fao_year(year) for year in list(reversed(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1)))]
        if item in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
            for years in relevant_years:
                if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                    first_year = int(years.replace("Y",""))
                    break
                else:
                    first_year= None
                    #break
            for years in backward:
                if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                    last_year = int(years.replace("Y",""))
                    break
                else:
                    last_year= None
                    
            for years in backward:
                if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                    value =landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] 
                    value=float(value.to_string(index=False, header=False))
                    year_zero = int(years.replace("Y",""))
                    if value == 0 :
                        for years in ([make_valid_fao_year(year) for year in list(range(year_zero,parameters.get("year_of_interest").get("end")+1))]):   
                            landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] = 0
                            
            if  (first_year == None and last_year == None):
                continue
            
            if first_year==last_year :

                value_unique = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year)]]
                value_unique=float(value_unique.to_string(index=False, header=False))
                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=value_unique
                landuse.to_csv('itemland_use_regression2.csv',index = False)    
                continue
            if (last_year - first_year==1) :
                value_1 = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year)]]
                value_1=float(value_1.to_string(index=False, header=False))
                value_2 = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(last_year)]]
                value_2=float(value_2.to_string(index=False, header=False))
                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=(value_1+value_2)/2
                landuse.to_csv('itemland_use_regression2.csv',index = False) 
                continue
            
            else :
                if  not last_year == parameters.get("year_of_interest").get("end"):
                    if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year)]].isnull().values.all():
                        x = np.array([1, 2, 3]).reshape((-1, 1))
                        begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                        end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                                        
                        model = LinearRegression().fit(x, begin) 
                        model2 = LinearRegression().fit(x, end)
                        if  np.sign(model.coef_) == np.sign(model2.coef_):
                            for num in first_values:
                                value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year+num-1)]]
                                value_num=float(value_num.to_string(index=False, header=False))
                                first_consecutive_values[(num)]=value_num  
                            for num in last_values :
                                value_num=landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(last_year+4-num)]]
                                value_num=float(value_num.to_string(index=False, header=False))             
                                last_consecutive_values[(num)]=value_num


                            numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                            average = statistics.mean(numbers1)
                                
                            numbers2 = [last_consecutive_values[key] for key in last_consecutive_values]
                            average2 = statistics.mean(numbers2)
                                
                            x = np.array([first_year+1, last_year-1]).reshape((-1, 1))
                            linear = np.array([average, average2])
                            model3=LinearRegression().fit(x, linear)
                            for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                if model3.coef_ * years +model3.intercept_ >= 0 :
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                else :
                                    previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                    previous_value = float(previous_value.to_string(index=False, header=False))
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value
                            landuse.to_csv('itemland_use_regression2.csv',index = False)         
                            first_consecutive_values={}
                            last_consecutive_values={}    
        
                        else :
                            for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  


                                numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                average = statistics.mean(numbers1)
                                
               
                                landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                first_consecutive_values={}
                            landuse.to_csv('itemland_use_regression2.csv',index = False)            
  
                                                                               
            
    return landuse