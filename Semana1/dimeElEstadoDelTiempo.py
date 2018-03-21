
# modulos y librerias usadas
import android
import datetime
import urllib2, json
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

droid = android.Android()

ultimaLocalizacionConocida = droid.getLastKnownLocation().result

# asignamos una variable al contenido de la llave que no es nula usando una condicional

if ultimaLocalizacionConocida['gps'] is not None:
    ultimaLoc = ultimaLocalizacionConocida['gps']
else:
    ultimaLoc = ultimaLocalizacionConocida['network']

# del diccionario extraemos latitud y longitud y fecha
lat = ultimaLoc["latitude"]
lon = ultimaLoc["longitude"]
time = ultimaLoc["time"]

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