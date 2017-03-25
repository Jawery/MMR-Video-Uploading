import urllib2
import datetime
from bs4 import BeautifulSoup
import schedule
import time

def set_race_scroll_name(name): #Once the name on the calendar is known, update the text file
    day_of_week = datetime.datetime.today().weekday()
    f = open("standin.txt", "w")
    if day_of_week == 2 and "On Road" in name:
        f.write('Wednesday Night On Road Grinder Series')
    elif day_of_week == 4 and "Off Road" in name:
        f.write('Frovik\'s Friday Night Off Road Series')
    elif day_of_week == 6 and "On Road" in name:
        f.write('Sunday Morning Minnesota On Road Championship Series')
    elif day_of_week == 1 and "Whoop" in name:
        f.write('Tuesday Tiny Whoop Drone Racing Under The Lights')
    elif day_of_week == 5 and "Whoop" in name:
        f.write('Saturday Tiny Whoop Drone Racing')
    else:
        f.write('Molzer Mowery Racing: On Road, Off Road, Oval, And Tiny Whoop Racing')
    f = open("standin.txt", "r")
    print f.read()
    f.close()


def main(): #get current day and correlate it to see what race name is on the calendar
    now = datetime.datetime.now()
    site = 'http://www.localendar.com/public/ammdrew'
    hold = 0
    day = int(now.strftime("%d"))
    month = now.strftime("%m")
    year = now.strftime("%y")
    date = '%s-%s-%s' % (month, str(day), year)
    end_date = '%s-%s-%s' % (month, str(day+1), year)
    indices = []


    page = urllib2.urlopen(site)
    print page
    soup = BeautifulSoup(page, "lxml")
    soup = str(soup)
    soup_split = soup.split('span')
    print soup_split #Sole purpose of this is to make the program look cool from an outside perspective
    for i, elem in enumerate(soup_split):
        if 'd_%s' % (date) in elem:
            indices.append(i)
        
    index = indices[0]
    race_name = soup_split[index]
    while not 'class="m-usr m-event-title-theme' in race_name and hold<15 and not end_date in race_name:
        index += 1
        hold +=1
        race_name = soup_split[index]

    race_split = race_name.split('>')
    race = race_split[-1]
    race = race[0:-2]
    print race         #race now has exactly the text written on site
    set_race_scroll_name(race)
    
    
main()   #runs once on startup
schedule.every().day.at("5:00").do(main) #run every morning at 5, assuming the computer stays on, this will avoid issues of races past midnight
while True:
    schedule.run_pending()
    time.sleep(5) #sleep and send a heartbeat to terminal
    print '---Scrolling Text Heartbeat---'





