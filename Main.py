#!/usr/bin/python           # This is client.py file

from usersettings import *
from mmrfunctions import *
import socket               # Import socket module
import time
import mysql.connector
from mysql.connector import errorcode
import sys
import win32com.client
import subprocess
import glob
import os

db = Database()                                                                 #create a db object which has a side effect of ing that the db is online 

kill_process(obs_exe)
osb_running()                                                                   #make sure obs is running and in focus.



print "Program startup at %s" % int(time.time())

while 1:                                                                        #Infinite loop that is always trying to connect to the scoring server
        s = socket.socket()                                                     #Create socket  
        attempt+=1                                                              #Create counter for cpnnect attempts
        print "attempt %s" % attempt                                           #Show which attempt we are on.
        try:
                s.connect((host, port))                                         #Attempt to connect to remote server
                l =  s.recv(1024)                                               #create recieve queue
               
                while (l):                                                      #while items are in the queue and we are connected process 

                        line_count+=1
                        l = s.recv(1024)                                        #set queue to 1024 bytes
                        if debug: print "raw line ----> %s  <-----" % l
                        l = l.replace("\"","")                             #strip character from each line recieved      
                        cut_data = l.split(",")                                 #cut up the comma seperated values sent from scoring server
                        
                        if cut_data[0] == "$B":                               #Process data where the first value in the comma seperated vales is $B
                                race_desc = cut_data[2]                         #extract the race description
                        
                        if cut_data[0] == "$C":                               #Process data where the first value in the comma seperated vales is $B
                              
                                race_class = cut_data[2]                        #extract the race class
                                                     

                        if cut_data[0] == "$J":
                                try:
                                        dict_j[cut_data[1].replace("\"","")] = {cut_data[1]: {'number': cut_data[1], 'last_lap': cut_data[2], 'total_time_elapsed': cut_data[3] }}
                                                                                
                                except:
                                        print "whoops something went wrong processing $J data"

                        if cut_data[0] == "$F":                                                 #Process data where the first value in the comma seperated vales is $F
                                cut_name = "%s %s" % (race_class.rstrip('\n'),race_desc.rstrip('\n'))
                                if debug: print "%s in $F routine" % cut_data[2]
                                elist.insert(0,cut_data[2])                                     #Push latest time left value to elist list
                                del elist[3:]                                                   #Delete all any elist list elements past the 3rd element
                                                                                
                                if stop_test(is_recording):                                                 #Checks to see if the 3 valies for time remaining are all the same if so stop recording 
                                        print "stop_test() is true will run stop_recording()"
                                        stop_recording(file)
                                        print "I ran stop recording"
                                        is_recording = False                                     
                                
                                if cut_data[4] == "0:01":                                   #Has 1 second of the race elapsed
                                        print "fire start_record()"
                                        file = start_recording(cut_name)                                #If 1 second has elasped start recording
                                        is_recording = True
                                
                                update_timeleft(cut_data[2])                       #Fire function to update text file with how much time is remaining


                        if cut_data[0] == "$COMP":
                                
                                try:
                                        dict_comp[cut_data[1].replace("\"","")] = {cut_data[1]: {'number': cut_data[2], 'transponder': cut_data[3], 'first_name': cut_data[4], 'last_name': cut_data[5] }} #% (cut_data[2],cut_data[3],cut_data[4],cut_data[5]) #{'number': '%s', 'transponder': '%s', 'first_name': '%s', 'last_name': '%s'} % (cut_data[2],cut_data[3],cut_data[4],cut_data[5])}
                                except:
                                        print "Failed to push new data to comp dictionary"
                      
                        if cut_data[0] == "$G":

                                try:
                                        dict_g[cut_data[1]] = {cut_data[1]: {'position': cut_data[1] , 'registration_number': cut_data[2]}} #, 'registration_number': cut_data[3], 'laps': cut_data[4], 'total_time': cut_data[5] }}
                                except:
                                        print "Failed to push new data to comp dictionary g dictionary"
                               
                        cut_name = "%s %s" % (race_class.rstrip('\n'),race_desc.rstrip('\n'))             #set variable to concatination of $B and $C data
                        set_race_name(cut_name)
                                             

                print('Connection terminated from server side')                 #If we lose the connection this gets printed

        except:                                                                 #Exception for no connection made
                print "Server did not respond"                                  #Print out the fact we had the execption
                time.sleep(1)                                                   #sleep to slow down retries
s.close                                                                         #close the socket so we can try again
