import requests, json

KEY="YOUR_KEY_HERE"
DEVICE="YOUR_DEVICE_KEY_HERE"

headers = {"Access-Token": KEY}
postdata = {"device_iden": DEVICE, "type":"note", "body":"hello world", "title":"titleS"}
r = requests.post('https://api.pushbullet.com/v2/pushes', headers=headers, data=postdata)
res = r.content

decoded = json.loads(res)

print decoded
