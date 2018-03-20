
import android
import time
from haversine import *

droid = android.Android()

lat1 = 19.5197093
lon1 = -96.9155696

droid.startLocating()
time.sleep(15) 
while True:     
    loc = droid.readLocation().result    
    if loc == {}:       
        loc = droid.getLastKnownLocation().result   
    if loc != {}:    
        try:
            n = loc['gps']    
        except KeyError:  
            n = loc['network']   
    la = n['latitude']  
    lo = n['longitude'] 
    
    print haversine(la, lo, lat1, lon1) 
    
    if haversine(la, lo, lat1, lon1) > .1:    
        droid.toggleRingerSilentMode(True)  
        droid.vibrate(1000)
        droid.ttsSpeak("saliendo de granja")
    else:         
        droid.toggleRingerSilentMode(False)