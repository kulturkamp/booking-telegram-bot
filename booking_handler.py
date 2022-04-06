import json
import datetime as dt
import pandas as pd


START_TIME = '09:00:00'
END_TIME = '18:00:00'
INTERVAL = '30min'

# removing end time itself
timestamps = pd.date_range(START_TIME,END_TIME, freq=INTERVAL).strftime('%H:%M').to_list()[:-1]


timestamps_dict = dict.fromkeys(timestamps, 0)

def write_booking_data(date, stamp, quant):
    data = read_booking_data() 
    print('read data on writing')    
    print(json.dumps(data, indent=4))  
    try:
        data[date][stamp] += 1 #optionally += quant
    except:
        data[date] = timestamps_dict
        data[date][stamp] += 1

    print('new data')
    print(json.dumps(data, indent=4)) 
    with open('booking.json', 'w') as f:
         json.dump(data, f, ensure_ascii=False)
    

def read_booking_data():
    with open('booking.json', 'r') as f:
         data = f.read()

    return json.loads(data)