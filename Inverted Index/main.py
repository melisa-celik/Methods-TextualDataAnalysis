from Operations.QuerySystem import QuerySystem
from Operations.IndexInverter import InvertedIndex

def main():
    documents = {
        1: "Friends, Romans, countrymen. So let it be with Caesar.",
        2: "Brutus −→ 1 2 4 11 31 45 173 174",
        3: "Caesar −→ 1 2 4 5 6 16 57 132",
        4: "Calpurnia −→ 2 31 54 101"
    }

    inverted_index = InvertedIndex()
    inverted_index.buildIndex(documents)

    query_processor = QuerySystem(inverted_index)

    # Testing query: word1 AND word2 AND word3
    query = "Brutus AND Caesar AND Calpurnia"
    result = query_processor.processQuery(query)
    print("Documents containing all words:", result)


if __name__ == "__main__":
    main()