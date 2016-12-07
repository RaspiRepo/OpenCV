##Summary:

Here is one of my fun projects with Raspberry PI using Python with OneDrive SDK. I do not consider myself as an export Python programmer.
I written this program to setup surveillance application, taking timelapse picture using Raspberry PI and Camera, to take picture, record video and upload to Microsoft Cloud OneDrive using Resetful API.

To access Onedrive storage space need access token.  To get Access token a  user has to authenticate manually on the web browser(a GUI web browser needed). Most of the people use Raspberry PI as headless node i.e. with out monitor/keyboard attached with it plus running as console mode.

To bypass this user intercation with Raspberry PI web browser, I used Selenium package which well suited for simulating/automating websites (scripts to invoke/click/fill information on the  website).

Another issue is, almost every websites require Javascript support.  So PhantomJS webdriver came into handy.  This package allows to render HTML/Javascript/CSS in virtual display i.e in MEMORY.  We can find text box names to fill and buttons to click on any website. 
Using all of these pacakge and using script virtually a raspberry PI can Authenticate itself WITHOUT any external user interaction or click buttons.

#Packages Needed
 Onedrivesdk - https://github.com/OneDrive/onedrive-sdk-python
 
 selenium    - http://www.seleniumhq.org/projects/webdriver/
 
 PhantomJS   - Scriptable Headless WebKit for Python - https://github.com/ariya/phantomjs/
  
 openCV      - To capture video or Image from USB or PICAMERA
 
 #One Drive App Registration:
https://apps.dev.microsoft.com/Landing?ru=https%3a%2f%2fapps.dev.microsoft.com%2f

Get Application Secrets  which is assigned to client_secret and Client Id (App Id) as client_id_str = "00000000xxxxxxx".

OneDrive API Reference  https://dev.onedrive.com/app-registration.htm

#Update needed in the code:
  1. Copy & Paste Authentication details from Onedrive developer console of your app/project.
  2. Update email address and passwword which is defined in top of the script.
  3. Modify local, remote folder name to be used.
  4. Modify Name of the file to be created.
  5. Connect USB webcamera to PI
  
#What this script can do

This program setup USB camera with resolution 640x480 (changable but depends on camera supports). PICamera supports higher resolution to tkae photo. Get access token from by OneDrive and create folder. Capture Video frame using openCV and store as jpeg photo into local folder (again local folder name can be changed) and upload the photo to Onedrive. 
Note : Every 10 seconds (can be changed) a jpeg picture captured and stored in local folder and uploaded to remote folder (onedrive).

Addional functions written to creating sharing URL and send to Email address.  Using this URL you can view the photo online.

## Onedrive provide 15GB free space!
 
  
