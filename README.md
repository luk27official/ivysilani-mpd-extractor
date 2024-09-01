# iVysilani MPD extractor

*Czech disclaimer: V případě problému prosím založte issue, pro běh skriptu stačí nainstalovat Selenium packge a skript pustit.*

This program extracts the `.mpd` file from a given iVysilani (ceskatelevize.cz) URL using Selenium. This `.mpd` file then may be used to download the video via various tools.

Feel free to [open an issue](https://github.com/luk27official/ivysilani-mpd-extractor/issues/new/choose) or create a PR.

## Install

Install Python and install Selenium Python package, either by `pip install selenium` or run `pip install -r requirements.txt`

## Usage

Run `python extract.py`.

There are three optional arguments:
- `-u, --url <URL>` - runs the program directly on a given URL, otherwise the program asks for the URL
- `-d, --download` - if present, downloads the video with [yt-dlp](https://github.com/yt-dlp/yt-dlp), assuming `yt-dlp` is in `PATH` (or any other env vars)
- `-n, --no-headless` - runs the program without the `--headless` option in Chrome, this means the program will create a Chrome testing tab, which is otherwise hidden, sometimes needed for videos

The `.mpd` link might be used in various tools enabling video downloads from the manifest files, e.g. `yt-dlp` or `VLC`. For `yt-dlp`, just run `yt-dlp <mpd_URL>`.

## Troubleshooting

If the MPD list is empty, try changing the waiting times and/or the CDN link (the current one can be found in the Networks tab in developer console). Also, for some series or movies, the `--no-headless` flag must be provided, otherwise it is not possible to get the `.mpd`.

If there are any issues with elements, try changing the XPath or CSS selectors.

If you are not a developer or the problem is not listed here, please let me know what the problem is and [open an issue](https://github.com/luk27official/ivysilani-mpd-extractor/issues/new/choose).
