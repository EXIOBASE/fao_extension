# import the python pandas package
import pandas as pd
 
# create  data_frame1 by creating a dictionary
# in which values are stored as list
data_frame1 = pd.DataFrame({'Fruits': ['Appple', 'Banana', 'Mango',
                                       'Dragon Fruit', 'Musk melon', 'grapes'],
                            'Sales in kg': [20, 30, 15, 10, 50, 40]})
 
# create  data_frame2 by creating a dictionary
# in which values are stored as list
data_frame2 = pd.DataFrame({'Vegetables': ['tomato', 'Onion', 'ladies finger',
                                           'beans', 'bedroot', 'carrot'],
                            'Sales in kg': [200, 310, 115, 110, 55, 45]})
 
# create  data_frame3 by creating a dictionary
# in which values are stored as list
data_frame3 = pd.DataFrame({'Baked Items': ['Cakes', 'biscuits', 'muffins',
                                            'Rusk', 'puffs', 'cupcakes'],
                            'Sales in kg': [120, 130, 159, 310, 150, 140]})
 
print(data_frame1)
print(data_frame2)
print(data_frame3)
 
# create a excel writer object
with pd.ExcelWriter("filename.xlsx") as writer:
   
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet
    data_frame1.to_excel(writer, sheet_name="Fruits", index=False)
    data_frame2.to_excel(writer, sheet_name="Vegetables", index=False)
    data_frame3.to_excel(writer, sheet_name="Baked Items", index=False)

writer