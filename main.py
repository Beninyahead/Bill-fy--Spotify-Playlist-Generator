import os
from dotenv import load_dotenv
from calendar import weekday
from datetime import datetime, timedelta

from billboard_web_scrapper import BillboardScrapper
from spotify_handler import SpotifyHandler

# Constants:
load_dotenv()# Spotify Client .env Files
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Billboard URL
URL = 'https://web.archive.org/web/20201026231157/https://www.billboard.com/charts/hot-100/'

# Date Handling
WEEKDAY = 5
DATE_FORMAT = '%Y-%m-%d'

# Entry Point
if __name__ == '__main__':
    # Date cannot be greater than 2020/10/14 
    date = input('Enter a date in the format of YYYY-MM-DD (A date before 2020-10-14): ')
    year = date.split('-')[0]

    # Convert to datetime
    date = datetime.strptime(date,DATE_FORMAT)
    # Adjust date to saturday  billboard weeks run from sunday to saturday)
    if date.weekday() != WEEKDAY:
        adjust_days = WEEKDAY - date.weekday() 
        date = date + timedelta(days=adjust_days)

    date = date.strftime(DATE_FORMAT)
    print(f'Billbooard Week Ending: {date}')

    spotify_handler = SpotifyHandler(CLIENT_ID,CLIENT_SECRET)
    bill_board = BillboardScrapper(URL, date)

    # Scrap data, find uris, create playlist
    track_data =  bill_board.scrap_billboard()
    song_uris = spotify_handler.search_for_song_on_spotify(track_data,year)
    spotify_handler.create_user_playlist(date, song_uris)