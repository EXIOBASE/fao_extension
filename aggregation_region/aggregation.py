import pandas as pd
import country_converter as coco
import shutil

def table_aggregation(final_tables):
    
     cc = coco.CountryConverter()
     cc.valid_class
     cc.get_correspondence_dict('ISO3', 'EXIO3')

     converter=coco.country_converter
     xls = pd.ExcelFile(str(final_tables)  + '/' + 'EXIOBASE_allocation_FAO.xlsx')
     df1 = pd.read_excel(xls, 'final cropland')
     # df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]     
     print(df1.set_index(['ISO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','Unit']))
     country_code = list(df1['ISO3'])
     print(country_code)
     df1.insert(1, 'EXIO3', converter.convert(names = country_code, to='EXIO3'))
     print(df1)
     for row in df1.iterrows():
        if (df1.loc[row[0]]['EXIOBASE product code'] == 'p02'):
            df1.loc[row[0],'EXIOBASE extension name']= 'Final consumption expenditure by households'
        if (df1.loc[row[0]]['EXIOBASE product code'] == 'y01'):
            df1.loc[row[0],'EXIOBASE extension name']= 'Products of forestry, logging and related services (02)'
        if (df1.loc[row[0]]['EXIOBASE product'] == 'Artificial Surfaces'):
            df1.loc[row[0],'EXIOBASE extension name']= 'Artificial Surfaces'
     group=df1.groupby(['EXIO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name'],dropna=False).sum()
     print(group)
     # group= group.drop(columns=['ISO3','EXIOBASE extension name'])
     table_pivot=group.pivot_table(index='EXIOBASE extension name',columns=['EXIO3','EXIOBASE product code'], fill_value=0)
     print(table_pivot)
     #table_pivot=df1.pivot_table(index='EXIO3',columns='EXIOBASE product')
     #table_pivot.to_csv('aggregation_per_product_code.csv',index=False)

     writer = pd.ExcelWriter('aggregation_per_year.xlsx', engine='xlsxwriter')
     for year in range(1961,2022):
          table_pivot.loc[:,'Y'+str(year)].to_excel(writer, sheet_name=str(year))
     writer.close()
     shutil.copy("aggregation_per_year.xlsx", final_tables /"aggregation_per_year.xlsx")

     #writer.save()

     '''
     To access values for a certain location and certain year
     '''
     #table_pivot.loc['BE','Y1961']

     '''
     To access a table for a particular year
     '''
     #table_pivot.loc[:,'Y1961']

     #return
     


