from functools import reduce


class EpsilonNondeterministicFiniteAutomata:
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

        return self.to_nfa().accepts(word)

    def to_nfa(self):
        nfa_transitions = {}
        for state in self.states:
            transitions = []

            state_closure = self.epsilon_closure(state)

            for symbol in self.alphabet:
                results = []

                for result in state_closure:
                    results += list(filter(lambda t: t['symbol'] == symbol, self.transitions[result]))

                results = reduce(lambda t1, t2: t1 + t2, list(map(lambda t: t['to'], results)), [])

                results_closures = list(
                    set(reduce(lambda t1, t2: t1 + t2, [self.epsilon_closure(res) for res in results], [])))

                transitions += [{"to": results_closures, "symbol": symbol}]

            nfa_transitions[state] = transitions
        # find all the states that can get to a final state with epsilon
        final_states = []
        for state in self.states:
            closure = self.epsilon_closure(state)
            for final_state in self.final_states:
                if final_state in closure:
                    final_states += state
        nfa = NondeterministicFiniteAutomata(self.alphabet, self.states, self.initial_state, final_states,
                                             nfa_transitions)
        return nfa

    def epsilon_closure(self, state, states=None):
        if states is None:
            states = [state]

        epsilons = self.epsilons_for(state)

        if len(epsilons) == 0:
            return states
        else:
            results = []
            for epsilon in epsilons:
                results += self.epsilon_closure(epsilon, states + epsilons)

            return list(set(results))

    def epsilons_for(self, state):
        epsilon_transitions = list(filter(lambda t: t['symbol'] == "", self.transitions[state]))
        return [target for transition in epsilon_transitions for target in transition['to']]


class NondeterministicFiniteAutomata:
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

        return self.any_final(self.initial_state, word_chars)

    def any_final(self, state, chars, level=0):
        if level == len(chars):
            return state in self.final_states
        else:
            symbol = chars[level]

            results = next(filter(lambda t: t['symbol'] == symbol, self.transitions[state]))['to']

            if results:
                for result in results:
                    return self.any_final(result, chars, level + 1)
            else:
                return False

    def to_dfa(self):
        new_states = [self.initial_state]
        transitions = {}

        while new_states:
            state = new_states.pop(0)
            sub_states = state.split(',')
            transitions[state] = []
            for symbol in self.alphabet:
                transition_results = []
                for sub_state in sub_states:
                    transition_results += next(filter(lambda t: t['symbol'] == symbol, self.transitions[sub_state]))['to']

                transition_results = list(set(transition_results))
                target_state = ",".join([str(tr) for tr in transition_results])
                transitions[state].append({
                    "to": target_state,
                    "symbol": symbol
                })
                if target_state not in list(transitions.keys()) + new_states:
                    new_states += new_states + [target_state]

        print(transitions)