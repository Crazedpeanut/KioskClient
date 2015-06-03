#!/usr/bin/env python3

from time import time, sleep
from random import randint
import struct
import os
import queue
import threading
import select
import sys
import socket
import debug as dbug
import simplejson as json

#from gi.repository import Gtk, GObject

#GObject.threads_init()

path = os.path.dirname(__file__)

def cmp(a, b):
    return (a > b) - (a < b)

vlc = [
    '192.168.1.9',
    None,
    None,
]

start_signals = []
start_signals.append(7)

sequence = {}
sequence[0] = [
    ('wait', 1, 0, 0, 7),
    ('led', 1, 8, 0),
    ('output', 1, 7, 0),
    ('pwm', 1, 0, 35),
    ('delay', .5),
    ('pwm', 1, 0, 10),
    ('pwm', 1, 1, 0),
    ('vlc', b'add click.mp3'),
    ('delay', 2),
    ('vlc', b'add money.mp3'),
    ('led', 1, 8, 0xffff00),
    ('delay', 3.5),
    ('led', 1, 8, 0x00ff00),
    ('delay', .5),
    ('led', 1, 8, 0xff0000),
    ('delay', .5),
    ('led', 1, 8, 0x0000ff),
    ('vlc', b'add boom.mp3'),
    ('led', 1, 8, 0),
    ('pwm', 1, 0, 35),
    ('output', 11, 3, 1),
    ('delay', .15),
    ('output', 11, 3, 0),
    ('pwm', 1, 1, 100),
    ('delay', 2),
    ('vlc', b'clear'),
]

class Can:
    frame_fmt = "=IB3x8s"
    frame_size = struct.calcsize(frame_fmt)
    dlc = 8

    def __init__(self, parent, interface):
        self.name = 'can'
        self.parent = parent
        self.interface = interface
        self.s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
        self.s.bind(('can0',))
        
        self.light_bars = [2]
        self.leds_per_bar = 8
        self.saving_sequence = False
        self.playing_sequence = False


    def start(self):
        self.thread = threading.Thread(target = self.run)
        self.thread.name = self.name
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        self.poll = select.poll()
        self.poll.register(self.s, select.POLLIN)
        while 1:
            msg = self.s.recv(100)
            address, dlc, esource, eclass, num, data = struct.unpack("=IIBBH4s", msg) 
            if (address & 0x780) == 0x700:
                self.parent.handle_event(address & 0x7f, esource, eclass, num)
                print('Can RX: address %d %d %d' % (address & 0x7f, eclass, num))
            

    def send(self, can_id, data):
        """send(0x400, b'\x01\x02\x03\x04\x05\x06\x07\x08')"""
        data = data.ljust(8, b'\x00')
        msg = struct.pack(Can.frame_fmt, can_id, Can.dlc, data)
        self.s.send(msg)
    
    def recv(self, ):
        print(s.recv(100))
    
    def flash(self, n):
        send(0x720, b'\x01\x02\x03\x04\x05\x06\x07\x08')
        print(s.recv(100))
    
    def sdo_read(self, ):
        send(0x614, b'\x40\x18\x10\x02\x00\x00\x00\x00')
        print(s.recv(100))
    
    def sdo_write(self, node, data):
        m = struct.pack("=BHBI", 0x2b, 0x2001, 0, n)
        send(0x0600 + node, m)
        #print(s.recv(100))
    
    def led(self, node, led, color):
        m = struct.pack("=BHBI", 0x23, 0x2001, led, color)
        self.send(0x0600 + node, m)
        #print(s.recv(100))
    
    def output(self, node, n, state):
        m = struct.pack("=BHBB", 0x2f, 0x2002, n, state)
        self.send(0x0600 + node, m)
        #print(s.recv(100))
    
    def pwm(self, node, n, state):
        m = struct.pack("=BHBB", 0x2f, 0x2003, n, state)
        self.send(0x0600 + node, m)
        #print(s.recv(100))
    
    def config(self, node, n, state):
        m = struct.pack("=BHBB", 0x2f, 0x2004, n, state)
        send(0x0600 + node, m)
        #print(s.recv(100))
    
    
    def set_color_grid_pixel_hex(self, x, y, color):
        if x > -1 and x < 255 and y > -1 and y < 255:
            self.led(self.light_bars[x], y, color)
    
    '''
    def set_color_grid_pixel(self, x, y, r, g, b):
        if(x < 0 or y < 0):
            return
        try:
            color = self.rgb_to_hex((r, g, b))
            self.led(self.light_bars[y], x, color)
        except Exception as e:
            dbug.debug(str(e))
            
    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb
    '''
            
            
    
    def sequence(self, t, s):
        while 1:
            for n in range(0, 100, s):
                print(n)
                pwm(1, 0, n)
                sleep(t)
                pwm(1, 1, n)
                sleep(t)
                output(1, 7, (n >> 3) & 1)
                output(2, 7, (n >> 3) & 1)
                output(3, 7, (n >> 3) & 1)
                output(4, 7, (n >> 3) & 1)
                output(5, 7, (n >> 3) & 1)
                output(6, 7, (n >> 3) & 1)
                output(7, 7, (n >> 3) & 1)
                if (n >> 2) & 1:
                    led(1, 8, 0x00ff00)
                    led(2, 8, 0xffff00)
                else:
                    led(1, 8, 0x000000)
                    led(2, 8, 0x0000ff)
    
    
    def cycle(self, nodes, delay):
        while 1:
            for node in nodes:
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                color = r << 16 | g << 8 | b
                led(node, randint(0, 7), color)
                sleep(delay)
    
    
    def color(self, r, g, b):
        data = struct.pack('>BBB', r, g, b)
        send(0x410, data)
    
    def wait_event(self):
        while 1:
            msg = s.recv(100)
            gizmo, dlc, esource, eclass, num, data = struct.unpack("=IIBBH4s", msg) 
    
            print('Gizmo %d: %s button %d' % (gizmo & 0x7f, ('press', 'release')[eclass], num))
    
    def rampup(self, node, x, t):
        for n in range(0,255):
            led(node, x, n<<16 | n<<8 | n)
            sleep(t)
    
    def rampdown(self, node, x, t):
        for n in range(255,0,-1):
            led(node, x, n<<16 | n<<8 | n)
            sleep(t)
    
    def waveup(self, node, t, c):
        for n in range(0,8):
            led(node, n, c)
            sleep(t)
            led(node, n, 0)
    
    def wavedown(self, node, t, c):
        for n in range(8,0, -1):
            led(node, n-1, c)
            sleep(t)
            led(node, n-1, 0)
    
    def colorwave(self, node, t, r, g, b):
        for n in range(0,r):
            waveup(node, t, n<<16 | 0<<8 | 0)
        for n in range(0,g):
            waveup(node, t, r<<16 | n<<8 | 0)
        for n in range(0,b):
            waveup(node, t, r<<16 | g<<8 | n)
            
    def update_lights(self, data):
        for led in data['leds']:
            set_color_grid_pixel_hex(led["x"], led["y"], led["color"])
            sleep(0.002)
    
    def load_sequence(self, data):
        
        dbug.debug("Saving sequence")
    
        while(self.saving_sequence == True):
            sleep(0.5)
    
        try:
            os.remove("sequence"+sequence_num+".sequence")
        except Exception as e:
            dbug.debug(str(e))
    
        try:
            self.saving_sequence = True
            self.sequence_num = data["sequence_num"]
            dbug.debug("Saving data")
            
            f = open("sequence"+sequence_num+".sequence", "w")
            f.write(str(data))
            f.close() 
        except Exception as e:
            dbug.debug(str(e))
        finally:
            self.saving_sequence = False


    def play_sequence(self, data):
    
        dbug.debug("About to play sequence..")
        while(self.playing_sequence == True):
            sleep(0.5)
    
        try:
            self.playing_sequence = True
            f = open("sequence" + data["sequence_num"] + ".sequence", "r")
            data = f.read()
            f.close()
            dbug.debug(data)
            dbug.debug("playing sequence...\n: " + data)
            data = data.replace("\'", "\"")
            data = json.loads(data) 
            for x in range(int(data["loop"])):
                for frame in data['frames']:
                    for led in frame['leds']:
                        color = int(led["color"].lower(), 16)
                        self.set_color_grid_pixel_hex(int(led["x"]), int(led["y"]), color)
                        sleep(0.002)
                    sleep(1/int(data["fps"]))
    
            self.reset_leds()
            
        except Exception as e:
            dbug.debug(str(e))
        finally:
            self.playing_sequence = False
    
    def blank_lightbars(self, data):
    
        while(self.playing_sequence == True):
            sleep(0.5)
        try:
            self.playing_sequence = True
            reset_leds()
        except Exception as e:
            dbug.debug(str(e))
        finally:
            self.playing_sequence = False
            
    def reset_leds(self):
        for bar in self.light_bars:
            for l in range(self.leds_per_bar):
                self.led(bar, l,0x000000)
                print("LED: (%d, %d) to 0x000000" % (bar, l))
                sleep(0.0001) 
    



