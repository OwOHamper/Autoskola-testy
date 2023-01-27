from bs4 import BeautifulSoup
from InquirerPy import prompt
import json, time, os
import requests
from alive_progress import alive_bar


base_url = "https://www.asnova.sk"
data = '1=a&2=a&3=a&4=a&5=a&6=a&7=a&8=a&9=a&10=a&11=a&12=a&13=a&14=a&15=a&16=a&17=a&18=a&19=a&20=a&21=a&22=a&23=a&24=a&25=a&26=a&27=a'
headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
pocet_testov = 35
def download_testy(cooldown=3):
    try:
        os.mkdir("testy-html")
    except FileExistsError:
        pass
    with alive_bar(pocet_testov, bar="blocks", spinner="dots_waves2") as bar:
        for i in range(pocet_testov):
            i += 1
            url = f"{base_url}/test/{i}"
            r = requests.post(url, headers=headers, data=data)
            if not r.ok:
                time.sleep(5)
                r = requests.post(url, headers=headers, data=data)
            with open(f"./testy-html/autoskola_test_{i}.html", "w", encoding="utf-8") as f:
                f.write(r.text)
            bar()
            time.sleep(cooldown)

def parse_testy():
    otazka_n = 1
    testy = {}
    with alive_bar(pocet_testov, bar="blocks", spinner="dots_waves2") as bar:
        for test in range(pocet_testov):
            test += 1
            testy.update({test: {}})
            with open(f"./testy-html/autoskola_test_{test}.html", encoding="utf-8") as f:
                soup = BeautifulSoup(f, "html.parser")
            form = soup.form
            for otazka in form:
                if otazka.name in (None, "hr", "button", "input", "p"):
                    continue
                testy[test].update({otazka_n: {
                    "otazka": None,
                    "asnwers": {
                        "a": None,
                        "b": None,
                        "c": None,
                        "img": None,
                        "correct_answer": None
                    }
                }})
                for element in otazka:
                    if element.name in (None, "br", "strong"):
                        continue
                    if element.get("class") in ("green", "strong"):
                        continue
                    if "test_otazka" in str(element.get("class")) and element.name == "label":
                        otazka = element.text[3:].strip()
                        testy[test][otazka_n]["otazka"] = otazka
                    if "test_odpoved" in element.get("class") and element.name == "label":
                        value = element.text.strip()[0]
                        testy[test][otazka_n]["asnwers"][value] = element.text.strip()[3:]
                        if "green" in element.get("class"):
                            testy[test][otazka_n]["asnwers"]["correct_answer"] = value
                    if "img-responsive" in element.get("class"):
                        testy[test][otazka_n]["asnwers"]["img"] = element.get("src")
                otazka_n += 1
            bar()

    with open("autoskola_testy.json", "w", encoding="utf-8") as f:
        json.dump(testy, f, indent=4, ensure_ascii=False)

def download_images(cooldown=0.1):
    with open("autoskola_testy.json", encoding="utf-8") as f:
        testy = json.load(f)
    try:
        os.mkdir("testy-images")
    except FileExistsError:
        pass
    for test in testy:
        try:
            os.mkdir(f"./testy-images/{test}")
        except FileExistsError:
            pass

    img_count = 0
    for test in testy:
        for otazka in testy[test]:
            if testy[test][otazka]["asnwers"]["img"] is not None:
                img_count += 1

    with alive_bar(img_count, bar="blocks", spinner="dots_waves2") as bar:
        for test in testy:
            for otazka in testy[test]:
                if testy[test][otazka]["asnwers"]["img"] is not None:
                    img_url = testy[test][otazka]["asnwers"]["img"]
                    r = requests.get(f"{base_url}/{img_url}")
                    if not r.ok:
                        time.sleep(5)
                        r = requests.get(f"{base_url}/{img_url}")
                    with open(f"./testy-images/{test}/{otazka}.jpg", "wb") as f:
                        f.write(r.content)
                    bar()
                    time.sleep(cooldown)

questions = [{
    "type": "list",
    "name": "action",
    "message": "What do you want to do?",
    "choices": [
        "Download tests",
        "Convert tests to .json file",
        "Download images from tests",
        "Exit"
    ]
}]

answer = prompt(questions)
if answer["action"] == "Stiahnuť testy":
    questions = [
        {
            'type': 'input',
            'name': 'seconds',
            'message': 'Enter the amount of seconds to wait between requests:',
            'validate': lambda val: val.replace(".","").isdigit() or "Please enter a valid number"
        },
    ]
    answers = prompt(questions)
    seconds = float(answers['seconds'])
    download_testy(cooldown=seconds)
elif answer["action"] == "Skonvertovať testy do .json súboru":
    parse_testy()
elif answer["action"] == "Stiahnuť obrázky z testov":
    questions = [
        {
            'type': 'input',
            'name': 'seconds',
            'message': 'Enter the amount of seconds to wait between requests:',
            'validate': lambda val: val.replace(".","").isdigit() or "Please enter a valid number"
        },
    ]
    answers = prompt(questions)
    seconds = float(answers['seconds'])
    download_images(cooldown=seconds)
elif answer["action"] == "Exit":
    os._exit(0)