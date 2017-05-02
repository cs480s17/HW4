import copy
import random
import sys

FileString = ""
NodesExplored = 0
OutputFile = open("output.txt", 'w')

wins = [[[1, 1], [2, 2], [3, 3], [4, 4]],
        [[1, 1], [2, 2], [3, 4], [4, 3]],
        [[1, 1], [2, 3], [3, 2], [4, 4]],
        [[1, 1], [2, 3], [3, 4], [4, 2]],
        [[1, 1], [2, 4], [3, 3], [4, 2]],
        [[1, 1], [2, 4], [3, 2], [4, 3]],

        [[1, 2], [2, 1], [3, 3], [4, 4]],
        [[1, 2], [2, 1], [3, 4], [4, 3]],
        [[1, 2], [2, 3], [3, 1], [4, 4]],
        [[1, 2], [2, 3], [3, 4], [4, 1]],
        [[1, 2], [2, 4], [3, 3], [4, 1]],
        [[1, 2], [2, 4], [3, 1], [4, 3]],

        [[1, 3], [2, 1], [3, 2], [4, 4]],
        [[1, 3], [2, 1], [3, 4], [4, 2]],
        [[1, 3], [2, 2], [3, 1], [4, 4]],
        [[1, 3], [2, 2], [3, 4], [4, 1]],
        [[1, 3], [2, 4], [3, 2], [4, 1]],
        [[1, 3], [2, 4], [3, 1], [4, 2]],

        [[1, 4], [2, 1], [3, 2], [4, 3]],
        [[1, 4], [2, 1], [3, 3], [4, 2]],
        [[1, 4], [2, 2], [3, 1], [4, 3]],
        [[1, 4], [2, 2], [3, 3], [4, 1]],
        [[1, 4], [2, 3], [3, 2], [4, 1]],
        [[1, 4], [2, 3], [3, 1], [4, 2]]]

abexp = 0
mnexp = 0

def miniMaxAlphaBeta(B, alpha, beta, ply):
    global abexp
    abexp += 1
    B._ABEval()
    val = B.h
    if val == None:
        return (0, B)
    if ply == 0:
        return (val, B)
    if (val != -100) and (val != 100): # 1,.5, 0, -1 = leafnodes, if 7 expand
        children = getChildren(B)
        bestleaf = None
        if B.move == 1:
            res = alpha
            for c in children:
                (cval, aleaf) = miniMaxAlphaBeta(c, res, beta, ply-1)
                if(cval > res):
                    res = cval
                    bestleaf = aleaf
                if(res >= beta):
                    return (res, bestleaf)
        elif B.move == 2:
            res = beta
            for c in children:
                (cval, aleaf) = miniMaxAlphaBeta(c, alpha, res,ply-1)
                if(cval < res):
                    res = cval
                    bestleaf = aleaf
                if(res <= alpha):
                    return (res, bestleaf)
        else:
            print("Oh the humanity")
        return (res, bestleaf)
    else:
        return (val, B)

def minMax(B):
    global mnexp
    val = B._minmaxEval()
    mnexp += 1
    if val == 7: # 1,.5, 0, -1 = leafnodes, if 7 expand
        children = getChildren(B)
        bestleaf = None
        if B.move == 2:
            min = 2
            for c in children:
                (cval, aleaf) = minMax(c)
                if(cval < min):
                    min = cval
                    bestleaf = aleaf
            stringBoardAndOutcome(B, min)
            return (min, bestleaf)
        if B.move == 1:
            max = -2
            for c in children:
                (cval, aleaf) = minMax(c)
                if(cval > max):
                    max = cval
                    bestleaf = aleaf
            stringBoardAndOutcome(B, max)
            return (max, bestleaf)
    else:
        stringBoardAndOutcome(B, val)
        return (val, B)

def getChildren(B):
    children = []
    if B.move == 1:
        move = 2
    elif B.move == 2:
        move = 1
    else:
        move = None
    for i in range(len(B.b)):
        for j in range(len(B.b[i])):
            if(B.b[i][j] == 0):
                arr = copy.deepcopy(B.b)
                arr[i][j] = B.move
                child = board(arr)
                child.move = move
                child.parent = B
                children.append(child)
    return children

