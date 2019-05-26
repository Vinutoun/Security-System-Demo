import os
import glob
import picamera
import RPi.GPIO as GPIO
import smtplib
from smbus import SMBus
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

sender = '......@gmail.com' #Gmail account (Turn on Less secured mode)
password = '.........'      #Password
receiver = '....@gmail.com' #Gmail account (Turn on Less secured mode)

Directory = './MyRoom/' #Create before run the program or put the one that already exits
PicName = 'image'
            
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.IN)  

def sendEmail():
    print ('Sending email....')   
    files = sorted(glob.glob(os.path.join(Directory, PicName + '[0-9][0-9][0-9].jpg')))
    count = 0
    if len(files) > 0:
        count = int(files[-1][-7:-4])+1
    filename = os.path.join(Directory, PicName + '%03d.jpg' % count)
    with picamera.PiCamera() as camera:
        pic = camera.capture(filename)
   
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = 'Motion Detected'
    
    body = 'Object captured'
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


slave_address = 0x8
bus = SMBus(1)

while True:
    detect = GPIO.input(15)
    if detect == 0:
        print ("Inactive", detect)
        bus.write_byte(slave_address, 0)
        sleep(0.5)
    elif detect == 1:
        print("Active", detect)
        bus.write_byte(slave_address, 1)
        sendEmail()
