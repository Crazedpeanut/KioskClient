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

#from gi.repository import Gtk, GObject

#GObject.threads_init()

path = os.path.dirname(__file__)

vlc = [
    '192.168.1.9',
    None,
    None,
]

start_signals = [
    1,
    2,
    3,
]

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

sequence[1] = [
    ('wait', 1, 0, 0, 7),
    ('delay', 0.5),
    ('vlc', b'stop'),
    ('vlc', b'add /home/mcruse/Wildlife.wmv'),
    ('delay', 5),
    ('output', 12 , 0, 1),
    ('led', 2, 8, 0xff0000),
    ('delay', 1),
    ('led', 2, 8, 0x00ff00),
    ('delay', 1),
    ('led', 2, 8, 0x0000ff),
    ('delay', 1),
    ('led', 2, 8, 0x000000),
    ('delay', .1),
    ('led', 2, 8, 0xffffff),
    ('delay', .1),
    ('led', 2, 8, 0x000000),
    ('delay', .1),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('delay', .05),
    ('led', 2, 8, 0xffffff),
    ('delay', .05),
    ('led', 2, 8, 0x000000),
    ('output', 12 , 0, 0),
    ('vlc', b'clear'),
]

sequence[2] = [
    ('wait', 1, 0, 0, 7),
    ('output', 13, 0, 1),
    ('delay', 5),
    ('vlc', b'add boom.mp3'),
    ('pwm', 3, 0, 100),
    ('delay', 2.26),
    ('pwm', 3, 0, 0),
    ('delay', 2.2),
    ('pwm', 3, 0, 100),
    ('delay', 2.25),
    ('pwm', 3, 0, 0),
    ('delay', 2.2),
    ('pwm', 3, 0, 50),
    ('led', 3, 8, 0xffff00),
    ('delay', 2),
    ('vlc', b'clear'),
    ('output', 13, 0, 0),
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
    



class Unit:
    vlc = None

    def __init__(self, name, parent, start_signal, sequence, vlc_host=None):
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

        if (vlc_host != None) and (Unit.vlc == None):
            print('Opening VLC connection to %s' % vlc_host)
            Unit.vlc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Unit.vlc.connect((vlc_host, 4212))
        print(self.name, Unit.vlc)


    def start(self):
        self.thread = threading.Thread(target = self.run)
        self.thread.name = self.name
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        #self.poll = select.poll()
        #self.poll.register(self.sp, select.POLLIN)

        if self.vlc != None:
            sleep(1)
            Unit.vlc.send(b'vlc\r\n')
            #self.vlc.send(b'add /home/mcruse/Music/Bobby McFerrin/Beyond Words/Kalimba Suite.flac\r\n')
            #self.vlc.send(b'add /home/mcruse/black.png\r\n')
            Unit.vlc.send(b'add /home/mcruse/Wildlife.wmv\r\n')
            sleep(1)
            Unit.vlc.send(b'pause\r\n')

        self.parent.register(self, self.start_signal)

        #self.textbuffer.create_tag("highlighted",  background = "red")
        #start = self.textbuffer.get_iter_at_line(0)
        #end = self.textbuffer.get_iter_at_line(1)

        while 1:
            if self.stopped:
                if self.step:
                    self.step = 0
                else:
                    sleep(.1)
                    continue    
            #if self.parent.page_num == int(self.name[-1]) + 1:
            #    self.textbuffer.remove_tag_by_name("highlighted", start, end)
            #    start = self.textbuffer.get_iter_at_line(self.state)
            #    end = self.textbuffer.get_iter_at_line(self.state + 1)
            #    self.textbuffer.apply_tag_by_name("highlighted", start, end)

            command = self.sequence[self.state]
            print(self.name, command)
            
            if command[0] == 'wait':
                while self.wait:
                    sleep(.1)
                self.wait = 1
                if self.msg[2] == 1:
                    continue
                print('%s started' % self.name)


            if command[0] == 'led':
                self.parent.can.led(command[1], command[2], command[3])

            if command[0] == 'output':
                self.parent.can.output(command[1], command[2], command[3])

            if command[0] == 'pwm':
                self.parent.can.pwm(command[1], command[2], command[3])


            if command[0] == 'vlc':
                if Unit.vlc != None:
                    Unit.vlc.send(command[1] + b'\r\n')
                    print('Sending vlc command')

            if command[0] == 'delay':
                sleep(command[1])
            #sleep(.1)
            self.state += 1
            self.state = self.state % len(self.sequence)


class Penny:
    def __init__(self):
        self.event_list = []
        self.page_num = 0
        """
        self.gladefile = "penny.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladefile)

        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window1")
        self.notebook = self.builder.get_object("notebook1")
        self.runstop = self.builder.get_object("runstop")
        self.notebook.remove_page(-1)
        self.notebook.remove_page(-1)
        """

        self.can = Can(self, 'can0')
        self.can.start()

        self.unit = []
        for n in range(len(sequence)):
            unit = Unit('Unit%d' % n, self, start_signals[n], sequence[n], vlc[n])
            #unit.tablabel = Gtk.Label(unit.name)
            #unit.textview = Gtk.TextView()
            #unit.textbuffer = unit.textview.get_buffer()
            #unit.textbuffer.set_text(sequence[n].__repr__()[1:-1].replace('),', ')\n'))
            #self.notebook.insert_page(unit.textview, unit.tablabel, -1)

            unit.start()
            self.unit.append(unit)

        #self.window.show_all()
        #self.notebook.set_current_page(0)

    def register(self, unit, address):
        self.event_list.append({'address': address, 'unit': unit})
        print('Register', address, unit.name)

    def handle_event(self, address, esource, eclass, num):
        print('received event: %d %d %d %d' % (address, esource, eclass, num))
        for e in self.event_list:
            print(e['address'])
            if address == e['address']:
                print('Sending signal to %s' % e['unit'].name)
                e['unit'].msg = (address, esource, eclass, num)
                e['unit'].wait = 0

    def on_window1_destroy(self, object, data=None):
        print("quit with cancel")
        Gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        print ("quit from menu")
        Gtk.main_quit()

    def on_runstop_toggled(self, object, data=None):
        self.unit[self.page_num - 1].stopped = not object.get_active()
        print ("runstop", object.get_active())

    def on_next_clicked(self, object, data=None):
        self.unit[self.page_num - 1].step = 1
        print ("next")

    def on_prev_clicked(self, object, data=None):
        print ("prev")

    def on_notebook1_switch_page(self, notebook, page, page_num, data=None):
        self.page_num = page_num
        self.runstop.set_active(not self.unit[self.page_num - 1].stopped)
        print ("notebook %d" % page_num)

if __name__ == "__main__":
    main = Penny()
    #Gtk.main()
    while 1:
        sleep(1)
        print('.')



