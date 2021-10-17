import requests , json
import pandas as pd
file = open('db.json')
data = json.load(file)

# print(data['results'][0]['properties']['status']['rich_text'][0]['plain_text'])
# print(data['results'][0]['properties']['values']['rich_text'][0]['plain_text'])
# print(data['results'][0]['properties']['Name']['title'][0]['plain_text'])

# a = pd.DataFrame(data[])
# d = []
# def clean_data():
#     a = data['results'][0]['properties']['status']['rich_text'][0]['plain_text']
#     b = data['results'][0]['properties']['values']['rich_text'][0]['plain_text']
#     c = data['results'][0]['properties']['Name']['title'][0]['plain_text']
#     d.append(a,b,c)

def get_projects_titles(data):
    return list(data["results"][0]["properties"].keys())

title = get_projects_titles(data)

# print(get_projects_titles(data))

# def query(data,title):
#     pro_data = {}
#     for p in title:
#         if p != "Name":
#             pro_data[p] = [data["results"][0]["properties"][p]['rich_text'][0]['plain_text']]
#         elif p == "Name":
#              pro_data[p] = [data["results"][0]["properties"][p]['title'][0]['plain_text']]
#     return pro_data
# print(query(data,title))

# def alldata():
#     dd = {}
#     for i in title:
#         for i in 
#             dd[i] = data['results'][1]['properties']['status']['rich_text'][0]['plain_text']
# a = {}
lendat = len(data['results'])
# for i in range(0,lendat):
#     a['results'] = [data['results'][i]['properties']['status']['rich_text'][0]['plain_text']]
# print(lendat) 
# print(a)   
# print({key:[index for index in [data['results'][i]['properties']['status']['rich_text'][0]['plain_text']for i in range(0,lendat) ]] for key in title})

b = {}
# z = ['status','values','Name']
for x in reversed(title):
    if x != 'Name':
        b[x] = [[data['results'][i]['properties'][x]['rich_text'][0]['plain_text']] for i in range(0,lendat) ]
    elif x == 'Name':
        b[x] = [[data['results'][i]['properties'][x]['title'][0]['plain_text']] for i in range(0,lendat) ]
print(b)
df = pd.DataFrame.from_dict(b)
df= df[::-1]
print(df)
# columns_titles = ['Name','values','status']
# df_reorder=df.reindex(columns=columns_titles)
# print(df_reorder)

# c= ['Name','values','status']



# print(len(data['results']))
# datatitle = get_projects_titles(data)

# def get_projects_data(data_json,projects):
#     projects_data = {}
#     for p in projects:
#         if p!="Name" and p !="Date":
#             projects_data[p] = [data_json["results"][i]["properties"][p]["checkbox"] for i in range(len(data_json["results"]))]
#         elif p=="Date":
#             dates = [data_json["results"][i]["properties"]["Date"]["date"]["start"] for i in range(len(data_json["results"]))]
#     return projects_data,dates

# def getp(data,datatitle):
#     return 
# get_projects_data(data,datatitle)
