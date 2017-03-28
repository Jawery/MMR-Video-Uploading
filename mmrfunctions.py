from usersettings import *
import socket               # Import socket module
import time
import mysql.connector
from mysql.connector import errorcode
import sys
import win32com.client
import subprocess
import glob
import os
import urllib2
import psutil


class Database:

    def __init__(self):
    	try:
    		self.connection = mysql.connector.connect(user=db_user, password=db_pass,database=db_database)
        	self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
        	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
   		    	print "Something is wrong with your user name or password"
    			print "Program will now exit"
    			sys.exit(1)

    		elif err.errno == errorcode.ER_BAD_DB_ERROR:
    			print("Database does not exist")
    			print "Program will now exit"
    			sys.exit(1)
    			print(err)	


    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()


    def update(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()


    def query(self, query):
    	self.cursor.execute(query)
        return(self.cursor.fetchall())


    def transcode_in_progess(self):
    	self.cursor.execute("select file from race_data where status = 'recording_done' and  transcode_started is not null and transcode_ended is null")
    	self.cursor.fetchall()
    	self.cursor.rowcount
    	return(int(self.cursor.rowcount))


    def next_transcode(self):
    	self.cursor.execute("select file from race_data where status = 'recording_done' and  transcode_started is null order by id asc limit 1")
    	return(self.cursor.fetchall())


    def upload_in_progess(self):
    	self.cursor.execute("select file from race_data where status = 'recording_done' and transcode_ended is not null and upload_started is not null and upload_ended is null")
    	self.cursor.fetchall()
    	self.cursor.rowcount
    	return(int(self.cursor.rowcount))


    def next_upload(self):
    	self.cursor.execute("select file from race_data where status = 'recording_done' and  transcode_ended is not null and upload_started is null order by id asc limit 1")
    	return(self.cursor.fetchall())


    def __del__(self):
    	#self.cursor.close()
        self.connection.close



def record_length(file):
	db=Database()
	sql = "select * , finished_recording - started_recording as diff from race_data where file = '%s'" % file
	print sql
	diff = db.query(sql)
	
	#print diff
	for item in diff:
		#print type(item)
		length = int(item[15])
	sql = "UPDATE race_data SET video_length='%s' WHERE file = '%s'" % (length,file)
	print sql
	db.update(sql)


def kill_process(process):
	print "looking for --%s--" % process
	for proc in psutil.process_iter():
	   	if proc.name() == process:
	   		print "match"
	   		proc.kill()


def set_video_duration(file):
	command = "ffprobe %s 2>&1 |findstr Duration" % file
	print command
	#subprocess.call(command, shell=True)
	process = subprocess.Popen(command, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

	# wait for the process to terminate
	out, err = process.communicate()
	errcode = process.returncode
	print "OUTPUT IS %s exit code %s" % (out,errcode)
	split_data = out.split(",")
	#print split_data[0]
	split_data2 = split_data[0].split(":")
	time = "%s:%s:%s" % (split_data2[1].strip(),split_data2[2],split_data2[3])
	print "made it here"
	db = Database()
	sql = "update race_data set estimated_video_duration = '%s' where file = '%s'" % (time,file.replace("\\","\\\\"))
	print sql
	db.update(sql)
	#return(time) 

def transcode_file(file):
	command = "ffmpeg %s 2>&1 |findstr Duration" % file
	#subprocess.call(command, shell=True)
	process = subprocess.Popen(command, shell=True,
                           stdout=subprocess.PIPE, 
                           stderr=subprocess.PIPE)

	# wait for the process to terminate
	out, err = process.communicate()
	errcode = process.returncode
	split_data = out.split(",")
	#print split_data[0]
	split_data2 = split_data[0].split(":")
	time = "%s:%s:%s" % (split_data2[1].strip(),split_data2[2],split_data2[3])
	return(time) 


def osb_running():
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
    
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    #time.sleep(1)
    print "text is\n%s" % text
    print "------------ raw dict_g --------------"
    print dict_g
    print "------------ raw dict_g --------------"
    print dict_g
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


def get_numuber_of_laps():
        pass

def set_race_name(race_name): #Sets the new race name and heat in a .txt file which is implemented in OBS
      
    f = open("RaceName.txt", "w")
    f.write(race_name.replace("\"",""))
    f.close()
    
def update_li(li): # Updates the list of most recent times in order to determine the end of the race
  
    li = cut_data[4] + li
    del li[-1] #Does this work or does it simply create an instanced copy of time_li---TESTING NEEDED

def latest_video_file():
	try:
	        time.sleep(5)
	        list_of_files = glob.glob(video_path) # * means all if need specific format then *.csv
	        latest_file = max(list_of_files, key=os.path.getctime)
	        print latest_file
	        return(latest_file)
	except:
		print "something went wrong with latest_video_file"
      
def start_recording(race_name): #Opens and virtually presses button to start recording
	try:
		wsh = win32com.client.Dispatch("WScript.Shell")
		if wsh.AppActivate(osb_fgw_name):
			time.sleep(0.25)
			wsh.SendKeys("{F10}")
			file = latest_video_file()
        	sql = "insert into race_data (name, started_recording, file,status) values ('%s', '%s', '%s', 'recording')" % (race_name,int(time.time()),file.replace("\\","\\\\"))
        	print sql
        	
        	try:
        		db = Database()
        		db.insert(sql)
        		return(file)
        	except: 
        		print "sql shit the bed"
	except:
		print "something went wrong in start_record()" 
    

def stop_recording(file): #Opens and virtually presses button to stop recording
   
   wsh = win32com.client.Dispatch("WScript.Shell")
   if wsh.AppActivate(osb_fgw_name):
        time.sleep(0.25)
        wsh.SendKeys("{F11}")
        print "stopping record"
        #file = "C:\\placeholder.txt"
        sql = "UPDATE race_data SET status='recording_done',finished_recording='%s' WHERE file = '%s'" % (int(time.time()),file.replace("\\","\\\\"))
        print "THIS IS A SQL LOOK HERE ----> %s" % (sql)
        try:
        		db = Database()
        		db.update(sql)
        		record_length(file.replace("\\","\\\\"))
        		set_video_duration(file)

        except:
        	print "stop record sql update is broken"



def stop_test(is_recording):

        if debug: print "*******\n** %s **\n** %s **\n** %s **" % (len(elist),len(set(elist)),is_recording)
        if len(elist) == 3 and len(set(elist)) == 1 and is_recording:
                if debug: print "STOP TEST TRUE"
                return True
        else:
                if debug: print "STOP TEST FALSE"
                return False

def update_timeleft(timeleft):
        if debug: print "entered update time"
        f = open("timeleft.txt", "w")
        f.write(timeleft.replace("\"",""))
        f.close()


def youtube_online_check(): #Check youtube connectivity
    try:
        urllib2.urlopen('http://youtube.com', timeout=1)
        return True
    except urllib2.URLError: 
        return False
    
    
def upload_file(address):
    #TODO upload file
    pass
    

def transcode_file(address):
    #TODO transcode file
    pass    