class board:

    def __init__(self, b):
        self.b = b
        self.move = None
        self.parent = None

    def printBoard(self):
        for r in self.b:
            for i in r:
                sys.stdout.write(str(i) + " ")
            sys.stdout.write("\n")

    def toStringBoard(self):
        global FileString
        for r in self.b:
            for i in r:
                FileString += str(i) + " "
            FileString += "\n"

    def ClearBoard(self):
        blank = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        self.b = blank
        self.move = None
        self.parent = None

    def GenRandomBoard(self,NumMoves):
        self.ClearBoard()
        for i in range(NumMoves):
            index = random.randint(0, 15)
            while self.b[index % 4][index // 4] != 0:
                index = random.randint(0, 15)
            if i % 2 == 0:
                self.b[index % 4][index // 4] = 1
            else:
                self.b[index % 4][index // 4] = 2

    def _minmaxEval(self):
        self.h = 0
        if self.move == None:
            self._determineMove()
        oneWon = False
        twoWon = False
        yazero = False
        for w in wins:
            oneseen = False
            twoseen = False
            nulseen = False
            for i in w:
                if self.b[i[0]-1][i[1]-1] == 1:
                    oneseen = True
                elif self.b[i[0]-1][i[1]-1] == 2:
                    twoseen = True
                else:
                    nulseen = True
                    yazero = True
            if oneseen and not twoseen:
                if not nulseen:
                    oneWon = True

            if twoseen and not oneseen:
                if not nulseen:
                    twoWon = True
        if oneWon and not twoWon:
            return 1
        elif twoWon and not oneWon:
            return 0
        elif not twoWon and not oneWon and not yazero:
            return .5
        else:
            return 7

    def _determineMove(self):
        numOnes = 0
        numTwos = 0
        for i in range(len(self.b)):
            for j in range(len(self.b[i])):
                if (self.b[i][j] == 1):
                    numOnes += 1
                elif (self.b[i][j] == 2):
                    numTwos += 1

        if numOnes == numTwos:
            self.move = 1
        elif numOnes == numTwos + 1:
            self.move = 2
        else:
            return -1

    def _ABEval(self):
        self.h = 0
        cat = True
        if self.move == None:
            self._determineMove()
        for w in wins:
            oneseen = False
            twoseen = False
            nulseen = False
            for i in w:
                if self.b[i[0]-1][i[1]-1] == 1:
                    oneseen = True
                elif self.b[i[0]-1][i[1]-1] == 2:
                    twoseen = True
                else:
                    nulseen = True
            if oneseen and not twoseen:
                if nulseen:
                    cat = False
                    self.h += 1
                else:
                    self.h = 100
                    return
            if twoseen and not oneseen:

                if nulseen:
                    cat = False
                    self.h -= 1
                else:
                    self.h = -100
                    return
        if cat == True:
            self.h = None

def stringBoardAndOutcome(B, Outcome):
    global FileString
    global NodesExplored
    global OutputFile
    NodesExplored += 1
    B.toStringBoard()
    FileString += "~" + str(Outcome) + "#\n"
    if NodesExplored%10000 == 0:
        print(NodesExplored, "Nodes Explored...")
        OutputFile.write(FileString)
        FileString = ""

def outputPath(node):
    if node.parent == None:
        print(node.b)
    else:
        outputPath(node.parent)
    print(node.b)

def NextMove(node):
    if node.parent == None:
        print("Game Already Over.")
    if node.parent.parent == None:
        for i in node.b:
            print(i)
    else:
        NextMove(node.parent)



def main():
    '''
    arrr = [[1, 2, 0, 0],
            [1, 0, 2, 0],
            [2, 0, 0, 1],
            [2, 0, 0, 1]]
    arrr = [[1, 2, 2, 0],
            [1, 1, 2, 0],
            [0, 0, 0, 0],
            [2, 1, 0, 0]]
    arrr = [[2, 0, 0, 2],
            [2, 1, 0, 1],
            [2, 0, 0, 1],
            [0, 0, 0, 1]]
            1 2 0 0 1 0 2 0 2 0 0 1 2 0 0 1
    '''

    global mnexp, abexp, FileString
    arrr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    B = board(arrr)

    for i in range(1):
        print("Generating Board")
        B.GenRandomBoard(7)
        print("running minMax(B)")
        minMax(B)
    print("writing to file")
    out.write(FileString)
    return
    #string = input("Please input your board below, as a 4x4 matrix of 2's, 1's, and 0's: \nInput should be of form:\n1 2 0 0\n1 0 2 0\n2 0 0 1\n2 0 0 1\n")
    #b = string.split()
    #if len(b) == 4:
    #    for i in range(3):
    #        tempstring = input()
    #        tempb = tempstring.split()
    #        b.extend(tempb[:])
    #for i in range(4):
    #    for j in range(4):
    #        arrr[i][j] = int( b[i*4 + j])
    #thing = board(arrr)
    #(Minmax, MMOptimal) = minMax(thing)
    #(Alphabeta, ABOptimal) = miniMaxAlphaBeta(thing, -256, 255, 6)
    #print("Minmax has expanded ", mnexp, " nodes.")
    #print("Minmax returns: ", Minmax)
    #print("Minmax Recomends next move:")
    #NextMove(MMOptimal)
    #print("Alphabeta has expanded ", abexp, " nodes.")
    #print("Alphabeta returns: ", Alphabeta)
    #print("Alphabeta Recomends next move:")
    #NextMove(ABOptimal)

if __name__ == "__main__":
    main()

