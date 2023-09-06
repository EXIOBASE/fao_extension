# Import the packages and classes needed in this example:
import numpy as np
from sklearn.linear_model import LinearRegression
import statistics
from make_years import make_valid_fao_year as mvy

def regression(country,parameters,table_of_interest,item_list,col_years):

   
    relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
    backward = [mvy(year) for year in list(reversed(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1)))]


    
    df_copy=table_of_interest.copy()
    unit_list=table_of_interest['Unit'].unique()
    
    for code in country:
        first_consecutive_values={}
        last_consecutive_values={}
        first_values =[1,2,3]   
        last_values = [4,5,6]  
        print(code)
        if code in parameters.get("exeptions"):
            relevant_years = [mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]
            backward = [mvy(year) for year in list(reversed(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1)))]
                
            for item in item_list:
                print(item)
                unit_ind=[]

                for a in unit_list:
                    if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                        unit_ind.append(a) 
                for b in unit_ind:        
    
                    for years in relevant_years:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():
                            first_year = int(years.replace("Y",""))
                            break
                        else :
                            first_year = None
                    for years in backward:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():
                            last_year = int(years.replace("Y",""))
                            break
                        else :
                            last_year = None
    
                    for years in backward:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():
                            value =df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[years]] 
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                for years in ([mvy(year) for year in list(range(year_zero,parameters.get("exeptions").get(code).get("end")+1))]):   
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[years]] = 0
                    if first_year == parameters.get("exeptions").get(code).get("begin") and last_year == parameters.get("exeptions").get(code).get("end"):
                        continue
                    
                    if  (first_year == None and last_year == None):
                       continue    
                                                    
                    if first_year == last_year:
                        value =df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[mvy(first_year)]]
                        value=float(value.to_string(index=False, header=False))
                        for years in ([mvy(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]):   
                            df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[years]] = value
    
                        continue
                    pass
             
                    if last_year-first_year==1 :
                        valeur=0
                        for years in range (first_year, last_year+1):
                            instant=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]
                            instant=float(instant.to_string(index=False, header=False))
                            valeur=valeur+instant
                        valeur= valeur // 2
                        
                        
                        for years in range (parameters.get("exeptions").get(code).get("begin"),first_year):
                            if df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]].isnull().values.all():
                                df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=valeur
    
                        for years in range (last_year,parameters.get("exeptions").get(code).get("end")+1):
                            if df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]].isnull().values.all():
                                df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=valeur
                        
                        continue
                    
                    pass
                        
                        
    
    
                        
                       
                    if last_year-first_year<5 and last_year-first_year>=2:
                        for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                            for num in first_values:
                                value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+num)]]
                                value_num=float(value_num.to_string(index=False, header=False))
                                first_consecutive_values[(num)]=value_num  
                            numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                            average = statistics.mean(numbers1)
                            df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                        first_consecutive_values={}
    
                        for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                            for num in first_values:
                                value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-num)]]
                                value_num=float(value_num.to_string(index=False, header=False))
                                first_consecutive_values[(num)]=value_num 
                                    
                                    
                            numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                            average = statistics.mean(numbers1)
                            df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                        first_consecutive_values={}
                        
                           
                        
                        continue
                    pass                
                
                    
                
                    if not first_year == parameters.get("exeptions").get(code).get("begin") and last_year == parameters.get("exeptions").get(code).get("end"):
                        if not df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("end"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("end")-2)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("end")-1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("end"))]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                
                                for num in first_values:
                                    value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("end")+4-num)]]
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
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value         
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                                    
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                    
                                    
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                  
                    if  first_year == parameters.get("exeptions").get(code).get("begin") and not last_year == parameters.get("exeptions").get(code).get("end"):
                        if not df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("begin"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("begin"))]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("begin")+1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("begin")+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                            
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            
    
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
    
                                for num in first_values:
                                    value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("exeptions").get(code).get("begin")+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(last_year+4-num)]]
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
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value         
                                
                                first_consecutive_values={}
                                last_consecutive_values={}
        
                            else :
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                    
                                    
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
      
                                                                            
                    
                    if not first_year == parameters.get("exeptions").get(code).get("begin") and not last_year == parameters.get("exeptions").get(code).get("end"):
                        if not df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(last_year)]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-2)]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                
                                for num in first_values:
                                    value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(last_year+4-num)]]
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
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value         
                                
                                
                                
                                
                                
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value         
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("exeptions").get(code).get("begin")-1,-1):
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                        
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)    
                                        
                                    
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                
                                for years in range(last_year+1,parameters.get("exeptions").get(code).get("end")+1):
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                        
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)    
                                    
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}

                                             
            
                 
        if  not code in parameters.get("exeptions"):
            
            relevant_years = [mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
            backward = [mvy(year) for year in list(reversed(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1)))]  
            for item in item_list:
                print(item)
                unit_ind=[]

                for a in unit_list:
                    if a in df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item),['Unit']].values:
                        unit_ind.append(a) 
                for b in unit_ind:

                    for years in relevant_years:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():
                            first_year = int(years.replace("Y",""))
                            break
                        else:
                            first_year= None
                            
                    for years in backward:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():
                            last_year = int(years.replace("Y",""))
                            break
                        else :
                            last_year= None
                            

                   
                    if first_year == parameters.get("year_of_interest").get("begin") and last_year == parameters.get("year_of_interest").get("end"):
                        continue
                                                                            
                    for years in backward:
                        if  not df_copy.loc[((df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b)),[years]].isnull().values.all():
                            value =df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[years]] 
                            value=float(value.to_string(index=False, header=False))
                            year_zero = int(years.replace("Y",""))
                            if value == 0 :
                                for years in ([mvy(year) for year in list(range(year_zero,parameters.get("year_of_interest").get("end")+1))]):   
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[years]] = 0
                    
                    if  (first_year == None and last_year == None):
                       continue
                    
                    if first_year == last_year:
                        value =df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[mvy(first_year)]]
                        value=float(value.to_string(index=False, header=False))
                        for years in ([mvy(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]):   
                            df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),[years]] = value
    
                        continue
                    pass
             
                    if last_year-first_year==1 :
                        valeur=0
                        for years in range (first_year, last_year+1):
                            instant=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]
                            instant=float(instant.to_string(index=False, header=False))
                            valeur=valeur+instant
                        valeur= valeur // 2
                        
                        
                        for years in range (parameters.get("year_of_interest").get("begin"),first_year):
                            if df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]].isnull().values.all():
                                df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=valeur
    
                        for years in range (last_year,parameters.get("year_of_interest").get("end")+1):
                            if df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]].isnull().values.all():
                                df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=valeur
                        
                        continue
                    
                    pass
                        

                       
                    if last_year-first_year<5 and last_year-first_year>=2:
                        for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                            for num in first_values:
                                value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+num)]]
                                value_num=float(value_num.to_string(index=False, header=False))
                                first_consecutive_values[(num)]=value_num  
                            numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                            average = statistics.mean(numbers1)
                            df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                        first_consecutive_values={}
    
                        for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                            for num in first_values:
                                value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-num)]]
                                value_num=float(value_num.to_string(index=False, header=False))
                                first_consecutive_values[(num)]=value_num 
                                    
                                    
                            numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                            average = statistics.mean(numbers1)
                            df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                        first_consecutive_values={}
                        
                           
                        
                        continue
                    pass                                    
                    
                    

                    
                    if not first_year == parameters.get("year_of_interest").get("begin") and last_year == parameters.get("year_of_interest").get("end"):
                        if not df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("end"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("end")-2)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("end")-1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("end"))]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("end")+4-num)]]
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
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value                                   
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                
                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                

                    
                    if  first_year == parameters.get("year_of_interest").get("begin") and not last_year == parameters.get("year_of_interest").get("end"):
                        if not df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("begin"))]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("begin"))]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("begin")+1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("begin")+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-2)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year)]]).to_string(index=False,header=False))])
                            
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)

                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(parameters.get("year_of_interest").get("begin")+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(last_year+4-num)]]
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
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value                                        
                                first_consecutive_values={}
                                last_consecutive_values={}
        
                            else :
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                               


                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                
 
                                                                            
                    
                    if not first_year == parameters.get("year_of_interest").get("begin") and not last_year == parameters.get("year_of_interest").get("end"):
                        if not df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(last_year)]].isnull().values.all():
                            x = np.array([1, 2, 3]).reshape((-1, 1))
                            begin = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(first_year+2)]]).to_string(index=False,header=False))])
                            end = np.array([float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-1)]]).to_string(index=False,header=False)), float((df_copy.loc[(df_copy['ISO3']==code)&(df_copy['Item Code']==item)&(df_copy['Unit']==b),["Y" + str(last_year-2)]]).to_string(index=False,header=False))])
                            model = LinearRegression().fit(x, begin) 
                            model2 = LinearRegression().fit(x, end)
                            if  np.sign(model.coef_) == np.sign(model2.coef_):
                                for num in first_values:
                                    value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(first_year+num-1)]]
                                    value_num=float(value_num.to_string(index=False, header=False))
                                    first_consecutive_values[(num)]=value_num  
                                for num in last_values :
                                    value_num=df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(last_year+4-num)]]
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
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value              
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    if model3.coef_ * years +model3.intercept_ >= 0 :
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=model3.coef_ * years +model3.intercept_
                                    else :
                                        previous_value = df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-1)]]
                                        previous_value = float(previous_value.to_string(index=False, header=False))
                                        df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]= previous_value                                   
                                first_consecutive_values={}
                                last_consecutive_values={}
                                    
                            else :
                                for years in range(first_year-1,parameters.get("year_of_interest").get("begin")-1,-1):
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years+num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)
                                
                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
                                
                                for years in range(last_year+1,parameters.get("year_of_interest").get("end")+1):
                                    for num in first_values:
                                        value_num= df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years-num)]]
                                        value_num=float(value_num.to_string(index=False, header=False))
                                        first_consecutive_values[(num)]=value_num  
                                

                                    numbers1 = [first_consecutive_values[key] for key in first_consecutive_values]
                                    average = statistics.mean(numbers1)

                                    df_copy.loc[(df_copy['Item Code']==item)&(df_copy['ISO3']==code)&(df_copy['Unit']==b),["Y" + str(years)]]=average
                                    first_consecutive_values={}
   
    
    df_copy.to_csv('regression.csv',index = False)
                            
    table_of_interest = df_copy.copy()
    return table_of_interest 