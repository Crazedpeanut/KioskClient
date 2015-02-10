#!/usr/bin/python3

'''
Author: John Kendall
Date: 18/12/14

Description: Main script for the kiosk application. Functions called from the main loop are ran in separate threads
'''
#TODO - Don't add full http request to data file after failed connection

import sqlite3 as lite
import kiosk_http as http
import time, datetime
import simplejson as json
import read_from_hidraw as bcode_listen
import socket
import commands
import threading
import debug as dbug
import settings
import queue
import datetime

HOST = settings.WEB_SERVER_HOST
PORT = settings.WEB_SERVER_PORT
METHOD = "POST"
TEST_RESOURCE = "/barcode/test.php"

#Resource must end with slash to work with Andrews' Django App
ADD_CHECKIN = "/kiosk/user_checkin/" 
ADD_HEARTBEAT = "/kiosk/heartbeat_checkin/"
ADD_CHECKIN_BATCH = "/kiosk/checkin_batch/"

PAUSE_BETWEEN_HEARBEAT = 60
DATA_FILE = settings.STORED_REQUESTS_FILE
MAINLOOP_PAUSE = 0.001
LOCALDB = settings.LOCAL_DB

LAST_SERVER_CONTACT = ""

data_file_operation_queue = queue.Queue()

class thread_worker(threading.Thread):
    def __init__(self, delegate, delegate_params):
        threading.Thread.__init__(self)
        self.delegate = delegate
        self.delegate_params = delegate_params

    def run(self):
        if(self.delegate_params != None):
            self.delegate(self.delegate_params)
        else:
            self.delegate()

def create_check_in(barcode):	
    kiosk = socket.gethostname()
    timestamp = str(datetime.datetime.now())
    
    return {"checkin":{"barcode": barcode, "address": kiosk, "timestamp":timestamp}}

def file_operation_queue_add(delegate, params):
    queue_node = {"delegate" : delegate, "params":params}
    data_file_operation_queue.put(queue_node)
    dbug.debug("Added file operation to queue")

def file_operation_queue_perform_operations():
    while(True):
        if(data_file_operation_queue.qsize()):
            node = data_file_operation_queue.get()
            operation = node["delegate"]
            params = node["params"]
            operation(params)
        time.sleep(0.2)

def record_request(params):
    request = str(params['request']).replace('\'', '\"')
    
    try:
        dbug.debug("Recording request for retransmission at a later time..")
        
        db_conn = lite.connect(LOCALDB)
        db_cur = db_conn.cursor()

        request = json.loads(request)
        
        if('heartbeat' in request):
            db_cur.execute("INSERT INTO heartbeats (host, ip) VALUES ('%s', '%s')" % (request['heartbeat']['host'], request['heartbeat']['ip']))
            dbug.debug("Heartbeat stored.")
            db_conn.commit()
        elif('checkin' in request):
            db_cur.execute("INSERT INTO check_ins (barcode, host, timestamp) VALUES ('%s', '%s', '%s')" % (request['checkin']['barcode'],request['checkin']['address'], request['checkin']['timestamp']))
            dbug.debug("Check in stored.")
            db_conn.commit()

    except Exception as e:
        dbug.debug("Recording request failed: " + str(e))

def create_heartbeat():
    timestamp = str(datetime.datetime.now())
    kiosk = socket.gethostname()
    ip = socket.gethostbyname(kiosk)
    
    heartbeat = {"heartbeat":{"timestamp": timestamp, "host": kiosk, "ip": ip}}
    return heartbeat

def send_heartbeat():
    heartbeat = create_heartbeat()
    heartbeat_data = heartbeat["heartbeat"]
    
    result = http.http_request_2(HOST, PORT, METHOD, ADD_HEARTBEAT, heartbeat_data)
    
    if(result is not None):
        http_result_handler(result)
    else:
        request = str(heartbeat)
        params = {"request": request}
        file_operation_queue_add(record_request, params) 
        
def send_checkin(checkin):
    check_in_data = checkin["checkin"]
    
    result = http.http_request_2(HOST, PORT, METHOD, ADD_CHECKIN, check_in_data)
    
    if(result is not None):
        http_result_handler(result)
    else:
        request = str(checkin)
        params = {"request": request}
        file_operation_queue_add(record_request, params) 

def send_stored_data():
     
    db_conn = lite.connect(LOCALDB)
    db_cur = db_conn.cursor()

    db_cur.execute("SELECT * from check_ins")
    rows = db_cur.fetchall()
   
    checkins = []

    for row in rows:
        barcode = row[1]
        host = row[2]
        timestamp = row[3]
        checkins.append({'barcode':barcode, 'address':host, 'timestamp':timestamp})

    f = open("tmp.txt.gz", "wb")
    f.write(bytes(str({'checkins':checkins}), 'UTF-8'))
    
    files = {'files': open('tmp.txt.gz', "rb")}
    
    http.send_file(HOST, PORT, ADD_CHECKIN_BATCH,files)
    
    '''
        check_in = create_check_in(row[1])
        
        create_thread_worker(send_checkin, check_in)
        query = "DELETE FROM check_ins WHERE id = %d" % (row[0])
        db_cur.execute(query)
        db_conn.commit()
    '''
     
def http_result_handler(result):
    command_list = {"play_sequence":commands.play_sequence,"test": commands.test_command, "loadsequence":commands.load_sequence, "printdata":commands.print_data, "updateleds":commands.update_lights, "blanklightars":commands.blank_lightbars}

    LAST_SERVER_CONTACT = datetime.datetime.now()

    send_stored_data()

    if(len(result) < 1):
        return

    try:
        json_data = json.loads(result)
    
        serv_commands = json_data['commands']

        for comm in serv_commands:
            if(comm['command'] in command_list):
                command_list[comm['command']](comm)
    except Exception as e:
        dbug.debug("response from webserver probably isn't JSON format.. " + str(e))
        
def bcode_handler(bcode):
    check_in = create_check_in(bcode)
    dbug.debug('adding thread worker..')
    create_thread_worker(send_checkin, check_in)

def create_thread_worker(delegate, delegate_params):
    new_thread = thread_worker(delegate, delegate_params)
    new_thread.start()
    dbug.debug("Creating new thread. Count: " + str(len(threading.enumerate())))
    return new_thread

def ticker(params):
    time_in_seconds = params["time"]
    delegate = params["delegate"]
    delegate_params = params["delegate_params"]

    while(True):
        time.sleep(time_in_seconds)
        
        if(delegate_params is not None):
            delegate(delegate_params)
        else:
            delegate()

def main():
    bcode_listen.start_listening(bcode_handler)
    
    ticker_params = {"time":PAUSE_BETWEEN_HEARBEAT, "delegate": send_heartbeat, "delegate_params": None}
    create_thread_worker(ticker, ticker_params)	
    
    create_thread_worker(file_operation_queue_perform_operations, None)

    while(True):    	  
        time.sleep(MAINLOOP_PAUSE)

if __name__ == "__main__":
	main()	
