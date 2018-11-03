from machine import I2C, Pin
import utime
import bme280
import ambient

ssid = 'SHIBATAK16HOME2'
password = 'keiichiroshibataisking'
channelId = 7188
writeKey = '88d1de7965cf47d1'

def do_connect(ssid, password):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

i2c = I2C(scl=Pin(4), sda=Pin(5))
bme = bme280.BME280(i2c=i2c)
am = ambient.Ambient(channelId, writeKey)

do_connect(ssid, password)

while True:
    data = bme.read_compensated_data()
    print(bme.values)
    r = am.send({'d1': data[0] / 100.0, 'd2': data[2] / 1024.0, 'd3': data[1] / 25600.0})
    print(r.status_code)
    r.close()

    utime.sleep(30)
