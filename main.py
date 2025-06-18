import json
def dic2Json(dic, fname="data.json"):
  json_file= open(fname, 'w')
  json.dump(dic, json_file, indent=4)
  json_file.close()

def json2Dic(fname="data.json"):
  json_file= open(fname, 'r')
  dic = json.load(json_file)
  json_file.close()
  return dic

import sys
if __name__=='__main__':
  if len(sys.argv)>1 and sys.argv[1]=="write":
    if sys.argv[2]=='test':
      data = {
        "name": "John",
        "age": 30,
        "city": "New York"
      }
    if sys.argv[2]=='trans':
      data= {
        'q0':{'The':'q1','A':'q1','My':'q1', 'Your': 'q1'},
        'q1': {'cat': 'q2', 'mouse':'q2'},
        'q2': {'sleeps': 'q3', 'chases': 'q3', 'runs': 'q3'},
        'q3': {'.': 'q4'},  # Final state
        'final_state': ['q3','q4']
      }
    dic2Json(data, sys.argv[2]+".json")
  if len(sys.argv)>1 and sys.argv[1]=="read":
    data= json2Dic(sys.argv[2]+".json")
    print(data)

# DFA
class DFA:
    def __init__(self, transitions, start_state, final_states):
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def accepts(self, input_str):
        state = self.start_state
        for symbol in input_str:
            if symbol in self.transitions.get(state, {}):
                state = self.transitions[state][symbol]
            else:
                return False
        return state in self.final_states

# NFA
class NFA:
    def __init__(self, transitions, start_state, final_states):
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def _epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in self.transitions.get(state, {}).get('', []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def accepts(self, input_str):
        current_states = self._epsilon_closure([self.start_state])
        for symbol in input_str:
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions.get(state, {}).get(symbol, []))
            current_states = self._epsilon_closure(next_states)
        return any(state in self.final_states for state in current_states)

# DFA to NFA
def reverse_dfa_to_nfa(dfa_dict):
    transitions = dfa_dict['transitions']
    start_state = dfa_dict['start_state']
    final_states = dfa_dict['final_states']

    reversed_transitions = {}

    for src_state, trans in transitions.items():
        for symbol, dst_state in trans.items():
            if dst_state not in reversed_transitions:
                reversed_transitions[dst_state] = {}
            if symbol not in reversed_transitions[dst_state]:
                reversed_transitions[dst_state][symbol] = []
            reversed_transitions[dst_state][symbol].append(src_state)

    new_start = 'new_start'
    reversed_transitions[new_start] = {'': final_states}

    return NFA(reversed_transitions, new_start, [start_state])

def generate_all_strings(alphabet, length):
    if length == 0:
        return ['']
    smaller = generate_all_strings(alphabet, length - 1)
    return [s + a for s in smaller for a in alphabet]

def test_language(fname):
    dfa_dict = json2Dic(fname)
    dfa = DFA(dfa_dict['transitions'], dfa_dict['start_state'], dfa_dict['final_states'])

    print(f"Testing DFA for language defined in {fname}:")
    for string in generate_all_strings(['a', 'b'], 2):
        if dfa.accepts(string):
            print(f"DFA accepts: {string}")

    reversed_nfa = reverse_dfa_to_nfa(dfa_dict)

    print(f"\nTesting NFA for reversed language of {fname}:")
    for string in generate_all_strings(['a', 'b'], 2):
        reversed_str = string[::-1]
        if reversed_nfa.accepts(reversed_str):
            print(f"NFA accepts reversed string: {reversed_str}")

if __name__ == '__main__':
    ab_dfa = {
        'transitions': {
            'q0': {'a': 'q0', 'b': 'q1'},
            'q1': {}
        },
        'start_state': 'q0',
        'final_states': ['q1']
    }
    dic2Json(ab_dfa, 'a_b_dfa.json')

    ba_dfa = {
        'transitions': {
            'q0': {'b': 'q1'},
            'q1': {'a': 'q2'},
            'q2': {}
        },
        'start_state': 'q0',
        'final_states': ['q2']
    }
    dic2Json(ba_dfa, 'ba_dfa.json')

    test_language('a_b_dfa.json')
    print("\n" + "="*40 + "\n")
    test_language('ba_dfa.json')
