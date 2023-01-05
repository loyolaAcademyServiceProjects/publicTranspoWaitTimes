import requests
from bs4 import BeautifulSoup
import time
import pyairtable

#initialize Online Database
api_key = ("keylqwDZvM1uGClmD")
table = pyairtable.Table(api_key, 'appj1B1TakHpVkHpX', 'Times')

def login(username,password):
    return username == 'LoyolaPaceAdmin' and password == 'LoyolaService'

#get departure times using above urls
def get_times(route,direction):
    routes = {'421East': 'http://tmweb.pacebus.com/TMWebWatch/LiveADADepartureTimes?r=83&d=1&s=984',
                '421West': 'http://tmweb.pacebus.com/TMWebWatch/LiveADADepartureTimes?r=83&d=4&s=24267',
                '422East': 'http://tmweb.pacebus.com/TMWebWatch/LiveADADepartureTimes?r=84&d=1&s=986',
                '422West': 'http://tmweb.pacebus.com/TMWebWatch/LiveADADepartureTimes?r=84&d=4&s=24267',
                '423North': 'http://tmweb.pacebus.com/TMWebWatch/LiveADADepartureTimes?r=85&d=2&s=24267',
                '423South': 'http://tmweb.pacebus.com/TMWebWatch/LiveADADepartureTimes?r=85&d=3&s=984'}
    url = routes.get(route+direction)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #get table with id MainContent_tblADA
    times = soup.find('table', id='MainContent_tblADA')

    times = times.find_all('tr')
    #find tr that contains 'class="adatime"'
    times = [time for time in times if 'class="adatime"' in str(time)]
    #find td that contains 'class="adatime"'
    times = str(times)
    #get titles
    times = times.split('title="')
    times = times[1:]
    times = [time.split('"')[0] for time in times]
    return times


#update airtable values
def update_airtable(route,direction):
    airID ={'421East': 'rec4eeQbGOA6bh1qH','421West':'recWkb4t0PNGEID7m','422East':'recDCAGqFshuTSZWk','423South':'recKPs05Bvmi9Eces','422West':'recsedVWahwgBLqGh','423North':'recvEZY9Efi7GD9wd'}
    times = get_times(route,direction)
    #remove direction from times
    times = [time for time in times if 'pm' in time]
    flag = True
    if times == []:
        times = ['No Buses in Route']
        flag = False
    times = times[0]
    table.update(airID.get(route+direction),{'Arrival Times':times})
    print(times)
    print(route+direction)
    print(airID.get(route+direction))
    print("")
    return flag

def update_custom(route,direction,custom):
    airID ={'421East': 'rec4eeQbGOA6bh1qH','421West':'recWkb4t0PNGEID7m','422East':'recDCAGqFshuTSZWk','423South':'recKPs05Bvmi9Eces','422West':'recsedVWahwgBLqGh','423North':'recvEZY9Efi7GD9wd'}
    table.update(airID.get(route+direction),{'Arrival Times':custom})
    print(custom)
    print(route+direction)
    print(airID.get(route+direction))
    print("")
    return -1

def Pac():
    x1,x2,x3,x4,x5,x6 = (update_airtable('421','East'),update_airtable('421','West'),update_airtable('422','East'),
        update_airtable('422','West'),update_airtable('423','North'),update_airtable('423','South'))
    #if x1, x2, x3, x4, x5, x6 are return False, print xy bus not in route
    if x1 == False:
        print("\033[91m" + "421 East not in route" + "\033[0m")
    if x2 == False:
        print("\033[91m" + "421 West not in route" + "\033[0m")
    if x3 == False:       
        print("\033[91m" + "422 East not in route" + "\033[0m")
    if x4 == False:
        print("\033[91m" + "422 West not in route" + "\033[0m")
    if x5 == False:          
        print("\033[91m" + "423 North not in route" + "\033[0m")
    if x6 == False:
        print("\033[91m" + "423 South not in route" + "\033[0m")
    #print in Green text "bus times last updated at: " + current time
    print("\033[92m" + "Bus times updated at: " + time.strftime("%H:%M", time.localtime()) + "\033[0m")
