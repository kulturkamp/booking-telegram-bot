import json
import pandas as pd


START_TIME = '09:00:00'
END_TIME = '18:00:00'
INTERVAL = '30min'

# removing end time itself
timestamps = pd.date_range(START_TIME, END_TIME, freq=INTERVAL).strftime('%H:%M').to_list()[:-1]

def write_booking_data(date, stamp, quant):
    data = read_booking_data() 

    if date not in data:
        data[date] = dict.fromkeys(timestamps, 0)

    data[date][stamp] += 1

    with open('booking.json', 'w') as f:
         json.dump(data, f, ensure_ascii=False)
    

def read_booking_data():
    with open('booking.json', 'r') as f:
         data = f.read()

    return json.loads(data)