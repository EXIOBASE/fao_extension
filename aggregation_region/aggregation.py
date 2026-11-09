from pathlib import Path

import pandas as pd
import country_converter as coco


def aggregate_final_cropland(df1):
     """The 'final cropland' sheet summed to EXIO3 regions: extension name rows,
     (EXIO3, EXIOBASE product code) columns under each Y<year>."""
     converter=coco.country_converter
     df1 = df1.copy()
     country_code = list(df1['ISO3'])
     df1.insert(1, 'EXIO3', converter.convert(names = country_code, to='EXIO3'))

     # group=df1.groupby(['EXIO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name','ISO3','Unit'],dropna=False).sum()
   # table_pivot=group.pivot_table(index=['EXIOBASE extension name','Unit'],columns=['EXIO3','EXIOBASE product code'], fill_value=0)

     group=df1.groupby(['EXIO3','EXIOBASE product code','EXIOBASE product','EXIOBASE extension name'],dropna=False).sum()
     group = group.drop(columns=['ISO3','Unit'])
     return group.pivot_table(index='EXIOBASE extension name',columns=['EXIO3','EXIOBASE product code'], fill_value=0)


def write_per_year(table_pivot, path, years=range(1961,2024)):
     """One sheet per year, the layout exiobase_land_extensions_final_format.py reads."""
     writer = pd.ExcelWriter(path, engine='xlsxwriter')
     for year in years:
          table_pivot.loc[:,'Y'+str(year)].to_excel(writer, sheet_name=str(year))
     writer.close()


#: Workbook names, the same as the tracked copies in the repository root.
#: processing_classification/landuse_calculation.py writes ALLOCATION_XLSX
#: into final_tables; this step reads it there and writes AGGREGATION_XLSX
#: next to it. Neither is written into the working directory, so a run of
#: run_all.py from a clone does not overwrite the tracked workbooks.
ALLOCATION_XLSX = 'EXIOBASE_allocation_FAO.xlsx'
AGGREGATION_XLSX = 'aggregation_per_year.xlsx'


def table_aggregation(final_tables):

     xls = pd.ExcelFile(Path(final_tables) / ALLOCATION_XLSX)
     df1 = pd.read_excel(xls, 'final cropland')
     table_pivot = aggregate_final_cropland(df1)

     write_per_year(table_pivot, Path(final_tables) / AGGREGATION_XLSX)

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
     


