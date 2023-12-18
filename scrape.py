import pandas as pd
import requests
# import json
import os
import time
import datetime

start_time = time.time() # record the current time

ftime = datetime.datetime.now().strftime("%Y%m%d-%H-%M")


# url = 'https://www.dallasopendata.com/resource/qv6i-rri7.json?$limit=1200000'
limit = 1200000
url = f"https://www.dallasopendata.com/resource/qv6i-rri7.json?$where=nibrs_code%20=%20%2709A%27%20or%20ucrcode=110%20or%20ucrcode=120&$limit={str(limit)}"

print(url)
json_data = []

def grab_data(url):
    paginate = False

    r = requests.get(url)
    # json_data.append(r.json())
    data = r.json()
    for entry in data: json_data.append(entry)
    offset = limit
    new_url = url+'&$offset='+str(limit)
    
    if len(data) == limit: 
        print('this is lendata', len(data))
        print('this is limit', limit)
        print('set paginate ot true')
        paginate = True
    else:
        print('did not hit limit')
        print(len(data))
    
    if paginate == True: 
        grab_data(new_url)
        offset = offset+limit
        print('limit hit, new offset', offset)
        
    
grab_data(url)
print(len(json_data))
df = pd.DataFrame(json_data)

#df.to_csv('dallasopendata.csv', index=False)

#d2 = pd.read_csv('dallasopendata.csv')

#print(d2.shape[0])

#filter to just murders
if not os.path.exists('data/created'):
    os.makedirs('data/created')

df = (df.sort_values('date1', ascending=False)
        .drop_duplicates(subset = ['incidentnum'], keep='first')
        .reset_index(drop=True)
        .copy())

df.to_csv(f'data/created/dpd_murders_data_{ftime}.csv', index=False)

end_time = time.time() # record the current time again
elapsed_time = end_time - start_time # calculate the elapsed time

print(f"Elapsed time: {elapsed_time} seconds")
