# Import the packages and classes needed in this example:
import numpy as np
from sklearn.linear_model import LinearRegression
import yaml
import statistics

def regression(code,parameters,landuse):

    with open(r'aux_data/items_primary.yaml') as file:
        items_primary = yaml.load(file, Loader=yaml.FullLoader)
    
    
    def make_valid_fao_year(year):
        """Make a valid fao year string from int year"""
        return "Y" + str(year)
    
    first_consecutive_values={}
    last_consecutive_values={}
    first_values =[1,2,3]   
    last_values = [4,5,6]  
    
    
    
    for item in items_primary:
        if not code in parameters.get("exeptions"):
            if not item in parameters.get("exeptions"):
                relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
                backward = [make_valid_fao_year(year) for year in list(reversed(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1)))]
                print(relevant_years)
                if item in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :

                    for years in relevant_years:
                        print(item, code,years)
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            first_year = int(years.replace("Y",""))
                            print(first_year)
                            break
                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            last_year = int(years.replace("Y",""))
                            print(last_year)
                            break

                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            value =landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] 
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                for years in ([make_valid_fao_year(year) for year in list(range(year_zero,parameters.get("year_of_interest").get("end")+1))]):   
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] = 0
                    if first_year == parameters.get("year_of_interest").get("begin") and last_year == parameters.get("year_of_interest").get("end"):
                        continue
                                                                            
                    
                    if not first_year == parameters.get("year_of_interest").get("begin") and last_year == parameters.get("year_of_interest").get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("year_of_interest").get("end"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("year_of_interest").get("end")-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("year_of_interest").get("end")-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("year_of_interest").get("end"))]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("year_of_interest").get("end")+4-num)]]
                                    value_num=float(value_num.to_string(index=False, header=False))             
                                    last_consecutive_values[(num)]=value_num


                                numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                average = statistics.mean(numbers1)
                                
                                numbers2 = [last_consecutive_values[key] for key in last_consecutive_values]
                                average2 = statistics.mean(numbers2)
                                
                                x = np.array([first_year+1, parameters.get("year_of_interest").get("end")-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                
                                
                                
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value         
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                    
                                    
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False)            
                  
                    if  first_year == parameters.get("year_of_interest").get("begin") and not last_year == parameters.get("year_of_interest").get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("year_of_interest").get("begin"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("year_of_interest").get("begin"))]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("year_of_interest").get("begin")+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("year_of_interest").get("begin")+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                            
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)

                            if  np.sign(model.coef_) == np.sign(model2.coef_):

                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("year_of_interest").get("begin"))+num-1]]
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
                                
                                x = np.array([parameters.get("year_of_interest").get("begin")+1, last_year-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value         
                                
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
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
                                landuse.to_csv('itemland_use_regression.csv',index = False)            
  
                                                                            
                    
                    if not first_year == parameters.get("year_of_interest").get("begin") and not last_year == parameters.get("year_of_interest").get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(last_year)]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False))])
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
                                
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value         
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                
                                
                                
                                
                                
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value         
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                        
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)    
                                        
                                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                        
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)    
                                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 

                                             
            if  item in parameters.get("exeptions"):
                relevant_years=[make_valid_fao_year(year) for year in list(range(parameters.get("exeptions").get(item).get("begin"),parameters.get("exeptions").get(item).get("end")+1))]
                backward=[make_valid_fao_year(year) for year in list(reversed(range(parameters.get("exeptions").get(item).get("begin"),parameters.get("exeptions").get(item).get("end")+1)))]
                if item in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :

                    for years in relevant_years:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            first_year = int(years.replace("Y",""))
                            break
                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            last_year = int(years.replace("Y",""))
                            break

                           
                    if first_year == parameters.get("exeptions").get(item).get("begin") and last_year == parameters.get("exeptions").get(item).get("end"):
                        continue
                    
                    if first_year == last_year:
                        continue                                                                           
                    
                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            value =landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] 
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                for years in ([make_valid_fao_year(year) for year in list(range(year_zero,parameters.get("year_of_interest").get("end")+1))]):   
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] = 0
                    
                    
                    if not first_year == parameters.get("exeptions").get(item).get("begin") and last_year == parameters.get("exeptions").get(item).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(item).get("end"))]].isnull().values.all():
                            
                            if (last_year-first_year>3):
                                x = np.array([1, 2, 3]).reshape((-1, 1))
                                begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                                end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(item).get("end")-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(item).get("end")-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(item).get("end"))]]).to_string(index=False,header=False))])
                                model = LinearRegression().fit(x, begin) 
                                model2 = LinearRegression().fit(x, end)
                            
                            
                            
                            
                            
                                if  np.sign(model.coef_) == np.sign(model2.coef_):
                                    
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year+num-1)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                    for num in last_values :
                                        value_num=landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(item).get("end")-num+4)]]
                                        value_num=float(value_num.to_string(index=False, header=False))             
                                        last_consecutive_values[(num)]=value_num
    
    
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    
                                    numbers2 = [last_consecutive_values[key] for key in last_consecutive_values]
                                    average2 = statistics.mean(numbers2)
    
                                    x = np.array([first_year+1, parameters.get("exeptions").get(item).get("end")-1]).reshape((-1, 1))
                                    linear = np.array([average, average2])
                                    model3=LinearRegression().fit(x, linear)
                                    for years in range(first_year-1,parameters.get("exeptions").get(item).get("begin")-1,-1):
                                        if model3.coef_ * years +model3.intercept_ >= 0 :
                                            landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                        else :
                                            previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                            previous_value = float(previous_value.to_string(index=False, header=False))
                                            landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                    
                                    landuse.to_csv('itemland_use_regression.csv',index = False)         
                                    first_consecutive_values={}
                                    last_consecutive_values={}
                                        
                                else :
                                    for years in range(first_year-1,parameters.get("exeptions").get(item).get("begin")-1,-1):
                                        
                                        for num in first_values:
                                            value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                            value_num=float(value_num.to_string(index=False, header=False))
                                            first_consecutive_values[(num)]=value_num  
                                            
                                        numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                        average = statistics.mean(numbers1)    
                                        
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                        first_consecutive_values={}
                                    landuse.to_csv('itemland_use_regression.csv',index = False)            

                    
                    if  first_year == parameters.get("exeptions").get(item).get("begin") and not last_year == parameters.get("exeptions").get(item).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(item).get("begin"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(item).get("begin"))]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(item).get("begin")+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(item).get("begin")+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                            
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)

                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(item).get("begin")-1+num)]]
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
                                
                                x = np.array([parameters.get("exeptions").get(item).get("begin")+1, last_year-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                for years in range(last_year+1,parameters.get("exeptions").get(item).get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                     
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
                                first_consecutive_values={}
                                last_consecutive_values={}
        
                            else :
                                for years in range(last_year+1,parameters.get("exeptions").get(item).get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                    
                                    
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                
                                landuse.to_csv('itemland_use_regression.csv',index = False)            
        
                    if not first_year == max(parameters.get("exeptions").get(item).get("begin"),parameters.get("year_of_interest").get("begin")) and not last_year == parameters.get("exeptions").get(item).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(last_year)]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False))])
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
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                      
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,max(parameters.get("exeptions").get(item).get("begin"),parameters.get("year_of_interest").get("begin"))-1,-1):
                                    
                                    
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)

                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                
                                for years in range(last_year+1,parameters.get("exeptions").get(item).get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                 
        if  code in parameters.get("exeptions"):
            if not item in parameters.get("exeptions"):
                relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
                backward = [make_valid_fao_year(year) for year in list(reversed(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1)))]
                if item in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :

                    for years in relevant_years:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            first_year = int(years.replace("Y",""))
                            break
                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            last_year = int(years.replace("Y",""))
                            break
       
                    if first_year == parameters.get("exeptions").get(code).get("begin") and last_year == parameters.get("exeptions").get(code).get("end"):
                        continue
                                                                            
                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            value =landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] 
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                for years in ([make_valid_fao_year(year) for year in list(range(year_zero,parameters.get("year_of_interest").get("end")+1))]):   
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] = 0
                                    
                    if not first_year == parameters.get("exeptions").get(code).get("begin") and last_year == parameters.get("exeptions").get(code).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(code).get("end"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("end")-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("end")-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("end"))]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(code).get("end")+4-num)]]
                                    value_num=float(value_num.to_string(index=False, header=False))             
                                    last_consecutive_values[(num)]=value_num


                                numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                average = statistics.mean(numbers1)
                                
                                numbers2 = [last_consecutive_values[key] for key in last_consecutive_values]
                                average2 = statistics.mean(numbers2)

                                x = np.array([first_year+1, parameters.get("exeptions").get(code).get("end")-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                   
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                
                                landuse.to_csv('itemland_use_regression.csv',index = False)            

                    
                    if  first_year == parameters.get("exeptions").get(code).get("begin") and not last_year == parameters.get("exeptions").get(code).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(code).get("begin"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("begin"))]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("begin")+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("begin")+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                            
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)

                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(code).get("begin")+num-1)]]
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

                                x = np.array([parameters.get("exeptions").get(code).get("begin")+1, last_year-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                        
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
                                first_consecutive_values={}
                                last_consecutive_values={}
        
                            else :
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                               


                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                
                                landuse.to_csv('itemland_use_regression.csv',index = False)            
 
                                                                            
                    
                    if not first_year == parameters.get("exeptions").get(code).get("begin") and not last_year == parameters.get("exeptions").get(code).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(last_year)]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False))])
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
                                for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value              
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                   
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)

                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 


                        
            if  item in parameters.get("exeptions"):
                relevant_years=[make_valid_fao_year(year) for year in list(range(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")),parameters.get("exeptions").get(code).get("end")+1))]
                backward=[make_valid_fao_year(year) for year in list(reversed(range(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")),parameters.get("exeptions").get(code).get("end")+1)))]
                if item in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :

                    for years in relevant_years:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            first_year = int(years.replace("Y",""))
                            break
                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            last_year = int(years.replace("Y",""))
                            break

                    for years in backward:
                        if  not landuse.loc[((landuse['Item Code']==item)&(landuse['ISO3']==code)),[years]].isnull().values.all():
                            value =landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] 
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                for years in ([make_valid_fao_year(year) for year in list(range(year_zero,parameters.get("year_of_interest").get("end")+1))]):   
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),[years]] = 0
                                    
                    if first_year == max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")) and last_year == parameters.get("exeptions").get(code).get("end"):
                        continue
                                                                            
                    
                    if not first_year == max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")) and last_year == parameters.get("exeptions").get(code).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(item).get("end"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("end")-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("end")-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(parameters.get("exeptions").get(code).get("end"))]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(parameters.get("exeptions").get(code).get("end")+4-num)]]
                                    value_num=float(value_num.to_string(index=False, header=False))             
                                    last_consecutive_values[(num)]=value_num


                                numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                average = statistics.mean(numbers1)
                                
                                numbers2 = [last_consecutive_values[key] for key in last_consecutive_values]
                                average2 = statistics.mean(numbers2)

                                x = np.array([first_year+1, parameters.get("exeptions").get(code).get("end")-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                for years in range(first_year-1,max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                     
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))-1,-1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False)            

                    
                    if  first_year == max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")) and not last_year == parameters.get("exeptions").get(item).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin")))]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                            
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)

                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))+num-1)]]
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

                                x = np.array([max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))+1, last_year-1]).reshape((-1, 1))
                                linear = np.array([average, average2])
                                model3=LinearRegression().fit(x, linear)
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                                     
                                landuse.to_csv('itemland_use_regression.csv',index = False)         
                                first_consecutive_values={}
                                last_consecutive_values={}
        
                            else :
                                for years in range(last_year+1,parameters.get("exeptions").get(item).get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False)            
  
                    if not first_year == max(parameters.get("exeptions").get(item).get("begin"),parameters.get("exeptions").get(code).get("begin")) and not last_year == parameters.get("exeptions").get(code).get("end"):
                        if not landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(last_year)]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((landuse.loc[(landuse['ISO3']==code)&(landuse['Item Code']==item),["Y" + str(last_year-2)]]).to_string(index=False,header=False))])
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
                                for years in range(first_year-1,max(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(item).get("begin"))-1,-1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                            
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]= previous_value                             
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,max(parameters.get("exeptions").get(item).get("begin"),parameters.get("exeptions").get(code).get("begin"))-1,-1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
                                
                                landuse.to_csv('itemland_use_regression.csv',index = False)
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    for num in first_values:
                                        value_num= landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                
                                    landuse.loc[(landuse['Item Code']==item)&(landuse['ISO3']==code),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                landuse.to_csv('itemland_use_regression.csv',index = False) 
