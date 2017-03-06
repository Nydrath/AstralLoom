
from functions import gematria
from ziruph import Ziruphtable
import string

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

    def __str__(self):
        return "Link[*{0}*] | ngem = {1}".format(self.link, self.ngem())

    def __abs__(self):
        return gematria(self.link)

    def ngem(self):
        return abs(self)/len(self.link)
