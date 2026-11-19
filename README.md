# iVysilani MPD extractor

This program extracts the `.mpd` DASH manifest URL from a Česká televize iVysílání page using its public stream API. It does not require Selenium or Chrome.

## Install

Install Python and dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

Run:

```powershell
python extract.py
```

Optional arguments:

- `-u, --url <URL>` — extract from a specific iVysílání URL
- `-d, --download` — download with `yt-dlp` if it is available in `PATH`

Example:

```powershell
python extract.py -u "https://www.ceskatelevize.cz/porady/16866898966-pan-nikdo-proti-putinovi/"
```

The printed MPD URL can be used directly with tools such as `yt-dlp` or VLC.

Restricted, DRM-only, unavailable, or missing-rights videos are reported by the ČT stream API and skipped.

## Troubleshooting

If `yt-dlp` is not found, install it and ensure it is available through `PATH`.

If extraction fails, verify that the URL is public and still available, and open an issue with the URL and error message.

