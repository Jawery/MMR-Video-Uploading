#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import time
import mysql.connector
from mysql.connector import errorcode
import sys
import win32com.client
import subprocess
import glob
import os

#IMPORTANT GLOBALS
#host = "172.21.25.43"
host = "127.0.0.1"
port = 12345                # Reserve a port for your service.
attempt = 0
osb_fgw_name = "OBS 0.16.6 (64bit, windows) - Profile: MMR - Scenes: MMR"
is_recording = False
race_class = "no set class"
race_desc = "not set desc"
race_name = "not yet set"
elist = []
dict_comp = {}
dict_g = {}
dict_h = {}
line_count=0


#debug = True
debug = False
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


### END OBS DETECTION

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

def update_comp():
    f = open("overlay.txt", "w")
    text=""
    #print dict_g
    print "working on overlay\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO"
    for key in sorted(dict_g.iterkeys()):
        #print "working on position %s" % key

        (fn,ln) = find_driver(dict_g[key][key]["registration_number"])
        #print "%s: %s %s" % (key,fn,ln)
        text = "%s %s: %s %s\n" % (text, key,fn,ln)
        #driver_name = dict_comp[key]
        #text =  "%s %s\n" % (key, driver_name)
        #print "key is %s" % key
        #print "data for position %s %s" % (key,dict_g[key])
        #print (dict_comp[key][key]['first_name'] , dict_comp[key][key]['last_name'])
        #print "%s: %s %s" % (key, dict_comp[key][key]['first_name'] , dict_comp[key][key]['last_name'])
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "text is\n%s" % text
    #find_driver("1")  
    #print dict_g

    f.write(text)
    f.close()

def find_driver(reg_num):
        try:
                if debug: print "looking for registration number %s" % reg_num
                for key in dict_comp.iterkeys():
                        if dict_comp[key][key]["number"] == reg_num:
                                return (dict_comp[key][key]["first_name"],dict_comp[key][key]["last_name"])

        except:
                print "you broke find_driver method!"


def set_race_name(): #Sets the new race name and heat in a .txt file which is implemented in OBS
      
    f = open("RaceName.txt", "w")
    f.write(race_name.replace("\"",""))
    f.close()
    
def update_li(li): # Updates the list of most recent times in order to determine the end of the race
  
    li = cut_data[4] + li
    del li[-1] #Does this work or does it simply create an instanced copy of time_li---TESTING NEEDED

def latest_video_file():
        time.sleep(5)
        list_of_files = glob.glob('C:\Users\Emery\Videos\*.mp4') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print latest_file
        return(latest_file)

      
def start_recording(): #Opens and virtually presses button to start recording
  
    wsh = win32com.client.Dispatch("WScript.Shell")
    if wsh.AppActivate(osb_fgw_name):
        time.sleep(0.25)
        #wsh.SendKeys("{F10}")
        
        print "starting record"
        file = latest_video_file()
        sql = "insert into race_data (name, started_recording, file) values ('%s', '%s', '%s')" % (race_name.replace("\"",""),int(time.time()),file)
        cursor.execute(sql)
        cnx.commit()
        return(file)
        
        if debug: print "End of start_recording" 
    else:
        print "something went wrong" 

def stop_recording(): #Opens and virtually presses button to stop recording
   
   wsh = win32com.client.Dispatch("WScript.Shell")
   if wsh.AppActivate(osb_fgw_name):
        time.sleep(0.25)
        wsh.SendKeys("{F11}")
        print "stopping record"
        #file = "C:\\placeholder.txt"
        sql = "UPDATE race_data SET status='recording_done',finished_recording='%s' WHERE file = '%s'" % (int(time.time()),file)
        print "THIS IS A SQL LOOK HERE ----> %s" % (sql)
        #sql = "insert into race_data (name, start, file) values ('%s', '%s', '%s')" % (race_name,int(time.time()),file)
        cursor.execute(sql)
        cnx.commit()
        #is_recording = False
        #if debug: print "End of stop_recording" 
   #else:
   #     print "something went wrong" 


def stop_test():

        if debug: print "*******\n** %s **\n** %s **\n** %s **" % (len(elist),len(set(elist)),is_recording)
        if len(elist) == 3 and len(set(elist)) == 1 and is_recording:
                if debug: print "STOP TEST TRUE"
                return True
        else:
                if debug: print "STOP TEST FALSE"
                return False

