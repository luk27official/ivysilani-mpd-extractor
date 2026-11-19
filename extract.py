from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

import requests

STREAM_API = "https://api.ceskatelevize.cz/video/v1/playlist-vod/v1/stream-data/media/external/{idec}"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0.0.0 Safari/537.36"


def get_idec(url: str) -> tuple[str, str]:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
        timeout=30,
    )
    response.raise_for_status()

    match = re.search(r"IDEC=([0-9]+)", response.text)
    if not match:
        match = re.search(r"/porady/[\" ]*/([0-9]+)/?", response.url)
    if not match:
        raise RuntimeError("Could not find the video IDEC in the page")

    title_match = re.search(r"<title[^>]*>(.*?)</title>", response.text, re.DOTALL | re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "video"
    title = re.sub(r"\s*[|–-]\s*(iVysílání|Česká televize)$", "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s+", " ", title).replace("/", "_").replace("\\", "_")
    return match.group(1), title


def get_stream(idec: str) -> str:
    response = requests.get(
        STREAM_API.format(idec=idec),
        params={
            "canPlayDrm": "false",
            "quality": "web",
            "streamType": "dash",
            "origin": "ivysilani",
        },
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
        timeout=30,
    )

    data = response.json()
    if response.status_code >= 400:
        message = data.get("message", {})
        labels = message.get("labels", {}) if isinstance(message, dict) else {}
        detail = labels.get("textShort") or labels.get("generalError") or "Video is unavailable"
        raise RuntimeError(detail)

    streams = data.get("streams") or []
    if not streams:
        raise RuntimeError("The API returned no playable stream")
    return streams[0]["url"]


def extract(url: str, download: bool = False, folder: str = "") -> None:
    idec, title = get_idec(url)
    print("Loaded URL:", url)
    print("Video IDEC:", idec)

    mpd_url = get_stream(idec)
    print("MPD:", mpd_url)

    if download:
        subprocess.call(["yt-dlp", "--no-overwrites", "-o", os.path.join(folder, title) + ".%(ext)s", mpd_url])


def main(args: argparse.Namespace) -> int:
    url = args.url or input(
        "Enter URL (e.g.: https://www.ceskatelevize.cz/porady/16866898966-pan-nikdo-proti-putinovi/): "
    )

    try:
        extract(url, download=args.download)
    except (requests.RequestException, RuntimeError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract the DASH MPD URL from a Česká televize iVysílání URL")
    parser.add_argument("-u", "--url", help="URL of the video", default="", dest="url")
    parser.add_argument("-d", "--download", help="Download with yt-dlp", action="store_true")
    args = parser.parse_args()

    sys.exit(main(args))
