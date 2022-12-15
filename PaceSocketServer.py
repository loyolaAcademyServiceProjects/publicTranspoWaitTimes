import sys
import pac
import time
import os
import asyncio
import socket

class Console:
    
    def execute(self):
        while True:
            if time.strftime("%H:%M") >= "14:00" and time.strftime("%H:%M") <= "16:00":
                pac.Pac()
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
    def __init__(self):
        #start parrell process that creates a socket server and gets data from client
        #get username and password from client
        connection = asyncio.new_event_loop()
        asyncio.set_event_loop(connection)
        connection.run_in_executor(None, self.connect)
        #get username from connection process
        self.username = sys.stdin.read()
        self.username = sys.stdin.read()
        print('recieved username: ' + self.username)
        self.password = sys.stdin.read()
    
        if pac.login(self.username,self.password):
            print("Login Successful")
        else:
            print("Login Failed")
            sys.exit()
        #get commands
    def send_command(self,command):
            if command == 'exit':
                print("\033[91m" + "Exiting..." + "\033[0m")
                sys.exit()
            elif command == 'execute':
                #execute self.execute() and run it in a new thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_in_executor(None, self.execute)
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
                print("Invalid Command:")
                print(command)
                print("Type 'help' for list of commands")
    def connect(self):
        s = socket.socket()
        s.bind(('localhost', 5001))
        s.listen()
        conn, addr = s.accept()
        while True:
            data = conn.recv(1024)
            data1 = data.decode().split(' ')[1]
            #strip eveything that isnt a letter or number
            data1 = ''.join(e for e in data1 if e.isalnum())
            if not data:
                break
            if 'USERNAME' in data.decode():
                self.username = data1
            elif 'PASSWORD' in data.decode():
                self.password = data1
            elif 'COMMAND' in data.decode():
                self.send_command(data1)



#create object with arguements from command line
object = Console()
