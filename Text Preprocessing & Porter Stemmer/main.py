import os
import time
from TextFromBook.BookDownloader import BookDownloader
from TextFromBook.TextExtractor import Text

def calculateElapsedTime(startTime):
    endTime = time.time()
    elapsedTime = endTime - startTime
    print("Elapsed Time:", elapsedTime, "seconds")

def main():
    startTime = time.time()
    inputFolder = 'Gutenberg'
    outputFolder = 'Preprocessed Books'

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    downloader = BookDownloader()
    print("Downloading books...")
    downloader.download()
    calculateElapsedTime(startTime)

    print("Books downloaded successfully")

    startTime = time.time()
    textProcessor = Text(inputFolder, outputFolder)

    print("Preprocessing books...")
    textProcessor.preprocessBooks()
    calculateElapsedTime(startTime)

    print("Books preprocessed successfully")

if __name__ == '__main__':
    main()
