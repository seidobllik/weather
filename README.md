# weather
Get a weather report printed in the command line! Who needs to look out a window?

## Table of contents
* [General Info](#general-info)
* [Technologies](#technologies)
* [Features](#features)

## General Info
Simply open the command line, navigate to the directory in which this script is stored, and run `python weather.py` to get a weather report printed directly to your command line!

    Getting coordinates...
    Getting weather data...
    --------------------------------------------------------------------------------
    Somewhere, USA 10101 [08 PM, Oct 09, 2021]
    68°F
    Clear: Total cloud cover less than 20%
    Wind 0.3-3.4m/s (light), S
    R.H. 44%
    Precip. None None
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Somewhere, USA 10101 [11 PM, Oct 09, 2021]
    68°F
    Clear: Total cloud cover less than 20%
    Wind 0.3-3.4m/s (light), S
    R.H. 45%
    Precip. None None
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------
    Somewhere, USA 10101 [02 AM, Oct 10, 2021]
    64°F
    Clear: Total cloud cover less than 20%
    Wind 0.3-3.4m/s (light), S
    R.H. 44%
    Precip. None None
    --------------------------------------------------------------------------------
    Press enter to close...

## Technologies
This project was developed and tested using **Python 3.9.2** running on **Windows 10**. It requires an internet connection, and uses [https://ipinfo.io](https://ipinfo.io) and [http://www.7timer.info](http://www.7timer.info) for IP-based location info and coordinate-based weather info. 

## Features
By default, you are provided with one weather report accurate to within a three hour window from your local time. An optional argument can be passed into the script via the command line to provide up to 64 weather reports (8 days worth), in three hour increments. Typing `python weather.py 10` for instance will print ten reports.

Additionally, when prompted with `Press enter to close...`, you can type 'view' and then hit `enter` to open *[http://www.7timer.info](http://www.7timer.info)*'s graphical report for your location.
