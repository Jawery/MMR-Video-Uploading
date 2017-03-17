import time
import mysql.connector
from mysql.connector import errorcode
import sys
import urllib2

def youtube_check(): #Check youtube connectivity
    try:
        urllib2.urlopen('http://youtube.com', timeout=1)
        return True
    except urllib2.URLError: 
        return False
    
    
def upload_file(address):
    #TODO upload file
    

def transcode_file(address):
    #TODO transcode file
    
    
#Check DB connectivity
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

print "Connected to DB at %s" % int(time.time())


while 1:                                       #finds files ready to be uploaded
    cursor.execute('SELECT file FROM race_data WHERE status="transcoding_done"')
    address = str(cursor.fetchone())
    if len(address) > 2 and youtube_check(): #if file name exists and can connect to youtube
        address = address[3:-3]              #cuts excess garbage from sides of string
        print ("Uploading file %s" % address)
        sql ="UPDATE race_data SET status='uploading',upload_started='%s' WHERE file = '%s'" % (int(time.time()),address)
        cursor.execute(sql)                  #set DB status to uploading, and sets uploading start time
        cnx.commit()
        upload_file(address)
        sql ="UPDATE race_data SET status='upload complete',upload_ended='%s' WHERE file = '%s'" % (int(time.time()),address)
        cursor.execute(sql)                  #sets DB status to completed uploading and sets end time of upload
        cnx.commit()
        
    else:                                    #if Youtube cannot be connected to, or no files need to be uploaded, checks for transcoding
        cursor.execute('SELECT file FROM race_data WHERE status="recording_done"')
        first_row = str(cursor.fetchone())   #finds files ready to be transcoded
        if len(first_row) >2:                #if file exists i.e. not a blank string
            print "Transcoding file"
            sql ="UPDATE race_data SET status='transcoding',transcode_started='%s' WHERE file = '%s'" % (int(time.time()),address)
            cursor.execute(sql)
            cnx.commit()                     #sets status as transcoding in DB 
            transcode_file(address)
            sql ="UPDATE race_data SET status='transcoding_done',transcode_ended='%s' WHERE file = '%s'" % (int(time.time()),address)
            cursor.execute(sql)              #completed transcoding is expressed in DB, ready to upload
            cnx.commit()
        else:
            time.sleep(2)                    #sleeps for 2 seconds and tries again



















