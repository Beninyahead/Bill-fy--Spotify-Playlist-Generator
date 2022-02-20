from bs4 import BeautifulSoup
import requests

class BillboardScrapper:
    """Class responsible for scraping the song and artist data from the Billboard Website"""
    def __init__(self, url:str, date:str) -> None:
        self.url_endpoint = f"{url}{date}/"
    
    def scrap_billboard(self):
        """Scrap target billboard for song names and artist names.

        Returns:
            dict {str:str}: track_data dictionary: 
            {
                'songs': songs,
                'artists': artists
            }
        """
        print('Scrapping data from billboard')
        response = requests.get(self.url_endpoint)
        response.raise_for_status()
        site_data = response.text

        soup = BeautifulSoup(site_data, 'html.parser')
        # Archived site - search for songs in html class and span
        song_names_spans = soup.find_all("span", class_="chart-element__information__song")
        songs = [song_name.getText() for song_name in song_names_spans]
        
        artist_names_spans = soup.find_all("span", class_='chart-element__information__artist')
        artists = [artist_name.getText() for artist_name in artist_names_spans]
        
        track_data = {
            'songs': songs,
            'artists': artists
        }
        return track_data
