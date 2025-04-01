import requests

word = ""
url = f"https://api.dictionaryapi.dev/api/v1/entries/en/{word}"


res = requests.get(url)


if res.status_code == 404:
    print("Word not found!")
else:
    response = res.json()
    meaning = response[0]["meaning"]["noun"][0]["definition"]
    print(f"Meaning of {word}: {meaning}")
