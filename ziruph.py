
import string

class Ziruphtable:
    def __init__(self, powers):
        self.powers = powers
        self.alphabet = string.ascii_lowercase

        rows = self.alphabet[len(self.powers):]+self.alphabet[:len(self.powers)]
        rows = rows[::-1]
        self.table = {}
        for row in self.alphabet:
            self.table[row] = {}

        counter = 0
        for rowidx, row in enumerate(rows):
            if rowidx%2:
                columns = self.powers[::-1]
            else:
                columns = self.powers[:]

            for column in columns:
                self.table[row][column] = self.alphabet[counter]
                counter = (counter+1)%len(self.alphabet)

    def __getitem__(self, args):
        """Format: [input word, power to convolve with]. Will error if power isn't in the list given in initialization."""
        (word, power) = args
        if power not in self.powers:
            print("ERROR: {1} requested to be ziruph'd with {0}, but {0} does not exist in the table as a power.".format(power, word))
            raise LookupError

        output = ""
        for c in word:
            if c.isalpha():
                tmp = self.table[c.lower()][power]
                if c.isupper():
                    tmp = tmp.upper()
                output += tmp
            else:
                output += c

        return output

    def __str__(self):
        output = " ".join(self.powers) + "   Input\n"
        for key, row in sorted(self.table.items()):
            for power in self.powers:
                output += self.table[key][power]
                output += " "*len(power)
            output += "| " + key + "\n"
        return output
