# README #

We are aiming to determine the area of several land use type defined by [EXIOBASE](https://www.exiobase.eu/) using only data available from [FAOSTAT](http://www.fao.org/faostat/en/#data).
This can be done as a 4 steps process as illustrated by the diagram below. Each step is refering to a folder containing all the modules needed to complete the step.

![flow.png](readme_pictures/flow.png)


The whole process is described in details [here](Method.md)

The main script **run_all.py** follows the 4 steps described in the diagram.

DATAFOLDER is the location where one can find all files we download from FAOSTAT but also all final tables we  generate through the whole process. 

```python
DATAFOLDER: Path = Path('/home/candyd/tmp/FAO')
```

Inside this folder one can found 3 repositories:

- **download** : which contains the 3 .zip files directly downloaded from FAO

- **data** : which contains all the tables contained in the 3 zip files mentionned above.

- **final_tables** : which contains 8 files.
    - *landuse_final_runnall.csv*. 

        This table contains all items from the land use table and item 6970, Artificial surfaces (including urban and associated areas) from the land cover table. 
        All areas (in **km<sup>2</sup>** ) are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.
        
        
        **Item Code**|**Item**
        :-----:|:-----:
        6600|Country area
        6601|Land area
        6602|Agriculture
        6610|Agricultural land
        6620|Cropland
        6621|Arable land
        6630|Temporary crops
        6633|Temporary meadows and pastures
        6640|Temporary fallow
        6650|Permanent crops
        6655|Permanent meadows and pastures
        6656|Perm. meadows & pastures - Cultivated
        6659|Perm. meadows & pastures - Nat. growing
        6649|Farm buildings and Farmyards
        6646|Forest land
        6717|Naturally regenerating forest
        6716|Planted Forest
        6670|Other land
        6680|Inland waters
        6773|Coastal waters
        6643|Exclusive Economic Zone (EEZ)
        6690|Land area equipped for irrigation
        6616|Land area actually irrigated
        6611|Agriculture area actually irrigated
        6694|Cropland area actually irrigated
        6657|Perm. meadows & pastures area actually irrig.
        6695|Forestry area actually irrigated
        6671|Agriculture area under organic agric.
        6672|Agriculture area certified organic
        6668|Cropland area under organic agric.
        6669|Cropland area certified organic
        6681|Perm. meadows & pastures area under organic agric.
        6682|Perm. meadows & pastures area certified organic
        6664|Cropland area under conventional tillage
        6665|Cropland area under conservation tillage
        6666|Cropland area under zero or no tillage
        6774|Cropland area under protective cover
        6762|Land used for aquaculture
        6767|Inland waters used for aquac. or holding facilities
        6771|Inland waters used for capture fisheries
        6641|Coastal waters used for aquac. or holding facilities
        6642|Coastal waters used for capture fisheries
        6644|EEZ used for aquac. or holding facilities
        6645|EEZ used for capture fisheries
        6714|Primary Forest
        6970|Artificial surfaces (including urban and associated areas)
    
    - *final_crops_primary.csv*. 
    
        This table contains the crops primary items from the crop and livestock products table. These include : Cereals, Citrus Fruit, Fibre Crops, Fruit, Oil Crops, Oil Crops and Cakes in Oil Equivalent, Pulses, Roots and Tubers, Sugar Crops, Treenuts and Vegetables. Data are expressed in terms of area harvested (in **km<sup>2</sup>**),  production quantity (in **tonnes**) and yield. 
        
        Cereals: Area and production data on cereals relate to crops harvested for dry grain only. Cereal crops harvested for hay or harvested green for food, feed or silage or used for grazing are therefore excluded.

        All areas and production quantities are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.

        **Item Code**|**Item**
        :-----:|:-----:
        15|Wheat
        27|Rice
        44|Barley
        56|Maize (corn)
        71|Rye
        75|Oats
        79|Millet
        83|Sorghum
        89|Buckwheat
        92|Quinoa
        94|Fonio
        97|Triticale
        101|Canary seed
        103|Mixed grain
        108|Cereals n.e.c.
        116|Potatoes
        122|Sweet potatoes
        125|Cassava, fresh
        135|Yautia
        136|Taro
        137|Yams
        149|Edible roots and tubers with high starch or inulin content, n.e.c., fresh
        156|Sugar cane
        157|Sugar beet
        161|Other sugar crops n.e.c.
        176|Beans, dry
        181|Broad beans and horse beans, dry
        187|Peas, dry
        191|Chick peas, dry
        195|Cow peas, dry
        197|Pigeon peas, dry
        201|Lentils, dry
        203|Bambara beans, dry
        205|Vetches
        210|Lupins
        211|Other pulses n.e.c.
        216|Brazil nuts, in shell
        217|Cashew nuts, in shell
        220|Chestnuts, in shell
        221|Almonds, in shell
        222|Walnuts, in shell
        223|Pistachios, in shell
        224|Kola nuts
        225|Hazelnuts, in shell
        226|Areca nuts
        234|Other nuts (excluding wild edible nuts and groundnuts), in shell, n.e.c.
        236|Soya beans
        242|Groundnuts, excluding shelled
        249|Coconuts, in shell
        254|Oil palm fruit
        260|Olives
        263|Karite nuts (sheanuts)
        265|Castor oil seeds
        267|Sunflower seed
        270|Rape or colza seed
        275|Tung nuts
        277|Jojoba seeds
        280|Safflower seed
        289|Sesame seed
        292|Mustard seed
        296|Poppy seed
        299|Melonseed
        305|Tallowtree seeds
        310|Kapok fruit
        328|Seed cotton, unginned
        333|Linseed
        336|Hempseed
        339|Other oil seeds, n.e.c.
        358|Cabbages
        366|Artichokes
        367|Asparagus
        372|Lettuce and chicory
        373|Spinach
        378|Cassava leaves
        388|Tomatoes
        393|Cauliflowers and broccoli
        394|Pumpkins, squash and gourds
        397|Cucumbers and gherkins
        399|Eggplants (aubergines)
        401|Chillies and peppers, green (Capsicum spp. and Pimenta spp.)
        402|Onions and shallots, green
        403|Onions and shallots, dry (excluding dehydrated)
        406|Green garlic
        407|Leeks and other alliaceous vegetables
        414|Other beans, green
        417|Peas, green
        420|Broad beans and horse beans, green
        423|String beans
        426|Carrots and turnips
        430|Okra
        446|Green corn (maize)
        449|Mushrooms and truffles
        459|Chicory roots
        461|Locust beans (carobs)
        463|Other vegetables, fresh n.e.c.
        486|Bananas
        489|Plantains and cooking bananas
        490|Oranges
        495|Tangerines, mandarins, clementines
        497|Lemons and limes
        507|Pomelos and grapefruits
        512|Other citrus fruit, n.e.c.
        515|Apples
        521|Pears
        523|Quinces
        526|Apricots
        530|Sour cherries
        531|Cherries
        534|Peaches and nectarines
        536|Plums and sloes
        541|Other stone fruits
        542|Other pome fruits
        544|Strawberries
        547|Raspberries
        549|Gooseberries
        550|Currants
        552|Blueberries
        554|Cranberries
        558|Other berries and fruits of the genus vaccinium n.e.c.
        560|Grapes
        567|Watermelons
        568|Cantaloupes and other melons
        569|Figs
        571|Mangoes, guavas and mangosteens
        572|Avocados
        574|Pineapples
        577|Dates
        587|Persimmons
        591|Cashewapple
        592|Kiwi fruit
        600|Papayas
        603|Other tropical fruits, n.e.c.
        619|Other fruits, n.e.c.
        656|Coffee, green
        661|Cocoa beans
        667|Tea leaves
        671|Maté leaves
        677|Hop cones
        687|Pepper (Piper spp.), raw
        689|Chillies and peppers, dry (Capsicum spp., Pimenta spp.), raw
        692|Vanilla, raw
        693|Cinnamon and cinnamon-tree flowers, raw
        698|Cloves (whole stems), raw
        702|Nutmeg, mace, cardamoms, raw
        711|Anise, badian, coriander, cumin, caraway, fennel and juniper berries, raw
        720|Ginger, raw
        723|Other stimulant, spice and aromatic crops, n.e.c.
        748|Peppermint, spearmint
        754|Pyrethrum, dried flowers
        771|Flax, raw or retted
        777|True hemp, raw or retted
        780|Jute, raw or retted
        782|Kenaf, and other textile bast fibres, raw or retted
        788|Ramie, raw or retted
        789|Sisal, raw
        800|Agave fibres, raw, n.e.c.
        809|Abaca, manila hemp, raw
        813|Coir, raw
        821|Other fibre crops, raw, n.e.c.
        826|Unmanufactured tobacco
        836|Natural rubber in primary forms
        839|Balata, gutta-percha, guayule, chicle and similar natural gums in primary forms or in plates, sheets or strip
# Download the data #
The folder **Download** contains the script **main.py** which allows us to download the 3 tables needed.
- [Land Use](https://www.fao.org/faostat/en/#data/RL) contains data on forty-four categories of land use, irrigation and agricultural practices and five indicators relevant to monitor agriculture, forestry and fisheries activities at national, regional and global level. Data are available by country and year, with global coverage and annual updates.

> [!IMPORTANT]
>It is important to note that when it comes to land use, multiple-cropped areas are counted only once. Please visit [FAOSTAT webpage related on land use](https://www.fao.org/faostat/en/#data/RL). First click on **Definitions and standards - Land Use**, then on **item**.
Look for the description of item code 6630.


- [Land Cover](https://www.fao.org/faostat/en/#data/LC) under the Agri-Environmental Indicators section contains land cover information organized by the land cover classes of the international standard system for Environmental and Economic Accounting Central Framework (SEEA CF).
- [Crop and livestock products](https://www.fao.org/faostat/en/#data/QCL) covering the following categories: crops primery, crops processed, live animals, livestock primary, livestock processed


# Process raw data #

Following this process where we deal with missing data with assumption, linear interpolation and regression, 6 tables are created and stored in 



3. We make sure the mathematical relation **major = minor1 + minor2 + minor3** is valid :         
```python
for code in country :
    if not code in parameters.get("exeptions"):
        relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("year_of_interest").get("begin"),parameters.get("year_of_interest").get("end")+1))]
    else:
        relevant_years = [make_valid_fao_year(year) for year in list(range(parameters.get("exeptions").get(code).get("begin"),parameters.get("exeptions").get(code).get("end")+1))]

    for key in diagram:
        for years in relevant_years :
            adj2.adjust(df,code,years, diagram,key,country)
```
If not, we adjust : 
```python
value_minor1= value_minor1*value_major/(value_minor1+value_minor2+value_minor3)
value_minor2= value_minor2*value_major/(value_minor1+value_minor2+value_minor3)value_minor3= value_minor3*value_major/(value_minor1+value_minor2+value_minor3)
                
df.loc[(df['ISO3']==code)&(df['Item Code']==diagram.get(key).get("minor1")),[years]]=value_minor1
df.loc[(df['ISO3']==code)&(df['Item Code']==diagram.get(key).get("minor2")),[years]]=value_minor2
df.loc[(df['ISO3']==code)&(df['Item Code']==diagram.get(key).get("minor3")),[years]]=value_minor3
```
4. We use the regression method in order to fill the empty cells at the beginning or at the end of the data sample.
```python
for code in country :
    reg.regression(code,parameters,df)
```
Folowwing this step, we check again if the mathematical relation **major = minor1 + minor2 + minor3** is still valid and adapt the values of the minor items in case this is not true.

5. After we dealt with the main diagram, we deal with the "lonely" items, the one that do not directly depend on another.
The list of these are contained in the yaml file called **unique_items.yaml**.
For these items, only the interpolation and the regression procedure are applied.

6. Finally, we deal with the small diagrams on the right hand side of the first picture. Here, we use the items listed in the files : **small_diagrams.yaml** and **items_small_diagrams.yaml**
Steps 1 to 4 are applied.


# Doing Calculation #

This concerne the module **landuse_calculation.py** in the [EXIOBASE](https://www.exiobase.eu/) folder. For the detailed split of the land use data to match the EXIOBASE sector resolution the following data sources were used:  [FAOSTAT](http://www.fao.org/faostat/en/#data). We split cropland into 21 sub-sectors based on information from FAOSTAT. Areas actually planted to crops in a given year were accounted for based on the amount of harvested area statistics from FAOSTAT’s crops domain. For this, we grouped individual crops into the EXIOBASE sector classification from [Stadler et al.](https://onlinelibrary.wiley.com/doi/full/10.1111/jiec.12715) (2018). 
Before to proceed to the different calculations, we need to convert each FAO item codes into Exiobase product code following the 
[Correspondance](Of_interest/Primary_production.csv). When the correspondance between FAO item to EXIOBASE product is done, we have to aggregate all the FAO item having the same corresponding EXIOBASE product code. The following table list the FAO items corresponding to the EXIOBASE category **Cereal grains nec** : **p01.c** :

| FAO item name | FAO item code | Subcategory       | Environmental extension | EXIOBASE product code | EXIOBASE product  |
|---------------|---------------|-------------------|-------------------------|-----------------------|-------------------|
| Barley        | 44            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Maize         | 56            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Popcorn       | 68            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Rye           | 71            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Oats          | 75            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Millet        | 79            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Sorghum       | 83            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Buckwheat     | 89            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Quinoa        | 92            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Fonio         | 94            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Triticale     | 97            | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Canary Seed   | 101           | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |
| Grain, mixed  | 103           | Cereal grains nec | Cereal grains nec       | p01.c                 | Cereal grains nec |


This aggregation leads us to the total crop production in **tonnes** per EXIOBASE product : 

| ISO3 | EXIOBASE product code | EXIOBASE product        | Unit   | Y1995   | Y1996   |
|------|-----------------------|-------------------------|--------|---------|---------|
| AFG  | n.a.                  | n.a.                    | tonnes | 68000   | 68000   |
| AFG  | p01.a                 | Paddy rice              | tonnes | 390000  | 340000  |
| AFG  | p01.b                 | Wheat                   | tonnes | 2100000 | 2300000 |
| AFG  | p01.c                 | Cereal grains nec       | tonnes | 752179  | 601915  |
| AFG  | p01.d                 | Vegetables, fruit, nuts | tonnes | 2260798 | 2286268 |
| AFG  | p01.e                 | Oil seeds               | tonnes | 49705   | 48189   |
| AFG  | p01.f                 | Sugar cane, sugar beet  | tonnes | 39000   | 39000   |
| AFG  | p01.h                 | Crops nec               | tonnes | 2005    | 4205    |

or to the total harvested crop area in **ha** per EXIOBASE product :

| ISO3 | EXIOBASE product code | EXIOBASE product        | Unit | Y1995      | Y1996       |
|------|-----------------------|-------------------------|------|------------|-------------|
| AFG  | n.a.                  | n.a.                    | ha   | 60000      | 60000       |
| AFG  | p01.a                 | Paddy rice              | ha   | 170000     | 175000      |
| AFG  | p01.b                 | Wheat                   | ha   | 1927468    | 2050000     |
| AFG  | p01.c                 | Cereal grains nec       | ha   | 571982     | 466670      |
| AFG  | p01.d                 | Vegetables, fruit, nuts | ha   | 270147     | 288291      |
| AFG  | p01.e                 | Oil seeds               | ha   | 75590      | 73253       |
| AFG  | p01.f                 | Sugar cane, sugar beet  | ha   | 2200       | 2200        |
| AFG  | p01.h                 | Crops nec               | ha   | 4749.99008 | 8750.017035 |

## Seed cotton ##
Areas on which seed cotton are grown were treated differently. 
We allocated the total area partly to the oil crops category and partly to fibres as stated in the supporting information S6 of [EXIOBASE 3: Developing a Time Series of Detailed Environmentally Extended Multi-Regional Input-Output Tables](https://onlinelibrary.wiley.com/doi/full/10.1111/jiec.12715) written by Stadler _et al._ (2018)

Seed cotton > oil crops       Allocation factor : 0.63
Seed cotton > fibre)          Allocation factor : 0.37       
```Python
seed_cotton_p01e=0.63
seed_cotton_p01g=0.37      
```
```Python
for code in res :
        for year in relevant_years:
            if 'n.a.' in (df_modified.loc[df_modified['ISO3']==code, ["EXIOBASE product code"]].values) :
                
                value_seed_cotton=df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='n.a.')),[year]]
                seed_cotton=value_seed_cotton.to_string(index=False, header=False)
                
                cotton_to_p01e=float(seed_cotton_p01e*float(seed_cotton))
                cotton_to_p01g=float(seed_cotton_p01g*float(seed_cotton))
       
                value_p01e=df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.e')),[year]]
                value_p01g=df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.g')),[year]]                
                p01e=float(value_p01e.to_string(index=False, header=False))
                p01g=float(value_p01g.to_string(index=False, header=False))
                
                new_p01e=p01e+cotton_to_p01e
                new_p01g=p01g+cotton_to_p01g
         
                
                '''Replace old value p01.e and p01.g with new vales in dataframe'''
                
                df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
                df_modified.loc[((df_modified['ISO3']==code) & (df_modified['EXIOBASE product code']=='p01.g')),[year]] = new_p01g  
```

## Fallowed areas ##
The fallowed area correspond to the difference between the cropland area and the harvested area :
```Python
fallowed=cropped-harvested
```

If harvested area was smaller than cropland area, the difference between the two was considered fallow area. We attributed **half of the fallow area proportionally to the different crop sectors and the other half to the primary livestock sectors**. The rationale for this choice is that FAOSTAT recently removed its information on dedicated fodder crops (e.g. maize for silage, fodder legumes) and we assume part of the “fallow” are planted to fodder crops. Also, is not uncommon for livestock to graze on fallow land in many countries. **The split between the different livestock sectors was performed based on information on the production of livestock products in a given country and a generic weighing key that reflects conversion efficiencies and roughage share in feed of for five different livestock products**. Based on literature (e.g., [Smil, 2002](https://www.sciencedirect.com/science/article/abs/pii/S014102290100504X?via%3Dihub)), the following weighing factors were applied for fallow area (here also a certain share of feed going to poultry and pigs, groups that usually do not feed on roughage, was assumed): 
- pig meat 2
- milk 1
- beef 20
- sheep and goat meat 10
- poultry 1

## Fallowed area attributed to primary livestock sectors ##
```Python
factor_beef_buffalo=20.0
factor_milk=1.0
factor_poultry=1.0
factor_pig=2.0
factor_sheep_goat=10.0 
```
Working with the Primary Livestock production means we have to deal with [Correspondance](Of_interest/List_Primary_livestock_FAO-CPA-EXIOBASE.csv) between FAO items and EXIOBASE categories. Then we have to aggregate data as a function of the EXIOBASE category. The foloowing table list the FAO items corresponding to the EXIOBASE product named **Cropland - Fodder crops-Pigs** : **p01.j**
| FAO item name        | FAO item code | EXIOBASE product code | EXIOBASE product             |
|----------------------|---------------|-----------------------|------------------------------|
| Fat, pigs            | 1037          | p01.j                 | Cropland - Fodder crops-Pigs |
| Meat, pig            | 1035          | p01.j                 | Cropland - Fodder crops-Pigs |
| Offals, pigs, edible | 1036          | p01.j                 | Cropland - Fodder crops-Pigs |

```Python
'''Values of Produced Livestock Products'''
            
p01i=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.i')),[year]]
p01i=float(p01i.to_string(index=False, header=False))
p01j=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.j')),[year]]
p01j=float(p01j.to_string(index=False, header=False))
p01k=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.k')),[year]]
p01k=float(p01k.to_string(index=False, header=False))
p01l=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.l')),[year]]
p01l=float(p01l.to_string(index=False, header=False))
p01n=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.n')),[year]]
p01n=float(p01n.to_string(index=False, header=False))
                   
sumfodder = p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk
                    
if not sumfodder == 0:
    fodder_p01i = fodder_crop * (p01i * factor_beef_buffalo) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
    fodder_p01j = fodder_crop * (p01j * factor_pig) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
    fodder_p01k = fodder_crop * (p01k * factor_poultry) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
    fodder_p01l = fodder_crop * (p01l * factor_sheep_goat) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
    fodder_p01n = fodder_crop * (p01n * factor_milk) / (p01i * factor_beef_buffalo + p01j * factor_pig + p01k * factor_poultry + p01l * factor_sheep_goat + p01n * factor_milk)
                        
    df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.i')),[year]] = fodder_p01i
    df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.j')),[year]] = fodder_p01j
    df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.k')),[year]] = fodder_p01k
    df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.l')),[year]] = fodder_p01l
    df_fodder_crop.loc[((df_fodder_crop['ISO3']==code) & (df_fodder_crop['EXIOBASE product code']=='p01.n')),[year]] = fodder_p01n
                         
```
## Fallowed area attributed to crop sectors ##
```Python
 '''Values of Harvested area'''
                    
p01a=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.a')),[year]]
p01a=float(p01a.to_string(index=False, header=False))
p01b=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.b')),[year]]
p01b=float(p01b.to_string(index=False, header=False))
p01c=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.c')),[year]]
p01c=float(p01c.to_string(index=False, header=False))
p01d=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.d')),[year]]
p01d=float(p01d.to_string(index=False, header=False))
p01e=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.e')),[year]]
p01e=float(p01e.to_string(index=False, header=False))
p01f=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.f')),[year]]
p01f=float(p01f.to_string(index=False, header=False))
p01g=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.g')),[year]]
p01g=float(p01g.to_string(index=False, header=False))
p01h=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.h')),[year]]
p01h=float(p01h.to_string(index=False, header=False))

sum_all=p01a+p01b+p01c+p01d+p01e+p01f+p01g+p01h  if not sum_all == 0:
                  
'''Values of Fallowed crops'''
        
    fallow_p01a=fallowed_crop*p01a/sum_all
    fallow_p01b=fallowed_crop*p01b/sum_all
    fallow_p01c=fallowed_crop*p01c/sum_all
    fallow_p01d=fallowed_crop*p01d/sum_all
    fallow_p01e=fallowed_crop*p01e/sum_all
    fallow_p01f=fallowed_crop*p01f/sum_all
    fallow_p01g=fallowed_crop*p01g/sum_all
    fallow_p01h=fallowed_crop*p01h/sum_all
                           
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.a')),[year]] = fallow_p01a
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.b')),[year]] = fallow_p01b
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.c')),[year]] = fallow_p01c
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.d')),[year]] = fallow_p01d
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.e')),[year]] = fallow_p01e
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.f')),[year]] = fallow_p01f
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.g')),[year]] = fallow_p01g
    df_fallow_crop.loc[((df_fallow_crop['ISO3']==code) & (df_fallow_crop['EXIOBASE product code']=='p01.h')),[year]] = fallow_p01h
```

**If harvested area was larger than cropland area (in case of multi-cropping) it was reduced proportionally for the different sectors to match available cropland area.**  
```Python
'''Values of Harvested area'''

p01a=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.a')),[year]]
p01a=float(p01a.to_string(index=False, header=False))
p01b=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.b')),[year]]
p01b=float(p01b.to_string(index=False, header=False))
p01c=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.c')),[year]]
p01c=float(p01c.to_string(index=False, header=False))
p01d=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.d')),[year]]
p01d=float(p01d.to_string(index=False, header=False))
p01e=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.e')),[year]]
p01e=float(p01e.to_string(index=False, header=False))
p01f=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.f')),[year]]
p01f=float(p01f.to_string(index=False, header=False))
p01g=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.g')),[year]]
p01g=float(p01g.to_string(index=False, header=False))
p01h=df_modified2.loc[((df_modified2['ISO3']==code) & (df_modified2['EXIOBASE product code']=='p01.h')),[year]]
p01h=float(p01h.to_string(index=False, header=False))
sum_all=p01a+p01b+p01c+p01d+p01e+p01f+p01g+p01h  if not sum_all == 0:
                  
'''New values of Harvested area'''
                      
    new_p01a=cropped*p01a/sum_all
    new_p01b=cropped*p01b/sum_all
    new_p01c=cropped*p01c/sum_all
    new_p01d=cropped*p01d/sum_all
    new_p01e=cropped*p01e/sum_all
    new_p01f=cropped*p01f/sum_all
    new_p01g=cropped*p01g/sum_all
    new_p01h=cropped*p01h/sum_all
                           
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.a')),[year]] = new_p01a
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.b')),[year]] = new_p01b
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.c')),[year]] = new_p01c
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.d')),[year]] = new_p01d
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.e')),[year]] = new_p01e
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.f')),[year]] = new_p01f
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.g')),[year]] = new_p01g
    df_harvested_corrected.loc[((df_harvested_corrected['ISO3']==code) & (df_harvested_corrected['EXIOBASE product code']=='p01.h')),[year]] = new_p01h
```

## Grazing sectors ##
For the grazing sectors, only ruminant products were considered, resulting in the following weighing scheme:
- milk 1
- beef 20
- sheep and goat meat 10


The allocation of grazing lands (distinction between pasture and rangeland is not done here) corresponds to the FAOSTAT category permanent pastures and meadows. This allocation of grazing land correspond to :
- Grazing land - forests 
- Grazing land - pastures
- Grazing land - rangeland

However, an other distinction is done here.
FAOSTAT splits Permanent meadows and pastures (item 6655) unto :
- Naturally growing (item 6659)
- Cultivated (item 6656)

with :item 6655 = item 6659 + item 6656

This is also implemented in the final table. 

```Python
'''Values of Produced Livestock Products'''
            
p01i=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.i')),[year]]
p01i=float(p01i.to_string(index=False, header=False))
p01l=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.l')),[year]]
p01l=float(p01l.to_string(index=False, header=False))
p01n=df_livestock.loc[((df_livestock['ISO3']==code) & (df_livestock['EXIOBASE product code']=='p01.n')),[year]]
p01n=float(p01n.to_string(index=False, header=False))
                    
                    
sumgrazzing = p01i * factor_beef_buffalo + p01l * factor_sheep_goat + p01n * factor_milk

if not sumgrazzing == 0:
    grazzing_p01i = grazzing * (p01i * factor_beef_buffalo) / (sumgrazzing)
    grazzing_p01l = grazzing * (p01l * factor_sheep_goat) / (sumgrazzing)
    grazzing_p01n = grazzing * (p01n * factor_milk) / (sumgrazzing)
    
    natgrowing_p01i = natgrowing * (p01i * factor_beef_buffalo) / (sumgrazzing)
    natgrowing_p01l = natgrowing * (p01l * factor_sheep_goat) / (sumgrazzing)
    natgrowing_p01n = natgrowing * (p01n * factor_milk) / (sumgrazzing)
    
    cultivated_p01i = cultivated * (p01i * factor_beef_buffalo) / (sumgrazzing)
                        cultivated_p01l = cultivated * (p01l * factor_sheep_goat) / (sumgrazzing)
                        cultivated_p01n = cultivated * (p01n * factor_milk) / (sumgrazzing)
    
    df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.i')),[year]] = grazzing_p01i
    df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.l')),[year]] = grazzing_p01l
    df_grazzing.loc[((df_grazzing['ISO3']==code) & (df_grazzing['EXIOBASE product code']=='p01.n')),[year]] = grazzing_p01n
```

## Forest area ##
The forest area correspond to faostat item Forest land (6646) 

## Final Demand ##
The final demand correspond to faostat item Other land (6670)

