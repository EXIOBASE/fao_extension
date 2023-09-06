import pandas as pd
import yaml

itemgroup=pd.read_csv('itemGroup_crop_livestock.csv')
list_itemgroup= list(itemgroup['Item Group Code'])
list_item= list(itemgroup['Item Code'])

print(list_item)
itemgroup_list =[]
item_list=[]



for i in list_itemgroup:
    if not i.isalpha() :
        #print(i)
        if i not in itemgroup_list :
            #print(type(i))
            itemgroup_list.append(i)
#print(itemgroup_list)
            
            
for i in list_item:
    if i not in item_list :
       item_list.append(i) 
            
group = dict()
df1 = pd.DataFrame(columns = ['Item Group','Item Code'])

for item in itemgroup_list:
    #print(item)
    for item_2 in item_list :
        #print(item, item_2)
        if item_2 in (itemgroup.loc[(itemgroup['Item Group Code']==item),['Item Code']].values) :
            df1 = df1.append(pd.Series([item,item_2], index=['Item Group','Item Code']),ignore_index=True)
        group[item]=df1.copy()

'''            
for a in itemgroup_list:
    test_unit=[]
    print(a)
    test_group=itemgroup.loc[(itemgroup['Item Group Code']==a),['Item Code']].values
print(test_group)
'''
'''
def generate_yaml_doc(yaml_file):
    py_object = {'Item Group': 
                ['a', 'b']}
    file = open(yaml_file, 'w', encoding='utf-8')
    yaml.dump(py_object, file)
    file.close()
current_path = os.path.abspath(".")
yaml_path = os.path.join(current_path, "generate.yaml")
generate_yaml_doc(yaml_path)



dict_file = [{'sports' : ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
{'countries' : ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]

with open(r'store_file.yaml', 'w') as file:
    documents = yaml.dump(dict_file, file)
'''