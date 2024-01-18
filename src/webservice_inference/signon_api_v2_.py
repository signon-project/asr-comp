"""
Author: Aditya Parikh
CLST, Radboud University, Nijmegen, Netherlands
This script is created for integrating ASR webservice with SignON project WP3 dispatcher script.
The ASR API V2 documentation can be find here: https://signon-wav2vec2.cls.ru.nl/docs 
English (ENG) ASR is being provided via OpenAI Whisper Medium model.
Spanish, Dutch and Flemish (NLD) ASR is provided via wav2vec2.0 model.
There is a single model for Netherlands and Belgian Dutch (DUT and NLD) 
Irish ASR is provided via Kaldi based hybrid model's ASR webservice Version1 (https://restasr.cls.ru.nl/api-docs/)
"""


import requests,os

def retrieveCodeLanguage(sourceLanguage):
    switcher = {
        "ENG": 1,
        "SPA": 2,
        "DUT": 3,
        "GLE": 4,
        "NLD": 3
    }
    return switcher.get(sourceLanguage, 1)

# Login and get access token in CLST ASR API
# CLST ASR API Credentials
username_signon_wav2vec2 = "signon@project.eu"
password_signon_wav2vec2 = "*****************"

url_signon_wav2vec2 = 'https://signon-wav2vec2.cls.ru.nl/login'
payload_signon_wav2vec2 = {
    'grant_type': '',
    'username': username_signon_wav2vec2,
    'password': password_signon_wav2vec2,
    'scope': '',
    'client_id': '',
    'client_secret': ''
}
headers_signon_wav2vec2 = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'accept': 'application/json'
}
response_signon_wav2vec2 = requests.post(url_signon_wav2vec2, data=payload_signon_wav2vec2, headers=headers_signon_wav2vec2)
access_token_signon_wav2vec2 = response_signon_wav2vec2.json()['access_token']


# Login and get access token in  RESTASR API
# RESR ASR API Credentials
username_restasr = "SignOnASR"
password_restasr = "*********"
url_restasr_login = 'https://restasr.cls.ru.nl/auth/login'
payload_restasr_login = {
    "username": username_restasr,
    "password": password_restasr
}
headers_restasr_login = {
    'Content-Type': 'application/json'
}
response_restasr = requests.post(url_restasr_login, json=payload_restasr_login, headers=headers_restasr_login)
access_token_restasr = response_restasr.json()['data']['access_token']


def transcribe(filename, lang_code):
    if lang_code in [2,3,4]:
        url = f'https://signon-wav2vec2.cls.ru.nl/user/1/{lang_code}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token_signon_wav2vec2}'
        }
        files = {
            'file': (filename, open(filename, 'rb'), 'audio/wav')
        }
        response = requests.post(url, headers=headers, files=files)
        output = response.json()
        transcript = output[0].split(': ')[-1]
        return transcript

    elif lang_code == 1:
        url = f'https://signon-wav2vec2.cls.ru.nl/user/2/4/{lang_code}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {access_token_signon_wav2vec2}'
        }
        files = {
            'file': (filename, open(filename, 'rb'), 'audio/wav')
        }
        response = requests.post(url, headers=headers, files=files)
        output = response.json()
        transcript = output[0].split(': ')[-1]
        return transcript

    elif lang_code == 4:
        url = 'https://restasr.cls.ru.nl/users/SignOnASR/audio'
        audio_filename = os.path.basename(filename)
        multipart_form_data = {
            'file':(audio_filename, open(filename, 'rb'), 'audio/wav')
        }
        headers = {
            'Authorization': 'Bearer ' + access_token_restasr,
        }
        r2 = requests.post(url, headers=headers, files=multipart_form_data)
        id_audio = r2.json()['data']['filename']
        params = {
            "code": 11,
            "text": "custom text",
            "keep": True
        }
        r3 = requests.post('https://restasr.cls.ru.nl/users/SignOnASR/audio/'+id_audio,
                           json=params, headers={'Authorization': "Bearer "+access_token_restasr})
        transcript = r3.json()['data']['nbest']
        return transcript

if __name__ == "__main__":
    lang_code = retrieveCodeLanguage("DUT")
    #lang_code = retrieveCodeLanguage(data['App']['sourceLanguage'])
    text = transcribe("sample_audiofile.mp3", lang_code)
    #transcribe(filename,retrieveCodeLanguage(data['App']['sourceLanguage']))
    print(text)