class Unit:

    def __init__(self, name, parent, start_signal, sequence):
        self.name = name
        self.parent = parent
        self.start_signal = start_signal
        self.sequence = sequence
        self.state = 0
        self.watch = None
        self.queue = queue.PriorityQueue(1000)
        self.lock = threading.Lock()
        self.thread = None
        self.poll = None
        self.stopped = 0
        self.step = 0
        self.wait = 1
        self.msg = (0, 0, 0, 0)

    def start(self):
        self.thread = threading.Thread(target = self.run)
        self.thread.name = self.name
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        #self.poll = select.poll()
        #self.poll.register(self.sp, select.POLLIN)

        self.parent.register(self, self.start_signal)

        #self.textbuffer.create_tag("highlighted",  background = "red")
        #start = self.textbuffer.get_iter_at_line(0)
        #end = self.textbuffer.get_iter_at_line(1)

        while(1): 

            if(cmp(self.msg, (0,0,0,0))):
               print("Button %d pressed" % self.msg[3]) 
               
            sleep(1)
            


class CanOperations:
    def __init__(self):
        self.event_list = []

        self.can = Can(self, 'can0')
        self.can.start()
        
        # TEST
        self.can.reset_leds()
        

        #self.window.show_all()
        #self.notebook.set_current_page(0)

    def register(self, delegate):
        self.event_list.append(delegate)
        print('Register delegate')

    def handle_event(self, address, esource, eclass, num):
        print('received event: %d %d %d %d' % (address, esource, eclass, num))
        for e in self.event_list:
            e(address, esource, eclass, num)

if __name__ == "__main__":
    main = CanOperations()
    #Gtk.main()
    while 1:
        sleep(1)
        print('.')



