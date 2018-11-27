import operator
from fractions import Fraction, gcd
from itertools import cycle, chain, islice

def seq2int(seq):
    n = 0
    for e in seq:
        n = 2 * n + e
    return n

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

# long division 
#
# return an infinite periodic sequence of binary digits
def divide(x):
    p = x._numerator % x._denominator
    q = x._denominator

    l = []
    b = []
    # loop until the q repeats
    # note that this implies that we cannot that loop more than q times
    while p not in l:
        l.append(p)
        if 2*p > q: # denominator divides numerator
            b.append(1)
            p = 2*p - q
        else:
            b.append(0)
            p = 2*p
        
    #print(b, p, l)
    i = l.index(p)
    return b[:i], b[i:]

def clock(initial, repeat):
    return chain(initial, cycle(repeat))

take = islice

class Clock:
    def __init__(self, x, y=None):
        if isinstance(x, Fraction):
            self.signal = divide(x)
        elif isinstance(x, int) and isinstance(y, int):
            self.signal = divide(Fraction(x%y,y))
        elif isinstance(x, list) and isinstance(y, list):
            self.signal = (x, y)
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
       den = 1 << len(self.prefix() + self.suffix())
       if self.prefix():
           den -= 1 << len(self.prefix())
       else:
           den -= 1
       num = seq2int(self.prefix() + self.suffix()) - seq2int(self.prefix())
       return Fraction(num, den)

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
        #print(x)
        #print(y)

        return Clock( on(x.prefix(), y.prefix()), on(x.suffix(), y.suffix()) )


#x = Clock(1,6)
#print(x)
#print(x.to_fraction())
#print(x.pos(2))
#print(list(take(x, 10)))

#y = Clock(2,3)
#print(y)
#print(y.to_fraction())
#print(list(take(y, 10)))

#print(x & y)
#print(x | y)
#print(x ^ y)
#print(~ x)

#y = x >> 1
#print(y)
#print(y.to_fraction())
#y = x << 3
#print(y)
#print(y.to_fraction())

x = Clock([],[0,1])
y = Clock([],[1,0,1])
print(x,'on',y,'=',x.on(y))

x = Clock([0, 1, 0],[0,0,1,1,0,0])
y = Clock([1, 0, 0, 0, 1],[1,0])
print(x,'on',y,'=',x.on(y))
