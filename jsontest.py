import json
from datetime import datetime

# Load the taqweem JSON file
with open('tqwTashkent2023.json') as f:
    taqweem_data = json.load(f)

# Function to get month name from date string
def get_month_name(date_str):
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    return date_obj.strftime("%B")

# Print out the date, day of the week, and iftar/suhur times for the first three days of Ramadan
for i in range(1, 4):
    day_key = f'ramadan_day_{i}'
    day_data = taqweem_data[day_key]
    date = day_data['date']
    day_of_week = day_data['day']
    iftar = day_data['iftar']
    suhur = day_data['suhur']
    month_name = get_month_name(date)
    print(f"Day {i}: Date: {date} ({month_name}), Day of the Week: {day_of_week}, Iftar: {iftar}, Suhur: {suhur}")
