from collections import Counter, defaultdict
from datetime import timedelta

def format_time(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"

def generate_ytmusic_report(wrapper, history_limit=10000):
    # Fetch history
    history = wrapper.get_history()[:history_limit]
    total_tracks = len(history)
    unique_tracks = len({t.get('videoId', t.get('title', '')) for t in history})

    # Estimate total listening time (YouTube Music history does not provide durations, so we estimate)
    # Default average: 3.5 minutes per track if duration missing.
    total_minutes = 0
    artist_counter = Counter()
    album_counter = Counter()
    track_counter = Counter()
    track_album_map = {}
    track_artist_map = defaultdict(list)

    for track in history:
        title = track.get('title', 'Unknown')
        album = track.get('album', {}).get('name') if track.get('album') else 'Unknown'
        artists = [a.get('name', 'Unknown') for a in track.get('artists', [{'name': 'Unknown'}])]
        duration_str = track.get('duration')
        if duration_str:
            # duration is in format "3:41" or "56"
            parts = duration_str.split(':')
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = int(parts[1])
                duration = minutes * 60 + seconds
            else:
                duration = int(parts[0])
            total_minutes += duration // 60
        else:
            total_minutes += 3.5  # Estimate
        artist_counter.update(artists)
        album_counter[(album, ', '.join(artists))] += 1
        track_counter[(title, ', '.join(artists))] += 1
        track_album_map[(title, ', '.join(artists))] = album
        track_artist_map[title].extend(artists)

    # Structure text output
    report_lines = []
    report_lines.append("🎵 YouTube Music Analytics Report (All Time)")
    report_lines.append("=" * 50)
    report_lines.append("")
    report_lines.append(f"⏱ Total Listening Time: {format_time(int(total_minutes))}")
    report_lines.append(f"🎵 Total Tracks Played: {total_tracks}")
    report_lines.append(f"🔀 Unique Tracks: {unique_tracks}")
    report_lines.append("")
    report_lines.append("❤ Top Artists:")
    for i, (artist, plays) in enumerate(artist_counter.most_common(5), 1):
        # Calculate artist time (approx)
        artist_minutes = int((plays / total_tracks) * total_minutes) if total_tracks else 0
        report_lines.append(
            f"  {i}. {artist} - {format_time(artist_minutes)} ({plays} plays)"
        )
    report_lines.append("")
    report_lines.append("🏆 Top Albums:")
    for i, ((album, album_artist), plays) in enumerate(album_counter.most_common(5), 1):
        album_minutes = int((plays / total_tracks) * total_minutes) if total_tracks else 0
        report_lines.append(
            f"  {i}. {album} - {album_artist} - {format_time(album_minutes)} ({plays} plays)"
        )
    report_lines.append("")
    report_lines.append("🔥 Most Played Tracks:")
    for i, ((title, artists), plays) in enumerate(track_counter.most_common(5), 1):
        report_lines.append(
            f"  {i}. {title} - {artists} - {plays} plays"
        )

    return "\n".join(report_lines)

# Example usage with your wrapper:
if __name__ == "__main__":
    from ytmusic_analytics_wrapper import YTMusicAnalyticsWrapper

    # Fill your credentials here as before
    CLIENT_ID = "YOUR_CLIENT_ID.apps.googleusercontent.com"
    CLIENT_SECRET = "YOUR_CLIENT_SECRET"
    REDIRECT_URIS = ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]

    wrapper = YTMusicAnalyticsWrapper(
        user_token_path="oauth.json",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uris=REDIRECT_URIS
    )

    print(generate_ytmusic_report(wrapper, history_limit=10000))
