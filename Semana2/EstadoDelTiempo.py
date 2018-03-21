
# modulos y librerias usadas
import android
import datetime
import urllib2, json
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

droid = android.Android()

# comienza a registrar datos de localizacion 
droid.startLocating()

# 5 segundos para obtener la lectura
time.sleep(5)

# obtener lectura
localizacion = droid.readLocation().result

if localizacion == {}:
    localizacion = droid.getLastKnownLocation().result
    
# de cada proveedor analiza cuale es el mas reciente

proveedorAUsar = ''
ultimaLocalizacion = 0

for proveedor in ['passive', 'network', 'gps']:
    if proveedor in localizacion:
        if not localizacion[proveedor] == None:
            if 'time' in localizacion[proveedor]:
                if localizacion[proveedor]['time'] >= ultimaLocalizacion:
                    proveedorAUsar = proveedor
                    ultimaLocalizacion =localizacion[proveedor]['time']


# si aun no encuentra localizacion algo esta pasando
if ultimaLocalizacion == 0:
    droid.notify("No es posible localizar", "Revisa que la antena de GPS o WiFi estan encendidas")
    exit()

# latitud y longitud de la localizacion 
lat = localizacion[proveedor]["latitude"]
lon = localizacion[proveedor]["longitude"]
time = localizacion[proveedor]["time"]

fecha = datetime.datetime.fromtimestamp(time/1e3).strftime('%Y-%m-%d %H:%M:%S')

direccion = droid.geocode(lat,lon).result

codigoPostal = direccion[0]["postal_code"]
codigoPais = direccion[0]["country_code"]

url="http://api.openweathermap.org/data/2.5/weather?zip={0},{1}&APPID=dfeea5e604e1948b28652216ad910d11".format(codigoPostal,codigoPais)

response = urllib2.urlopen(url)
respuesta = response.read()
response.close()

estadoDelTiempo = json.loads(respuesta)

# es una lista
descripcion = estadoDelTiempo["weather"][0]['description']

# mensaje
mensaje='En la ciudad de {0}, siendo las {1} horas, en la calle de {2}, el estado del tiempo es {3}'.format( \
                                direccion[0]['locality'], fecha,direccion[0]['thoroughfare'],descripcion)

droid.ttsSpeak(mensaje)