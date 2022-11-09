
'''
stop : 984_75
route {
        421: 83 - 421 - Wilmette Avenue
        422: 84 - 
        423: 85
}
direction{
        East: 1
        North: 2
        South: 3
        West: 4
}
domain: tmweb.pacebus.com
path: /TMWebWatch

NOTES:
    Possible exploit under jquery protocol
        ```
        var matches = (new RegExp(this._generatePrefix() + "=([^;]+);")).exec(document.cookie);
            if (matches && document.location.protocol !== matches[1]) {
               window.sessionStorage.clear();
               this._initCache();
               for (var key in this._cookieCache) {
                   window.sessionStorage.setItem(key, this._cookieCache[key])
               }
            }
        ```  Website checks if cookies have been changed and sets the key accordingly.  
             Could create a false cookie and inject it using the same ID

    Possible exploit using stored key values.  Inject on path /TMWebWatch to test auth walls?
    ```
    stop - MainContent_stopList_chosen
    route - MainContent_routeList_chosen
    driver.add_cookie({"name": "route", "value": "83", "domain":"tmweb.pacebus.com","path":"/TMWebWatch"})
    ```
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import keyboard
import time

driver = webdriver.Chrome('/Users/Admin/Desktop/Pace/paceprogram/chromedriver')#change to path of chromedriver
driver.get("http://tmweb.pacebus.com/TMWebWatch/LiveArrivalTimes")

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
        for direct in directions:
            self.search('MainContent_routeList_chosen',self.route)
            self.direction(direct)
            self.search('MainContent_stopList_chosen','Loyola Academy')
            time.sleep(1)
            try:
                result = driver.find_element(By.ID,"resultBox")
                self.result += result.text
            except:
                print("ERROR: COULD NOT FIND TIME")
        self.clean_result()
    def clean_result(self):
        times = []
        result = list(self.result.split("\n"))
        for e in result:
            if "Scheduled" not in e and "Last" not in e and "Next" not in e:
                times.append(e)
        self.times = times
            
route421 = route('421',['East','West'])
route422 = route('422',['East','West'])
route423 = route('423',['North','South'])

print("421:")
print(route421.times)
print("422:")
print(route422.times)
print("423:")
print(route423.times)

