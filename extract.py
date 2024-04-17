from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import subprocess
import argparse
import sys
import re

# css selectors
COOKIE_ACCEPT_BUTTON_ID = "onetrust-accept-btn-handler"
VIDEO_CLASS_NAME = "playerPageWrapper"
MOVIE_RUN_XPATH = '//button[contains(@aria-label, "Přehrát")]'
AD_SKIP_BUTTON_XPATH = '//span[text()="Přeskočit"]'
AD_18_SKIP_BUTTON_XPATH = '//span[text()="Přeskočit"]'

# wait times
AD_WAIT_TIME = 10
AD_18_WAIT_TIME = 10
VIDEO_LOAD_WAIT_TIME = 5

# other constants
CDN_REGEX = r"https:\/\/.+\.o2tv\.cz\/cdn.*"


def main(args):
    """Extracts the MPD URL from the given URL using Selenium and optionally downloads the video with yt-dlp"""
    url = (
        args.url
        if args.url != ""
        else input("Enter URL (e.g.: https://www.ceskatelevize.cz/porady/10640154216-most/214381477720001/): ")
    )

    options = Options()

    options.add_argument("window-size=1920x1080")
    if not args.no_headless:
        options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-gpu")
    options.add_argument("--mute-audio")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-web-security")  # allows to bypass CORS
    options.add_argument("--disable-site-isolation-trials")

    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    chrome = webdriver.Chrome(options=options)
    chrome.get(url)
    print("Loaded URL: ", url)

    chrome.implicitly_wait(1)

    chrome.find_element(By.ID, COOKIE_ACCEPT_BUTTON_ID).click()
    print("Clicked cookie accept button")

    try:
        chrome.find_element(By.CLASS_NAME, VIDEO_CLASS_NAME).click()
        print("Clicked on the video - detected series")
    except:
        chrome.find_element(By.XPATH, MOVIE_RUN_XPATH).click()
        print("Clicked on the video - detected movie")

    chrome.switch_to.frame(chrome.find_element(By.TAG_NAME, "iframe"))

    try:
        WebDriverWait(chrome, AD_WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, AD_SKIP_BUTTON_XPATH))
        ).click()
        print("Skipped ad")
    except:
        print("No ad to skip")

    try:
        WebDriverWait(chrome, AD_18_WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, AD_18_SKIP_BUTTON_XPATH))
        ).click()
        print("Skipped 18+ warning")
    except:
        print("No 18+ warning to skip")

    # wait for the video to load
    print("Waiting for the video to load...")
    time.sleep(VIDEO_LOAD_WAIT_TIME)

    # go to the networks console and find the latest .mpd file
    # the script simplifies the entries because there might be circular references
    timings = chrome.execute_script("return window.performance.getEntries().map(entry => entry.name);")
    timings_json = json.dumps(timings)
    timings_json = json.loads(timings_json)

    mpd_list = []

    for timing in timings_json:
        if re.match(CDN_REGEX, timing):
            mpd_list.append(timing)

    print("Done.")
    print("MPD list: ", mpd_list)
    print("")
    if len(mpd_list) > 0:
        print("Most recent MPD: ", mpd_list[-1])
    else:
        print("No MPD found. Try running the script with the --no-headless flag.")
        sys.exit(1)

    title = chrome.title.replace("/", "_").replace("\\", "_")
    chrome.quit()

    if args.download:
        subprocess.call(["yt-dlp", "-o", title + ".%(ext)s", mpd_list[-1]])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL to the video", default="", type=str, dest="url")
    parser.add_argument(
        "-d",
        "--download",
        help="Download the video with yt-dlp, if in PATH",
        default=False,
        dest="download",
        action="store_true",
    )
    parser.add_argument(
        "-n",
        "--no-headless",
        help="Run in a window (no --headless option)",
        default=False,
        dest="no_headless",
        action="store_true",
    )
    args = parser.parse_args()

    main(args)
