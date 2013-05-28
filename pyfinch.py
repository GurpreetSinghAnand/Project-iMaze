# Copyright 2012 Justas Sadzevicius
# Licensed under the MIT license: http://www.opensource.org/licenses/MIT
"""
This library provides simple API to control the Finch robot via USB.

The Finch is a robot for computer science education. Its design is the result
of a four year study at Carnegie Mellon's CREATE lab.

http://www.finchrobot.com

Simple usage:

import time
import pyfinch

finch = pyfinch.Finch()
finch.wheels(-1.0,1.0) # turn left
time.sleep(0.1)
finch.wheels(1.0,-1.0) # turn right
time.sleep(0.1)
finch.wheels(0,0) # stop
print finch.obstacle()


"""
import atexit
import os
import ctypes
import threading
import datetime
import time

import notes

PING_FREQUENCY_SECONDS = 2.0 # seconds

hid_api = ctypes.CDLL("/usr/lib/libhidapi32.so")

_open_finches = []


class NoConnection(Exception):
    """We are not connected to the robot."""


class FinchNotConnected(Exception):
    """Finch robot is not plugged in."""


def _inherit_docstring(cls):
    def doc_setter(method):
        parent = getattr(cls, method.func_name)
        method.func_doc = parent.func_doc
        return method
    return doc_setter


class FinchConnection(object):
    """Low level connection to the Finch robot."""

    VENDOR_ID = 0x2354
    DEVICE_ID = 0x1111

    c_finch_handle = ctypes.c_void_p(0)
    c_io_buffer = ctypes.c_char_p(0)
    cmd_id = 0

    @property
    def is_open(self):
        """Returns True if connected to the robot."""
        return bool(self.c_finch_handle)

    def open(self):
        """Connect to the robot.

        This method looks for an USB port the Finch is connceted to."""
        _before_new_finch_connection(self)
        if self.is_open:
            self.close()
        try:
            self.c_finch_handle = hid_api.hid_open(
                ctypes.c_ushort(self.VENDOR_ID),
                ctypes.c_ushort(self.DEVICE_ID),
                ctypes.c_void_p(0))
            self.c_io_buffer = ctypes.create_string_buffer(9)
            _new_finch_connected(self)
            self.cmd_id = self.read_cmd_id()
        except NoConnection:
            raise FinchNotConnected("Failed to connect to the Finch robot.")

    def close(self):
        """Disconnect from the robot."""
        if self.c_finch_handle:
            self.send('X') # stop
            self.send('R') # exit to idle (rest) mode
            hid_api.hid_close(self.c_finch_handle)
        self.c_finch_handle = ctypes.c_void_p(0)
        self.c_io_buffer = ctypes.c_char_p(0)
        global _open_finches
        if self in _open_finches:
            _open_finches.remove(self)

    def read_cmd_id(self):
        """Read the robot's internal command counter."""
        self.send('z', receive=True)
        return ord(self.c_io_buffer[0])

    def send(self, command, payload=(), receive=False):
        """Send a command to the robot (internal).

        command: The command ASCII character
        payload: a list of up to 6 bytes of additional command info
        receive: if True, read the result to the IO buffer
        """
        if not self.is_open:
            raise NoConnection("Connection to Finch was closed.")
        self.c_io_buffer[0] = chr(0)
        self.c_io_buffer[8] = chr(0)
        self.c_io_buffer[1] = command[0]
        for n in range(6):
            if payload and n < len(payload):
                self.c_io_buffer[n+2] = chr(payload[n])
            else:
                self.c_io_buffer[n+2] = chr(0)

        if receive:
            self.cmd_id = (self.cmd_id + 1) % 256
        self.c_io_buffer[8] = chr(self.cmd_id)
        res = 0

        while not res:
            res = hid_api.hid_write(self.c_finch_handle,
                                    self.c_io_buffer,
                                    ctypes.c_size_t(9))
        if not receive:
            return res
        while res > 0:
            res = hid_api.hid_read(self.c_finch_handle,
                                    self.c_io_buffer,
                                    ctypes.c_size_t(9))
            if command == 'z' or self.cmd_id == ord(self.c_io_buffer[8]):
                break
        return res

    def receive(self, command, payload=()):
        """Send a command to the robot (internal) and read the result
        to the IO buffer.

        command: The command ASCII character
        payload: a list of up to 6 bytes of additional command info
        """
        return self.send(command, payload=payload, receive=True)

    @property
    def data(self):
        """Bytes in the IO buffer."""
        return [
            ord(self.c_io_buffer[n])
            for n in range(9)]


