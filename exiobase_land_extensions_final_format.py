# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:11:29 2024

@author: richa
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:09:52 2024

@author: richa
"""

import pandas as pd
import os

INDECOLROOT = 'd:/indecol/'

path_extensions_source = INDECOLROOT + 'data/fao/final_tables/'
path_extensions_output = INDECOLROOT + 'Projects/MRIOs/EXIOBASE3/EXIOBASE_3_9_4/txt/Extensions/land/'
path_market_share =      INDECOLROOT + 'Projects/MRIOs/EXIOBASE3/EXIOBASE_3_9_4/SUT/MRSUT/'
path_mr_meta =           INDECOLROOT + 'Projects/EXIOBASE_dev/exioRoot/meta_info_and_func/mr/'    

classification_pro = pd.read_excel(path_mr_meta + 'meta.xlsx', sheet_name='pro')
ordered_columns_pro = pd.MultiIndex.from_arrays([
    classification_pro['Country'],
    classification_pro['CodeNr']
])

classification_ind = pd.read_excel(path_mr_meta + 'meta.xlsx', sheet_name='ind')
ordered_columns_ind = pd.MultiIndex.from_arrays([
    classification_ind['Country'],
    classification_ind['CodeNr']
])

classification_fd = pd.read_excel(path_mr_meta + 'meta.xlsx', sheet_name='FD')
ordered_columns_fd = pd.MultiIndex.from_arrays([
    classification_fd['Country'],
    classification_fd['CodeNr']
])




for yr in range(1995,2022):
    exten=pd.read_excel(path_extensions_source + 'aggregation_per_year.xlsx', sheet_name=str(yr),header=[0,1],index_col=[0,1])
    
    market_share=pd.read_csv(path_market_share + 'MarketShare_' + str(yr) + '.csv', header=0)
    market_share['CountryDest'] = market_share['CountryOrigin']
    market_share_pivot = market_share.pivot_table(index=['CountryOrigin', 'SectorOrigin'], columns=['CountryDest', 'SectorDest'], values='Value').fillna(0)
    
    market_share_pivot = market_share_pivot.reindex(columns=ordered_columns_ind,index=ordered_columns_pro).fillna(0)
    
    market_share_t= market_share_pivot.T
    
    
    df_pivot_ordered = exten.reindex(columns=ordered_columns_pro).fillna(0)
    df_pivot_ordered_fd = exten.reindex(columns=ordered_columns_fd).fillna(0)
    
    df_pivot_T = df_pivot_ordered @ market_share_pivot
    
    # Define the output directory
    output_dir = os.path.join(path_extensions_output , 'pxp/IOT_' + str(yr) + '_pxp')
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Define the output file path
    output_file = os.path.join(output_dir, 'F.tsv')
    
    # Save the pivot table to a CSV file
    df_pivot_ordered.to_csv(output_file, sep='\t')
    # final demand
    output_file = os.path.join(output_dir, 'F_Y.tsv')
    df_pivot_ordered_fd.to_csv(output_file, sep='\t')
    
    
    # Define the output directory
    output_dir = os.path.join(path_extensions_output , 'ixi/IOT_' + str(yr) + '_ixi')
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Define the output file path
    output_file = os.path.join(output_dir, 'F.tsv')
    
    # Save the pivot table to a CSV file
    df_pivot_T.to_csv(output_file, sep='\t')
    # final demand
    output_file = os.path.join(output_dir, 'F_Y.tsv')
    df_pivot_ordered_fd.to_csv(output_file, sep='\t')