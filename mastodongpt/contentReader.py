import requests
from bs4 import BeautifulSoup

def fetch_clean_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        clean_text = soup.get_text(separator=" ", strip=True)

        return clean_text
    except requests.exceptions.RequestException as e:
        return f"Error fetching page: {e}"

