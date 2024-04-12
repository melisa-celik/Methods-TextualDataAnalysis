class BruteForceSearch:
    def search(self, pat, txt):
        M = len(pat)
        N = len(txt)
        occurrences = []

        for i in range(N - M + 1):
            j = 0
            while j < M:
                if txt[i + j] != pat[j]:
                    break
                j += 1
            if j == M:
                occurrences.append(i)

        return occurrences

