import requests

def fetch_signal(signal_url):
    response = requests.get(signal_url)
    response.raise_for_status()
    return response.json()
