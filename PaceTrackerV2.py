import sys
import pac
import time
import os
import asyncio

class Console:
    
    def execute(self):
        while True:
            if time.strftime("%H:%M") >= "14:00" and time.strftime("%H:%M") <= "16:00":
                pac.Pac()
                time.sleep(60)
            else:
                os.system('clear')
                #print in blue text "not in service hours of 2:00pm to 3:59pm"
                print("\033[94m" + "Not in service hours of 14:00 to 15:59" + "\033[0m")
                #print "current time": current time in green text
                print("\033[92m" + "Current time: " + time.strftime("%H:%M", time.localtime()) + "\033[0m")
                #print in blue blue text "Time until Live:" + time until 14:00 in green text
                print("\033[94m" + "Time until Live: " + str(13-time.localtime().tm_hour) + " hours and " + str(60-time.localtime().tm_min) + " minutes" + "\033[0m")
                #in blue text print "Command:"
                print("\033[94m" + "Command: " + "\033[0m")
                time.sleep(60)
    def __init__(self,username,password):
        #login
        self.username = username
        self.password = password
    
        if pac.login(self.username,self.password):
            print("Login Successful")
        else:
            print("Login Failed")
            sys.exit()
        #get commands
        while True:
            command = input('Command: ')
            if command == 'exit':
                print("\033[91m" + "Exiting..." + "\033[0m")
                sys.exit()
            elif command == 'execute':
                #execute self.execute() and run it in a new thread
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_in_executor(None, self.execute)
                except:
                    exit()
                while True:
                    command = input('Command: ')
                    if command == 'stop':
                        loop.stop()
                        break
            elif command == 'help':
                print("Commands: ")
                print("update - updates all airtable values")
                print("update [route] [direction] - updates airtable value for specified route and direction")
                print("exit - exits program")
            elif command == 'update':
                pac.Pac()
            elif command.split(' ')[0] == 'update':
                pac.update_custom(command.split(' ')[1],command.split(' ')[2],' '.join(command.split(' ')[3:]))
            else:
                print("Invalid Command")
                print("Type 'help' for list of commands")


#create object with arguements from command line
object = Console(sys.argv[1],sys.argv[2])
