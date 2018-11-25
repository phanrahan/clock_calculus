# A Clock Calculus for Infinite Periodic Signals

Infinite periodic signals are equivalent to proper fractions. 

A fraction is proper if its numerator is less than its denominator.

We use the notation ([0, 0], [0, 1]) to means the infinite sequence
beginning with 0, 0 and then repeating 0, 1. 

0, 0, 0, 1, 0, 1, 0, 1, ...

We will normally be interested in repeating sequences with at least one 1.

## Reducible / Normalizable

Infinite periodic Sequences can be converted to fractions.

Fractions can be converted to infinite periodic sequences.

Reducing a fraction means setting the numerator and denominator
so that they have no common factors. That is, their gcd(num, dem) == 1.

Infinite periodic sequences can be normalized by converting
them to a reduced proper fraction.

An infinite periodic sequence is the one with the shortest prefix
and the shortest repeating pattern.

## Operators

Two infinite periodic sequences are compatible if the length of the
initial sequences and repeating sequences are the same.

Given two infinite periodic sequences, we can make them compatible
with the length of the initial sequence equal to the max of the
lengths of the two initial sequences, and the length of the
repeating sequence equal to the lcm (least common multiple) of
the two repeating sequences.

Compatible sequences are no longer in the reduced form, but they
are equal to the original sequences.

We can form binary operators between sequences by making them compatible,
and then applying the binary operator between the initial and repeating
sequences.

The operator on subsamples a clock. c on w is defined.

0.w on w' = 0.(w on w')
1.w on 0.w' = 0.(w on w')
1.w on 1.w' = 1.(w on w')

For example,

(01) on (101) = (010101) on (101) = (010001)

## Digital Signals

Infinite binary sequences can be used to represent digital signals.

The delay or register operator shifts the sequence right.

Binary operators can be used to compute combinational functions
on the signals.

