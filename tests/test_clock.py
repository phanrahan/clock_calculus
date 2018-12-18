import pytest
from clock import Clock, take
from fractions import Fraction

@pytest.mark.parametrize("n", [1,2,-1,-2, 
    Fraction(1,3), 
    Fraction(-1,3),
    #Fraction(1,6), 
    Fraction(-1,6), 
    Fraction(5,3)])
def test_init(n):
    c = Clock(n)
    assert c.to_fraction() == n

def test_take():
    y = Clock(2,3)
    assert list(take(y, 10)) == [0, 1, 1, 0, 1, 0, 1, 0, 1, 0]

def test_seq():
    assert Clock([],[0,1]).to_fraction() == Fraction(-2,3)
    assert Clock([],[0,0,0,1]).to_fraction() == Fraction(-8,15)

def test_arith():
    x = Clock([], [1,0,0,0])
    y = Clock([1, 1], [0])
    z = x*y
    assert z.to_fraction() == Fraction(-1,5)
    assert (z/y).to_fraction() == Fraction(-1,15)

def test_logic():
    x = Clock([1,0],[1,1])
    y = Clock([1,1],[1,0])
    print(x & y)
    print(x | y)
    print(x ^ y)
    print(~ x)
    print(x >> 1)
    print(x << 3)

def test_on():
    x = Clock([0, 1, 0],[0,0,1,1,0,0])
    y = Clock([1, 0, 0, 0, 1],[1,0])
    print(x,'on',y,'=',x.on(y))


#print(Clock(1,3))
#print(Clock(1,3).to_fraction())
#print(Clock(-1,6))
#print(Clock(-1,6).to_fraction())
