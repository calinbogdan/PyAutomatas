class DeterministicFiniteAutomata:
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    def accepts(self, word):
        word_chars = list(word)

        if not all(char in self.alphabet for char in word_chars):
            return False

        current_state = self.initial_state
        while word_chars:
            current_symbol = word_chars.pop(0)

            next_state = self.next_state(current_state, current_symbol)
            if next_state:
                current_state = next_state
            else:
                break

        return current_state in self.final_states

    def next_state(self, current_state, current_symbol):
        matching_transition = next(filter(lambda t: t['symbol'] == current_symbol, self.transitions[current_state]), None)
        if matching_transition:
            return matching_transition['to']
        else:
            return None

