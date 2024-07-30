import pandas as pd
import country_converter as coco


cc = coco.CountryConverter()
cc.valid_class
cc.get_correspondence_dict('ISO3', 'EXIO3')

converter=coco.country_converter
xls = pd.ExcelFile('Cropland.xlsx')
df1 = pd.read_excel(xls, 'final cropland')
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]     
print(df1.set_index(['ISO3','EXIOBASE product code','EXIOBASE product','Unit']))
country_code = list(df1['ISO3'])
print(country_code)
df1.insert(1, 'EXIO3', converter.convert(names = country_code, to='EXIO3'))
print(df1)
table_pivot=df1.pivot_table(index='EXIO3',columns='EXIOBASE product')
table_pivot.to_csv('aggregation_per_product_code.csv',index=False)

writer = pd.ExcelWriter('aggregation_per_year.xlsx', engine='xlsxwriter')
for year in range(1961,2021):
    table_pivot.loc[:,'Y'+str(year)].to_excel(writer, sheet_name=str(year))
writer.save()

'''
To access values for a certain location and certain year
'''
#table_pivot.loc['BE','Y1961']

'''
To access a table for a particular year
'''
#table_pivot.loc[:,'Y1961']

#return
     


