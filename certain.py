#!/usr/bin/python

import sequence
import words

from automata import Automata
from multiword import Multiword


class Certain(object):
    """
    This class represents the language certain(w) for a given word w. 
    certain(w) contains every multiword in which word w is certain. 
    A word w is certain in a multiword M if every possible word of M contains
    the word w as a factor. See module multiword for more informations. 
    """
    
    def __init__(self, word):
        """ 
        Create the language certain(w) for a given word w.
        """
        if isinstance(word, str):
            self.word = word
        else:
            raise TypeError, 'Argument type %s unsupported' % type(word)
        
        
    def get_word(self):
        """
        Return the word used for the construction of certain(w).
        """
        return self.word
        
        
    def contains(self, multiword):
        """
        Return true iff certain(w) contains the given multiword.
        """
        if isinstance(multiword, Multiword):
            return self.word in M
        else:
            raise TypeError, 'Argument type %s unsupported' % type(multiword)

    
    def automaton(self):
        """
        return a deterministic finite automaton recognizing the current language.
        """   
        def next_state(state, w, symbol):
            """ 
            Return the (frozen) set of prefixes reachable from given state
            by reading (symbols of) symbol for the given word w. 
            """
            n_state = set()
            for e in state:
                for a in symbol:
                    n_state.add(sequence.sufpre(e+a, w))
            return frozenset(sequence.lower_bound(n_state, w))
            
        alphabet = words.get_alphabet(self.word)
        powerset_alphabet = frozenset(
            [frozenset([a, b]) for a in alphabet for b in alphabet]
        )   # This corresponds to the relevant subset of the powerset alphabet
        states = [frozenset([''])]
        states_left = [frozenset([''])]    
        while len(states_left) > 0:
            state = states_left.pop()
            for symbol in powerset_alphabet:
                dest = next_state(state, self.word, symbol)
                if dest not in states:
                    states.append(dest)
                    states_left.append(dest)
        start = frozenset([''])   # empty word
        accepts = [frozenset([])]   # empty set      
        delta = lambda q, a: next_state(q, self.word, a)
        return Automata(states, powerset_alphabet, delta, start, accepts)
        

    def __contains__(self, other):
        return contains(self, other)
        
        
    def __str__(self):
        return 'certain(%s)' % self.word
        
    def __repr__(self):
        return str(self)
        

