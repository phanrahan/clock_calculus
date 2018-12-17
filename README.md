# A Clock Calculus for Infinite Periodic Signals

We use the notation ([0, 0], [0, 1]) to means the infinite sequence
beginning with 0, 0 and then repeating 0, 1. 

0, 0, 0, 1, 0, 1, 0, 1, ...

Infinite periodic signals are equivalent to rational numbers in 2-adic.

Infinite binary sequences can be used to represent 
periodic digital signals.

We will normally be interested in repeating sequences where the
repeating part has at least one 1.

## Operators

Invert (~) is defined by inverting each bit in initial
and repeating parts of the sequence.
Shifting left and right is also easy to perform.

Two infinite periodic sequences are compatible if the length of the
initial sequences and repeating sequences are the same.

Given two infinite periodic sequences, we can make them compatible.
The length of the initial part is equal to the max of the
lengths of the two initial parts, and the length of the
repeating part is equal to the lcm (least common multiple) of
the two repeating parts.

We can form binary operators between sequences by making them compatible,
and then applying the binary operator between the initial and repeating
sequences. This allows us to define &, |, and ^. 

The operator on subsamples a clock. c on w is defined.

0.w on w' = 0.(w on w')
1.w on 0.w' = 0.(w on w')
1.w on 1.w' = 1.(w on w')

For example,

(01) on (101) = (010101) on (101) = (010001)

Define arithmetic operators: addition (+), subtraction (-).
multiplication (*), division (/), and modulo (%).
