from init import Storage
import pandas as pd
df = pd.read_csv('../data/laptops_all.csv')

def clean_laptop_name(name):
    name = name.lower()
    return name

items = []
for index, row in df.iterrows():
    items.append(str(row['code']) + '\n' + clean_laptop_name(row['full_name']))

s = Storage()

item_descriptions = []
for i in items:
    item_descriptions.append(i)

s.fit_data(item_descriptions)
print(s.tfidf_space)
