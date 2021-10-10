'''
Command line app which displays the weather based on the IP address location.

Default weather info covers the most recent data within 3 hours of local time.
An optional argument can be passed in via the command line to print out
additional data.

    Example:
        python weather.py 5
            -> prints five data data sets, the first of which will be within
               three hours of local time.


weather api reference: http://www.7timer.info/doc.php?lang=en
location info obtained using: https://ipinfo.io/json
'''

import urllib.request
import json
import ssl
import webbrowser
import time
import sys
import os

WEATHER_DICT = {
    'cloudcover': {
        1: '0%-6%',
        2: '6%-19%',
        3: '19%-31%',
        4: '31%-44%',
        5: '44%-56%',
        6: '56%-69%',
        7: '69%-81%',
        8: '81%-94%',
        9: '94%-100%',
    },
    'lifted_index': {
        -10: 'Below -7',
        -6: '-7 to -5',
        -4: '-5 to -3',
        -1: '-3 to 0',
        2: '0 to 4',
        6: '4 to 8',
        10: '8 to 11',
        15: 'Over 11',
    },
    'prec_amount': {
        0: 'None',
        1: '0-0.25mm/hr',
        2: '0.25-1mm/hr',
        3: '1-4mm/hr',
        4: '4-10mm/hr',
        5: '10-16mm/hr',
        6: '16-30mm/hr',
        7: '30-50mm/hr',
        8: '50-75mm/hr',
        9: 'Over 75mm/hr',
    },
    'prec_type': {
        'none': 'None',
        'snow': 'Snow',
        'rain': 'Rain',
        'frzr': 'Freezing Rain',
        'icep': 'Ice Pellets',
    },
    'rh2m': {},
    'temp2m': {},
    'timepoint': {},
    'weather': {
        'clearday':         'Clear: Total cloud cover less than 20%',
        'clearnight':       'Clear: Total cloud cover less than 20%',
        'pcloudyday':       'Partly Cloudy: Total cloud cover between 20%-60%',
        'pcloudynight':     'Partly Cloudy: Total cloud cover between 20%-60%',
        'mcloudyday':       'Cloudy: Total cloud cover between 60%-80%',
        'mcloudynight':     'Cloudy: Total cloud cover between 60%-80%',
        'cloudyday':        'Very Cloudy: Total cloud cover over over 80%',
        'cloudynight':      'Very Cloudy: Total cloud cover over over 80%',
        'humidday':         'Foggy: Relative humidity over 90% with total cloud cover less than 60%',
        'humidnight':       'Foggy: Relative humidity over 90% with total cloud cover less than 60%',
        'lightrainday':     'Light Rain: Precipitation rate less than 4mm/hr with total cloud cover more than 80%',
        'lightrainnight':   'Light Rain: Precipitation rate less than 4mm/hr with total cloud cover more than 80%',
        'oshowerday':       'Occasional Showers: Precipitation rate less than 4mm/hr with cloud cover between 60%-80%',
        'oshowernight':     'Occasional Showers: Precipitation rate less than 4mm/hr with cloud cover between 60%-80%',
        'ishowerday':       'Isolated showers: Precipitation rate less than 4mm/hr less than 60%',
        'ishowernight':     'Isolated showers: Precipitation rate less than 4mm/hr less than 60%',
        'lightsnowday':     'Light Snow: Precipitation rate less than 4mm/hr',
        'lightsnownight':   'Light Snow: Precipitation rate less than 4mm/hr',
        'rainday':          'Rain: Precipitation rate over 4mm/hr',
        'rainnight':        'Rain: Precipitation rate over 4mm/hr',
        'snowday':          'Snow: Precipitation rate over 4mm/hr',
        'snownight':        'Snow: Precipitation rate over 4mm/hr',
        'rainsnowday':      'Mixed: Precipitation type to be ice pellets or freezing rain',
        'rainsnownight':    'Mixed: Precipitation type to be ice pellets or freezing rain',
        'tsday': 'Thunderstorm Possible: Lifted Index less than -5 with precipitation rate below 4mm/hr',
        'tsnight': 'Thunderstorm Possible: Lifted Index less than -5 with precipitation rate below 4mm/hr',
        'tsrainday': 'Thunderstorm: Lifted Index less than -5 with precipitation rate over 4mm/hr',
        'tsrainnight': 'Thunderstorm: Lifted Index less than -5 with precipitation rate over 4mm/hr',
    },
    'wind10m': {
        1: 'Below 0.3m/s (calm)',
        2: '0.3-3.4m/s (light)',
        3: '3.4-8.0m/s (moderate)',
        4: '8.0-10.8m/s (fresh)',
        5: '10.8-17.2m/s (strong)',
        6: '17.2-24.5m/s (gale)',
        7: '24.5-32.6m/s (storm)',
        8: 'Over 32.6m/s (hurricane)',
    }
}

