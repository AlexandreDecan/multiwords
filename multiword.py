#!/usr/bin/python

import sequence

class Multiword():
    """ Multiwords are sequences of sets of symbols.
    Each method is documented. Traditionnal operators are surcharged :
    len(mw)     - size of current multiword
    mw & mw2    - union of two multiwords
    w in mw     - inclusion (if multiword) or 'sure containmnent' test
    mw == mw2   - same content
    mw[i]       - get and set (work by copy)
    mw[i:j]     - (partial and total) slices supported
    hash(mw)    - (experimental) hash method
    for x in mw - natural iterator over sets of symbols
    mw * x      - classical exponentiation over words
    str(mw),repr(mw)    - pretty printable representation

    Other operations are documented and described bellow. """

    def __init__(self, param=''):
        """ The parameter can be :
         - a word
         - a multiword
         - a list of words
         ... or nothing ! """
        self.content = []
        if isinstance(param, str):
            for e in param:
                self.content.append(set(e))
        elif isinstance(param, Multiword):
            for e in param:
                self.content.append(e)
        elif isinstance(param, list) or isinstance(param, tuple):
            m = Multiword()
            for word in param:
                m = m & word
            self.content = m.content
        else:
            raise TypeError, 'Argument type %s unsupported' % type(param)

    def __str__(self):
        """ # Other representation
        l1 = [' ']*len(self)
        l2 = [' ']*len(l1)
        for i,e in enumerate(self):
            if len(e) == 1:
                l1[i] = ''.join(e)
            else:
                e2 = sorted(e)
                l1[i] = e2[0]
                l2[i] = e2[1]
        return ''.join(l1)+'\n'+''.join(l2)
        """
        rslt = ''
        for el in self:
            if len(el) == 1:
                rslt = '%s %s' % (rslt, ''.join(el))
            else:
                rslt = '%s {%s}' % (rslt, ','.join(sorted(el)))
        return '<%s >' % rslt

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Multiword):
            if len(self) == len(other):
                for i in range(len(self)):
                    if self[i] != other[i]:
                        return False
                return True
            else:
                return False
        else:
            raise TypeError, 'Argument must be a Multiword, not %s' % type(other)

    def __add__(self, other):
        """ Add either a multiword or a word to the right """
        mw = Multiword()
        if isinstance(other, Multiword) or isinstance(other, str):
            for el in self:
                mw.append(el)
            for el in other:
                mw.append(el)
            return mw
        else:
            raise TypeError, 'Argument type %s unsupported' % type(other)


    def __len__(self):
        return len(self.content)

    def __getitem__(self, i):
        """ Return a copy of the set at position i """
        return self.content[i].copy()

    def __setitem__(self, i, el):
        """ Set a copy of el at position i """
        self.content[i] = el.copy()

    def __iter__(self):
        return self.content.__iter__()

    def __mul__(self, other):
        if isinstance(other, int):
            mw = Multiword()
            for i in range(other):
                for el in self:
                    mw.append(el)
            return mw
        else:
            raise TypeError, 'Argument type %s unsupported' % type(other)

    def __contains__(self, other):
        """ Check if parameter is in this multiword. Parameter can be :
         - a set of symbols. Return true if this set appears exactly
                somewhere in the multiword.
         - a word. Return true if the word is "sure" in this multiword.
         - another multiword : return true if the parameter is
                included in the current multiword. """
        if isinstance(other, set):
            return other in self.content
        elif isinstance(other, str):
            seq = sequence.Sequence(self, other)
            return len(seq.apply()) == 0
        elif isinstance(other, Multiword):
            if len(other) <= len(self):
                for i in range(len(other)):
                    if other[i] != self[i]:
                        return False
                return True
            return False
        else:
            raise TypeError, 'Argument type %s unsupported' % type(other)

    def __getslice__(self, i, j):
        i = max(0, i)
        j = min(j, len(self))
        m = Multiword()
        for p in range(i, j):
            m.append(self[p])
        return m

    def __and__(self, other):
        """ Called with (m & o). Perform the union between the current
        and the other multiwords. Parameter can be a word too """
        if isinstance(other, Multiword) or isinstance(other, str):
            mw = Multiword()
            for i in range(max(len(self), len(other))):
                el = set()
                if i < len(self):
                    el = el.union(self[i])
                if i < len(other):
                    el = el.union(other[i])
                mw.append(el)
            return mw
        else:
            raise TypeError, 'Argument type %s unsupported' % type(other)

    def __hash__(self):
        """ EXPERIMENTAL : Try to compute an appropriate hash value.
        Please note, as multiwords use lists and sets to store
        data, hash values can only be used if NO modifications are
        made AFTER on the multiword.
        Otherwise, border effects certainly appear. """
        return hash(''.join([list(i)[0] for i in self]))

    def __cmp__(self, other):
        """ Compare two multiwords by considering ONLY length """
        return len(self) - len(other)

    def words(self):
        """ Return the set of every possible words of this multiword """
        if len(self) == 1:
            return [x for x in sorted(self[0])]
        else:
            return [a + x for a in sorted(self[0]) for x in self[1:].words()]

    def append(self, el):
        """ Add a set of symbol to the right of the multiword.
        Note that the set is duplicated in order to avoid border effect """
        self.content.append(el.copy())

    def minimize(self, w):
        """ Return a new multiword which is obtained by
        removing first and last elements until w is not found. """
        if w not in self:
            raise Exception, 'Can\'t minimize: %s not in %s' % (w, self)
        i, j = 0, len(self)
        while w in self[i + 1:j]:
            i = i + 1
        while w in self[i:j-1]:
            j = j - 1
        return self[i:j]

    def isMinimal(self, w):
        """ Return true if current multiword coincide with the minimal
        one. """
        return self == self.minimize(w)

    def startswith(self, other):
        """ Return true if current multiword starts with given
        word or multiword """
        if isinstance(other, str) or isinstance(other, Multiword):
            if len(other) <= len(self):
                for i in range(len(other)):
                    if other[i] != self[i]:
                        return False
                return True
            else:
                return False
        else:
            raise TypeError, 'Argument type %s unsupported' % type(other)


def multiword_from_word(w, shift = 0):
    """ Return a new multiword that is constructed from word 
    w, this is, {w_1}{w_2}{w_3}...
    The shift parameter can be used to create a multiword that is 
    constructed from w + a shift of w. For example, if w = aab and 
    shift = 1, then the multiword will be {a}{a}{a,b}{b}. 

    shift must be between 0 and |w| - 1. """
    
    shifted_w = w[:shift] + w
    nonshifted_w = w + w[-shift:] if shift != 0 else w
    return Multiword([shifted_w, nonshifted_w])
