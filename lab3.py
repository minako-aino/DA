import pandas as pd
import numpy as np
import datetime

def dataframe():
    types_dict = {'Date':str, 'Time':str, 'Global_active_power':float, 'Global_reactive_power':float, 'Voltage':float, 'Global_intensity':float,'Sub_metering_1':float, 'Sub_metering_2':float, 'Sub_metering_3':float}
    df = pd.read_csv('household_power_consumption.txt', index_col = None, delimiter=';', na_values=['?'], dtype=types_dict)
    #dtype=types_dict,
    new_df = df.drop(df.loc[(df['Sub_metering_1'] == 0) & (df['Sub_metering_2'] == 0) & (df['Sub_metering_3'] == 0)].index)
    df = new_df.dropna()
    return df

def task1_dataframe(df):
    dates_list = []
    for (date, data) in zip(df['Date'], df['Global_active_power']):
        if data > 5:
            if date not in dates_list:
                dates_list.append(date)
    return dates_list
        
def task2_dataframe(df):
    dates_list = []
    for (date, data) in zip(df['Date'], df['Voltage']):
        if data > 235:
            if date not in dates_list:
                dates_list.append(date)
    return dates_list   

def task3_dataframe(df):
    dates_list = []
    for (date, data, fridge, air_cond) in zip(df['Date'], df['Global_intensity'], df['Sub_metering_3'], df['Sub_metering_2']):
        if data > 18 and data < 21:
            if fridge > air_cond:
                if date not in dates_list:
                    dates_list.append(date)
    return dates_list

def task4_and_5_dataframe(df):
    # task 4
    temp_df = df.sample(replace=True, n=500000)
    mean_1 = temp_df['Sub_metering_1'].mean()
    print('Mean 1: ', mean_1)
    mean_2 = temp_df['Sub_metering_2'].mean()
    print('Mean 2: ', mean_2)
    mean_3 = temp_df['Sub_metering_3'].mean()
    print('Mean 3: ', mean_3)
    
    # task 5
    cust_time = temp_df[temp_df['Time'].str.match(r'(^1[8-9]|2[0-3].*)') == True]
    dates_list = []
    print(cust_time)
    for (time, date, sm1, sm2, sm3) in zip(cust_time['Time'], cust_time['Date'], cust_time['Sub_metering_1'], cust_time['Sub_metering_2'], cust_time['Sub_metering_3']):
        if (60*(sm1 + sm2 + sm3))/1000 > 6:
            if sm2 > sm1 and sm2 > sm3:
                if date not in dates_list:
                    dates_list.append(date)
    
    mid = len(dates_list)//2
    first_half = dates_list[:mid]
    second_half = dates_list[mid:]
    
    print(first_half[::3])
    print(second_half[::4])
        
df = dataframe()
task4_and_5_dataframe(df)

