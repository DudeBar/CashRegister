import json
from time import sleep
import soco
import requests

while 1:
    sleep(15)
    for zone in soco.discover():
        try:
            info = zone.get_current_track_info()
            if info['metadata'] != 'NOT_IMPLEMENTED':
                URL = 'http://www.dudebar.fr/music'
                params = dict(login="", password="", data=json.dumps(info))
                requests.post(URL, data=params, headers=dict(Referer=URL))
        except:
            pass
