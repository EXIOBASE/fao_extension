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
     country_code = list(df1['ISO3'])
     df1.insert(1, 'EXIO3', converter.convert(names = country_code, to='EXIO3'))

     # group=df1.groupby(['EXIO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','ISO3','Unit'],dropna=False).sum()
   # table_pivot=group.pivot_table(index=['EXIOBASE extension name','Unit'],columns=['EXIO3','EXIOBASE product code'], fill_value=0)

     group=df1.groupby(['EXIO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name'],dropna=False).sum()
     group = group.drop(columns=['ISO3','Unit'])
     table_pivot=group.pivot_table(index='EXIOBASE extension name',columns=['EXIO3','EXIOBASE product code'], fill_value=0)


     writer = pd.ExcelWriter('aggregation_per_year.xlsx', engine='xlsxwriter')
     for year in range(1961,2023):
          table_pivot.loc[:,'Y'+str(year)].to_excel(writer, sheet_name=str(year))
     writer.close()
     shutil.copy("aggregation_per_year.xlsx", str(final_tables) + "/aggregation_per_year_new.xlsx")

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
     


