import requests, json

KEY="XXXXXX"

headers = {"Access-Token": KEY}
r = requests.get('https://api.pushbullet.com/v2/devices', headers=headers)
res = r.content

decoded = json.loads(res)
#print  type(decoded['devices'])

for peppe in decoded['devices']:
    if peppe['active']:
        print("%s -> %s" % (peppe['nickname'], peppe['iden']))
