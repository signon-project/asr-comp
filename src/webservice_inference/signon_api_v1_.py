"""
Author: Aditya Parikh
CLST, Radboud University, Nijmegen, Netherlands
This script is created for integrating ASR webservice with SignON project WP3 dispatcher script.
The ASR API V1 documentation can be find here: https://restasr.cls.ru.nl/api-docs/  
"""

import request, re

# ASR Language Code Identification
def retrieveCodeLanguage(sourceLanguage):
    switcher = {
        "DUT": 1,
        "NLD": 6,
        "ENG": 5,
        "SPA": 9
    }

    return switcher.get(sourceLanguage, 5)

# File has been downloaded Here will be integrated the ASRPost component
# ASRpost_version2.1.py
r = requests.post('https://restasr.cls.ru.nl/auth/login', json={
    "username": "SignOnASR",
    "password": "SignOnASR2022"
}, headers={'Content-Type': 'application/json'},
                timeout=(conf['externalServices']['timeout']))
# print(f"Status Code: {r.status_code}, Response: {r.json()}")

token = r.json()['data']['access_token']
url = 'https://restasr.cls.ru.nl/users/SignOnASR/audio'
audio_filename = os.path.basename(file_name)
multipart_form_data = {
    'file': (audio_filename, open(file_name, 'rb'), 'audio/wav')
}
headers = {
    'Authorization': 'Bearer ' + token,
}
r2 = requests.post(url, headers=headers, files=multipart_form_data,
                timeout=(conf['externalServices']['timeout']))
# print(f"Status Code: {r2.status_code}, Response: {r2.json()}")
id_audio = r2.json()['data']['filename']
languageCode = retrieveCodeLanguage(data['App']['sourceLanguage'])
params = {"code": languageCode,
        "text": "custom text",
        "keep": True
        }
r3 = requests.post('https://restasr.cls.ru.nl/users/SignOnASR/audio/' + id_audio,
                json=params, headers={'Authorization': "Bearer " + token},
                timeout=(conf['externalServices']['timeout']))
# print(f"Status Code: {r3.status_code}, Response: {r3.json()}")
text = r3.json()['data']['nbest']
ctm = r3.json()['data']['ctm']

print(text)
print(ctm)