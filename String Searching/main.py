import time
import sys
import random
from SearchTypes.BruteForce import BruteForceSearch
from SearchTypes.FiniteAutomaton import FiniteAutomatonSearch, DeterministicFiniteAutomatonSearch, NonDeterministicFiniteAutomatonSearch
from SearchTypes.Naive import NaiveSearch
from SearchTypes.BoyerMooreHorspool import BoyerMooreHorspoolSearch
from SearchTypes.RegularExpression import RegularExpressionSearch

def measure_time(search_func, search_type, *args, **kwargs):
    start_time = time.time()
    result = search_func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{search_type} Search Time:", execution_time)
    return result, execution_time

def load_text(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        return file.read()

def generate_random_words_from_text(text, word_length, number_of_words):
    words = []
    for _ in range(number_of_words):
        start = random.randint(0, len(text) - word_length)
        words.append(text[start:start + word_length])
    return words

if __name__ == "__main__":

    text = load_text("english.50MB")
    word_to_search = "survey"
    random_words = generate_random_words_from_text(text, len(word_to_search), 1000)
    regex = "a(b|c)*"
    brute_force_search = BruteForceSearch()
    dfa_search = DeterministicFiniteAutomatonSearch()
    regex_search = RegularExpressionSearch(regex=regex)
    naive_search = NaiveSearch()
    fa_search = FiniteAutomatonSearch(word_to_search)
    bmh_search = BoyerMooreHorspoolSearch(word_to_search)
    ndfa_search = NonDeterministicFiniteAutomatonSearch(word_to_search, 2)

    brute_force_occurrences, brute_force_time = measure_time(brute_force_search.search, "Brute Force", word_to_search, text)
    dfa_occurrences, dfa_time = measure_time(dfa_search.search, "Deterministic Finite Automaton", text, word_to_search)

    print(f"\nWord to search: {word_to_search}")
    print("\n")
    print("Brute Force Search Time:", brute_force_time)
    print("Occurrences found using brute force search:", len(brute_force_occurrences))
    # print("Brute Force occurrences:", brute_force_occurrences)  # Debugging
    print("\n")
    print("Deterministic Finite Automaton Search Time:", dfa_time)
    print("Occurrences found using deterministic finite automaton search:", len(dfa_occurrences))
    # print("DFA occurrences:", dfa_occurrences)  # Debugging
    print("\n")
    print("Are the occurrences the same?", brute_force_occurrences == dfa_occurrences)
    print("Are the times the same?", brute_force_time == dfa_time)
    search_times_1 = {
        brute_force_time: "Brute Force",
        dfa_time: "Deterministic Finite Automaton"
    }
    fastest_algorithm_1 = search_times_1[min(brute_force_time, dfa_time)]
    print("Which search algorithm among Brute Force and Deterministic Finite Automaton is the fastest one?", fastest_algorithm_1)
    print("How much faster is the fastest search algorithm?", max(brute_force_time, dfa_time) / min(brute_force_time, dfa_time), "times")
    print("\n")
    print("Brute Force occupies", sys.getsizeof(brute_force_occurrences), "bytes")
    print("DFA occupies", sys.getsizeof(dfa_occurrences), "bytes")

    print("\n")

    regex_occurrences, regex_time = measure_time(regex_search.search, "Regular Expression", text)

    print("Regular Expression Search Time:", regex_time)
    print("Occurrences found using regular expression search:", len(regex_occurrences))

    print("\n")

    naive_search_occurrences, naive_search_time = measure_time(naive_search.search, "Naive", word_to_search, random_words)
    fa_search_occurrences, fa_search_time = measure_time(fa_search.search, "Finite Automaton", random_words)
    bmh_search_occurrences, bmh_search_time = measure_time(bmh_search.search, "Boyer Moore Horspool", random_words)

    print(f"\nWord to search: {word_to_search}")

    print("\n")
    print(f"Occurrences found using Naive search: {len(naive_search_occurrences)}")
    print(f"Occurrences found using Finite Automaton search: {len(fa_search_occurrences)}")
    print(f"Occurrences found using Boyer-Moore-Horspool search: {len(bmh_search_occurrences)}")
    print("\n")
    print("Naive Search Time:", naive_search_time)
    print("Finite Automaton Search Time:", fa_search_time)
    print("Boyer-Moore-Horspool Search Time:", bmh_search_time)
    print("\n")
    print("Are the occurrences the same?", naive_search_occurrences == fa_search_occurrences == bmh_search_occurrences)
    print("Are the times the same?", naive_search_time == fa_search_time == bmh_search_time)
    search_times = {
        naive_search_time: "Naive",
        fa_search_time: "Finite Automaton",
        bmh_search_time: "Boyer-Moore-Horspool"
    }
    fastest_algorithm = search_times[min(naive_search_time, fa_search_time, bmh_search_time)]
    if naive_search_occurrences or fa_search_occurrences or bmh_search_occurrences:
        print("Which search algorithm among Naive, Finite Automaton, and Boyer-Moore-Horspool is the fastest one?", fastest_algorithm)
        print("How much faster is the fastest search algorithm?",
              max(naive_search_time, fa_search_time, bmh_search_time) / min(naive_search_time, fa_search_time, bmh_search_time), "times")
    else:
        print("No occurrences found for any search algorithm.")
    print("\n")
    print("Naive occupies", sys.getsizeof(naive_search_occurrences), "bytes")
    print("Finite Automaton occupies", sys.getsizeof(fa_search_occurrences), "bytes")
    print("Boyer-Moore-Horspool occupies", sys.getsizeof(bmh_search_occurrences), "bytes")

    print("\n")

    ndfa_occurrences, ndfa_time = measure_time(ndfa_search.search, "Non-Deterministic Finite Automaton", text)

    print(f"\nWord to search: {word_to_search}")
    print("\n")
    print("Non-Deterministic Finite Automaton Search Time:", ndfa_time)
    print("Occurrences found using non-deterministic finite automaton search:", len(ndfa_occurrences))
    # print("Non-Deterministic Finite Automaton occurrences:", ndfa_occurrences)  # Debugging
    print("\n")
    print("Non-Deterministic Finite Automaton occupies", sys.getsizeof(ndfa_occurrences), "bytes")
