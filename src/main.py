import json
from src.automatas.dfa import DeterministicFiniteAutomata

with open('./config/dfa.json') as json_file:
    data = json.load(json_file)

    dfa = DeterministicFiniteAutomata(data['alphabet'],
                                      data['states'],
                                      data['initialState'],
                                      data['finalStates'],
                                      data['transitions'])

    print(dfa.accepts('00'))
