import operator
from fractions import Fraction, gcd
from itertools import cycle, chain, islice

def seq2int(seq):
    n = 0
    for e in seq:
        n = 2 * n + e
    return n

def ones(seq):
    return sum(seq)

def map1(op, x):
    return [op(xi) & 1 for xi in x]

def map2(op, x, y):
    return [op(xi, yi) & 1 for xi, yi in zip(x,y)]

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

# expand x and y so that the 
#  len(prefix) = max(len(prefix(x)),len(prefix(y)))
#  len(suffix) = lcm(len(suffix(x)),len(suffix(y)))
def expand(x, y):
    nx = len(x.prefix())
    ny = len(y.prefix())
    nr = max(nx, ny)

    mx = len(x.suffix())
    my = len(y.suffix())
    mr = mx*my//gcd(mx, my) # lcm

    xl = list(take(x, nr+mr))
    yl = list(take(y, nr+mr))

    return Clock(xl[:nr], xl[nr:]), Clock(yl[:nr], yl[nr:])

# expand x and y so that their prefix/suffix has the same number of 1s
def onesexpand(x, y):
    pass

# expand x and y so that the prefix/suffix of x
# has the same number of ones as the length
# of the prefix/suffix of y.
def onexpand(s, y):
    pass

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

    def binaryop(self, other, op):
       x, y = expand(self, other)
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


    # two sequences are synchronizable if the percentage of ones are the same
    def synchronizable(self, other):
        x, y = expandones(self, other)
        x = Fraction(ones(x.suffix()), len(x.suffix())) 
        y = Fraction(ones(y.suffix()), len(y.suffix())) 
        return x == y

    # on


x = Clock(1,6)
print(x)
print(x.to_fraction())
#print(list(take(x, 10)))

#y = Clock(2,3)
#print(y)
#print(y.to_fraction())
#print(list(take(y, 10)))

#x, y = expand(x, y)
#print(x)
#print(y)

#print(x & y)
#print(x | y)
#print(x ^ y)
#print(~ x)

y = x >> 1
print(y)
print(y.to_fraction())
y = x << 3
print(y)
print(y.to_fraction())
