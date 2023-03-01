import pac
import time
import os
while True:
    if time.strftime("%H:%M") >= "14:00" and time.strftime("%H:%M") <= "16:00":
        pac.Pac()
        time.sleep(30)
    else:
        os.system('clear')
        #print in blue text "not in service hours of 2:00pm to 3:59pm"
        print("\033[94m" + "Not in service hours of 14:00 to 15:59" + "\033[0m")
        #print "current time": current time in green text
        print("\033[92m" + "Current time: " + time.strftime("%H:%M", time.localtime()) + "\033[0m")
        #print in blue blue text "Time until Live:" + time until 14:00 in green text
        print("\033[94m" + "Time until Live: " + str(13-time.localtime().tm_hour) + " hours and " + str(60-time.localtime().tm_min) + " minutes" + "\033[0m")
        time.sleep(30)