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
  
def stop_recording(): #Opens and virtually presses button to stop recording

    wsh = win32com.client.Dispatch("WScript.Shell")
    wsh.AppActivate("OpenSource Broadcaster")
    wsh.SendKeys("F10")


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
                        print "%s" % l #f.close()

                        cut_data = str.split(l,)

                        if cut_data[0] == '"$B"':
                                race_desc = cut_data[2]
                        if cut_data[0] == '"$C"':
                                race_class = cut_data[2]

                        race_name = "%s %s" % (race_class,race_desc)

                        if "$F" in l:
                                print "We found race heartneat data"

                        if is_recording and cut_data[0] == '"$F"':
                                print "foo"

                        if cut_data[0] == '"$F"':
                                update_li(time_li)  
                                if cut_data[4] == '"0:01"' and is_recording == False:
                                        start_recording()
                                elif time_li[0] == time:
                                        stop_recording()


                print('Connection terminated from server side')

        except:
                print "Server did not respond"
                time.sleep(1)

s.close
