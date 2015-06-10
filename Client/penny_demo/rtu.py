from time import time, sleep
import struct
import os
try:
    import Queue as queue
except:
    import queue
import threading
import select
import sys

path = os.path.dirname(__file__)

class ModbusRTU(serialport.SerialPort):
    def __init__(self, oid, name, parent):
        self.sequence = 0
        self.watch = None
        self.ctime = 0
        self.lasttime = 0
        self.state = 0
        self.response = ''
        self.silence_timer = None
        self.char_timer = None
        self.response_timer = None
        self.dindex = 0
        self.queue = queue.PriorityQueue(1000)
        self.silence_queue = queue.Queue(1)
        self.lock = threading.Lock()
        self.bytecount = 0
        self.thread = None
        self.poll = None
        self.current_device = None
        serialport.SerialPort.__init__(self, oid, name, parent)

        self.add_config('period', 1.0)
        self.load_config()

        for p in ('response_timeouts', 'char_timeouts'):
            self.add_property(p, 0)

    def start(self):
        super(ModbusRTU, self).start()
        if self.port != None:
            self.log(1, 'opening %s at %s' % (self.port, self.speed))
            self.open()
            #self.watch = timeout_add(int(self.period), self.poll)
        else:
            self.log(0, 'serial port not configured')

        self.thread = threading.Thread(target = self.run)
        self.thread.name = self.name
        self.thread.daemon = True
        self.thread.start()

    def refresh_devices(self):
        self.log(1)
        if self.sp == None:
            self.log(0, 'refresh_devices: serial port not configured')
            return

        for device in self.children.values():
            device.refresh()

        return True

    def seq(self):
        self.sequence += 1
        return self.sequence

    def read_holding(self, device, rq, priority=0, address=None):
        if self.sp == None:
            self.log(1, 'read_holding: serial port not configured')
            return
        self.sp.flush()
        
        # If an address was supplied then use it. This helps with auto discovery
        if address == None:
            address = device.address
        else:
            self.log(0, 'Probing address %s' % address)

        rlen = rq.count * 2 + 5
        msg = struct.pack('>BBHH', address, 3, rq.offset, rq.count)
        msg += struct.pack('<H', crc(bytearray(msg)))
        self.log(3, 'Sending %s' % dump(msg))
        self.queue.put((priority, (self.seq(), msg, device, rq, rlen)))

    def write_single_reg(self, device, offset, value, priority=0):
        if self.sp == None:
            self.log(0, 'write_single_reg: serial port not configured')
            return
        self.sp.flush()
        msg = struct.pack('>BBHH', device.address, 6, offset, value)
        msg += struct.pack('<H', crc(bytearray(msg)))
        self.log(3, 'Sending %s' % dump(msg))
        self.queue.put((priority, (self.seq(), msg, device, None, len(msg))))

    def write_single_coil(self, device, coil, value, priority=0):
        if self.sp == None:
            self.log(0, 'write_single_coil: serial port not configured')
            return
        
        if coil < 1 or coil > 65:
            self.log(0, 'write_single_coil: coil must be between 1 and 65 (%d)' % coil)
            return

        self.sp.flush()
        self.log(1, 'write_single_coil(%d, %d, %d)' % (device.address, coil, value))
        msg = struct.pack('>BBHH', device.address, 5, coil - 1, value)
        msg += struct.pack('<H', crc(bytearray(msg)))
        self.queue.put((priority, (self.seq(), msg, device, None, len(msg))))

    def run(self):
        self.log(1, 'thread started using %s' % (self.port,))
        self.poll = select.poll()
        self.poll.register(self.sp, select.POLLIN)

        try:
            while not Node.shutdown:
                if not self.children:
                    sleep(1)
                    continue;

                # Check to see if there is a message to send
                # If not, then refresh all devices on this serial port
                # The refresh will end up placing messages on the queue to transmit
                try:
                    priority, data = self.queue.get(timeout=self.period)
                    seq, msg, device, rq, rlen = data
                    self.log(4, 'Dequeued seq %d' % seq)
                except queue.Empty:
                    self.refresh_devices()
                    continue

                # Wait for 5 milliseconds of silence
                # Read and discard everything until we get there
                if self.state != 1:
                    self.state = 0;
                    #t = time()
                    while True:
                        if not self.poll.poll(5):
                            break;
                        self.sp.read()

                    self.state = 1;

                self.current_device = device
                self.log(2, 'Sending %s' % dump(msg))
                self.write(msg)

                fdset = self.poll.poll(100)
                if not fdset:
                    self.state = 0
                    if hasattr(rq, 'probe'):
                        self.log(0, 'No response at address %d' % (ord(msg[0]),))
                    else:
                        self.log(0, '%s response timeout on %s' % (self.name, self.current_device.name))
                    continue


                response = self.sp.read(rlen)
                t = time()
                if len(response) >= 5:
                    r = struct.unpack('BBB', response[:3])
                    if r[1] & 0x80:
                        self.log(0, 'Exception %s, %d, %s, %s' % (device.name, r[1] & 0x7f, rq, exceptions[r[2]]))
                    else:
                        if len(response) == rlen:
                            self.process_response(response, device, rq)
                        else:
                            self.log(1, 'Incomplete response (%d, %d)' % (rlen, len(response)))
                            print(dump(response))

                self.state = 0
                #continue
        except:
            print('thread shutting down')
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def process_response(self, response, device, rq):
        #self.lock.release()
        _crc = struct.unpack('H', response[-2:])[0]
        if _crc != crc(bytearray(response[:-2])):
            self.current_device.crc_errors += 1
            self.log(1, '%s bad CRC' % (device.name,))
        else:
            if hasattr(rq, 'probe'):
                self.log(0, 'Found device %s' % (dump(response)))
            else:
                device.handle_response(response, rq)
                self.log(1, '%s received %d bytes' % (self.current_device.name, len(response)))
                self.log(2, '%s' % (dump(response),))

    # Returns a web specific representation of the class
    #TODO: This has been disabled for the April 10th demo
    def handle_web_request_(self, request):
        return  """<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   version="1.1"
   width="250"
   height="250"
   preserveAspectRatio="xMinYMin meet"
   viewBox="0 0 250 250"
   id="svg2">
   <script type="text/ecmascript"><![CDATA[

   function foo(o)
   {
    test = document.getElementById('tspan2987');
    if (o == undefined)
    {
        test.firstChild.nodeValue = "I'm a modbus rtu protocol!"
    }
    else
    {
        test.firstChild.nodeValue = o.target.id;
    }
   }

   ]]>
   </script>
  <defs
     id="defs4">
    <linearGradient
       id="linearGradient3759">
      <stop
         id="stop3761"
         style="stop-color:#ffffff;stop-opacity:1"
         offset="0" />
      <stop
         id="stop3769"
         style="stop-color:#221ce5;stop-opacity:1"
         offset="0.25000003" />
      <stop
         id="stop3767"
         style="stop-color:#1813cb;stop-opacity:1"
         offset="0.50000006" />
      <stop
         id="stop3763"
         style="stop-color:#02003f;stop-opacity:1"
         offset="1" />
    </linearGradient>
    <radialGradient
       cx="87.714554"
       cy="86.065735"
       r="75.5"
       fx="87.714554"
       fy="86.065735"
       id="radialGradient3765"
       xlink:href="#linearGradient3759"
       gradientUnits="userSpaceOnUse"
       gradientTransform="matrix(1.1664844,0,0,1.1664844,-14.317661,-20.394343)" />
  </defs>
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <g
     transform="translate(0,-802.36218)"
     id="layer1">
    <text
       onmouseover = "foo(evt);"
       onmouseout = "foo();"
       x="44.5"
       y="832.86218"
       id="text2985"
       xml:space="preserve"
       style="font-size:2px;font-style:normal;font-weight:normal;line-height:125%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:1;stroke:none;font-family:Sans"><tspan
         x="44.5"
         y="832.86218"
         id="tspan2987"
         style="font-size:12px">Hi, I'm a modbus rtu protocol</tspan></text>
    <a xlink:href = "/"><path
       onmouseover = "foo(evt);"
       onmouseout = "foo();"
       d="m 192,106.5 a 75.5,75.5 0 1 1 -151,0 75.5,75.5 0 1 1 151,0 z"
       transform="matrix(1.1092715,0,0,0.17998115,10.019868,971.10561)"
       id="path2989-4"
       style="opacity:0.75;color:#000000;fill:#000000;fill-opacity:1;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />
    <path
       onmouseover = "foo(evt);"
       onmouseout = "foo();"
       d="m 192,106.5 a 75.5,75.5 0 1 1 -151,0 75.5,75.5 0 1 1 151,0 z"
       transform="translate(4,818.36218)"
       id="path2989"
       style="color:#000000;fill:url(#radialGradient3765);fill-opacity:1;stroke:none;stroke-width:2;marker:none;visibility:visible;display:inline;overflow:visible;enable-background:accumulate" />
  </g>
</svg>"""

