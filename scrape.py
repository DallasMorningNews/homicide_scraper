import pandas as pd
import requests
import json

# url = 'https://www.dallasopendata.com/resource/qv6i-rri7.json?$limit=1200000'
limit = 1200000
url = 'https://www.dallasopendata.com/resource/qv6i-rri7.json?$limit='+str(limit)


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
df = (df
      .loc[((df['nibrs_code'] == '09A') | 
            (df['ucrcode'].isin([110, 120])))]
        .sort_values('date1', ascending=False)
        .drop_duplicates(subset = ['incidentnum'], keep='first')
        .reset_index(drop=True)
        .copy())

df.to_csv('data/created/scraped_dpd_murders_data.csv', index=False)