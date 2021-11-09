import time  # time module
import webbrowser  # helps to open links in web browser
import pyautogui  # gui automation like click, press, hotkeys(like ctrl+C)
import spotipy  # spotify module to get music links
from spotipy.oauth2 import SpotifyClientCredentials # to get access token for spotify api to play music on web browser 

# api key generated on Spotify developers portal
api_key = "52108268a761458484e2f2392f60f239"
# verifying with spotify developers portal
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="a0865855c7d74e6a9c09a92fbb48db43", client_secret=api_key))


# function to facilitate music playing
def play_sound(song):
    # search music with given word and search results are limited to 1
    results = sp.search(q=song, limit=1)
    # extracting links data received from api
    data = results['tracks']['items'][0]['external_urls']['spotify']
    # open the url in default web browser
    webbrowser.open(data)
    # stopping the current thread(process) for 7 seconds can changed according to system performance and connectivity
    time.sleep(7)
    # click on play button on web
    pyautogui.click(x=375, y=700)
    # wait for song to start
    time.sleep(5)
    # redirect back to working arena
    pyautogui.hotkey('alt', 'tab')