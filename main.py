"""
Main module

Testing the web scraping functionality with requests
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

page = requests.get('https://forecast.weather.gov/MapClick.php?lat=41.894&lon=-88.0966')
soup = BeautifulSoup(page.content, 'html.parser')
seven_day = soup.find(id='seven-day-forecast')
period_tags = seven_day.select('.tombstone-container .period-name')
periods = [pt.get_text() for pt in period_tags]
short_descs = [sd.get_text() for sd in seven_day.select('.tombstone-container .short-desc')]
temps = [t.get_text() for t in seven_day.select('.tombstone-container .temp')]
descs = [d['title'] for d in seven_day.select('.tombstone-container img')]
weather = pd.DataFrame({
	"period": periods,
	"short_desc": short_descs,
	"temp": temps,
	"desc": descs
})
temp_nums = weather['temp'].str.extract(r'(?P<temp_num>\d+)', expand=False)
weather['temp_num'] = temp_nums.astype('int')
is_night = weather['temp'].str.contains('Low')
weather['is_night'] = is_night

print(weather)
