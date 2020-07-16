# EurosportOn

This is a fork of the Eurosport2 addon created by [James Muscat](https://github.com/jamesremuscat/plugin.video.eurosport2) which itself was derived from the original Eurosport Player addon by [JinRonin](https://github.com/JinRonin/plugin.video.eurosportplayer)


## Authentication

The authentication is still using James Muscat's method of copying the value of the session cookie 'st' into the settings.xml file (see notes below).

As per the previous versions, you must have a valid account for Eurosport Player for this addon to work

## Changes

- The schedule has been broken down into the following categories:

  - On earlier - Programmes that were shown earlier in the day and are still available.
  - On now - Programmes that are being shown on Eurosport 1 and 2 right now.
  - On later - Programmes coming up on Eurosport 1 and 2 later in the day.  The schedule time uses your
systems offset to UTC so make sure this is set up correctly, otherwise all times will be shown at UTC +0:00 
  - On demand - This will bring up a list of sports on Eurosport.  Selecting one of these will display a list of available videos.
Not all sports will have videos available.

## 'st' cookie

## License

This addon is licensed under the MIT licence - see `LICENSE` for details.
