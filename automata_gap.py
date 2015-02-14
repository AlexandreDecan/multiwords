#!/usr/bin/python

import subprocess
import re
import sequence

"""
Please note that this file is an old and non-maintained file. 
It's purpose is to propose another way of computing the size of a minimal
DFA in our context.

The function that can be used to do this is: 
size_of_minDFA(word)
""" 


"""
This library needs gap to be installed + the automata component of GAP. 
This component can be downloaded at:
http://www.gap-system.org/Packages/automata.html

The inner directory has to be moved to:
/usr/share/gap/pkg  (under Ubuntu >8.04)
"""

def KPM_DFA(w):
    """ Return a tuple (states, alphabet, transitions, initialState, 
        finalStates) which corresponds to a complete 
        Knuth-Morris-Pratt DFA for the given word w """
    alphabet = set([c for c in w])
    initialState = ''
    finalStates = [w]
    states = [w[:i] for i in range(len(w)+1)]
    transitions = []

    for from_s in states:
        for c in alphabet:
            if from_s == w:
                transitions.append( (from_s, from_s, c) )
            else:
                to_s = sequence.sufpre(from_s + c,w)
                transitions.append( (from_s, to_s, c) )
    
    return (states, alphabet, transitions, initialState, finalStates)


def powerset_table(alphabet):
    """ As most of FSA tools doesn't support symbols larger than 
    one character, we have to use a one-symbol representation. 
    Eg. : {a,b} is 0, {a,c} is 1, etc. 
    This function generates a list. l[0] = 'ab', l[1]='ac', ... """
    alphabet = list(set(alphabet))
    table = []
    for i in range(len(alphabet)):
        for j in range(i+1,len(alphabet)):
            table.append(alphabet[i]+alphabet[j])
    return table


def complement_DFA(states, alphabet, transitions, 
                                    initialState, finalStates):
    """ Return the complement of given DFA """
    new_finalStates = [state for state in states 
                        if state not in finalStates]
    return (states, alphabet, transitions, initialState, new_finalStates)
    

def our_completion_DFA(states, alphabet, transitions, 
                                    initialState, finalStates):
    """ For every transition (from, to, c) adds every transition
        (from, to, s') where s' represents c plus every other symbol """
    table = powerset_table(alphabet)
    new_alphabet = alphabet.union([str(i) for i in range(len(table))])
    new_transitions = []
    for from_s, to_s, c in transitions:
        for i,pairs in enumerate(table):
            if c in pairs and (from_s, to_s, str(i)) not in new_transitions:
                new_transitions.append( (from_s, to_s, str(i)) )
    return (states, new_alphabet, transitions + new_transitions, 
                initialState, finalStates)


def simplify_DFA(states, alphabet, transitions, initialState, finalStates):
    """ Return given DFA with every transition to initialState removed
        for clarity """
    new_transitions = []
    for from_s, to_s, s in transitions:
        if to_s != initialState:
            new_transitions.append( (from_s, to_s, s) )
    return (states, alphabet, new_transitions, initialState, finalStates)


def display_DFA(states, alphabet, transitions, initialState, finalStates):
    """ Pretty print of a DFA """
    s  = 'DFA {\n\talphabet = %s\n' % ','.join([str(s) for s in alphabet])
    s += '\tinitialState = %s\n' % str(initialState)
    s += '\tfinalStates = %s\n' % ','.join([str(s) for s in finalStates])
    for from_s, to_s, c in transitions:
        s += '\t%s --%s--> %s\n' % (str(from_s), c, str(to_s))
    return s + '}'


