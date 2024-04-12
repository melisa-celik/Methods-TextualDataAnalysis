import requests
import os

class BookDownloader:
    def __init__(self):
        self.baseUrl = "https://www.gutenberg.org/files/"

    def download(self, limit=100):
        if not os.path.exists("Gutenberg"):
            os.makedirs("Gutenberg")

        i = 1
        num = 0
        while num < limit:
            book = str(i) + "-0.txt"
            extendedUrl = self.baseUrl + str(i) + "/" + book

            r = requests.get(extendedUrl)
            content = str(r.content)
            if not "<!DOCTYPE" in content:
                open("Gutenberg/" + book, 'wb').write(r.content)
                num += 1

            i += 1
