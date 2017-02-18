import socket
import time
import win32com.client

TCP_IP = '127.0.0.1'
TCP_PORT = 12345
BUFFER_SIZE = 1024
data = ""
cut_data = ""
clas = ""
race = ""
long_race_name_1 = ""
long_race_name_2 = ""
is_recording = False
time_li = [1,2,3]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #possibly need a bind function for s

def get_data(): #Retrieves data from TCP server on timing computer in order to be manipulated 
      
    while 1:
        try:
            s.connect((TCP_IP, TCP_PORT)) #Under the assumption that an error will rise if unable to connect to port
        except:
            pass
        try:
            return s.recv(BUFFER_SIZE) #Using a seperate try function under the impression that attempting to connect
        except:                           #To an already connected server will rise an error
            time.sleep(5)
          
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
    data = get_data()
    cut_data = data.split(",")
    
    if cut_data[0] == '"$F"':
        update_li(time_li)  
        if cut_data[4] == '"0:01"' and is_recording == False:
            start_recording()
        elif time_li[0] == time_li[1] == time_li[2] and is_recording == True:
            stop_recording()
    
    
    elif cut_data[0] == '"$B"':
        clas = cut_data[1]
      
      
    elif cut_data[0] == '"$C"':
        race = cut_data[1]
        long_race_name_1 = race + clas
        if long_race_name_1 != long_race_name_2:
            long_race_name_2 = long_race_name_1
            set_race_name()
        
              
      
    
#Referential Code Segments  
'''
#-----TCP CLIENT-----#
import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data


#-----TCP SERVER-----#
import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()


#-----PRESSING A BUTTON-----#

import win32com.client
wsh = win32com.client.Dispatch("WScript.Shell")
wsh.AppActivate("app")
wsh.SendKeys("k")
'''

