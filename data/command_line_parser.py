import datetime
from collections import defaultdict
import pandas as pd

amount_of_data = 0
size_limit = 1000
#{'Station Name' -> 'Date' -> ['Start', 'End', 'Low', 'High']}

weather_data = defaultdict(dict)
while True:
    line = input()
    #parese line and extract relevant data
    weather_station, timestamp, temperature = line.split(",")
    temperature = float(temperature)
    #add entries to dictionary
    if weather_station not in weather_data:
        weather_data[weather_station] = defaultdict(list)
    #extract AM/PM convert timestamp to datetime
    time_zone = timestamp[-2:]  
    timestamp = datetime.datetime.strptime(timestamp, "%m/%d/%Y %H:%M:%S %p")
    month, day, year, hour = timestamp.month, timestamp.day, timestamp.year, timestamp.hour

    #insert in in weather data, and determine start, end, low, high temperatures
    date_key = str(month) + "/" + str(day) + "/" + str(year)
    if date_key not in weather_data[weather_station]:
        weather_data[weather_station][date_key] = [0, 0, float("-inf"), float("inf")]
    if timestamp.hour == 12 and time_zone == "AM":
        weather_data[weather_station][date_key][0] = temperature
    elif timestamp.hour == 11 and time_zone == "PM":
        weather_data[weather_station][date_key][1] = temperature
    
    max_temperature = weather_data[weather_station][date_key][2]
    min_temperature = weather_data[weather_station][date_key][3]
    
    if temperature > max_temperature:
        weather_data[weather_station][date_key][2] = temperature
    elif temperature < min_temperature:
        weather_data[weather_station][date_key][3] = temperature

    #no condition specified for stopping data parsing
    if amount_of_data == size_limit:
        break
    amount_of_data += 1

#create output list of all relevant information as csv
col_list = ["Station Name", "Date", "Start Temperature", "End Temperature", "Low Temperature", "High Temperature"]
number_of_columns = 365 * len(weather_data)
output_df = pd.DataFrame(columns = col_list, index = range(number_of_columns))
i = 0
for station in weather_data:
    for date in weather_data[station]:
        output_df.iloc[i, output_df.columns.get_loc("Station Name")] = station
        output_df.iloc[i, output_df.columns.get_loc("Date")] = date
        output_df.iloc[i, output_df.columns.get_loc("Start Temperature")] = weather_data[station][date][0]
        output_df.iloc[i, output_df.columns.get_loc("End Temperature")] = weather_data[station][date][1]
        output_df.iloc[i, output_df.columns.get_loc("Low Temperature")] = weather_data[station][date][2]
        output_df.iloc[i, output_df.columns.get_loc("High Temperature")] = weather_data[station][date][3]
        i += 1
output_df.to_csv("Organized Data")