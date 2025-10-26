import requests
import time
import json


# IMPORTANT: Replace 'YOUR_API_KEY' with your actual Gemini API key.
API_KEY = "AIzaSyAbKZo1s-_eR8mL-U6rMBExVKhtMvbobtk"
MODEL_NAME = 'gemini-2.5-flash-preview-09-2025'
API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent'

def online_assistant(prompt: str, system_instruction: str = None, max_retries: int = 3) -> str | bool:
    """
    Checks API reachability, sends prompt to Gemini API, and handles errors/retries.

    Returns:
        The generated text (str) on success, or False (bool) on any failure.
    """
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": API_KEY
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}]
    }

    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    for i in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, params=params, json=payload, timeout=15)

            if response.status_code == 429 and i < max_retries - 1:
                delay = 2 ** i
                print(f"API rate limit hit (429). Retrying in {delay} seconds...")
                time.sleep(delay)
                continue

            if not response.ok:
                # API is reachable but returned an error status (4xx/5xx)
                print(f"API Error ({response.status_code}): {response.json().get('error', {}).get('message', 'Unknown Error')}")
                return False

            # Success: extract and return generated text
            result = response.json()
            generated_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

            # Note: We skip extracting sources here to return only the text as requested
            return generated_text

        except requests.exceptions.Timeout:
            if i < max_retries - 1:
                delay = 2 ** i
                print(f"Request timed out. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            # Fall-through to final False return on persistent timeout

        except requests.exceptions.RequestException as e:
            if i < max_retries - 1:
                delay = 2 ** i
                print(f"Transient network error: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue

            # Persistent network failure
            print(f"Persistent network error: {e}")
            return False

  
    return False