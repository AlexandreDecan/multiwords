#!/usr/bin/python

class Sequence():
    """ Sequence construction in order to detect the "sure presence"
    of a word w in a multiword m """
    
    def __init__(self, m, w):
        self.m = m
        self.w = w
        self.i = 0
        self.S = set([''])
        self.iterator = self.__iter__()
        self.returns_string = True
        
    def __iter__(self):
        while self.i < len(self.m):
            yield self.S 
            self.S = set([sufpre(p+a, self.w) for p in self.S \
                                         for a in self.m[self.i]])
                                         
            self.S = lower_bound(self.S, self.w)                             
                                         
            while self.w in self.S:
                self.S.remove(self.w)
            self.i = self.i + 1
        yield self.S
        
    def next(self):
        """ Go to the next step and return the current result """
        # Maybe this method can be removed
        self.iterator.next()
        if self.returns_string:
            return str(self)
        else:
            return self.S		
        
    def apply(self):
        """ Apply the sequence and return the last result """
        for _ in self:
            pass
        return self.S
        
    def __index__(self):
        return self.i    
        
    def __str__(self):
        return 'Step %d = {%s}' % (self.i, ','.join(sorted(self.S)))
        
    def __repr__(self):
        return str(self)


def lower_bound(prefixes, w):
    """ Return the "lower bound" of a set of prefixes. This is, the minimal
    subset wrt. inclusion such that every element of prefixes has a suffix in
    the lower bound set """
    n_pref = set(prefixes.copy())
    for e in prefixes:
        for e2 in prefixes:
            if e != e2 and e2.endswith(e):
                try:
                    n_pref.remove(e2)
                except KeyError:
                    pass
    if w in n_pref:
        n_pref.remove(w)
    return n_pref


def sufpre(p, w):
    """ Return the maximal suffix of p which is also
        a prefix of w """
    for i in range(0, len(p)):
        if w.startswith(p[i:]):
            return p[i:]
    return ''

