class NaiveSearch:
    def search(self, pattern, text):
        occurrences = []
        m = len(pattern)
        n = len(text)
        for i in range(n - m + 1):
            if text[i:i+m] == pattern:
                occurrences.append(i)
        return occurrences

