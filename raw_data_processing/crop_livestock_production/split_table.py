def split(table_crop_livestock,code) :
    df=table_crop_livestock.loc[table_crop_livestock['Item Group Code']==code]
    return df


def split2(df_main,item_focused):
    df=df_main.loc[df_main['Item Code'].isin (item_focused['Item Code'])]

    return df

    






