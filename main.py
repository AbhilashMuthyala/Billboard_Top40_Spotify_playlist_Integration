import requests
from bs4 import BeautifulSoup
import spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

user_input = input("Enter the date in this format YYYYMMDD")
base_url = "https://www.officialcharts.com/charts/singles-chart/"

SPOTIPY_CLIENT_ID='<>'
SPOTIPY_CLIENT_SECRET='<>'
redirect_uri="<>"

response=requests.get(base_url+user_input)
soup = BeautifulSoup(response.text,"html.parser")
title_raw_list = soup.find_all(name="div", class_="title")
title_list = []
for title in title_raw_list:
    title_soup = BeautifulSoup(str(title),"html.parser")
    title_text = title_soup.find(name="a").string
    title_list.append(title_text)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=redirect_uri,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()['id']

playlist = sp.user_playlist_create(user=user_id,name=f"Billboard_Top40_{user_input}",public=False,description="Billboard playlist")

spotify_id_list = []
for ele in title_list:
    res = sp.search(q=f"track:{ele}",limit=1,market=None,offset=0)
    try:
        spotify_id_list.append(res["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"{ele} doesn't exist in Spotify. Skipped.")
res1 = sp.playlist_add_items(playlist_id=playlist["id"],items=spotify_id_list,position=None)


