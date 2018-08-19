import time
import time
from datetime import datetime
import cv2
import os, errno
from PIL import ImageFilter
from PIL import Image, ImageDraw, ImageFont

from fractions import Fraction


"""
#=================================ONEDRIVE SECTION=============================
Onedrive authencation and upload every photo taken by device
"""

import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from onedrivesdk.session import Session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import webbrowser
import smtplib

local_folder = 'timelapse'      #Local folder where picture stored
remote_folder = "2700usbcam_2015_Aug_14" #Remote foler name to be created

#OneDrive API Authentication. Created from Onedrive API developer console.
client_secret = ""
client_id_str = ""

#Onedrive account email and password
user_name    = 'email@example.com'
password     = 'passowrd'

num_of_seconds = 10 #Interval between each photo capture

# use a truetype font
font = ImageFont.load_default() #FreeTypeFont("arial.ttf", 15)

"""
Call this method to send notification/alert or anything specific
"""
def send_email (send_to, message):
    print("Sending Email")
    try:
        #SMTP server name. comcast smpt server used here.
        smtpserver = smtplib.SMTP("smtp.comcast.net", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(GMAIL_USER, GMAIL_PASS)
        header = 'To:' + send_to + '\n' + 'From: ' + From_email
        header = header + '\n' + 'Subject:' + SUBJECT + '\n'

        msg = header + '\n' + TEXT + ' \n\n'
        msg = msg +  message + '\n\n'
        msg = msg + "Your Name\n"
        smtpserver.sendmail(GMAIL_USER, send_to, msg)
        smtpserver.close()
        print("Sending ", send_to, ' Success')
    except Exception:
        print("Error:unable to send email")


#To get OneDrive Access Token.  This function is designed to all
# headless node like Raspberry PI
# to authenticate and access OneDrive API to upload files.
# NOTE: In case Failed to authenticate, connect the device with Monitor(display)
# and check if other errors.
def get_onedrive_access_token (user_name, password):

    redirect_uri  = "https://login.live.com/oauth20_desktop.srf"

    #setup authentication client
    client = onedrivesdk.get_default_client(client_id=client_id_str,
                                            scopes=['wl.signin',
                                                    'wl.offline_access',
                                                    'onedrive.readwrite'])

    auth_url = client.auth_provider.get_auth_url(redirect_uri)

    # Block thread until we have the code Original method
    # access_code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    #Method 1

    #print(auth_url)

    driver = webdriver.PhantomJS()

    #driver.set_window_size(1120, 550)
    driver.get(auth_url)


    #it may vary depends on your network speed and location
    driver.implicitly_wait(30)

    login_field = driver.find_element_by_name("loginfmt")
    login_field.send_keys(user_name)
    next_btn = driver.find_element(By.ID, "idSIButton9")
    next_btn.click()
    time.sleep(5)

    password_field = driver.find_element_by_name("passwd")
    password_field.send_keys(password)


    print("Onedrive authntication in progress....")
    try:

        signin_btn = driver.find_element(By.ID, "idSIButton9")
        signin_btn.click()
        driver.implicitly_wait(5)  # seconds, may changes needed depends on Internet connection speed
        idBtn_Accept = driver.find_element(By.ID, "idBtn_Accept")
        idBtn_Accept.click()

        driver.implicitly_wait(5)  # seconds, may changes needed depends on Internet connection speed

        #parse URL to get code and close the browser
        tokens = driver.current_url.split('=')
        driver.quit()

        #print(tokens[1].split('&')[0])
        access_code = tokens[1].split('&')[0]

        #print("access code is here ", access_code)

        #authenticate the client
        client.auth_provider.authenticate(access_code, redirect_uri, client_secret)

        #we dont need webdriver any more
        driver.quit()

    #if there is any error screen shot createdhere
    except Exception as e:
        screenshot_name = "exception.png"
        driver.get_screenshot_as_file(screenshot_name)
        print("Screenshot saved as '%s'" % screenshot_name)

    return client

def onedrive_create_folder(onedrive_access, folder_name):
    try:
        item_id = "root"
        drive   = "me"
        #method to create new folder
        f = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.folder = f
        i.name = folder_name
        onedrive_access.item(drive=drive, id=item_id).children.add(i)

    except Exception as e:
        #print('Folder create:: ', str(e))

        return


#Function to return given folder name to ID from OneDrive
def get_remote_folder_index (onedrive_access,folder_name):

    onedrive_folder_list = onedrive_access.item(drive="me", id="root").children.get()
    for count, item in enumerate(onedrive_folder_list):
        #print(count,item.name, folder_name)

        if item.name == folder_name:
            item_id = item.id
            break

    return item_id

#get all local folder file list
def get_local_folder_files (folder_name):

    folder_name = '{}{}'.format('', folder_name)
    files = os.listdir(folder_name)
    #for filename in files:
        #print(filename)
    return files

#upload given file to Onedrive
def upload_file(onedrive_access,folder_id, name_of_file):
    try:
        onedrive_access.item(drive='me', id=folder_id).children[name_of_file].upload("./"+ local_folder + "/" + name_of_file)
        print("Uploading ", name_of_file, "Success")

        #Enable this to delete uploaded files from local folder
        #print("File ", name_of_file, "Deleted from local system")
        #os.remove("./timelapse/" + name_of_file)

    except OSError:
        pass
    except Exception as e:
        print('upload_file() : exception', str(e))


#Given local folder name, get all Files and upload to OneDrive
def upload_folder_photo (onedrive_access, local_folder_name):

    # create folder name on remote drive
    #remote_folder = "picam_180"
    onedrive_create_folder(onedrive_access, remote_folder)

    #find folder id to upload picture
    id_of_folder = get_remote_folder_index (onedrive_access, remote_folder)

    #Upload single image file TEST *******
    #file_name = 'DSC_0001.JPG'
    #onedrive_access.item(drive='me', id=id_of_folder).children[file_name].upload("./timelapse/" + file_name)

    #get file name list
    file_list = get_local_folder_files(local_folder_name)
    for name_of_file in file_list:
        upload_file(onedrive_access, id_of_folder, name_of_file)

    #get share link
    #post_sharing_link(onedrive_access, id_of_folder, TO)

#uploading single photo or file
def upload_photo (onedrive_access, id_of_folder, name_of_file, img_label):

    #Upload single file
    #onedrive_access.item(drive='me', id=id_of_folder).children[file_name].upload("./"+ folder_name+ "/" + file_name)

    try:
        onedrive_access.item(drive='me', id=id_of_folder).children[img_label].upload(name_of_file)
        print("Uploading ", name_of_file, "Success")

        print("File ", name_of_file, "Deleted from local system")
        os.remove(name_of_file)

    except OSError:
        pass
    except Exception as e:
        print('upload_file() : exception', str(e))

def setup_onedrive ():
    #login name loginfmt
    #password field passwd
    #Button "SI"
    #https://www.projectoxford.ai/Subscription#

    try:
        #Authenticate Onedrive service
        onedrive_access = get_onedrive_access_token(user_name, password)
        #upload_photo(onedrive_access, local_folder)

    except Exception as e:
        print('Onedrive access failed:', str(e))

    return onedrive_access

def setup_picamera (camera):

    camera.resolution = (2592, 1944)
    #camera.resolution = (1280, 720)
    #camera.led = False
    camera.vflip = True
    camera.hflip = True
    camera.brightness = 40
    # Set a framerate of 1/6fps, then set shutter
    # speed to 1s and ISO to 400 For LOW light photo
    camera.framerate = Fraction(1, 3)
    camera.shutter_speed = 1000000
    #camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2016 Markrish LLc'

    camera.ISO = 800
    #camera.video_stabilization = True
    #camera.exposure_compensation = 0
    camera.exposure_mode = 'off' #'auto'
    camera.meter_mode = 'average'
    #camera.awb_mode = 'auto'

    camera.start_preview()
    #time.sleep(2)


def setup_usbcamera (camera):

    #camera.resolution = (1280, 720)
    #camera.led = False
    #camera.vflip = True
    #camera.hflip = True
    #camera.brightness = 40
    # Set a framerate of 1/6fps, then set shutter
    # speed to 1s and ISO to 400 For LOW light photo
    #camera.framerate = Fraction(1, 3)
    #camera.shutter_speed = 1000000
    #camera.exif_tags['IFD0.Copyright'] = 'Copyright (c) 2016 Markrish LLc'

    #camera.ISO = 800
    #camera.video_stabilization = True
    #camera.exposure_compensation = 0
    #camera.exposure_mode = 'off' #'auto'
    #camera.meter_mode = 'average'
    #camera.awb_mode = 'auto'

    camera.start_preview()
    #time.sleep(2)


def capture (pi_cam, angle, file_name):
    # Set a framerate of 1/6fps, then set shutter
    # speed to 6s and ISO to 800
    pi_cam.framerate = Fraction(1, 6)
    pi_cam.shutter_speed = 6000000
    pi_cam.exposure_mode = 'off'
    pi_cam.iso = 800
    pi_cam.annotate_text = 'Hello world!'

    # Give the camera a good long time to measure AWB
    # (you may wish to use fixed AWB instead)
    time.sleep(10)
    #pi_cam.awb_mode = 'auto'

    file_path = './' + local_folder + '/' + file_name
    pi_cam.capture(file_path)

    #draw text mark on image
    im = Image.open(file_path)
    draw = ImageDraw.Draw(im)

    label = str(datetime.now()) + " Angle " + str(angle * 10)
    draw.text(((im.width - 250), (im.height - 30)), label, font=font)

    im.save(file_path)
    print("Captured:", file_path, label)


def capture_usbcamera (usbcamera, file_name):

    usbcamera.resolution = (1280, 720)
    usbcamera.annotate_text = 'Hello world!'

    # Give the camera a good long time to measure AWB
    # (you may wish to use fixed AWB instead)
    time.sleep(10)

    file_path = './' + local_folder + '/' + file_name
    usbcamera.capture(file_path)

    #draw text mark on image
    im = Image.open(file_path)
    draw = ImageDraw.Draw(im)

    label = str(datetime.now())
    draw.text(((im.width - 250), (im.height - 30)), label, font=font)

    im.save(file_path)
    print("Captured:", file_path, label)

def upload (onedrive_conn, remote_folder_id, file_name):
    #upload captured photo
    file_path = './' + local_folder + '/' + file_name
    upload_photo(onedrive_conn, remote_folder_id, file_path, file_name)



#setup onedrive access
onedrive_conn = setup_onedrive()

# create folder name on remote drive
onedrive_create_folder(onedrive_conn, remote_folder)

#find folder id to upload picture
remote_folder_id = get_remote_folder_index (onedrive_conn, remote_folder)
print("Remote folder id", remote_folder_id)

#USB Camera
usbcam = cv2.VideoCapture(0)
CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS          = 5
CV_CAP_PROP_FRAME_COUNT  = 7

#usbcam = cv2.VideoCapture(0)
#usbcam.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 640)
#usbcam.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, 480)
#usbcam.set(CV_CAP_PROP_FPS, 10)


file_count = 0

try:
    """
    This section will capture video frame from camera, store as jpg
    call function to upload the picture to onedrive
    """
    while(usbcam.isOpened()):
        ret, frame = usbcam.read()
        if ret==True:
            #frame = cv2.flip(frame,0)

            # write the flipped frame
            file_name = "Image_" + str(file_count) + ".jpg"
            file_path = './' + local_folder + '/' + file_name

            cv2.imwrite(file_path, frame)

            upload(onedrive_conn, remote_folder_id, file_name)
            file_count += 1

            #cv2.imshow('frame',frame)
            #print("Photo captured", file_path)
            cv2.waitKey(100)
            time.sleep(num_of_seconds)

            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
        else:
            break
except KeyboardInterrupt:
    pass

# Release everything if job is finished
cap.release()
#cv2.destroyAllWindows()


print("Timelapse Capture completed....")
