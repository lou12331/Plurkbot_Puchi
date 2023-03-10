import re
import json
import urllib.request
import openai

from plurk_oauth import PlurkAPI
plurk = PlurkAPI.fromfile('API.keys')
comet = plurk.callAPI('/APP/Realtime/getUserChannel')
comet_channel = comet.get('comet_server') + "&new_offset=%d"
jsonp_re = re.compile('CometChannel.scriptCallback\((.+)\);\s*')
new_offset = -1
while True:
    plurk.callAPI('/APP/Alerts/addAllAsFriends')
    req = urllib.request.urlopen(comet_channel % new_offset, timeout=80)
    rawdata = req.read()
    match = jsonp_re.match(rawdata.decode())
    if match:
        rawdata = match.group(1)
    data = json.loads(rawdata)
    new_offset = data.get('new_offset', -1)
    msgs = data.get('data')
    if not msgs:
        continue
    for msg in msgs:
        if msg.get('type') == 'new_plurk':
            pid = msg.get('plurk_id')
            content = msg.get('content_raw')
            if content.find("hello") != -1:
                plurk.callAPI('/APP/Responses/responseAdd',
                              {'plurk_id': pid,
                               'content': 'world',
                               'qualifier': ':' })