def _convert_raw_accel(raw):
    if raw > 31:
        raw -= 64
    return raw * 1.6 / 32.0


class Acceleration(tuple):
    """Acceleration readings.

    Acceleration is measured in floating point units of g-force.

    When the Finch is put on the table, z axis will measure 1 g.
    But when it sits on it's tail, z axis will measure 0g, x axis will measure -1 g.
    """
    x = property(lambda d: _convert_raw_accel(d[0]),
                 doc="Acceleration over X axis.")
    y = property(lambda d: _convert_raw_accel(d[1]),
                 doc="Acceleration over Y axis.")
    z = property(lambda d: _convert_raw_accel(d[2]),
                 doc="Acceleration over Y axis.")
    tap = property(lambda d: bool(d[3]&0x20),
                   doc="Was the robot tapped.")
    shake = property(lambda d: bool(d[3]&0x80),
                   doc="Was the robot shaken.")

    def __str__(self):
        num = lambda f: ('%5s' % ('%.2f' % f))
        return 'acceleration xyz %s %s %s %s %s' % (
            num(self.x), num(self.y), num(self.z),
            self.tap and 'tap' or '   ',
            self.shake and 'shake' or '     ')

    __repr__ = object.__repr__


class Lights(tuple):
    """Light sensor readings.

    Measures from 0.0 to 1.0
    """
    left = property(lambda d: float(d[0])/255.0,
                    doc="Left eye light readings")
    right = property(lambda d: float(d[1])/255.0,
                     doc="Right eye light readings")

    def __str__(self):
        return 'see light left %.3f, right %.3f' % (self.left, self.right)

    __repr__ = object.__repr__


class Obstacles(tuple):
    """Obstacle sensor readings."""
    left = property(lambda d: bool(d[0]),
                    doc="Is there an obstacle on the left?")
    right = property(lambda d: bool(d[1]),
                    doc="Is there an obstacle at right?")

    def __str__(self):
        return '%s obstacle left, %s obstacle right' % (
            self.left and 'some' or 'no',
            self.right and 'some' or 'no')

    __repr__ = object.__repr__


class ThreadedFinchConnection(FinchConnection):

    lock = None
    thread = None
    main_thread = None
    last_cmd_sent = None

    @_inherit_docstring(FinchConnection)
    def open(self):
        FinchConnection.open(self)
        if not self.is_open:
            return
        self.last_cmd_sent = datetime.datetime.now()
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.__class__._pinger, args=(self, ))
        self.main_thread = threading.current_thread()
        self.thread.start()

    @_inherit_docstring(FinchConnection)
    def send(self, command, payload=(), receive=False):
        try:
            if self.lock is not None:
                self.lock.acquire()
            res = FinchConnection.send(self, command, payload=payload, receive=receive)
            self.last_cmd_sent = datetime.datetime.utcnow()
        finally:
            if self.lock is not None:
                self.lock.release()
        return res

    def _pinger(self):
        """Sends keepalive commands every few secconds of inactivity."""
        global PING_FREQUENCY_SECONDS
        while True:
            if not self.lock:
                break
            if not self.c_finch_handle:
                break
            if not self.main_thread.isAlive():
                break
            try:
                self.lock.acquire()
                if self.last_cmd_sent:
                    now = datetime.datetime.utcnow()
                    delta = (now - self.last_cmd_sent).total_seconds()
                    if delta >= PING_FREQUENCY_SECONDS:
                        self.last_cmd_sent = now
                        FinchConnection.send(self, 'z', receive=True)
            finally:
                self.lock.release()
            time.sleep(0.1)

    @_inherit_docstring(FinchConnection)
    def close(self):
        FinchConnection.close(self)
        self.thread.join()
        self.lock = None
        self.thread = None


