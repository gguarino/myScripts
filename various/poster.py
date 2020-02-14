import requests, json

url = "http://tvtap.net/tvtap1/index_new.php?case=get_channel_by_country_revised"

datas = {
    "country": ".IT",
    "username": "603803577"
}

r = requests.post(url, data={
    "country": ".IT",
    "username": "603803577"
},  headers={
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'USER-AGENT-tvtap-APP-V2',
    'app-token': '37a6259cc0c1dae299a7866489dff0bd',
    'Accept': 'text/plain'
})

print r.text

