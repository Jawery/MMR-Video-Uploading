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
elist = []
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
  cnx = mysql.connector.connect(user='root', password='no_password_on_github',database='raceinfo')
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


cursor = cnx.cursor()
print "Database connection successful"

print "Program startup at %s" % int(time.time())

def set_race_name(): #Sets the new race name and heat in a .txt file which is implemented in OBS
      
    f = open("RaceName.txt", "w")
    f.write(long_race_name_1)
    f.close()
    
def update_li(li): # Updates the list of most recent times in order to determine the end of the race
  
    li = cut_data[4] + li
    del li[-1] #Does this work or does it simply create an instanced copy of time_li---TESTING NEEDED
      
def start_recording(): #Opens and virtually presses button to start recording
  
    wsh = win32com.client.Dispatch("WScript.Shell")
    wsh.AppActivate("OpenSource Broadcaster")
    wsh.SendKeys("F10")
    print "starting record"
    file = "C:\\placeholder.txt"
    sql = "insert into race_data (name, start, file) values ('%s', '%s', '%s')" % (race_name,int(time.time()),file)
    cursor.execute(sql)
    cnx.commit()
    is_recording == True

def stop_recording(): #Opens and virtually presses button to stop recording

    wsh = win32com.client.Dispatch("WScript.Shell")
    wsh.AppActivate("OpenSource Broadcaster")
    wsh.SendKeys("F10")
    is_recording == False


def stop_test():
        if len(elist) == 3 and len(set(elist)) == 1 and not is_recording:
                return True
        else:
                return False




def update_timeleft():
        f = open("timeleft.txt", "w")
        f.write(cut_data[2])
        f.close()














while 1:
        s = socket.socket()
        attempt+=1
        print "attempt %s" % attempt
        try:
                s.connect((host, port))
                l =  s.recv(1024)
                #if l then print "connected to server"
                #print s.recv(1024)
                while (l):

                        l = s.recv(1024)
                        print "%s" % l.rstrip('\n') #f.close()

                        cut_data = l.split(",")
                        
                        if cut_data[0] == '"$B"':
                                race_desc = cut_data[2]
                        
                        if cut_data[0] == '"$C"':
                                race_class = cut_data[2]

                        if cut_data[0] == '"$F"':
                                elist.insert(0,cut_data[2])
                                update_elapsed()
                                del elist[3:]
                                if cut_data[4] == "\"0:01\"":
                                        start_recording()

                        print "cut - %s" % cut_data[0]
                        race_name = "%s %s" % (race_class,race_desc)  
                        print race_name

                        
                         
                print('Connection terminated from server side')

        except:
                print "Server did not respond"
                time.sleep(1)

s.close
