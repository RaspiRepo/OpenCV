 # Summary:

This is one of my fun project that was written for Raspberry PI using OpenCV Python to access OneDrive. This is a miniature version of surveillance system, which takes timelapse photos using Raspberry PI and Camera, and/ or record video and upload it to Microsoft Cloud OneDrive using REST API.

Accessing Onedrive storage space needs access token.  In order to get the token users has to manually authenticate via the web browser which will not be possible if you are using your Raspberry PI as a headless node (i.e. with out monitor/keyboard attached), running in console mode. There are two issues that I've tackled with the below approach:

To bypass this issue of user intercation with web browser via Raspberry PI, I've used the "Selenium" package which is well suited for simulating/automating GET/POST on any web browsers. (scripts to invoke/click/fill information on the  website).

Another issue is, the interface required for filling text box and button clicks on HTML Pages. I've used phantomJS webdriver to achieve this.  This package allows the user to render HTML/Javascript/CSS via virtual display i.e in MEMORY which will render the html tags.

Using these pacakges Raspberry PI can virtually authenticate itself without any external user interaction or clicking of buttons.

# Packages Needed
 Onedrivesdk - https://github.com/OneDrive/onedrive-sdk-python
 
 selenium    - http://www.seleniumhq.org/projects/webdriver/
 
 PhantomJS   - Scriptable Headless WebKit for Python - https://github.com/ariya/phantomjs/
  
 openCV      - To capture video or Image from USB or PICAMERA
 
 # One Drive App Registration:
https://apps.dev.microsoft.com/Landing?ru=https%3a%2f%2fapps.dev.microsoft.com%2f

Get Application Secrets  which is assigned to client_secret and Client Id (App Id) as client_id_str = "00000000xxxxxxx".

OneDrive API Reference  https://dev.onedrive.com/app-registration.htm

# Update needed in the code:
  1. Copy & Paste Authentication details from the Onedrive developer console.
  2. Update email address and passwword variables in the script.
  3. Modify local, remote folder variable names to be used.
  4. Modify Name of the file to be created.
  5. Connect USB webcamera to PI.
  
# What this script can do

This program sets up USB camera with resolution 640x480 (changable but depends on camera configurations). For example, PICamera supports higher resolution for taking photos. 
Get access token from OneDrive API and creates the corresponding folder name given in the script in the cloud.
Capture Video frame using openCV and store it as .jpeg format into the local folder name given and then will upload it as a photo in to Onedrive. 

There is also addional functionality added for creating and sharing  the URL, which can be shared with the speicified email address.  Using this URL they can view the photos online.
 
  
