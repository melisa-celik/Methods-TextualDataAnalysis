class FiniteAutomatonSearch:
    def __init__(self, pattern):
        self.pattern = pattern
        self.transition = self.compute_transition()

    def compute_transition(self):
        transition = [{} for _ in range(len(self.pattern) + 1)]
        alphabet = set(self.pattern)  # Get unique characters in the pattern
        m = len(self.pattern)
        for q in range(m + 1):
            for char in alphabet:
                k = min(m, q + 1)
                while k > 0 and self.pattern[:k] != (self.pattern[:q] + char)[-k:]:
                    k -= 1
                transition[q][char] = k
        return transition

    def search(self, text):
        occurrences = []
        n = len(text)
        q = 0
        for i in range(n):
            char = text[i]
            if char not in self.transition[q]:
                q = 0  # Reset to initial state
            else:
                q = self.transition[q][char]
            if q == len(self.pattern):
                occurrences.append(i - len(self.pattern) + 1)
        return occurrences


class DeterministicFiniteAutomatonSearch:
    def __init__(self):
        self.initial_state = 0
        self.transitions = {}
        self.terminals = set()

    def pre_aut(self, pattern):
        state = self.initial_state
        for i, char in enumerate(pattern):
            self.transitions[(state, char)] = i + 1
            state = i + 1
        self.terminals.add(state)

    def search(self, text, pattern):
        occurrences = []
        self.pre_aut(pattern)
        state = self.initial_state
        m = len(pattern)
        for j, char in enumerate(text):
            state = self.transitions.get((state, char), 0)
            if state in self.terminals:
                occurrences.append(j - m + 1)
        return occurrences

class NonDeterministicFiniteAutomatonSearch:
    def __init__(self, pattern, k):
        self.pattern = pattern
        self.k = k
        self.transitions = self._compute_transitions()

    def _compute_transitions(self):
        transitions = []
        m = len(self.pattern)
        for state in range((self.k + 1) * (m + 1)):
            transitions.append({})
            for char in range(256):
                next_state = min(state + 1, (self.k + 1) * (m + 1) - 1)
                for k in range(1, min(self.k + 1, m - state % (m + 1)) + 1):
                    pattern_index = (state // (m + 1)) * (m + 1) + state % (m + 1) - 1
                    if pattern_index >= 0 and pattern_index < m and chr(char) == self.pattern[pattern_index]:
                        next_state = state + k + 1
                transitions[state][chr(char)] = next_state
        return transitions

    def search(self, text):
        positions = []
        n = len(text)
        for i in range(n):
            state = 0
            for j in range(i, min(i + len(self.pattern) + 1, n)):
                state = self.transitions[state].get(text[j], 0)
                if state % (len(self.pattern) + 1) == 0 and state != 0:
                    positions.append(i)
                    break
        return positions