def get_coordinates():
    '''
    Get coordinates based on IP address. 
    
        args:
            None
        
        returns:
            Dictionary with latitude, longitude, and location (city, state zip).
                { 
                    'lat': float, 
                    'lon': float, 
                    'loc': str 
                }
    '''
    IP_INFO_URL = 'https://ipinfo.io/json'
    print('Getting coordinates...')
    try:
        response = urllib.request.urlopen(IP_INFO_URL)
    except:
        raise
    data = json.load(response)
    latitude, longitude = data['loc'].split(',')
    location = data['city'] + ', ' + data['region'] + ' ' + data['postal']
    return {'lat': latitude, 'lon': longitude, 'loc': location}

def get_weather(lat, lon):
    '''
    Get weather info based on latidude and longitude.

        args:
            lat (float): 
            lon (float): 

        returns:
            Dict containing the weather conditions for the next 8 days in 3 hour intervals.
                {
                    'product': str,
                    'init': str,                                        # YYYYMMDDHH.
                    'dataseries': [{
                        'timepoint': int,                               # Hours past 'init'.
                        'cloudcover': int,
                        'lifted_index': int,
                        'prec_type': str,
                        'prec_amount': int,
                        'temp2m': int,
                        'rh2m': str,
                        'wind10m': { 'direction': str, 'speed': int },
                        'weather': str,
                        },
                        {...},
                    ],
                }
    '''
    ssl._create_default_https_context = ssl._create_unverified_context  # Used to fix urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired.
    api_call = f'https://www.7timer.info/bin/civil.php?lon={lon}&lat={lat}&product=civil&ac=0&unit=british&output=json&tzshift=0'
    user_link = f'https://www.7timer.info/bin/civil.php?lon={lon}&lat={lat}&product=civil&ac=0&unit=british&output=internal&tzshift=0'
    print('Getting weather data...')
    try:
        response = urllib.request.urlopen(api_call)
    except:
        raise
    data = json.load(response)
    data['user_link'] = user_link
    return data

def display_weather(data, timepoints=1):
    '''
    Print the weather info to the console. 

        args:
            data (dict): Dictionary returned from get_weather(). Must add data['loc'], which is provided by get_coordinates().
            timepoints (int): The number of data points to print. [Default is 1]
        
        returns:
            None
    '''
    CONSOLE_WIDTH = 80
    CURRENT_TIME = time.localtime()
    DATA_INIT_TIME = time.strptime(data['init'][:-2] + str(int(data['init'][-2:]) + int(int(time.strftime('%z', CURRENT_TIME)) / 100)).rjust(2, '0'), '%Y%m%d%H')  # Apply
    DIFFERENCE = int((time.mktime(CURRENT_TIME) - time.mktime(DATA_INIT_TIME)) / 60 / 60)  # Difference in hours.
    INDEX = int(DIFFERENCE / 3) - 1  # Each dataseries is 3 hrs apart, index 0 is the DATA_INIT_TIME + 3 hrs.
    try:
        for point in range(timepoints):
            timepoint_data = data['dataseries'][point + INDEX]
            for key, val in timepoint_data.items():
                try:
                    timepoint_data[key] = WEATHER_DICT[key][val]
                except Exception as e:
                    if key == 'wind10m':
                        timepoint_data[key] = f'{ WEATHER_DICT[key][val["speed"]]}, {val["direction"]}'
                    else:
                        pass
                    continue
            print('-' * CONSOLE_WIDTH)
            timestamp = time.strftime('%I %p, %h %d, %Y', time.localtime(time.mktime(DATA_INIT_TIME) + (timepoint_data['timepoint'] * 60 * 60)))
            print(f'{data["loc"]} [{timestamp}]'.ljust(CONSOLE_WIDTH))
            print(f'{timepoint_data["temp2m"]}\u00b0F')
            print(timepoint_data["weather"])
            print(f'Wind {timepoint_data["wind10m"]}')
            print(f'R.H. {timepoint_data["rh2m"]}')
            print(f'Precip. {timepoint_data["prec_type"]} {timepoint_data["prec_amount"]}')
            print('-' * CONSOLE_WIDTH)
    except IndexError:
        pass

if __name__ == '__main__':
    os.system('mode con: cols=80 lines=30')
    coords = get_coordinates()
    weather_data = get_weather(coords['lat'], coords['lon'])
    weather_data['loc'] = coords['loc']
    timepoints = 1
    # Check if optional timepoints argument was passed through the command line.
    if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
        timepoints = int(sys.argv[1])
    display_weather(weather_data, timepoints)
    user_input = input('Press enter to close...\n')
    # Easter egg? If the user types 'view' before pressing enter, a webpage will open to the API's graphical output.
    if user_input == 'view':
        webbrowser.open_new_tab(weather_data['user_link'])
