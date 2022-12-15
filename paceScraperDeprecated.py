'''
MIT License

Copyright (c) 2022 Seaver Olson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import keyboard,time,pyairtable,colorama

#pretty color
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN


#initialize Online Database
api_key = ("keylqwDZvM1uGClmD")
table = pyairtable.Table(api_key, 'appj1B1TakHpVkHpX', 'Times')

#declare Driver Path and retrieve Bus Website URL
driver = webdriver.Chrome('/Users/Admin/Desktop/Projects/Pace/paceprogram/chromedriver')#change to path of chromedriver
driver.get("http://tmweb.pacebus.com/TMWebWatch/LiveArrivalTimes")

#Basic Functions of route class| handles all keyboard outputs
class route_functions:
    def __init__(self,route,directions):
        self.route = route
        self.directions = list(directions)
    def search(self,titleID,text):
        #used to write route and stop
        element = driver.find_element(By.ID,titleID)
        element.click()
        keyboard.write(text)
        keyboard.press_and_release("enter")
        time.sleep(1)
    def direction(self,direction):
        #used to write direction - chose to use another funciton due to abstraction level
        element = driver.find_element(By.ID,"MainContent_directionList_chosen")
        element.click()
        if direction.lower() == "west" or direction.lower() == "south":
            keyboard.press_and_release("down arrow")
        keyboard.press_and_release("enter")

#sub-class used to clean up program and keep functions seperate from __main__
class route(route_functions):
    def __init__(self,route,directions):
        super().__init__(route,directions)
        self.result = ""
        self.ID =list()
        #Dictionary of IDs and their matching Airtable ID
        #NOTE probably a better way to do this 
        airID ={'421East': 'rec4eeQbGOA6bh1qH','421West':'recWkb4t0PNGEID7m','422East':'recDCAGqFshuTSZWk','423South':'recKPs05Bvmi9Eces','422West':'recsedVWahwgBLqGh','423North':'recvEZY9Efi7GD9wd'}
        for direct in directions:
            self.ID.append(route+direct)
            self.search('MainContent_routeList_chosen',self.route)
            self.direction(direct)
            self.search('MainContent_stopList_chosen','Loyola Academy')
            time.sleep(1)#gives connection time to load
            try:
                result = driver.find_element(By.ID,"resultBox")
                self.result += result.text
            except: print(f"{RED}ERROR: COULD NOT FIND TIME")
        self.clean_result()
        for i in range(1):#only ever 2 directions
            table.update(airID.get(self.ID[i]),{'Arrival Times':self.times[i]})
        print(f'{GREEN}Route ' + route + " has been loaded")

    def clean_result(self):
        times = []
        result = list(self.result.split("\n"))
        #handles Error Cases
        if 'No upcoming' in result[0]:
            self.times = ['Not in Route','Not in Route']
        else:
            for e in result:
                if "Scheduled" not in e and "Last" not in e and "Next" not in e:
                    times.append(e)
            self.times = times

#Object Declaration
route421 = route('421',['East','West'])
route422 = route('422',['East','West'])
route423 = route('423',['North','South'])


