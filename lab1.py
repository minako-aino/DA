import pandas as pd
import urllib
from datetime import datetime
import glob

path = r'C:\Vaznoe\proga\AD'


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
    while i < 28:
        get_data(i)
        i = i + 1 
   
        
#stack tables into one dataframe
def dataframe(path):
    headers = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi', 'empty']
    headers_active = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi']
    all_files = glob.glob(path + "/vhi_id*.csv")
    li = []
    i = 1
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=1, names=headers, usecols = headers_active)
        # data-cleaning block
        #drop rows which have -1 in vhi column
        df = df.drop(df.loc[df['vhi'] == -1].index)
        #drop rows with na
        df = df.dropna()
        #adding index in order to find needed area in dataset
        df['area'] = i
        #adding data from file to list
        li.append(df)
        i = i + 1
    
    frame = pd.concat(li, axis=0, ignore_index=True) 
    return frame

def change_index(frame):
    old = 1
    areas_list = ["22", "24", "23", "25", "3", "4", "8", "19", "20", "21", "9", "26", "10", "11", "12", "13", "14", "15", "16", "27", "17", "18", "6", "1", "2", "7", "5", "eof"]
    for new in areas_list:
        frame["area"].replace({old:new}, inplace=True)
        old=old+1
    frame.to_csv('vhi_full.csv')
    print("Indexes were changed")
    #test
    #print(frame[:4000])

def area_vhi(frame, area, year):
    vhi_list = []
    
    frame_area = frame[(frame["area"] == area) & (frame["year"] == year)]
    for record in frame_area["vhi"]:
        vhi_list.append(record)
    
    print("Do you want to see the whole table for that year?(y)")
    answ = input()
    if answ == "y" or answ == "Y":
        print(frame_area)
    
    print("Vhi list:", vhi_list)
    
    print("Max value is: {}".format(frame_area["vhi"].max()))
    print("Min value is: {}".format(frame_area["vhi"].min()))
      
def drought(area, perc, _type):
    year = "2015"
    frame_vhi = frame[frame["area"] == area]
    
    
    i = 0
    years = []
    bad_years = []
    
    for record in frame_vhi["year"]:
        if record not in years:
            years.append(record)
    
    for year in years:
        bad_weeks = 0 
        frame_years = frame_vhi[frame["year"] == year]
        #print(frame_years)
        weeks = len(frame_years)
       # print(year, weeks)   
        for vhi_data in frame_years["vhi"]:
     #           print(vhi_data)
           # print(vhi_data)
            if vhi_data < _type:
                bad_weeks += 1
            i += 1
            if i > (weeks+1): break
        print(year, "-", bad_weeks, "-", weeks)    
        maths = (bad_weeks/weeks)*100
        print(maths)
        if maths > perc:
            bad_years.append(year)
    print(bad_years)
    
print("Do you want to get brand new data?(y)")
answ = input()
if answ == "y" or answ == "Y":
    get_data_all()

frame = dataframe(path)
    
print("Do you want to change indexes?(y)")
answ = input()
if answ == "y" or answ == "Y":    
    change_index(frame)
    
#print("Interested in analytics?(y)")
#answ = input()
#if answ == "y" or answ == "Y":
#    print("Please enter the area:")
#    area = input()
#    print("Please enter the year:")
#    year = input()
#    print("Please enter the needed percent:")
#    perc = input()
#    print("Which type are you interested in?(1 or 2)")
area = 22
year = "2000"
perc = 50    
type_ = 2
if type_ == 1:
        _type = 15
if type_ == 2:
        _type = 35
area_vhi(frame, area, year)
drought(area, perc, _type)
