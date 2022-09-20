import collections
from pprint import pprint
from pydoc import pager

import requests
from bs4 import BeautifulSoup


def extract_lyrics(url):
    print("Fetching lyrics...")
    r = requests.get(url)
    if r.status_code != 200:
        print("Error")                 

    soup = BeautifulSoup(r.content, 'html.parser')
    lyrics = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
    if not lyrics:
        return extract_lyrics(url)

    all_words = []
    for sentence in lyrics.stripped_strings:
        sentence_words =[word.strip(".,").lower() for word in sentence.split()]
        all_words.extend(sentence_words)

    counter = collections.Counter(all_words)
    print(counter.most_common(5))

    #pprint(all_words)

def get_all_urls():
    page_number = 1
    links = [] 
    while True:
        r = requests.get(f"https://genius.com/api/artists/63068/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            response = r.json().get('response',{})
            next_page = response.get('next_page')

            songs = response.get('songs')
            links.extend([song.get('url')for song in songs])
            page_number += 1

            if not next_page:
                print("no more pages to fetch.")
                break
    
    pprint(links)
    pprint(len(links))

get_all_urls()
print("encore et encore:")
extract_lyrics(url="https://genius.com/Francis-cabrel-encore-et-encore-lyrics")



