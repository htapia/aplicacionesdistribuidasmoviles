import android
import datetime, time
from haversine import *
droid = android.Android()

logName = 'locationLog-'+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
localLog = '/sdcard/sl4a/scripts/RySI/'+logName+'.txt'

logHeader = "Time, Latitude, Longitude, Distance, Provider\n"

lat1 = 19.5197093
lon1 = -96.9155696
hd = haversine(lat1, lon1, lat1, lon1)
prov = '-'

droid.wakeLockAcquirePartial()
droid.startLocating()
time.sleep(15)

with open(localLog, 'a') as logFile:
    logFile.write(logHeader)
    curTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logFile.write("{0}, {1}, {2}, {3}, {4}, {5}\n".format(curTime, lat1, lon1, hd, prov, '-'))
    
    while True:
        loc = droid.readLocation().result
        if loc == {}:
            loc = droid.getLastKnownLocation().result
            newLoc = False
        if loc != {}:
            newLoc = True
            try:
                prov = 'gps'
                n = loc[prov]                
            except KeyError:
                prov = 'network'
                n = loc[prov]
            
        la = n['latitude']
        lo = n['longitude']
        ts = n['time']
        t = datetime.datetime.fromtimestamp(ts/1e3).strftime('%H:%M:%S')
        
        hd = haversine(la, lo, lat1, lon1)
        time.sleep(10)
        
        logLine = "{0}, {1}, {2}, {3}, {4}, {5}\n".format(t, lat1, lon1, hd, prov, newLoc)
        logFile.write(logLine)
        logFile.flush()
        
        print "{0}, {1}, {2}, {3}".format(t, hd, prov, newLoc)
            
        if hd > .1:
            droid.toggleRingerSilentMode(True)
            droid.vibrate(1000)
            droid.ttsSpeak("Dejando geocerca")
        else:
            droid.toggleRingerSilentMode(False)
    
    logFile.close()