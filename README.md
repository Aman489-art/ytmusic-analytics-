# YouTube Music Analytics

A Python toolkit to generate listening reports and analytics for your YouTube Music account using [ytmusicapi](https://github.com/sigma67/ytmusicapi).

## Features

- Fetch your YouTube Music history and liked songs
- Generate detailed analytics reports: top artists, albums, tracks, total listening time, and more
- Uses OAuth for secure authentication

## Project Structure

```
ytmusic-analytics/
│
├── yt.py                       # Main script to generate the analytics report
├── ytmusic_analytics_wrapper.py # Wrapper for ytmusicapi with analytics methods
├── requirements.txt            # Dependencies
├── README.md                   # This documentation
```

## Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Aman489-art/ytmusic-analytics.git
   cd ytmusic-analytics
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up OAuth:**
   - Follow the [ytmusicapi OAuth guide](https://ytmusicapi.readthedocs.io/en/latest/setup.html#oauth) to generate your `oauth.json`.
   - Place `oauth.json` in the project directory.

4. **Configure API credentials:**
   - In `yt.py`, fill in your `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URIS`.

## Usage

```sh
python yt.py
```

The script will output your all-time YouTube Music analytics report.

## License

MIT (or your preferred license)
