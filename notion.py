import json , requests
file = open('SECRET.json')
data = json.load(file)

#secret token
secret = data['id']

#database id
database = data['database']

file.close()

#url
url = 'https://api.notion.com/v1/pages'

# Headers
headers = {
    'Authorization': f'Bearer {secret}',
    'Content-Type': 'application/json',
    'Notion-Version': '2021-05-13'
}

# Data input
data_input = {
    "parent": { "database_id": f"{database}" },
    "properties": {
      "Name": {
        "title": [
          {
            "text": {
              "content": "hi"
            },
            "multi_select": {
              "content": "Yurts in Big Sur, California"
            }
            
          }
        ]
      }
    }
  }

  
# check request 
response = requests.post(url, headers=headers, json=data_input)
print(response.json())


