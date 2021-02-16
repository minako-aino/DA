import pandas as pd
import urllib
from datetime import datetime
import glob

path = r'C:\Users\Professional'


#prepare dataset
def get_data(i):
    #getting current date
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M")
    filename = 'vhi_id_{}_{}.csv'.format(i, dt_string)

    #getting all the data from the website
    url='https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2021&type=Mean'.format(i)

    vhi_url = urllib.request.urlopen(url)
    
    out=open(filename , 'wb')
    out.write(vhi_url.read())
    out.close()
    
    print("File for {} is ready!".format(i))

#download all the data
def get_data_all():
    i = 1
    #indexes of the areas
    while i < 29:
        get_data(i)
        i = i + 1 
    
def dataframe(path):
    headers = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi', 'empty']
    headers_active = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi']
    all_files = glob.glob(path + "/*.csv")
    li = []
    i = 1
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=1, names=headers, usecols = headers_active)
        df["area"] = i
        li.append(df)
        i = i + 1
    
    frame = pd.concat(li, axis=0, ignore_index=True) 
    print(frame.columns)   
    print(frame[:50])
#    return frame

get_data_all()
dataframe(path)





#df = pd.read_csv('vhi_id_{}.csv'.format(dt_string),index_col=False, header=1)
#print (df[:10])