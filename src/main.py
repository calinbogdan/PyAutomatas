import json
from src.automatas.ndfa import EpsilonNondeterministicFiniteAutomata

with open('./config/ndfa.json') as json_file:
    data = json.load(json_file)

    dfa = EpsilonNondeterministicFiniteAutomata(data['alphabet'],
                                      data['states'],
                                      data['initialState'],
                                      data['finalStates'],
                                      data['transitions'])

    print(dfa.accepts('00'))