class FinchAPI(FinchConnection):
    """Python bindings for the standard Finch API."""

    def led(self, *args):
        """Control three LEDs (orbs).

        Accepts:
          - hex triplet string: led('#00FF8B')
          - 0-255 RGB values: led(0, 255, 139)
        """
        if len(args) == 3:
            r, g, b = args
            self.send('O', [int(r)%256, int(g)%256, int(b)%256])
        elif (len(args) == 1 and isinstance(args[0], str)):
            color = args[0].strip()
            if len(color) == 7 and color.startswith('#'):
                color = color[1:]
            if len(color) == 6:
                r = ord(color[0:2].decode('hex'))
                g = ord(color[2:4].decode('hex'))
                b = ord(color[4:6].decode('hex'))
                self.send('O', [r, g, b])

    def buzzer(self, duration, frequency):
        """Outputs sound.

        duration - duration to beep, in seconds (s).
        frequency - frequency, in hertz (HZ).
        """
        millisec = int(duration*1000)
        frequency = int(frequency)
        self.send('B', [(millisec&0xff00)/256, millisec&0x00ff,
                        (frequency&0xff00)/256, frequency&0x00ff])

    def light(self):
        """Get light sensor readings."""
        res = self.receive('L')
        if res <= 0:
            return
        return Lights((self.data[0], self.data[1]))

    def obstacle(self):
        """Get obstacle sensor readings."""
        res = self.receive('I')
        if res <= 0:
            return
        return Obstacles((self.data[0], self.data[1]))

    def temperature(self):
        """Get temperature readings (in Celcius)"""
        res = self.receive('T')
        if res <= 0:
            return None
        raw = self.data[0]
        celcius = (raw - 127) / 2.4 + 25;
        return celcius

    def temperature_F(self):
        """Get temperature readings (in Fahrenheit)."""
        celcius = self.temperature()
        return celcius * 9. / 5. + 32

    def acceleration(self):
        """Get the acceleration readings."""
        res = self.receive('A')
        if res <= 0:
            return
        return Acceleration(self.data[1:5])

    def wheels(self, left, right):
        """Control the left and right wheels.

        Values must range from -1.0 (full throttle revers) to
        1.0 (full throttle forward).
        """
        dir_left = int(left<0)
        left = min(abs(int(left*255)), 255)
        dir_right = int(right<0)
        right = min(abs(int(right*255)), 255)
        self.send('M', [dir_left, left, dir_right, right])

    def idle(self):
        """Turn off the motors and go to the resting (color cycling) state."""
        self.send('R')

    def halt(self):
        """Set all motors and LEDs to off."""
        self.send('X')

    def sing(self, sheet, speed=0.05):
        """Sing a melody.

        sheet - a string of notes.  For the format see parse method in notes.py
        speed - speed of a single tick in seconds.

        Example: sing('C D E F G A B C5', speed=0.1)
        """
        music = notes.parse(sheet, speed=speed)
        for freq, duration in music:
            if duration:
                self.buzzer(duration, int(freq))
            time.sleep(duration+.01)


class Finch(ThreadedFinchConnection, FinchAPI):

    AUTO_CONNECT = True

    def __init__(self):
        super(Finch, self).__init__()
        if self.AUTO_CONNECT:
            self.open()


def _before_new_finch_connection(finch):
    global _open_finches
    # close other connections
    for robot in _open_finches:
        if robot.is_open:
            robot.close()


def _new_finch_connected(finch):
    global _open_finches
    if finch not in _open_finches:
        _open_finches.append(finch)


def _close_all_finches():
    global _open_finches
    if not _open_finches:
        return
    for finch in _open_finches:
        if finch.is_open:
            finch.close()

atexit.register(_close_all_finches)


def test_finch():
    import math
   
    finch = Finch()
    
    finch.sing(
        (
        'C4  C#  C-C-C-C3'
        'C4- C#- C - C3- '
        'C4  C#  C-C-C-C4'
        'CECECGCGCACACGCG'
        ),
    speed=0.05)
    
    finch.led('#FF8000')

    print 'temperature: %f'%finch.temperature()

    light = finch.light()
    print 'left eye light %.3f,' % light.left, 'right eye light %.3f' % light.right

    obstacle = finch.obstacle()
    print 'obstacle left %s,' % obstacle.left, 'obstacle right %s' % obstacle.right

    finch.buzzer(0.1, 700)
    time.sleep(0.1)
    finch.buzzer(0.1, 900)

    time.sleep(0.1)
    finch.wheels(-0.25,0.25)
    time.sleep(1.5)
    finch.wheels(0,0)
    time.sleep(1)

    x=0
    while x<5:
        time.sleep(1)
        ticks = 20
        pulse = int((math.sin(((x%ticks)*math.pi*2/ticks))+1)/2*255)

        finch.led(0, pulse, 0)
        print finch.acceleration()
        print finch.obstacle()
        print finch.light()
        print ''
        x+=1


def test_song():
    finch = Finch()
    finch.sing(
        (
        'C4  C#  C-C-C-C3'
        'C4- C#- C - C3- '
        'C4  C#  C-C-C-C4'
        'CECECGCGCACACGCG'
        ),
        speed=0.05)
   
    

if __name__ == '__main__':
    test_finch()
