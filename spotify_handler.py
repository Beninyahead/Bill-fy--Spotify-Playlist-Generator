import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser

class SpotifyHandler:
    
    def __init__(self, client_id:str, client_secret:str) -> None:
        """Args:
            client_id (str): Spotify Developer Account client id
            client_secret (str): Spotify Developer Account client secret
        """
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.sp = None
        self.USER_ID = None
        self.setup_spotify_oauth()

    def setup_spotify_oauth(self):
        """Sets up spotify oath through spotipy connection, set user id 
        """
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                client_secret=self.CLIENT_SECRET,
                                                redirect_uri="http://example.com",
                                                scope="playlist-modify-private",
                                                show_dialog=True,
                                                cache_path=".cache")
        )
        self.USER_ID = self.sp.current_user()['id']

    def search_for_song_on_spotify(self, track_data:dict, year:str):
        """Iterate through song list, for each song use spotipy api search to fnd song uri:
        * 1). Search for uri using song and artist.
        * 2). if song and artist api search does not result in any uri, search on song and year.
        * 3). if song and year does not result in any uri data, search on song name only.
        * Add song uri to uri list

        Args:
            track_data (dict): Dict conaitain songs and artist key value pairs
            year (str): year of publication of billboard eg 2016
        
        Returns:
            list: List of spotify song uris
        """  
        songs:list = track_data['songs']
        artists:list =track_data['artists']

        song_uris = []
        for song in songs:
            index = songs.index(song)
            artist = artists[index]
            # Try and get song title and artist title
            query =f'track: {song} artist: {artist}'
            results = self.sp.search(q=query,limit=1,type="track")
            try:
                uri =results["tracks"]["items"][0]["uri"]
                song_uris.append(uri)
            except IndexError:
                print(f"song:'{song}' and artist:'{artist}' doesn't exist. Searching by Year")
                # Try and get song title and year
                query =f'track: {song} year: {year}'
                results = self.sp.search(q=query,limit=1,type="track")
                try:
                    uri =results["tracks"]["items"][0]["uri"]
                    song_uris.append(uri)
                except IndexError:
                    print(f"song:'{song}' and year:{year}' doesn't exist. Searching by song title")
                    # Try and get song
                    query =f'track: {song}'
                    results = self.sp.search(q=query,limit=1,type="track")
                    try:
                        uri =results["tracks"]["items"][0]["uri"]
                        song_uris.append(uri)
                    except IndexError:
                        print(f"song:'{song}' doesn't exist")
        return song_uris

    def create_user_playlist(self, date:str, song_uris:list):
        """Create a new playlist for the provided song uris.
        Open the browser to display playlist once done.

        Args:
            date (str): Billboard Date as a string
            song_uris (list): List of song uris in order
        """
        playlist = self.sp.user_playlist_create(self.USER_ID, f'{date} Billboard 100', public=False, collaborative=False, description=f'Billboards Top 100 as at {date}.')
        self.sp.playlist_add_items(playlist['id'], items=song_uris)
        print('Playlist Created')
        external_url = playlist['external_urls']['spotify']
        webbrowser.open(external_url,2)