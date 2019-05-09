import json
from src.automatas.ndfa import EpsilonNondeterministicFiniteAutomata, NondeterministicFiniteAutomata

with open('./config/ndfa.json') as json_file:
    data = json.load(json_file)

    dfa = NondeterministicFiniteAutomata(data['alphabet'],
                                      data['states'],
                                      data['initialState'],
                                      data['finalStates'],
                                      data['transitions'])
    print(dfa.to_dfa())
    print(dfa.accepts('00'))