def update_timeleft():
        if debug: print "entered update time"
        f = open("timeleft.txt", "w")
        f.write(cut_data[2].replace("\"",""))
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

                        line_count+=1
                        l = s.recv(1024)                                        #set queue to 1024 bytes
                        if debug: print "raw line ----> %s  <-----" % l
                        l = l.replace("\"","")                             #strip character from each line recieved      
                        cut_data = l.split(",")                                 #cut up the comma seperated values sent from scoring server
                        
                        if cut_data[0] == "$B":                               #Process data where the first value in the comma seperated vales is $B
                                race_desc = cut_data[2]                         #extract the race description
                        
                        if cut_data[0] == "$C":                               #Process data where the first value in the comma seperated vales is $B
                                race_class = cut_data[2]   
                                                     #extract the race class

                        if cut_data[0] == "$J":
                                dict_j[[cut_data[1].replace("\"","")]] = {cut_data[1]: {'number': cut_data[2], 'transponder': cut_data[3] }}

                        if cut_data[0] == "$F":                               #Process data where the first value in the comma seperated vales is $F
                                update_comp()                                 # ALL THE RESULTS SHOULD BE IN FROMT HE PREVIOUS SECOND TIME TO UPDATE THE OVERLAY
                                if debug: print "%s in $F routine" % cut_data[2]
                                elist.insert(0,cut_data[2])                     #Push latest time left value to elist list
                                del elist[3:]                                   #Delete all any elist list elements past the 3rd element
                                if stop_test():
                                        print "I SHOULD STOP"
                                        stop_recording()
                                        print "I ran stop recording"
                                        dict_comp.clear()
                                        dict_g.clear()
                                        is_recording = False                                     #Checks to see if the 3 valies for time remaining are all the same if so stop recording 
                                if cut_data[4] == "\"0:01\"":                   #Has 1 second of the race elapsed
                                        file = start_recording()                       #If 1 second has elasped start recording
                                        is_recording = True
                                #if is_recording:                                #Check to see if we are recording 
                                update_timeleft()                       #Fire function to update text file with how much time is remaining

                        if cut_data[0] == "$COMP":

                                #print "FOUND COMP"
                                #print "pushing key %s value %s" % (cut_data[1],cut_data[2]) 
                                try:
                                        #print " adding key" + cut_data[1]
                                        dict_comp[cut_data[1].replace("\"","")] = {cut_data[1]: {'number': cut_data[2], 'transponder': cut_data[3], 'first_name': cut_data[4], 'last_name': cut_data[5] }} #% (cut_data[2],cut_data[3],cut_data[4],cut_data[5]) #{'number': '%s', 'transponder': '%s', 'first_name': '%s', 'last_name': '%s'} % (cut_data[2],cut_data[3],cut_data[4],cut_data[5])}
                                except:
                                        print "WRONG"
                                #print "---------------------------"
                                #print dict_comp
                        #if "COMP" in l:
                        #        print "FOUND COMP %s" % line_count
                        #        print dict_comp
                        #        print "pushing key %s value %s" % (cut_data[1],cut_data[2]) 
                        #        dict_comp[cut_data[1]]=cut_data[2]
                        #        print dict_comp


                        if cut_data[0] == "$G":

                                #dict_g[cut_data[1]] = "%s" % cut_data[2]
                                try:
                                        dict_g[cut_data[1]] = {cut_data[1]: {'position': cut_data[1] , 'registration_number': cut_data[2]}} #, 'registration_number': cut_data[3], 'laps': cut_data[4], 'total_time': cut_data[5] }}
                                except:
                                        print "WRONG 2"
                                #print dict_g

                        cut_name = "%s %s" % (race_class.rstrip('\n'),race_desc.rstrip('\n'))             #set variable to concatination of $B and $C data
                        if cut_name != race_name:                               #set race_name to new data if it chnages
                                race_name = cut_name                            #set race_name on updates
                                set_race_name()                                 #write the data to the textfile
                       
                        
                        #dict_g.clear()
                        #for key in sorted(dict_comp.iterkeys()):
                        #        print "%s: %s" % (key, dict_comp[key])
                        

                print('Connection terminated from server side')                 #If we lose the connection this gets printed

        except:                                                                 #Exception for no connection made
                print "Server did not respond"                                  #Print out the fact we had the execption
                time.sleep(1)                                                   #sleep to slow down retries
s.close                                                                         #close the socket so we can try again
