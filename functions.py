def gematria(s):
    output = 0
    for c in s.lower():
        if c.isalpha():
            output += ((ord(c)-ord('a'))%9+1) * 10**int((ord(c)-ord('a'))/9)
        elif c.isdigit():
            output += int(c)
    return output

def sumofdigits(s):
    a = str(sum([int(c) for c in s]))
    if len(a) > 1:
        return sumofdigits(a)
    else:
        return int(a)
