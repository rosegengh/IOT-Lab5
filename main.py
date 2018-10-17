import network
import socket
from socket import *
import ssd1306
import machine
import time
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('HomeOfLove', '106W105th11')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()

i2c = machine.I2C(-1, machine.Pin(5), machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
rtc = machine.RTC()
rtc.datetime((2018,10,15,2,13,30,34,300))
pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
lights = False
showtime = False

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP8266 Pins</title> </head>
    <body> <h1>PINs</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""
import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

s.settimeout(0.5)

print('listening on', addr)
while True:
    print(1)
    (year, month, day, weekday, hour, minute, second, subsecond) = rtc.datetime()

    try:
        cl, addr = s.accept()
        print('client connected from', addr, 'with socket', cl)
    except OSError:
        print("Nothing")
    else:
        req = cl.recv(4096)
        print(req)
        cl_file = cl.makefile('rwb', 0)
        html = req
        html = html.split(b'\r\n\r\n')
        data = html[-1]  # gets unsplited data
        data1 = data.decode("utf-8")  # byte to string conversion
        data2 = data1.split("=", 1)  # split it using "=" sign
        data4 = data2[1]
        data3 = data2[0]
        data5 = " "
        data5 = data4
        data6 = data5.replace("+", " ")
        print('the data I want is')
        data7 = data3.replace("+", " ")
        print(data7)
        del(req)
        if(data7 == 'show time'):
            print('11')
            showtime = True
            resp12 = "HTTP/1.1 200 TIME\r\nContent-Type: application/text\r\nContent-Length: 10\r\n\r\n{'response'}"
        if(data7 == 'turn off'):
            print('22')
            lights = False
            showtime =False
            oled.init_display()
            resp12 = "HTTP/1.1 200 OFF\r\nContent-Type: application/text\r\nContent-Length: 10\r\n\r\n{'response'}"
        if(data7 == 'turn on'):
            lights = True
            resp12 = "HTTP/1.1 200 ON\r\nContent-Type: application/text\r\nContent-Length: 10\r\n\r\n{'response'}"
        cl.send(resp12)
        cl.close()

    # del (req)
    if lights == True:
        oled.poweron()
        if showtime==True:
            oled.fill(0)
            oled.text(str(month), 0, 10)
            oled.text(',', 15, 10)
            oled.text(str(day), 25, 10)
            oled.text(str(hour), 55, 10)
            oled.text(':', 70, 10)
            oled.text(str(minute), 80, 10)
            oled.text(':', 90, 10)
            oled.text(str(second), 100, 10)
            oled.show()




        if len(data7) > 21:
            rohit = "BIG MESSAGE"
            oled.text(rohit,0,0)
            oled.show()

        else:
            oled.text(data7,0,0)
            oled.show()


    else:
        oled.poweroff()





