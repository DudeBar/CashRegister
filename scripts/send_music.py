import json
import soco
import requests

for zone in soco.discover():
    info = zone.get_current_track_info()
    json_info = json.loads(info)
    if json_info.metadata != 'NOT_IMPLEMENTED':
        URL = 'http://www.dudebar.fr/current_music'
        params = dict(login="", password="", data=info)
        requests.post(URL, data=params, headers=dict(Referer=URL))
