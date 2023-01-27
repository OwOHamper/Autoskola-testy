import requests, time, os

base_url = "https://www.asnova.sk/test/"
data = '1=a&2=a&3=a&4=a&5=a&6=a&7=a&8=a&9=a&10=a&11=a&12=a&13=a&14=a&15=a&16=a&17=a&18=a&19=a&20=a&21=a&22=a&23=a&24=a&25=a&26=a&27=a'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

cooldown = 0.5
print("Downloading starting with cooldown {}s".format(cooldown))
try:
    os.mkdir("testy-html")
except FileExistsError:
    pass
for i in range(35):
    i += 1
    url = base_url + str(i)
    r = requests.post(url, headers=headers, data=data)
    with open(f"./testy-html/autoskola_test_{i}.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Downloaded test {}".format(i))

    time.sleep(0.1)