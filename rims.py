 #!/usr/bin/python

"""
Module that provides several functions to handle (un)rimmed words. 
"""

import words

def rims_of(word):
    """ Return the rims for the given word. A rim is a (nonempty) word u such 
    that w = u.s = p.u' for some s,p,u' such that |u'| = |u|, and u' and u 
    agree on every position except one. 
    For example, a and aab are rims for aabb. """
    rims = []
    for shift in words.get_koverlaps(word, 1):
        rims.append(word[:len(word)-shift])
    return rims

def pretty_print(word, rims = None):
    """ Pretty print of the rims of the given word. """
    if rims == None:
        rims = rims_of(word)
    print word
    for r in rims:
        print word.rjust(len(word)*2-len(r), ' ')

def mismatch_pos(word, rim):
    """ Return the position (in the rim) of the mismatch between 
    the word and the rim. Position starts at 0. """
    shift = len(word) - len(rim)
    for k in range(len(rim)):
        if word[shift + k] != rim[k]:
            return k
    return -1

def rim_index(word, rim):
    """ Return the index of a rim in the given word. The index of a rim 
    is a position in w where the corresponding suffix of the rim starts. """
    return len(word) - len(rim) + 1

