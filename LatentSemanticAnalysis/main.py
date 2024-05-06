from LSA.LSA import *
from time import sleep

def loadTextFromFile(filePath):
    with open(filePath, 'r', encoding='ISO-8859-1') as file:
        text = file.read()
    return text

def main():
    print("\n---Latent Semantic Analysis---")

    filePath = "C:\\Users\\Lenovo\\PycharmProjects\\Methods-TextualDataAnalysis\\StringSearching\\english.50MB"
    fileName = "english.50MB"

    print(f"\nLoading the Book of {fileName}...")
    text = loadTextFromFile(filePath)
    sleep(1)
    print(f"Text from {fileName} loaded successfully!\n")

    print("-----------------------------------------------------------------------------------------------------------")
    lsa = LSA(text=text)

    print(f"\nInitializing Vector Model {lsa}")
    sleep(1)
    print("The Model for Latent Semantic Analysis created successfully!\n")

    print("-----------------------------------------------------------------------------------------------------------")
    print("Extracting most significant sentences and terms...")
    sleep(1)
    highestSentences, lowestSentences = lsa.getMostSignificantSentences(2)
    highestTerms, lowestTerms = lsa.getMostSignificantTerms(5)

    print("Most Significant Sentences (Highest):")
    for sentence in highestSentences:
        print("- ", sentence)

    print("\nMost Significant Sentences (Lowest):")
    for sentence in lowestSentences:
        print("- ", sentence)

    print("\nMost Significant Terms (Highest):", highestTerms)
    print("Most Significant Terms (Lowest):", lowestTerms)


if __name__ == "__main__":
    main()