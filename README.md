# iVysilani MPD extractor

This program extracts the `.mpd` file from a given iVysilani (ceskatelevize.cz) URL using Selenium. This `.mpd` file then may be used to download the video via various tools.

Feel free to open an issue or create a PR.

## Install

Install Python and install Selenium Python package, either by `pip install selenium` or run `pip install -r requirements.txt`

## Usage

Run `python extract.py`.

There are two optional arguments:
- `-u, --url <URL>` - runs the program directly on a given URL, otherwise the program asks for the URL
- `-d, --download` - if present, downloads the video with [yt-dlp](https://github.com/yt-dlp/yt-dlp), assuming `yt-dlp` is in `PATH` (or any other env vars)

The `.mpd` link might be used in various tools enabling video downloads from the manifest files, e.g. `yt-dlp` or `VLC`. For `yt-dlp`, just run `yt-dlp <mpd_URL>`.