def named_stuff_to_number(states, alphabet, transitions, initialState, finalStates):
    """ (Documentation added lately) Seems to return an new DFA where each 
    named stuff is replaced by a numbered stuff (alphabet is now a subset of 
    integers for example). """
    def get_state(name):
        return 1 + states.index(name)
    def get_letter(name):
        return 1 + list(alphabet).index(name)
    
    n_states = range(1, len(states) + 1)
    n_alphabet = range(1, len(alphabet) + 1)
    n_initialState = get_state(initialState)
    n_finalStates = [get_state(x) for x in finalStates]
    n_transitions = [(get_state(f), get_state(t), get_letter(c)) for \
                        (f,t,c) in transitions]
    return (n_states, n_alphabet, n_transitions, n_initialState, n_finalStates)


def get_transition_table(DFA):
    """ Return the transition table as a matrix. eg. :
    [[3,,3,4],[3,4,0,4]] means : 
      |  1  2  3  4
    -----------------
    0 |  3     3  4
    1 |  3  4     4 
    where 0 is first letter, 1 is second """
    states, alphabet, transitions, initialState, finalStates = DFA
    matrix = []
    for c in alphabet:
        submatrix = []
        for f in states:
            tr = []
            for t in states:
                if (f,t,c) in transitions:
                    tr.append(t)
            if len(tr) == 0:
                submatrix.append(0)
            elif len(tr) == 1:
                submatrix.append(tr[0])
            else:
                submatrix.append(tr)
        matrix.append(submatrix)
    return matrix
    

def DFA_string_for_GAP(w):
    """ Return the string needed to encode the DFA for w in GAP. """
    DFA = KPM_DFA(w)
    DFA = complement_DFA(*DFA)
    alphabet = DFA[1]
    DFA = our_completion_DFA(*DFA)
    
    A = []
    pwt = powerset_table(alphabet)
    for ch in DFA[1]:
        if str.isdigit(ch):
            ch = pwt[int(ch)]
        A.append(ch)
    if __name__ == '__main__':
		print 'Alphabet is: %s' % ', '.join( ['%d=%s' % (1+i,c) for \
				i,c in enumerate(A) ] )
    DFA = named_stuff_to_number(*DFA)
    matrix = get_transition_table(DFA)
    DFA = simplify_DFA(*DFA)
    
    states, alphabet, transitions, initialState, finalStates = DFA

    return '%s:=Automaton("%s", %d, %s, %s, [%d], %s);' % \
        ('fsa', 'nondet', len(states), str(alphabet), 
                str(matrix), int(initialState), str(finalStates))
                
                
__my_re__ = re.compile('gap> < deterministic automaton on [0-9]+ letters with ([0-9]+) states >\n')
def size_of_minDFA(w):
    """ Return the size of the minimal DFA in terms of number of states """
    p = subprocess.Popen(['gap', '-b'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write('LoadPackage("automata");\n')
    
    s = DFA_string_for_GAP(w)
    s += 'fsa:=NFAtoDFA(fsa);\n'
    s += 'fsa:=MinimalizedAut(fsa);\n'
    p.stdin.write(s)
    p.stdin.write('quit;\n')
    output = p.stdout.readlines()
    for line in output:
        r = __my_re__.match(line)
        if r:
            size = int(r.groups()[0])
            return size
    return None
            
            
def minDFA(w, draw = False):
    """ Return the min DFA. If draw is set to true, display this DFA and
    save it to current path. """
    from os import path
    s = 'LoadPackage("automata");\n'
    s += DFA_string_for_GAP(w)
    s += 'fsa:=NFAtoDFA(fsa);\n'
    s += 'fsa:=MinimalizedAut(fsa);\n'
    s += 'Display(fsa);\n'
    if draw:
        s += 'DrawAutomaton(fsa,"../..%s/%s");\n' % (path.realpath('.'),w)
    s += 'FAtoRatExp(fsa);\n'
    s += 'quit;\n'
   
    p = subprocess.Popen(['gap', '-b'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(s)
    output = p.stdout.readlines()[:-1]
    display = False
    real_output = []
    for line in output:
        if not display:
            if '|' in line:
                line = line[5:]
                display = True
        if 'Accepting states' in line:
            line = 'Non-%s' % line
        if display:
            real_output.append(line[:-1])
    return '\n'.join(real_output)
