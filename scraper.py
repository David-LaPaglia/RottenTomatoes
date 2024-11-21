import json
import datetime
import os
import requests
from bs4 import BeautifulSoup

# Record the current time
current_timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Retrieve movie URL from environment variable or fallback
movie_url = os.getenv('MOVIE_URL', 'https://www.rottentomatoes.com/m/venom_the_last_dance')

def rotten_tomatoes_soup(url):
    """
    Retrieve a website and convert its content into BeautifulSoup.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, features='html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def parse_data(soup, ts):
    """
    Parse the Soup of a Rotten Tomatoes page into a dictionary.
    """
    try:
        details_d = {
            'timestamp': ts,
            'critics_score': soup.find('rt-text', {'slot': 'criticsScore'}).text if soup else 'N/A',
            'critics_count': soup.find('rt-link', {'slot': 'criticsReviews'}).text.strip() if soup else 'N/A',
            'audience_score': soup.find('rt-text', {'slot': 'audienceScore'}).text if soup else 'N/A',
            'audience_count': soup.find('rt-link', {'slot': 'audienceReviews'}).text.strip() if soup else 'N/A',
        }
        return details_d
    except AttributeError as e:
        print(f"Error parsing data: {e}")
        return {
            'timestamp': ts,
            'critics_score': 'N/A',
            'critics_count': 'N/A',
            'audience_score': 'N/A',
            'audience_count': 'N/A',
        }

def update_data(filename, data):
    """
    Append a dictionary to a list of dictionaries in a JSON file.
    """
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
        data_list.append(data)
    else:
        data_list = [data]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data_list, f)

def main():
    """
    Retrieve content, parse data, and update JSON file.
    """
    soup = rotten_tomatoes_soup(movie_url)
    data = parse_data(soup=soup, ts=current_timestamp)
    update_data('data.json', data)

if __name__ == "__main__":
    main()
