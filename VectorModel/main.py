from Part1.VectorModel import *
from time import sleep

def main():
    print("\n---Vector Space Model---")

    filePath = "Documents.json"
    model = VectorModel(filePath)

    print(f"\nInitializing Vector Model {model}")
    sleep(1)
    print("Vector Model created successfully!\n")

    print("-----------------------------------------------------------------------------------------------------------")
    print(f"\nLoading Documents {filePath}...")
    sleep(1)
    print("Documents loaded successfully!\n")

    print("-----------------------------------------------------------------------------------------------------------")
    print("\nProcessing Queries...\n")
    sleep(1)

    queries = [
        "artificial intelligence",
        "machine learning",
        "data science",
        "biotechnology renewable energy",
        "autonomous vehicles",
        "deep learning",
        "computer vision",
        "natural language processing",
        "reinforcement learning",
        "robotics",
        "internet of things",
        "neural networks",
        "cloud computing",
        "blockchain",
        "computer"
    ]

    for query in queries:
        queryTerms = query.split()
        results = model.scoreDocuments(queryTerms)
        print(f"Query: {query}")
        for docId, score in results:
            print(f"Document ID: {docId}, Score: {score}")
            sleep(0.001)
        print()
        sleep(1)

if __name__ == "__main__":
    main()