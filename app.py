import requests
import gi
import os
gi.require_version('Notify', '0.7')
from bs4 import BeautifulSoup
from gi.repository import GObject
from gi.repository import Notify
from pathlib import Path
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

class Status(GObject.Object):
    def __init__(self):

        super(Status, self).__init__()
        # lets initialise with the application name
        Notify.init("JioFi 3")

    def send_notification(self, title, text):
        imguri=""
        if os.path.exists("jiodot.png"):
            imguri = os.path.abspath('jiodot.png')
            print(imguri)
        else :
            imguri =os.getcwd()+"/jiodot.png"
            print(imguri)

        
        n = Notify.Notification.new(title, text, imguri)
        n.show()

    def getBattery(self):
        url = 'http://jiofi.local.html/cgi-bin/en-jio/mStatus.html'
        res = requests.get(url)
        html_page = res.content
        soup = BeautifulSoup(html_page, 'html.parser')
        battery=soup.find(id='lDashBatteryQuantity').getText()
        return battery

    def run(self):
        bat=myStatus.getBattery()
        if(int(bat.strip('%'))<50):
            myStatus.send_notification("JioFi3 Battery", bat)

myStatus = Status()

# Start the scheduler
scheduler = BlockingScheduler()
scheduler.add_job(myStatus.run, 'interval', minutes=30)
scheduler.start()

