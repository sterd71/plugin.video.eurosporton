# EurosportOn

This is built on the Eurosport2 addon created by [James Muscat](https://github.com/jamesremuscat/plugin.video.eurosport2) which itself was derived from the original Eurosport Player addon by [JinRonin](https://github.com/JinRonin/plugin.video.eurosportplayer)


## Inputstream adaptive

A few people have found that streams no longer play when they are using inputstream.adaptive on Kodi 18.7 & Kodi 18.8.

Disabling inputstream.adaptive, allowed the stream to play correctly.

A new playback engine option has been added to settings.  It will default to inputstream.adaptive, you can change it to use
ffmpeg or direct (on my development machine direct used ffmpeg).

If you have problems playing streams, try one of the other options.

## Authentication

The authentication is still using James Muscat's method of copying the value of the session cookie 'st' into the settings.xml file (see notes below).

As per the previous versions, you must have a valid account for Eurosport Player for this addon to work

## Installation

- Download the zip file
- Start Kodi
- Select addons
- Select install from zip file
- Locate the downloaded zip file and click OK to install

## Changes

A main menu is now presented that breaks down the schedule into different categories.

![Alt text](resources/media/MainMenu.jpg?raw=true "Main menu")

  - On earlier - Programmes that were shown earlier in the day and are still available.
  - On now - Programmes that are being broadcast on Eurosport 1 and 2.

  ![Alt text](resources/media/OnNow.jpg?raw=true "On now")
    
  - On later - Programmes coming up on Eurosport 1 and 2 later in the day.  The schedule time uses your
system locale so make sure this is set up correctly, otherwise all times will be shown at UTC +0:00

![Alt text](resources/media/OnLater.jpg?raw=true "On now")
   
  - On demand - This will bring up a list of sports on Eurosport.  Selecting one of these will display a list of available videos.
Not all sports may have videos available.

![Alt text](resources/media/OnDemand.jpg?raw=true "Available sports")

![Alt text](resources/media/OnDemandVideos.jpg?raw=true "On demand videos")


## settings.xml

There are two ways to get the login token:

### Method 1
If you have already installed and used James Muscat's Eurosport2 addon then you can re-use your existing settings.xml file.

After installing EurosportOn, enter the settings panel and enter a dummy token e.g. 123 and click 'OK'.

Then copy settings.xml from your userdata folder `userdata/addon_data/plugin.video.eurosport2` to `userdata/addon_data/plugin.video.eurosporton`

Userdata is located at:  
Linux ~/.kodi/userdata  
Windows %APPDATA\Kodi\userdata  


### Method 2

Obtain the "st" cookie value from your browser.

- Chrome:
    - Log into Eurosport player
    - Press F12 to access developer tools
    - Select Application
    - On the left hand side of the popup select Cookies in the Storage section.
    - Locate the 'st' cookie and copy it's value.

- Firefox:
    - Log into Eurosport player
    - Press F12 to access developer tools
    - Select Storage (you may need to click on '>>' to find it.
    - Under 'Cookies', locate the 'st' cookie and copy it's value.

- Opera:
    - Log into Eurosport player
    - Press Ctrl+Shift+I to access developer tools
    - Select Application (you may need to click on '>>' to find it.
    - Under 'Cookies', locate the 'st' cookie and copy it's value.

## License

This addon is licensed under the MIT licence - see [LICENSE](LICENSE) for details.
