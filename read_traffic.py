import json

with open("./example.json") as f:
    traffic = json.load(f)

def data_translate(p):
    try:
        time = float(p["_source"]["layers"]["frame"]["frame.time_relative"])
        time = int(p["_source"]["layers"]["nordic_ble"]["nordic_ble.event_counter"])
        value =  p["_source"]["layers"]["btatt"]["btatt.value"]
        
    except:
        return 0, 0
    
    def twos_complement(x):
        x = eval('0x'+x)
        if x >= 128:
            x = x - 256
        return x
    
    value = list(map( twos_complement  ,value.split(":")))
    return time, value


print(len(traffic))
traffic = [ data_translate(p)
               for p in traffic if p["_source"]["layers"]["btle"]["btle.length"] != "0" ]

print(len(traffic))
traffic = [ p
               for p in traffic if p != (0,0) ]

from turtle import *
color('red')
p = (-100,100)
setpos(p)
clear()
begin_fill()
last_t = 0
# the drawing start from about 1700th packet
for d in traffic[1700:]:
    if d[0] == 0: continue
    else :
        last_t = d[0]
        
        try:
            if d[1][0] == 1: color('red'); pensize(5)
            else: color('pink'); pensize(1)
            p = (p[0]+(d[1][1]*0.5), p[1]+d[1][2]*-0.5)
        except:
            print(d)
        setpos(p)
done()
