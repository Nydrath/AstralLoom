import math
import random

class MagicalSquare:
    def __init__(self, size):
        self.size = size
        self.createsq(self.size)
        self.mutatesq()

    def __str__(self):
        n = (len(self.square)-1) + len(self.square)*(int(math.log10(len(self.square)**2))+1) + 2
        output = "-"*n+"\n"
        for row in zip(*self.square):
            output += "|"
            numbers = []
            for x in row:
                s = str(x).zfill(int(math.log10(len(row)**2))+1)
                s = " "*(len(s)-len(s.lstrip("0")))+s.lstrip("0")
                numbers.append(s)
            output += " ".join(numbers)
            output += "|\n"
        return output + "-"*n

    def getluxbox(self, x, y, m):
        if y < m:
            return [(1, 0), (0, 1), (1, 1), (0, 0)]# L
        elif y == m:
            if x == m:
                return [(0, 0), (0, 1), (1, 1), (1, 0)]# U
            else:
                return [(1, 0), (0, 1), (1, 1), (0, 0)]# L
        elif y == m+1:
            if x == m:
                return [(1, 0), (0, 1), (1, 1), (0, 0)]# L
            else:
                return [(0, 0), (0, 1), (1, 1), (1, 0)]# U
        else:
            return [(0, 0), (1, 1), (0, 1), (1, 0)]# X

    def createsq(self, n):
        self.square = [[0]*n for j in range(n)]

        counter = 1
        if n%2:
            # Create square by siamese method
            x = int(n/2)
            y = 0
            while counter <= n**2:
                self.square[x][y] = counter
                counter += 1
                if self.square[(x+1)%n][(y-1)%n] == 0:
                    x = (x+1)%n
                    y = (y-1)%n
                else:
                    y = (y+1)%n
        elif n != 2:
            if (n/2)%2:
                # Use Conway method
                m = int((n-2)/4)
                m2 = 2*m+1
                x = int(m)
                y = 0
                while counter <= n**2:
                    for i, j in self.getluxbox(x, y, m):
                        self.square[2*x+i][2*y+j] = counter
                        counter += 1
                    if self.square[2*((x+1)%m2)][2*((y-1)%m2)] == 0:
                        x = (x+1)%m2
                        y = (y-1)%m2
                    else:
                        y = (y+1)%m2
            else:
                # Use https://arxiv.org/ftp/arxiv/papers/1202/1202.0948.pdf
                for x in range(int(n/2)):
                    for y in range(n):
                        self.square[x][y] = counter
                        counter += 1
                for x in range(int(n/2), n):
                    for y in range(n-1, -1, -1):
                        self.square[x][y] = counter
                        counter += 1

                for y in range(n):
                    for x in range(int(n/2)):
                        if self.square[x][y]%2 == (y>=n/2):
                            tmp = self.square[n-x-1][y]
                            self.square[n-x-1][y] = self.square[x][y]
                            self.square[x][y] = tmp

                for i in range(-1, 1):
                    tmp = self.square[int(n/2)+i][int(n/2)]
                    self.square[int(n/2)+i][int(n/2)] = self.square[int(n/2)+i][n-1]
                    self.square[int(n/2)+i][n-1] = tmp

    def mutatesq(self):
        if random.randint(0, 1):
            self.square = [list(x) for x in zip(*self.square)]
        for r in range(random.randint(1, 3)):
            self.square = [list(x) for x in zip(*self.square[::-1])]

