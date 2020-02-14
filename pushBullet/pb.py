from pushbullet import Pushbullet

api_key = "YOUR_KEY_HERE"

pb = Pushbullet(api_key)

push = pb.push_note("This is the title", "This is the body")