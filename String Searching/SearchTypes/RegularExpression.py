class RegularExpressionSearch:
    def __init__(self, regex):
        self.regex = regex
        self.nfa = self.build_nfa_from_regex(regex)
        self.dfa = self.convert_to_dfa(self.nfa)

    def build_nfa_from_regex(self, regex):
        nfa = {
            'states': set(),
            'alphabet': set(),
            'transitions': {},
            'initial_state': 0,
            'accept_states': set(),
        }
        state_counter = 0

        stack = []
        for char in regex:
            if char == '(':
                stack.append('(')
            elif char == '|':
                stack.append('|')
            elif char == '*':
                pass
            elif char == ')':
                pass
            else:
                nfa['states'].add(state_counter)
                nfa['states'].add(state_counter + 1)
                nfa['alphabet'].add(char)
                nfa['transitions'][(state_counter, char)] = {state_counter + 1}
                state_counter += 1

        nfa['accept_states'].add(state_counter)

        return nfa

    def convert_to_dfa(self, nfa):
        dfa = {
            'states': set(),
            'alphabet': nfa['alphabet'],
            'transitions': {},
            'initial_state': frozenset({nfa['initial_state']}),
            'accept_states': set(),
        }

        queue = [dfa['initial_state']]

        while queue:
            current_states = queue.pop(0)
            dfa['states'].add(current_states)
            for char in dfa['alphabet']:
                next_states = set()
                for state in current_states:
                    next_states.update(nfa['transitions'].get((state, char), set()))
                next_states = frozenset(next_states)
                dfa['transitions'][(current_states, char)] = next_states
                if next_states not in dfa['states']:
                    queue.append(next_states)
            if nfa['accept_states'] & current_states:
                dfa['accept_states'].add(current_states)

        return dfa

    def search(self, text):
        current_states = {self.dfa['initial_state']}
        match_positions = []

        for i, char in enumerate(text):
            next_states = set()
            for state in current_states:
                next_states.update(self.dfa['transitions'].get((state, char), set()))
            current_states = next_states

            if current_states & self.dfa['accept_states']:
                match_positions.append(i)

        return match_positions


