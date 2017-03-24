
import functions
from ziruph import Ziruphtable
import string
import math
import struct
import base64

class Link:
    def __init__(self, link):
        self.link = link

    def ziruph(self, other):
        p = string.ascii_letters
        if abs(self) > len(p):
            p = " "*(abs(self) - len(p)) + p
        else:
            p = p[:abs(self)]
        z = Ziruphtable(p)

        output = ""
        n = min(len(self.link), len(other.link))
        for i in range(n):
            output += z[self.link[i], other.link[i]]
        self.link = output

    def antiziruph(self, other):
        p = string.ascii_letters
        if abs(self) > len(p):
            p = " "*(abs(self) - len(p)) + p
        else:
            p = p[:abs(self)]
        z = Ziruphtable(p)

        n = min(len(self.link), len(other.link))
        outputs = [""]
        for i in range(n):
            tmp = []
            for r in z.reverse((self.link[i], other.link[i])):
                for o in outputs:
                    tmp.append(o+r)
            if len(tmp) > 0:
                outputs = tmp[:]
        return [Link(o) for o in outputs]

    def __str__(self):
        return "Link[*{0}*]".format(self.link)

    def __abs__(self):
        return functions.gematria(self.link)

    def ngem(self):
        return math.log10(abs(self)/len(self.link))

    def optimal_compression(self):
        return functions.optimal_compression(self.link)

    def compress(self):
        self.link = self.optimal_compression()
        return self

    def binary(self):
        output = b""
        for c in self.link:
            output += struct.pack("=B", ord(c)-ord('A'))
        return base64.b64encode(output)
