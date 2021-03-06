import operator
from math import gcd
from fractions import Fraction
from itertools import cycle, chain, islice

# lsb first
def seq2int(seq):
    return sum([e<<i for i, e in enumerate(seq)])

# lsb first
def int2seq(n):
    l = []
    while n > 0:
        l.append( n & 1 )
        n >>= 1
    return l

def lcm(x, y):
    return x*y//gcd(x, y) 

def ones(seq):
    return sum(seq)

def map1(op, x):
    return [op(xi) & 1 for xi in x]

def map2(op, x, y):
    return [op(xi, yi) & 1 for xi, yi in zip(x,y)]

# subsample x according to y
def on(x, y):
    if not y:
        return []
    if x[0] == 0:
        return [0] + on(x[1:], y)
    else:
        if y[0]:
            return [1] + on(x[1:], y[1:])
        else:
            return [0] + on(x[1:], y[1:])

# long division from the right
#
# return an infinite periodic sequence of binary digits
def divide(x):
    p = x._numerator 
    q = x._denominator
    if q < 0:
        p = -p
        q = -q

    n = 0
    while q&1 == 0:
        n += 1
        q //= 2

    b = []
    l = []
    # loop until p repeats
    # note that this fact implies that we cannot loop more than q times
    while p not in l:
        #print(p)
        l.append(p)
        if p & 1:
            b.append(1)
            p -= q
        else:
            b.append(0)
        p //= 2

        
    #print(b, p, l)
    i = l.index(p)
    return b[:i], b[i:], n

def clock(initial, repeat):
    return chain(initial, cycle(repeat))

take = islice

class Clock:
    def __init__(self, x, y=1):
        if isinstance(x, Fraction):
            self.signal = divide(x)
        elif isinstance(x, int) and isinstance(y, int):
            self.signal = divide(Fraction(x,y))
        elif isinstance(x, list) and isinstance(y, list):
            self.signal = (x, y, 0)
        else:
             raise ValueError('Clock init')

    def prefix(self):
        return self.signal[0]

    def suffix(self):
        return self.signal[1]

    # return the position of the p'th 1
    #  note that in the paper, positions start at 1, here they start at 0
    def pos(self, p):
        n = 0
        for i, c in enumerate(self):
            if c:
                n += 1
            if n == p:
                return i

    def __str__(self):
        return str(self.signal)

    def __iter__(self):
        return clock(self.prefix(), self.suffix())

    def to_fraction(self):
       n = self.signal[2] 
       p = list(self.prefix())
       np = len(p)
       s = list(self.suffix())
       ns = len(s)

       p = Fraction(seq2int(p))
       s = Fraction(seq2int(s)<<np,((1<<ns)-1))
       return (p-s)*Fraction(1,1<<n)

    def unaryop(self, op):
       return Clock( map1(op, self.prefix()),
                     map1(op, self.suffix()) )

    def __invert__(self):
       return self.unaryop(operator.__invert__)

    def expand(self, nr, mr):
        l = list(take(self, nr+mr))
        return Clock(l[:nr], l[nr:])

    def binaryop(self, other, op):
        x, y = self, other

        # expand x and y so that the 
        #  len(prefix) = max(len(prefix(x)),len(prefix(y)))
        #  len(suffix) = lcm(len(suffix(x)),len(suffix(y)))
        nr = max( len(x.prefix()), len(y.prefix()) )
        mr = lcm( len(x.suffix()), len(y.suffix()) )

        x = x.expand(nr, mr)
        y = y.expand(nr, mr)

        return Clock( map2(op, x.prefix(), y.prefix()), 
                      map2(op, x.suffix(), y.suffix()) )


    def __and__(self, other):
       return self.binaryop(other, operator.__and__)
    def __rand__(self,other):
       return self&other

    def __or__(self, other):
       return self.binaryop(other, operator.__or__)
    def __ror__(self,other):
       return self|other

    def __xor__(self, other):
       return self.binaryop(other, operator.__xor__)
    def __rxor__(self,other):
       return self^other

    def __lshift__(self, other):
       assert isinstance(other, int)
       f = self.to_fraction()
       return Clock(f._numerator << other, f._denominator)

    def __rshift__(self,other):
       assert isinstance(other, int)
       f = self.to_fraction()
       return Clock(f._numerator, f._denominator << other)

    def __neg__(self):
       return Clock(~x+Clock(1))

    def __add__(self, other):
       x = self.to_fraction()
       y = other.to_fraction()
       return Clock(x-y)
    def __radd__(self,other):
       return self+other

    def __sub__(self, other):
       x = self.to_fraction()
       y = other.to_fraction()
       return Clock(x-y)
    def __rsub__(self,other):
       return self-other

    def __mul__(self, other):
       x = self.to_fraction()
       y = other.to_fraction()
       return Clock(x*y)
    def __rmul__(self,other):
       return self*other

    def __truediv__(self, other):
       x = self.to_fraction()
       y = other.to_fraction()
       return Clock(x/y)
    def __rtruediv__(self,other):
       return self/other

    # the rate is the percentage of ones
    def rate(self):
        return Fraction(ones(x.suffix()), len(x.suffix())) 

    # two sequences are synchronizable if their rates are equal
    def synchronizable(self, other):
        return self.rate() == other.rate()

    def on(self, other):
        x, y = self, other

        xl = ones(x.prefix())
        yl = len(y.prefix())
        n = lcm( ones(x.suffix()), len(y.suffix()) )
        m = len(x.suffix()) * n // ones(x.suffix())
        #print(m,n)
        if   xl < yl:
            x = x.expand( x.pos(yl)+1, m )
        elif yl < xl:
            x = x.expand( len(x.prefix()), m )
            y = y.expand( xl, n )
        else:
            x = x.expand( len(x.prefix()), m )
            y = y.expand( len(y.prefix()), n )

        return Clock( on(x.prefix(), y.prefix()), on(x.suffix(), y.suffix()) )

