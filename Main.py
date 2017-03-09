#!/usr/bin/python           

import socket               
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

#IMPORTANT PRETESTS 

#### SEE IF WE CAN FIND OSB RUNNING

shell = win32com.client.Dispatch("WScript.Shell")
if not shell.AppActivate(osb_fgw_name):
        print "Open Source Broadcaster is not running or can not be brought to the foreground looking for %s \nEXITING" % osb_fgw_name
        sys.exit(1)

if shell.AppActivate(osb_fgw_name):
        print "OSB found with name %s" % osb_fgw_name


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
                        if "$F" in l:
                                print "We found race heartneat data"


                print('Connection terminated from server side')

        except:
                print "Server did not respond"
                time.sleep(1)

s.close
