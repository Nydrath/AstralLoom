import math
import random
from PIL import Image
from PIL import ImageDraw

class MagicalSquare:
    def __init__(self, planet):
        self.planetidx = "Saturn Jupiter Mars Sun Venus Mercury Moon Earth".split().index(planet)+3
        self.createsq(self.planetidx)
        self.mutatesq()

    def __str__(self):
        n = (len(self.square)-1) + len(self.square)*(int(math.log10(len(self.square)**2))+1) + 2
        output = "-"*n+"\n"
        for row in zip(*self.square):
            output += "|"+" ".join([str(x).zfill(int(math.log10(len(row)**2))+1) for x in row])+"|\n"
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


    def sumofdigits(self, s):
        a = str(sum([int(c) for c in s]))
        if len(a) > 1:
            return self.sumofdigits(a)
        else:
            return int(a)

    def __getitem__(self, intent):

        # COMPLETELY BROKEN, RETHINK

        intent = "".join([c for c in intent if c.isalpha()]).lower()
        S = 0
        for c in intent:
            number = ((ord(c)-ord('a'))%9+1)*10**int((ord(c)-ord('a'))/9)
            S += number
        #imagescale = 100
        #border = int(imagescale*1.0)
        #im = Image.new("L", (planet*imagescale+2*border, planet*imagescale+2*border), color=255)
        #drawer = ImageDraw.Draw(im)
        #dotsize = int(imagescale*0.4/math.sqrt(2))
        outputsq;
        x, y = 0, 0
        for i in range(self.planetidx**2):
            if self.sumofdigits(str(self.square[x][y])+str(S)[i%len(str(S))]) == self.planetidx:
                print(self.square[x][y])
                outputsq[x][y] = "#"*(int(math.log10(len(self.square)**2))+1)
                #drawer.ellipse((x*imagescale-dotsize+border, y*imagescale-dotsize+border, x*imagescale+dotsize+border, y*imagescale+dotsize+border), fill=0)
            else:
                outputsq[x][y] = " "*(int(math.log10(len(self.square)**2))+1)
            x = (x+1)%self.planetidx
            if x == 0:
                y = (y+1)%self.planetidx

        #im.save(intent+".png")
        output = 
        return str(outputsq)



a = MagicalSquare("Mercury")
print(a["ABA"])
