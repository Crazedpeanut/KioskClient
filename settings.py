'''
Author: John Kendall
Date: 18/12/14

Description: Global application settings
'''


'''
General
'''
STORED_REQUESTS_FILE = "data.json"
LOCAL_DB = "data.db"
HEARTBEAT_WAIT = 60
'''

Web Server Connection
'''
WEB_SERVER_HOST = "192.168.2.5"
WEB_SERVER_PORT = 8000
ENCODING = "utf-8"


HTTP_TIMEOUT = 5
'''
Debug
'''
DEBUGGING = True
DEBUGGING_MODE = 1
PRINT_DATETIME = True
PRINT_FRAME_INFO = True

'''
BARCODE SCANNER
'''
USB_DEVICE = '/dev/hidraw0'
SERIAL_DEVICE = '/dev/ttyO2'
SERIAL_DEVICE_BAUD = 9600

'''
DIFFICULTY SETTINGS
'''
DIFFICULTY_DEFAULT = "0"
DIFFICULTY_1 = "1"
DIFFICULTY_2 = "3"
DIFFICULTY_3 = "5"
