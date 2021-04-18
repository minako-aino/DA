import pandas as pd
import numpy as np
import time as t
import math

def dataframe():
    types_dict = {'Date':str, 'Time':str, 'Global_active_power':float, 'Global_reactive_power':float, 'Voltage':float, 'Global_intensity':float,'Sub_metering_1':float, 'Sub_metering_2':float, 'Sub_metering_3':float}
    df = pd.read_csv('household_power_consumption.txt', index_col = None, delimiter=';', na_values=['?'], dtype=types_dict)
    #dtype=types_dict,
    new_df = df.drop(df.loc[(df['Sub_metering_1'] == 0) & (df['Sub_metering_2'] == 0) & (df['Sub_metering_3'] == 0)].index)
    df = new_df.dropna()
    return df

def numpy_array(df):
    arr = df.to_numpy()
    return arr

def task1_dataframe(df):
    dates_list = []
    for (date, data) in zip(df['Date'], df['Global_active_power']):
        if data > 5:
            if date not in dates_list:
                dates_list.append(date)
    return dates_list

def task1_numpy(arr):
    dates_list = []
    all_cases = arr[np.where(arr[:, 2] > 5)]
    for case in all_cases:
        if case[0] not in dates_list:
            dates_list.append(case[0])
    return dates_list
        
def task2_dataframe(df):
    dates_list = []
    for (date, data) in zip(df['Date'], df['Voltage']):
        if data > 235:
            if date not in dates_list:
                dates_list.append(date)
    return dates_list  

def task2_numpy(arr):
    dates_list = []
    all_cases = arr[np.where(arr[:, 4] > 235)]
    for case in all_cases:
       if case[0] not in dates_list:
            dates_list.append(case[0])
    return dates_list

def task3_dataframe(df):
    dates_list = []
    for (date, data, fridge, air_cond) in zip(df['Date'], df['Global_intensity'], df['Sub_metering_3'], df['Sub_metering_2']):
        if data > 18 and data < 21:
            if fridge > air_cond:
                if date not in dates_list:
                    dates_list.append(date)
    return dates_list

def task3_numpy(arr):
    dates_list = []
    all_cases = arr[np.where((arr[:, 5] > 18) & (arr[:, 5] < 21) & (arr[:, 8] > arr[:, 7]))]
    for case in all_cases:
        if case[0] not in dates_list:
            dates_list.append(case[0])
    return dates_list        

def task4_and_5_dataframe(df):
    # task 4
    temp_df = df.sample(replace=True, n=500000)
    mean_1 = temp_df['Sub_metering_1'].mean()
    mean_2 = temp_df['Sub_metering_2'].mean()
    mean_3 = temp_df['Sub_metering_3'].mean()
    #print('Mean 1: ', mean_1)
    #print('Mean 2: ', mean_2)
    #print('Mean 3: ', mean_3)
    
    # task 5
    cust_time = temp_df[temp_df['Time'].str.match(r'(^1[8-9]|2[0-3].*)') == True]
    dates_list = []
    for (time, date, sm1, sm2, sm3) in zip(cust_time['Time'], cust_time['Date'], cust_time['Sub_metering_1'], cust_time['Sub_metering_2'], cust_time['Sub_metering_3']):
        if (60*(sm1 + sm2 + sm3))/1000 > 6:
            if sm2 > sm1 and sm2 > sm3:
                if date not in dates_list:
                    dates_list.append(date)
    
    mid = len(dates_list)//2
    first_half = dates_list[:mid]
    second_half = dates_list[mid:]
    
    f_h = first_half[::3]
    s_h = second_half[::4]
    #print('First half: ', first_half[::3])
    #print('Second half: ', second_half[::4])
    
def task4_and_5_numpy(arr):
    # task 4
    number_of_rows = arr.shape[0]
    random_indices = np.random.choice(number_of_rows, size=500000, replace=False)
    random_rows = arr[random_indices, :]
    mean1 = np.mean(random_rows[:, 6], axis=0)
    mean2 = np.mean(random_rows[:, 7], axis=0)
    mean3 = np.mean(random_rows[:, 8], axis=0)
    #print('Mean 1: ', np.mean(random_rows[:, 6], axis=0))
    #print('Mean 2: ', np.mean(random_rows[:, 7], axis=0))
    #print('Mean 3: ', np.mean(random_rows[:, 8], axis=0))
    
    # task 5
    all_time_cases = random_rows[pd.Series(random_rows[:, 1]).str.match(r'(^1[8-9]|2[0-3].*)') == True]
    ap = all_time_cases[:, 2].flatten()
    rp = all_time_cases[:, 3].flatten()
    formula = []
    all_power_cases = []
    dates_list = []
    for (a, r) in zip(ap,rp):
        value = math.sqrt(pow(a, 2) + pow(r, 2)) 
        formula.append(value)
    all_power_cases = all_time_cases[np.where(np.asarray(formula) > 6)]
    cases = all_power_cases[:, 0].flatten()
    for date in cases:    
        if date not in dates_list:
            dates_list.append(date)
    
    mid = len(dates_list)//2
    first_half = dates_list[:mid]
    second_half = dates_list[mid:]
    
    f_h = first_half[::3]
    s_h = second_half[::4]
    #print('First half: ', first_half[::3])
    #print('Second half: ', second_half[::4])
    return dates_list

def Timer(func):
    tic = t.perf_counter()
    res = func
    toc = t.perf_counter()
    time = toc - tic
    return round(time, 15)

print('Preparing data')    
df = dataframe()
arr = numpy_array(df)

print('Results:\tdataframe\t\t   numpy array')
print('task1:   ', Timer(task1_dataframe(df)), 's - ', Timer(task1_numpy(arr)), 's')
print('task2:   ', Timer(task2_dataframe(df)), 's - ', Timer(task2_numpy(arr)), 's')
print('task3:   ', Timer(task3_dataframe(df)), 's - ', Timer(task3_numpy(arr)), 's')
print('task4,5: ', Timer(task4_and_5_dataframe(df)), 's - ', Timer(task4_and_5_numpy(arr)), 's')
