import requests
import os
from bs4 import BeautifulSoup
import time
import logging
from plyer import notification

URL_TO_MONITOR = "https://gog-games.to/"
DELAY_TIME = 180  # seconds

def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select('script'):
        s.extract()

    # remove meta tags
    for s in soup.select('meta'):
        s.extract()

    # remove style tags
    for s in soup.select('style'):
        s.extract()

    # remove span tags
    for s in soup.select('span'):
        s.extract()

    # remove head tags
    for s in soup.select('head'):
        s.extract()

    # remove header tags
    for s in soup.select('header'):
        s.extract()

    # remove h1 tags
    for s in soup.select('h1'):
        s.extract()

    # remove h2 tags
    for s in soup.select('h2'):
        s.extract()

    # remove h3 tags
    for s in soup.select('h3'):
        s.extract()

    # remove p tags
    for s in soup.select('p'):
        s.extract()

    # remove br tags
    for s in soup.select('br'):
        s.extract()

    # remove img tags
    for s in soup.select('img'):
        s.extract()

    # convert to a string, remove some things, and return
    return str(soup).replace('Last Update: ', '').replace('</div></a><a class="block" ', '').replace('</div>', '').replace('</a>', '').replace(' ', '').replace('\n', '')


def webpage_was_changed():
    """Returns true if the webpage was changed, otherwise false."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"):
        open("previous_content.txt", 'w+').close()

    filehandle = open("previous_content.txt", 'r')
    previous_response_html = filehandle.read()
    filehandle.close()

    processed_response_html = process_html(response.text)

    if processed_response_html == previous_response_html:
        return False
    else:
        filehandle = open("previous_content.txt", 'w', encoding="utf-8")
        filehandle.write(processed_response_html)
        filehandle.close()
        return True


def main():
    log = logging.getLogger(__name__)
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
    log.info("Running Website Monitor")
    while True:
        try:
            if webpage_was_changed():
                log.info("WEBPAGE WAS CHANGED.")
                notification.notify(
                    title='GOG Alert',
                    message='GOG-Games.to has been updated!',
                    app_icon="gog.ico",
                    timeout=10,
                )
            else:
                log.info("Webpage was not changed.")
        except Exception as e:
            log.info(e)
        time.sleep(DELAY_TIME)

if __name__ == "__main__":
    main()
