#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time
import mysql.connector
from mysql.connector import errorcode
import sys
import win32com.client
import subprocess

#IMPORTANT GLOBALS
host = "172.21.25.43"
port = 12345                # Reserve a port for your service.
attempt = 0
osb_fgw_name = "OBS 0.16.6 (64bit, windows) - Profile: MMR - Scenes: MMR"
is_recording = False
race_class = "no set class"
race_desc = "not set desc"
race_name = "not yet set"
elist = []
debug = True
#IMPORTANT PRETESTS 

#### SEE IF WE CAN FIND OSB RUNNING

shell = win32com.client.Dispatch("WScript.Shell")
if not shell.AppActivate(osb_fgw_name):
        print "Open Source Broadcaster is not running or can not be brought to the foreground looking for %s \nAttempting to launch OBS" % osb_fgw_name
        subprocess.Popen(r'C:\Program Files (x86)\obs-studio\bin\64bit\obs64.exe', cwd=r'C:\Program Files (x86)\obs-studio\bin\64bit')
        time.sleep(5)
        if shell.AppActivate(osb_fgw_name):
                print "I was able to launch OBS and bring %s to the foreground window" % osb_fgw_name
        else:
                print "ubale to launch obs with focus window check OBS is installed and correct profile is set to default"
                sys.exit(1)

if shell.AppActivate(osb_fgw_name):
        print "OSB found with name %s" % osb_fgw_name

#### END OBS DETECTION

#### CHECK DB CONNECTIVITY #######
try:
  cnx = mysql.connector.connect(user='root', password='',database='raceinfo')
  cursor = cnx.cursor()
  print "Database connection successful"
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
    print "Program will now exit"
    sys.exit(1)
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    print "Program will now exit"
    sys.exit(1)
    print(err)


print "Program startup at %s" % int(time.time())

def set_race_name(): #Sets the new race name and heat in a .txt file which is implemented in OBS
      
    f = open("RaceName.txt", "w")
    f.write(race_name)
    f.close()
    
def update_li(li): # Updates the list of most recent times in order to determine the end of the race
  
    li = cut_data[4] + li
    del li[-1] #Does this work or does it simply create an instanced copy of time_li---TESTING NEEDED
      
def start_recording(): #Opens and virtually presses button to start recording
  
    wsh = win32com.client.Dispatch("WScript.Shell")
    if wsh.AppActivate(osb_fgw_name):
        #time.sleep(1)
        wsh.SendKeys("{F10}")
        print "starting record"
        file = "C:\\placeholder.txt"
        sql = "insert into race_data (name, start, file) values ('%s', '%s', '%s')" % (race_name,int(time.time()),file)
        cursor.execute(sql)
        cnx.commit()
        is_recording == True
        if debug: print "End of start_recording" 
    else:
        print "something went wrong" 

def stop_recording(): #Opens and virtually presses button to stop recording

   if wsh.AppActivate(osb_fgw_name):
        #time.sleep(1)
        wsh.SendKeys("{F11}")
        print "stopping record"
        #file = "C:\\placeholder.txt"
        #sql = "insert into race_data (name, start, file) values ('%s', '%s', '%s')" % (race_name,int(time.time()),file)
        #cursor.execute(sql)
        #cnx.commit()
        is_recording == False
        
        if debug: print "End of stop_recording" 
   else:
        print "something went wrong" 


def stop_test():
        if len(elist) == 3 and len(set(elist)) == 1 and not is_recording:
                return True
        else:
                return False

def update_timeleft():
        f = open("timeleft.txt", "w")
        f.write(cut_data[2])
        f.close()






while 1:                                                                        #Infinite loop that is always trying to connect to the scoring server
        s = socket.socket()                                                     #Create socket  
        attempt+=1                                                              #Create counter for cpnnect attempts
        print "attempt %s" % attempt                                           #Show which attempt we are on.
        try:
                s.connect((host, port))                                         #Attempt to connect to remote server
                l =  s.recv(1024)                                               #create recieve queue
                #if l then print "connected to server"
                #print s.recv(1024)
                while (l):                                                      #while items are in the queue and we are connected process 

                        l = s.recv(1024)                                        #set queue to 1024 bytes
                        print "%s" % l.rstrip('\n')                             #strip character from each line recieved      
                        cut_data = l.split(",")                                 #cut up the comma seperated values sent from scoring server
                        
                        if cut_data[0] == "$B":                               #Process data where the first value in the comma seperated vales is $B
                                race_desc = cut_data[2]                         #extract the race description
                        
                        if cut_data[0] == "$C":                               #Process data where the first value in the comma seperated vales is $B
                                race_class = cut_data[2]                        #extract the race class

                        if cut_data[0] == "$F":                               #Process data where the first value in the comma seperated vales is $F
                                if debug: print "In $F routine"
                                elist.insert(0,cut_data[2])                     #Push latest time left value to elist list
                                del elist[3:]                                   #Delete all any elist list elements past the 3rd element
                                if stop_test():
                                        stop_recording()                                     #Checks to see if the 3 valies for time remaining are all the same if so stop recording 
                                if cut_data[4] == "\"0:01\"":                   #Has 1 second of the race elapsed
                                        start_recording()                       #If 1 second has elasped start recording
                                if is_recording:                                #Check to see if we are recording 
                                        update_timeleft()                       #Fire function to update text file with how much time is remaining

                        cut_name = "%s %s" % (race_class,race_desc)             #set variable to concatination of $B and $C data
                        #if cut_name != race_name:                               #set race_name to new data if it chnages
                        #        race_name = cut_name                            #set race_name on updates
                        #        set_race_name()                                 #write the data to the textfile
                       

                print('Connection terminated from server side')                 #If we lose the connection this gets printed

        except:                                                                 #Exception for no connection made
                print "Server did not respond"                                  #Print out the fact we had the execption
                time.sleep(1)                                                   #sleep to slow down retries
s.close                                                                         #close the socket so we can try again
