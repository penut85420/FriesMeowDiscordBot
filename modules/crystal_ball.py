import json
import random
import requests

class CrystalBallMeow:
    def __init__(self):
        url = 'https://git.io/Jfcii'
        r = requests.get(url)
        self.emojis = json.loads(r.content)

    def get(self):
        return random.choice(self.emojis)

if __name__ == "__main__":
    cbm = CrystalBallMeow()

    for i in range(10):
        print(cbm.get())
