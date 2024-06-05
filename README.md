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
    
# Download the data #
The folder **Download** contains the script **main.py** which allows us to download the 3 tables needed.
- [Land Use](https://www.fao.org/faostat/en/#data/RL) contains data on forty-four categories of land use, irrigation and agricultural practices and five indicators relevant to monitor agriculture, forestry and fisheries activities at national, regional and global level. Data are available by country and year, with global coverage and annual updates.

- [Land Cover](https://www.fao.org/faostat/en/#data/LC) under the Agri-Environmental Indicators section contains land cover information organized by the land cover classes of the international standard system for Environmental and Economic Accounting Central Framework (SEEA CF).
- [Crop and livestock products](https://www.fao.org/faostat/en/#data/QCL) covering the following categories: crops primery, crops processed, live animals, livestock primary, livestock processed

> [!IMPORTANT]
>It is important to note that when it comes to land use, multiple-cropped areas are counted only once. Please visit [FAOSTAT webpage related on land use](https://www.fao.org/faostat/en/#data/RL). First click on **Definitions and standards - Land Use**, then on **item**.
Look for the description of item code 6630.


# Process raw data #

Following this process where we deal with missing data with assumption, linear interpolation and regression, 6 tables are created and stored in **final_tables** mentioned in previous section.
This tables consist of :

- *landuse_final_runnall.csv*. 

    This table contains all items from the land use table and item 6970, Artificial surfaces (including urban and associated areas) from the land cover table. All areas (in **km<sup>2</sup>** ) are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.
    
    <!--
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
    -->

- *final_crops_primary.csv*. 

    This table contains the crops primary items from the crop and livestock products table. These include : Cereals, Citrus Fruit, Fibre Crops, Fruit, Oil Crops, Oil Crops and Cakes in Oil Equivalent, Pulses, Roots and Tubers, Sugar Crops, Treenuts and Vegetables. Data are expressed in terms of area harvested (in **km<sup>2</sup>**),  production quantity (in **tonnes**) and yield. 
    
    Cereals: Area and production data on cereals relate to crops harvested for dry grain only. Cereal crops harvested for hay or harvested green for food, feed or silage or used for grazing are therefore excluded. All areas and production quantities are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.

<!--
    **Item Code**|**Item**|**Item Code**|**Item**
    :-----:|:-----:|:-----:|:-----:
    15|Wheat|403|Onions and shallots, dry (excluding dehydrated)
    27|Rice|406|Green garlic
    44|Barley|407|Leeks and other alliaceous vegetables
    56|Maize (corn)|414|Other beans, green
    71|Rye|417|Peas, green
    75|Oats|420|Broad beans and horse beans, green
    79|Millet|423|String beans
    83|Sorghum|426|Carrots and turnips
    89|Buckwheat|430|Okra
    92|Quinoa|446|Green corn (maize)
    94|Fonio|449|Mushrooms and truffles
    97|Triticale|459|Chicory roots
    101|Canary seed|461|Locust beans (carobs)
    103|Mixed grain|463|Other vegetables, fresh n.e.c.
    108|Cereals n.e.c.|486|Bananas
    116|Potatoes|489|Plantains and cooking bananas
    122|Sweet potatoes|490|Oranges
    125|Cassava, fresh|495|Tangerines, mandarins, clementines
    135|Yautia|497|Lemons and limes
    136|Taro|507|Pomelos and grapefruits
    137|Yams|512|Other citrus fruit, n.e.c.
    149|Edible roots and tubers with high starch or inulin content, n.e.c., fresh|515|Apples
    156|Sugar cane|521|Pears
    157|Sugar beet|523|Quinces
    161|Other sugar crops n.e.c.|526|Apricots
    176|Beans, dry|530|Sour cherries
    181|Broad beans and horse beans, dry|531|Cherries
    187|Peas, dry|534|Peaches and nectarines
    191|Chick peas, dry|536|Plums and sloes
    195|Cow peas, dry|541|Other stone fruits
    197|Pigeon peas, dry|542|Other pome fruits
    201|Lentils, dry|544|Strawberries
    203|Bambara beans, dry|547|Raspberries
    205|Vetches|549|Gooseberries
    210|Lupins|550|Currants
    211|Other pulses n.e.c.|552|Blueberries
    216|Brazil nuts, in shell|554|Cranberries
    217|Cashew nuts, in shell|558|Other berries and fruits of the genus vaccinium n.e.c.
    220|Chestnuts, in shell|560|Grapes
    221|Almonds, in shell|567|Watermelons
    222|Walnuts, in shell|568|Cantaloupes and other melons
    223|Pistachios, in shell|569|Figs
    224|Kola nuts|571|Mangoes, guavas and mangosteens
    225|Hazelnuts, in shell|572|Avocados
    226|Areca nuts|574|Pineapples
    234|Other nuts (excluding wild edible nuts and groundnuts), in shell, n.e.c.|577|Dates
    236|Soya beans|587|Persimmons
    242|Groundnuts, excluding shelled|591|Cashewapple
    249|Coconuts, in shell|592|Kiwi fruit
    254|Oil palm fruit|600|Papayas
    260|Olives|603|Other tropical fruits, n.e.c.
    263|Karite nuts (sheanuts)|619|Other fruits, n.e.c.
    265|Castor oil seeds|656|Coffee, green
    267|Sunflower seed|661|Cocoa beans
    270|Rape or colza seed|667|Tea leaves
    275|Tung nuts|671|Maté leaves
    277|Jojoba seeds|677|Hop cones
    280|Safflower seed|687|Pepper (Piper spp.), raw
    289|Sesame seed|689|Chillies and peppers, dry (Capsicum spp., Pimenta spp.), raw
    292|Mustard seed|692|Vanilla, raw
    296|Poppy seed|693|Cinnamon and cinnamon-tree flowers, raw
    299|Melonseed|698|Cloves (whole stems), raw
    305|Tallowtree seeds|702|Nutmeg, mace, cardamoms, raw
    310|Kapok fruit|711|Anise, badian, coriander, cumin, caraway, fennel and juniper berries, raw
    328|Seed cotton, unginned|720|Ginger, raw
    333|Linseed|723|Other stimulant, spice and aromatic crops, n.e.c.
    336|Hempseed|748|Peppermint, spearmint
    339|Other oil seeds, n.e.c.|754|Pyrethrum, dried flowers
    358|Cabbages|771|Flax, raw or retted
    366|Artichokes|777|True hemp, raw or retted
    367|Asparagus|780|Jute, raw or retted
    372|Lettuce and chicory|782|Kenaf, and other textile bast fibres, raw or retted
    373|Spinach|788|Ramie, raw or retted
    378|Cassava leaves|789|Sisal, raw
    388|Tomatoes|800|Agave fibres, raw, n.e.c.
    393|Cauliflowers and broccoli|809|Abaca, manila hemp, raw
    394|Pumpkins, squash and gourds|813|Coir, raw
    397|Cucumbers and gherkins|821|Other fibre crops, raw, n.e.c.
    399|Eggplants (aubergines)|826|Unmanufactured tobacco
    401|Chillies and peppers, green (Capsicum spp. and Pimenta spp.)|836|Natural rubber in primary forms
    402|Onions and shallots, green|839|Balata, gutta-percha, guayule, chicle and similar natural gums in primary forms or in plates, sheets or strip.

    -->


- *final_crops_processed.csv*. 

    This table contains the crops processed items from the crop and livestock products table. These include : Beer of barley; Cotton lint; Cottonseed; Margarine, short; Molasses; Oil, coconut (copra); Oil, cottonseed; Oil, groundnut; Oil, linseed; Oil, maize; Oil, olive, virgin; Oil, palm; Oil, palm kernel; Oil, rapeseed; Oil, safflower; Oil, sesame; Oil, soybean; Oil, sunflower; Palm kernels; Sugar Raw Centrifugal; Wine. Data are expressed in terms of production quantity (in **tonnes**). All production quantities are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.
    
<!--
    **Item Code**|**Item**
    :-----:|:-----:
    51|Beer of barley, malted
    60|Oil of maize
    162|Raw cane or beet sugar (centrifugal only)
    165|Molasses
    237|Soya bean oil
    244|Groundnut oil
    252|Coconut oil
    256|Palm kernels
    257|Palm oil
    258|Oil of palm kernel
    261|Olive oil
    268|Sunflower-seed oil, crude
    271|Rapeseed or canola oil, crude
    281|Safflower-seed oil, crude
    290|Oil of sesame seed
    311|Kapokseed in shell
    329|Cotton seed
    331|Cottonseed oil
    334|Oil of linseed
    564|Wine
    675|Green tea (not fermented), black tea (fermented) and partly fermented tea, in immediate packings of a content not exceeding 3 kg
    767|Cotton lint, ginned
    778|Kapok fibre, raw
    1242|Margarine and shortening-->



- *final_livestock_primary.csv*.

    This table contains the livestock primary items from the crop and livestock products table. These include : Beeswax; Eggs (various types); Hides buffalo, fresh; Hides, cattle, fresh; Honey, natural; Meat (ass, bird nes, buffalo, camel, cattle, chicken, duck, game, goat, goose and guinea fowl, horse, mule, Meat nes, meat other camelids, Meat other rodents, pig, rabbit, sheep, turkey); Milk (buffalo, camel, cow, goat, sheep); Offals, nes; Silk-worm cocoons, reelable; Skins (goat, sheep); Snails, not sea; Wool, greasy. All quantities are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.

<!--
    **Item Code**|**Item**|**Item Code**|**Item**
    :-----:|:-----:|:-----:|:-----:
    867|Meat of cattle with the bone, fresh or chilled|1062|Hen eggs in shell, fresh
    868|Edible offal of cattle, fresh, chilled or frozen|1069|Meat of ducks, fresh or chilled
    869|Cattle fat, unrendered|1073|Meat of geese, fresh or chilled
    882|Raw milk of cattle|1080|Meat of turkeys, fresh or chilled
    919|Raw hides and skins of cattle|1083|Other birds
    947|Meat of buffalo, fresh or chilled|1089|Meat of pigeons and other birds n.e.c., fresh, chilled or frozen
    948|Edible offal of buffalo, fresh, chilled or frozen|1091|Eggs from other birds in shell, fresh, n.e.c.
    949|Buffalo fat, unrendered|1097|Horse meat, fresh or chilled
    951|Raw milk of buffalo|1098|Edible offals of horses and other equines,  fresh, chilled or frozen
    957|Raw hides and skins of buffaloes|1108|Meat of asses, fresh or chilled
    977|Meat of sheep, fresh or chilled|1111|Meat of mules, fresh or chilled
    978|Edible offal of sheep, fresh, chilled or frozen|1127|Meat of camels, fresh or chilled
    979|Sheep fat, unrendered|1128|Edible offals of camels and other camelids, fresh, chilled or frozen
    982|Raw milk of sheep|1129|Fat of camels
    987|Shorn wool, greasy, including fleece-washed shorn wool|1130|Raw milk of camel
    995|Raw hides and skins of sheep or lambs|1141|Meat of rabbits and hares, fresh or chilled
    1017|Meat of goat, fresh or chilled|1151|Meat of other domestic rodents, fresh or chilled
    1018|Edible offal of goat, fresh, chilled or frozen|1158|Meat of other domestic camelids, fresh or chilled
    1019|Goat fat, unrendered|1163|Game meat, fresh, chilled or frozen
    1020|Raw milk of goats|1166|Other meat n.e.c. (excluding mammals), fresh, chilled or frozen
    1025|Raw hides and skins of goats or kids|1176|Snails, fresh, chilled, frozen, dried, salted or in brine, except sea snails
    1035|Meat of pig with the bone, fresh or chilled|1182|Natural honey
    1036|Edible offal of pigs, fresh, chilled or frozen|1183|Beeswax
    1037|Fat of pigs|1185|Silk-worm cocoons suitable for reeling
    1058|Meat of chickens, fresh or chilled| | -->




- *final_livestock_processed.csv*.

    This table contains the livestock processed items from the crop and livestock products table. These include : Butter (of milk from sheep, goat, buffalo, cow); Cheese (of milk from goat, buffalo, sheep, cow milk); Cheese of skimmed cow milk; Cream fresh; Ghee (cow and buffalo milk); Lard; Milk (dry buttermilk, skimmed condensed, skimmed cow, skimmed dried, skimmed evaporated, whole condensed, whole dried, whole evaporated); Silk raw; Tallow; Whey (condensed and dry); Yoghurt. All quantities are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.

- *final_live_animal.csv*.

    This table contains the number of live animal items from the crop and livestock products table. These include : Animals live n.e.s.; Asses; Beehives; Buffaloes; Camelids, other; Camels; Cattle; Chickens; Ducks; Geese and guinea fowls; Goats; Horses; Mules; Pigeons, other birds; Pigs; Rabbits and hares; Rodents, other; Sheep; Turkeys. All quantities are available, unless specified in this [file](aux_data/parameters.yaml), from 1961 to 2021.




# Process Classification #