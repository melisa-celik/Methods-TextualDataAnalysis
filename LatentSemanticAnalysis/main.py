from LSA_Model.LSA import LSA
from time import sleep

def loadTextFromFile(filePath):
    with open(filePath, 'r', encoding='ISO-8859-1') as file:
        text = file.read()
    return text

def main():
    print("\n---Latent Semantic Analysis---")

    filePath = "TestText.txt"
    fileName = "Test Text"

    print(f"\nLoading the Book of {fileName}...")
    text = loadTextFromFile(filePath)
    sleep(1)
    print(f"Text from {fileName} loaded successfully!\n")

    print("-----------------------------------------------------------------------------------------------------------")
    lsa = LSA(text=text)
    tf_matrix, terms = lsa.construct_tf_matrix(lsa.sentences, max_features=1000)
    U, S, V_T = lsa.applySVD(tf_matrix, n_components=100)

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