#!/usr/bin/python

import os
import words
from certain import Certain

PATH_RESULTS = 'results'
RESULT_SEP = '    '
USE_GAP = False

try:
    if USE_GAP:
        import automata_gap
except ImportError as e:
    USE_GAP = False
   
""" Dear user, 
I really need to warn you before you make use of the following code. This code
is not really part of the Multiword Project, it was written to conduct several
(exhaustive and random) studies. Please, do not use this code on your own! 
You should better write your own code based on the other modules (certain.py, 
multiword.py, etc.). The code in this file is very specific to what we needed, 
I can not ensure that you will be fine with that... """


# ####### Experiments for the size of the minimal DFA

def size_of_minimal_dfa_for(w):
    """
    Return the size of the minimal automaton recognizing the language
    certain(w) for the given word w. 
    """
    if isinstance(w, str):
        if USE_GAP:
            return automata_gap.size_of_minDFA(w)            
        else:
            dfa = Certain(w).automaton()
            dfa.minimize()
            return len(dfa.states)
    else:
        raise TypeError, 'Argument type %s unsupported' % type(word)


def results_for(iterable):
    """
    Return a generator that yield (word, size of min dfa) for every word in 
    iterable.
    """
    return ( (word, size_of_minimal_dfa_for(word)) for word in iterable )
    

def exp_for(iterable, filename, display = False):
    """ 
    Run an experiment for words in given iterable and save its
    results to PATH_RESULTS/filename. If display is set to True, also
    print output to screen. 
    The output is formated as follows:
    [word]RESULT_SEP[size]RESULT_SEP[n+x]RESULT_SEP[diff with upperbound]
    """
    fp = open(os.path.join(PATH_RESULTS, 'mdfa_'+filename), 'w')
    i = 0
    for word, size in results_for(iterable):
        output = '%s%s%d%s%d+%d%s%d' % (word, RESULT_SEP,
                size, RESULT_SEP, len(word), size - len(word), 
                RESULT_SEP, size - (len(word) + len(word) / 2))
        fp.write(output+'\n')
        if display:
            print output
        i += 1
    fp.close()
    return i


def exp_exhaustive_for(alphabet, min_size, max_size, display = False):
    """ 
    Run an experiment for words over the given alphabet and save its results.
    The output file is PATH_RESULTS/[alphabet]_[min_size]_[max_size].txt
    Set display to True to print results.
    The output is formated as follows:
    [word]RESULT_SEP[size]RESULT_SEP[n+x]RESULT_SEP[diff with upperbound]
    """
    filename = '%s_%d_%d.txt' % (alphabet, min_size, max_size)
    iterable = words.words(alphabet, min_size, max_size)
    return exp_for(iterable, filename, display)
    
    
def exp_random_for(alphabet, number, min_size, max_size, display = False):
    """ 
    Run an experiment for [number] random words and save the results.
    The output file is PATH_RESULTS/rand_[alphabet]_[min_size]_[max_size]_[number].txt
    Set display to True to print results.
    The output is formated as follows:
    [word]RESULT_SEP[size]RESULT_SEP[n+x]RESULT_SEP[diff with upperbound]
    """
    filename = 'rand_%s_%d_%d_%d.txt' % (alphabet, min_size, max_size, number)
    iterable = words.random_words(alphabet, number, min_size, max_size)
    return exp_for(iterable, filename, display)
    

# ####### Experiments for/with our families

def exp_size_of_families(iterable):
    """
    Given an iterable containing words, return a 5-uple (a, b, c, d, e, f, g) such that:
    - a is the number of elements in iterable ;
    - b = [x,y] is the number x (resp. y) of elements for which (resp. only) family_primitive is True ;
    - c is for family_unbordered ;
    - d is for family_anchored ;
    - e is for family_no1overlap ;
    - f is the number of elements left.
    """
    numbers = [0, [0,0], [0,0], [0,0], [0,0], 0]
    for word in iterable:
        pri = words.family_primitive(word)
        unb = words.family_unbordered(word)
        anc = words.family_anchored(word)
        ove = words.family_no1overlap(word)
        numbers[0] += 1
        
        if pri:
            numbers[1][0] += 1
            if not unb and not anc and not ove:
                numbers[1][1] += 1
        if unb:
            numbers[2][0] += 1
            if not pri and not anc and not ove:
                numbers[2][1] += 1
        if anc:
            numbers[3][0] += 1
            if not pri and not unb and not ove:
                numbers[3][1] += 1

        if ove:
            numbers[4][0] += 1
            if not pri and not unb and not anc:
                numbers[4][1] += 1                
                
        numbers[5] += 1 - int(pri or unb or anc or ove)
    return tuple(numbers)

    
def exp_number_of_koverlap(iterable, k):
    """ 
    Given an iterable containing words, return a dict D of numbers. 
    An entry D[i] = x means there exist x words in iterable that have exactly
    i k-overlaps. 
    """
    result = dict()
    
    for word in iterable:
        nb = len(words.get_koverlaps(word, k))
        result[nb] = result.get(nb, 0) + 1
    
    return result
    
