#online assistant (using gemini ai)

import requests
import time 
import json

#model details (we will import from google docs information like api key, model name and url)

API_KEY = "AIzaSyDYL-_VJMkz2FzHqOaxZVzVg5ni_yUQmPI"
MODEL_NAME = 'gemini-2.5-flash-preview-09-2025'
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent'

def online_assistant(prompt : str,system_instruction : str = None,max_retries :int =3) -> str | bool :
    headers={
        "Content-type":"application/json"
    }
    params={
        "key":API_KEY
    }
    payload = {
        "contents":[{"parts":[{"text":prompt}]}],
        "tools":[{"google_search":{}}]

    }
    if system_instruction:
        payload['systemInstruction']={"parts":[{'text':system_instruction}]}
    for i in range(max_retries):
        try:
            response=requests.post(API_URL,headers=headers,params=params,json=payload,timeout=30)
            if response.status_code == 429 and i < max_retries -1:
                delay= 2**i
                print(f"API rate limit hit (429). Retrying in {delay} seconds.")
                time.sleep(delay)
                continue
            if not response.ok:
                print(f"API error ({response.status_code}):{response.json().get('error',{}).get('message','Unknown Error')}")
                return False
            result=response.json()
            generated_text=result.get('candidates',[{}])[0].get('content',{}).get('parts',[{}])[0].get('text','')
            return generated_text
        except requests.exceptions.Timeout as e:
            if i<max_retries - 1:
                delay=2**i
                print(f'request timed out. retrying in {delay} seconds')
                time.sleep(delay)
                continue
        except requests.exceptions.RequestException as e:
            if i < max_retries -1:
                delay=2 **i
                print(f"Transient network error : {e}, retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            print(f"persistent netwrok error {e}")
            return False
    return False
