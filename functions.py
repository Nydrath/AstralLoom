import string
import math

def gematria(s):
    output = 0
    for c in s.lower():
        if c.isalpha():
            output += ((ord(c)-ord('a'))%9+1) * 10**int((ord(c)-ord('a'))/9)
        elif c.isdigit():
            output += int(c)
    return output

def optimal_compression(s):
    alphabet = string.ascii_lowercase[::-1]
    output = ""
    for letter in alphabet:
        while gematria(letter) + gematria(output) <= gematria(s):
            output += letter
    return output

def sumofdigits(s):
    a = str(sum([int(c) for c in s]))
    if len(a) > 1:
        return sumofdigits(a)
    else:
        return int(a)

def primefactorization(n):
    factors = []
    isprime = lambda y: all(y%x != 0 for x in factors if x != y)
    for d in range(2, n+1):
        while n%d == 0:
            if isprime(d):
                factors.append(d)
                n /= d
    return factors
