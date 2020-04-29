import os
import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def downloader(url):
    time.sleep(2)
    return url


def main(urls):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = executor.submit(downloader, urls)

        while futures.running():
            yield "teste"
            time.sleep(1)
        yield futures.result()


if __name__ == '__main__':
    urls = "http://www.irs.gov/pub/irs-pdf/f1040.pdf"
    print(main(urls))