import esp
import webrepl
webrepl.start()
esp.osdebug(None)
import gc


import ntptime, socket, time, json, dht, machine, urequests

pubKey = 'pub-c-430b206d-a55d-4649-a303-ecf412ea6820'
subKey = 'sub-c-fff5d73a-2d2c-11e8-8305-f27a6a4e1feb'

dhtPower= 12#D6
dhtPin = 14#D5

dhtPower = machine.Pin(12,machine.Pin.OUT)
dhtPower.on()

miCanal = 'Edmundo' 

ssid = "PubliLANIA"
pswd = "DHC5+txpGQ"

dhtSensor = dht.DHT11(machine.Pin(14))

def do_connect(ssid,pswd):
	import network
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print('connecting to network...')
		sta_if.active(True)
		sta_if.connect(ssid,pswd)
		while not sta_if.isconnected():
			pass
	print('network config:', sta_if.ifconfig())


do_connect(ssid,pswd)
gc.collect()

def publicar(miCanal,mensaje):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port =80
	host = 'ps.pubnub.com'
	addr = socket.getaddrinfo(host,port)[0][-1]
	s.connect(addr)
	m = json.dumps(mensaje)
	cadenaParaPublicar = 'GET /publish/%s/%s/0/%s/0/%s HTTP/1.1\r\nHost: %s\r\n\r\n'%(pubKey,subKey,miCanal,m,host)
	s.send(cadenaParaPublicar)
	
def generateMessage():
	ntptime.settime();
	t = time.time()
	dhtSensor.measure()
	temp = dhtSensor.temperature()
	hum = dhtSensor.humidity()
	mensaje = {'Time':t,'Temperature':temp,'Humidity':hum}
	return mensaje
	
def generateMeasurements():
	# ntptime.settime();
	# t = time.time();
	dhtSensor.measure()
	temp = dhtSensor.temperature()
	hum = dhtSensor.humidity()
	message = '&temp={0}&hum={1}'.format(temp, hum)
	return message

def send2DataDrop(bin, m):
	# ntptime.settime();
	# t = time.time()
	# dhtSensor.measure()
	# temp = dhtSensor.temperature()
	# hum = dhtSensor.humidity()

	host = 'datadrop.wolframcloud.com'
	base_url = 'https://'+host
	bin_url = '/api/v1.0/Add?bin={0}'.format(bin)
	drop_url = base_url+bin_url+m
	#'&timestamp={0}&temp={1}&hum={2}'.format(t, temp, hum)
	response = urequests.post(drop_url)

while True:
	# m = generateMessage()
	m = generateMeasurements()
	# publicar(miCanal,m)
	send2DataDrop('tkJst52T', m)
	time.sleep(60)
	gc.collect()
	