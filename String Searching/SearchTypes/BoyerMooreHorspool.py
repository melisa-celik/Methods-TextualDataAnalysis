class BoyerMooreHorspoolSearch:
    def __init__(self, pattern):
        self.pattern = pattern
        self.bmBc = self.preprocess_bmBc(pattern)

    def preprocess_bmBc(self, pattern):
        bmBc = {}
        m = len(pattern)
        for i in range(m - 1):
            bmBc[pattern[i]] = m - i - 1
        return bmBc

    def search(self, text):
        occurrences = []
        m = len(self.pattern)
        n = len(text)
        j = 0
        while j <= n - m:
            if self.pattern == text[j:j+m]:
                occurrences.append(j)
            j += self.bmBc.get(text[j + m - 1], m)
        return occurrences