import os
from ytmusicapi import YTMusic
from typing import List, Dict, Any

class YTMusicAnalyticsWrapper:
    """
    Wrapper and analytics suite for YouTube Music using ytmusicapi.
    This uses the new OAuth authentication method as per ytmusicapi 1.4+.
    """

    def __init__(
        self,
        user_token_path: str = "oauth.json",
        client_id: str = "",
        client_secret: str = "",
        redirect_uris: list = None
    ):
        if not os.path.exists(user_token_path):
            raise FileNotFoundError(
                f"Could not find user token at {user_token_path}. "
                "Run 'ytmusicapi oauth' to generate this file after setting up OAuth credentials."
            )
        if not client_id or not client_secret or not redirect_uris:
            raise ValueError(
                "client_id, client_secret, and redirect_uris must be provided directly in code."
            )
        oauth_credentials = {
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uris": redirect_uris
        }
        self.ytmusic = YTMusic(user_token_path, oauth_credentials=oauth_credentials)

    def get_liked_songs(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.ytmusic.get_liked_songs(limit=limit)["tracks"]

    def get_history(self) -> List[Dict[str, Any]]:
        return self.ytmusic.get_history()

    def get_playlists(self) -> List[Dict[str, Any]]:
        return self.ytmusic.get_library_playlists()

    def get_playlist_tracks(self, playlist_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        playlist = self.ytmusic.get_playlist(playlist_id, limit=limit)
        return playlist.get("tracks", [])

    def analyze_top_artists(self, tracks: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, int]]:
        from collections import Counter
        artist_counter = Counter()
        for track in tracks:
            if "artists" in track:
                for artist in track["artists"]:
                    artist_counter[artist["name"]] += 1
        return artist_counter.most_common(top_n)

    def analyze_top_songs(self, tracks: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, int]]:
        from collections import Counter
        song_counter = Counter()
        for track in tracks:
            title = track.get('title', 'Unknown')
            artists = ', '.join(a.get('name', 'Unknown') for a in track.get('artists', [{}]))
            name = f"{title} - {artists}"
            song_counter[name] += 1
        return song_counter.most_common(top_n)

    def search(self, query: str, filter: str = "songs", limit: int = 10) -> List[Dict[str, Any]]:
        return self.ytmusic.search(query, filter=filter, limit=limit)
