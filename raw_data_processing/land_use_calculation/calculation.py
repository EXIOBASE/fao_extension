''' 
By using simple maths, we fill empty cells.
-> value major item = sum(values minor items)
'''

def calculation2(landuse,code,key,years,diagram):
    if not landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]].isnull().values.all():
        value_major = landuse.loc[(landuse['Item Code']==key)&(landuse['ISO3']==code),[years]]
        value_major=float(value_major.to_string(index=False, header=False))
        list_minor = ['minor1','minor2','minor3']
        for i in  list_minor:
            for j in list_minor:
                if j is not i:
                    for k in list_minor :
                        if ((k is not i and k is not j and (i == list_minor[0] or i == list_minor[2]) and (list_minor.index(k)>list_minor.index(j))) or ((k is not i and k is not j and (i == list_minor[1]) and (list_minor.index(k)<list_minor.index(j))))) :
                            if not diagram.get(key).get(i) in (landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) :
                                if not diagram.get(key).get(j) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values  :
                                    if diagram.get(key).get(k) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values  :
                                        if landuse.loc[((landuse['Item Code']==diagram.get(key).get(k))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                            landuse.loc[((landuse['Item Code']==diagram.get(key).get(k))&(landuse['ISO3']==code)),[years]] = value_major 


    return landuse



def calculation(landuse,code,key,years,diagram):
    if not landuse.loc[((landuse['Item Code']==key)&(landuse['ISO3']==code)),[years]].isnull().values.all():
        value_major = landuse.loc[(landuse['Item Code']==key)&(landuse['ISO3']==code),[years]]
        value_major=float(value_major.to_string(index=False, header=False))
        list_minor = ['minor1','minor2','minor3']
        for i in list_minor:
            for j in list_minor:
                if j is not i:
                    for k in list_minor :
                        if ((k is not i and k is not j and (i == list_minor[0] or i == list_minor[2]) and (list_minor.index(k)>list_minor.index(j))) or ((k is not i and k is not j and (i == list_minor[1]) and (list_minor.index(k)<list_minor.index(j))))) :
                            if ((diagram.get(key).get(i) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and  (diagram.get(key).get(j) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) ):
                                if not diagram.get(key).get(k) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values  :
                                    if landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                        if not landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                            value_known = landuse.loc[(landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code),[years]]
                                            value_known = float(value_known.to_string(index=False, header=False))
                                            landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]] = value_major - value_known
                                    if landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                        if not landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                            value_known = landuse.loc[(landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code),[years]]
                                            value_known = float(value_known.to_string(index=False, header=False))
                                            landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]] = value_major - value_known


        list_minor = ['minor1','minor2','minor3']
        for i in list_minor:
            for j in list_minor:
                if j is not i:
                    for k in list_minor :
                        if ((k is not i and k is not j and (i == list_minor[0] or i == list_minor[2]) and (list_minor.index(k)>list_minor.index(j))) or ((k is not i and k is not j and (i == list_minor[1]) and (list_minor.index(k)<list_minor.index(j))))) :

                            if ((diagram.get(key).get(i) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and  (diagram.get(key).get(j) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values) and  (diagram.get(key).get(k) in landuse.loc[landuse['ISO3']==code, ["Item Code"]].values)):
                                if landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                    if not landuse.loc[((landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                        value_j = landuse.loc[(landuse['Item Code']==diagram.get(key).get(j))&(landuse['ISO3']==code),[years]]
                                        value_j = float(value_j.to_string(index=False, header=False))
                                        if not landuse.loc[((landuse['Item Code']==diagram.get(key).get(k))&(landuse['ISO3']==code)),[years]].isnull().values.all():
                                            value_k = landuse.loc[(landuse['Item Code']==diagram.get(key).get(k))&(landuse['ISO3']==code),[years]]
                                            value_k = float(value_k.to_string(index=False, header=False))
                                            if (value_major - value_j - value_k)>0 :
                                                landuse.loc[((landuse['Item Code']==diagram.get(key).get(i))&(landuse['ISO3']==code)),[years]] = value_major - value_j - value_k                                   
                                            else :
                                                continue
    return landuse
    
