###########################################################################
## (C) TOHOURI ROMAIN-ROLLAND
## 10/15/2018
README:
This Python program updates dhis2 translation usin a csv files
############################################################################
import csv
import requests
import json

payload = None
response = None
dhis2_auth = ('admin', 'district')
baseurl = 'https://your_base_url/api/29/'

url = None
headers = {'Accept': 'application/json', "Content-Type": "application/json"}

with open('translation.csv', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        url = baseurl + row['classname'] + '/' + row['objectid']
        payload = {'property': row['property'], 'locale': row['locale'], 'value':row['value']}
        print(payload)
        # 1- get the dataElement object first
        response = requests.get(url, auth=dhis2_auth)
        print("GET response: ================================ \n" + response.text)
        if response.status_code == 200:

            data = json.loads(response.text)
            # 2 - Appending the new translation to list of existing translations

            print("Existing Translation values : \n")
            print(json.dumps(data['translations'], sort_keys=True, indent=4))
            
            if data['translations'] == []:
                data['translations'] = [payload]
            elif data['translations'] == [payload]:
                print('Translation already existing, skipping this record....')
            else:
                data['translations'].append(payload)

            print("\n New Translation values : \n")
            print(json.dumps(data['translations'], sort_keys=True, indent=4))
            print("\n URL: " + url)
            response = requests.put(url, data=json.dumps(data), auth=dhis2_auth, headers=headers)

            if response.status_code == 200:
                print ("Entity correctly updated :" + response.text)
            else:
                print("Error: Unable to update PUT record : ====================== \n" + response.text)   
                print(response.json)
                print(response.status_code)
                exit()
        else:
            print("error: Unable to get data")   
            print(response.text)
            print(response.status_code)
            exit()
