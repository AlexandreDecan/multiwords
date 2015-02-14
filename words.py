#!/usr/bin/python

import random
import itertools

# ######## Words generators

def words(alphabet, min_length, max_length = None):
    """ Return a generator of words over alphabet. Those words
    are of min_length length to max_length length. The max_length
    is set to min_length if not given. """

    if not max_length:
        max_length = min_length
    current_length = min_length
    while current_length <= max_length:
        words_of_current_length = itertools.product(alphabet, repeat = current_length)
        for word in words_of_current_length:
            yield ''.join(word)
        current_length += 1

        
fullwords = words   # For backward compatibility
  
  
def random_words(alphabet, number, min_length, max_length = None):
    """ Return a generator of [number] random words over alphabet. 
    Those words are of min_length length to max_length length. 
    The max_length is set to min_length if not given. Note that first symbol 
    is fixed and is the first element of alphabet. """   
    
    first_symbol = alphabet[0]
    if not max_length:
        max_length = min_length  
    generated = 0
    while generated < number:
        current_size = random.randint(min_length, max_length) - 1
        word = [first_symbol]
        for i in range(current_size):
            word.append(random.choice(alphabet))
        yield ''.join(word)
        generated += 1


# ######## Words operations

def get_alphabet(word):
    """ Return the smallest possible alphabet (as a list)
    which can be used for the given word. """
    return list(set(word))


def proper_prefixes(word):
    """ Return a list of nonempty proper prefixes of 
    the given word (sorted in increasing length). """
    return [word[:i] for i in range(1, len(word))]


def prefixes(word):
    """ Return a list of nonempty prefixes of
    the given word (sorted in increasing length). """
    return proper_prefixes(word) + [word]

    
def proper_suffixes(word):
    """ Return a list of nonempty proper suffixes
    of the given word (sorted in decreasing length). """
    return [word[i:] for i in range(1, len(word))]


def suffixes(word):
    """ Return a list of nonempty suffixes of
    the given word (sorted in decreasing length). """
    return proper_suffixes(word) + [word]    
    

def factors(word):
    """ Return a list of nonempty proper factors of the given word. """
    _factors = []
    for candidate in prefixes(word):
        for candidate_2 in suffixes(candidate):
            _factors.append(candidate_2)
    return list(set(_factors))


def primitive_root(word):
    """ Return the shortest word u such that word = u ^ i for some i >= 1. """
    _prefixes = prefixes(word)
    for u in _prefixes:
        i = len(word) / len(u)
        if word == u * i:
            return u
    
    
def reverse(w):
    """ Return the reverse of given word w. """
    return w[::-1]        


def get_koverlaps(word, k):
    """ Return the k-overlaps for the given word. """
    koverlap = []
    for gap in xrange(1, len(word)):
        w1, w2 = (' ' * gap) + word, word + (' ' * gap)
        count = 0
        for i in xrange(len(w1)):
            if w1[i] != ' ' and w2[i] != ' ':
                if w1[i] != w2[i]:
                    count += 1
        if count == k:
            koverlap.append(gap)
    return koverlap
    
    
# ######## Words identifications       

def uniquify(word, sigma = None):
    """ Return a canonical representation of the given word. """
    if sigma == None:
        sigma = list(set(word))
        sigma.sort()
    corresp = dict()
    symbol = iter(sigma)
    output = []
    for a in word:
        if a not in corresp:
            corresp[a] = symbol.next()
        output.append(corresp[a])
    return ''.join(output)

    
def uniquify_all(words, sigma = None):
    """ Return a list that contains the uniquified representation of
    every word in given list of words. """
    if sigma == None:
        sigma = set()
        for w in words:
            for a in w:
                sigma.add(a)
    return list(set(map(lambda x: uniquify(x, sigma), words)))

    
def is_unbordered(word):
    """ Return True iff word is unbordered. """
    _suffixes = proper_suffixes(word)
    _prefixes = proper_prefixes(word)
    length = len(word)
    # Number of suffixes and prefixes is the same as |w| - 1.
    for i in range(length - 1):
        if _prefixes[i] == _suffixes[length - i - 2]:
            return False
    return True
        

def is_palindrome(word):
    """ Return True iff word is a palindrome. """
    s = int(0.5 + len(word) / 2.0)
    return word[:s] == word[:-s-1:-1]


def is_primitive(word):
    """ Return True iff word is primitive, this is, if for every u,
    word = u ^ i implies i = 1. """
    return primitive_root(word) == word
           
    
def anchors(word):
    """ Return a list of possible anchors. 
    A word a.u.a is an anchor of w if a.u.a occurs in w and 
    u does not contain a. """
    anchors = []
    _factors = factors(word)
    for candidate in _factors:
        left, middle, right = candidate[0], candidate[1:-1], candidate[-1]
        if len(candidate) > 1 and left == right and left not in middle:
            anchors.append(candidate)
    return anchors

    
def family_primitive(word):
    """ Return True if given word is a power (>=3) of a primitive one. """
    _prefixes = prefixes(word)
    for u in _prefixes:
        i = len(word) / len(u) + 1
        if i >= 4 and (u * i).startswith(word) and is_primitive(u):
            return True
    return False
    
    
def family_unbordered(word):
    """ Return True iff word is a power of an unbordered word. """
    # Either word is unbordered or is an exact power of an unbordered word. 
    if is_unbordered(word):
        return True
    _prefixes = prefixes(word)
    for u in _prefixes:
        i = len(word) / len(u)
        if (u * i) == word and is_unbordered(u):
            return True
    return False

    
def family_anchored(word):
    """ Return True iff word is an anchored word. """
    _anchors = anchors(word)
    _prefixes = prefixes(word)
    _suffixes = suffixes(word)

    def overcount(w, pattern):
        """Returns how many p on s, works for overlapping"""
        ocu=0
        x=0
        while 1:
            try:
                i=w.index(pattern,x)
            except ValueError:
                break
            ocu+=1
            x=i+1
        return ocu
    
    for candidate in _anchors:
        # The anchor occurs only once in the word.
        if overcount(word,candidate) == 1:        
            left, right = word.split(candidate)
            _prefixes_candidate = prefixes(candidate)            
            _suffixes_candidate = suffixes(candidate)
            # If left is nonempty, we have to check if no prefix of w is a suffix of the anchor
            # Respectively, if right is nonempty, we check if no suffix of w is a prefix of the anchor
            if (left == '' or len([x for x in _prefixes if x in _suffixes_candidate]) == 0) and \
               (right == '' or len([x for x in _suffixes if x in _prefixes_candidate]) == 0):
                return True
    return False


def family_palindrome(word):
    """ Return True iff word is a palindrome. """
    return is_palindrome(word)

    
def family_no1overlap(word):
    """ Return True iff word has no 1-overlap. """
    return len(get_koverlaps(word, 1)) == 0
    
    
def family_outside(word):
    """ Return True if given word does not belong to the following families:
    pow. of primitive, pow. of unbordered, anchored, no1overlap. """
    return not(family_primitive(word) or family_unbordered(word) or
                family_anchored(word) or family_no1overlap(word))