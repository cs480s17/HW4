import copy
import random
import sys

FileString = ""
NodesExplored = 0
OutputFile = open("boards.txt", 'a')
DataSet = open("boards.txt", 'r')
StatsOutput = None
StatsRead = open("stats.txt", 'r')


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
    global p1_stats, p2_stats
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
    if(p1_stats == []):
        random.shuffle(children)
    else:
        if (B.move == 1):
            sortExpanded(children, p1_stats)
        else:
            sortExpanded(children, p2_stats)
    return children

def sortExpanded(children, stats):
    childs = []
    for i in range(len(children)):
        prob = calculateProbability(children[i], stats)
        childs.append([copy.deepcopy(children[i]), prob])
    childs.sort(key=lambda x: x[1])
    for c in childs:
        children[i] = c[0]
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
            FileString += (' '.join(map(str, r))) + '\n'
            #for i in r:
            #    FileString += str(i) + " "
            #FileString += "\n"

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

def calculateProbability(board, stats):
    for value in range(3):
        pass

def InputParse():
    global DataSet
    print("Reading data file to string")
    string = DataSet.read()
    print("Parsing string to list")
    b = string.split('#\n')[:-1]
    for i in range(len(b)):
        if i%100000 == 0:
            print("We have parced", i, "boards")
        b[i] = b[i].split('\n~')
        b[i][0] = b[i][0].split('\n')
        b[i][1] = float(b[i][1])
        for j in range(len(b[i][0])):
            b[i][0][j] = b[i][0][j].split()
            b[i][0][j] = list(map(int, b[i][0][j]))
    return b

def genStats(dataset):
    num_checked = 0
    num_p1_wins = 0 #set num p1 wins to 0
    num_p2_wins = 0 #num p2 wins
    count =              [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
    count_given_p1_win = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]]
    count_given_p2_win = [[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                          [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]] #Zeros
    print("Gathering cell counts")
    for b in range(len(dataset)):
        if b%100000 == 0:
            print("Processed", b, "boards")
        num_checked += 1
        if dataset[b][1] == 0.0:
            num_p2_wins += 1
            for i in range(4):
                for j in range(4):
                    count_given_p2_win[dataset[b][0][i][j]][i][j] += 1 #totally readable
                    count[dataset[b][0][i][j]][i][j] += 1 #totally readable
        elif dataset[b][1] == 1.0:
            num_p1_wins += 1
            for i in range(4):
                for j in range(4):
                    count_given_p1_win[dataset[b][0][i][j]][i][j] += 1 #totally readable
                    count[dataset[b][0][i][j]][i][j] += 1 #totally readable
        elif dataset[b][1] == 0.5:
            for i in range(4):
                for j in range(4):
                    count[dataset[b][0][i][j]][i][j] += 1 #totally readable i hope it works dude
        else:
            print("Oh shiiiiiiiiiitttttt " + str(b[1]))#ESxCEPTIONdsds
    #Prob_p1_wins_given_value = [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
    #                            [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
    #                            [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]]
    #Prob_p2_wins_given_value = [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
    #                            [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
    #                            [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]]
    #print("Computing win probabilities given specific cells")
    #for value in range(3):
    #    for i in range(4):
    #        for j in range(4):
    #            Prob_p1_wins_given_value[value][i][j] = (float(count_given_p1_win[value][i][j]+1)/float(num_p1_wins+1)) * (float(num_p1_wins+1)/float(num_checked+1))\
    #                                                    / (float(count[value][i][j]+1)/float(num_checked+1)) #P(x|win) * P(win) / P(x)
    #for value in range(3):
    #    for i in range(4):
    #        for j in range(4):
    #            Prob_p2_wins_given_value[value][i][j] = (float(count_given_p2_win[value][i][j]+1)/float(num_p2_wins+1)) * (float(num_p2_wins+1)/float(num_checked+1))\
    #                                                    / (float(count[value][i][j]+1)/float(num_checked+1)) #P(x|win) * P(win) / P(x)
    #return Prob_p1_wins_given_value, Prob_p2_wins_given_value
    return num_checked, num_p1_wins, num_p2_wins, count, count_given_p1_win, count_given_p2_win

def GenerateDataSet():
    global FileString, NodesExplored
    arrr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    B = board(arrr)
    initsize = 9
    for i in range(100):
        print("Generating "+ str(i) +"th board with " + str(initsize) + " initial placements")
        B.GenRandomBoard(initsize)
        print("running minMax(B)")
        minMax(B)
        NodesExplored = 0
        OutputFile.write(FileString)
    return

def GenDataAndStats():
    GenerateDataSet()
    GenerateAndSaveStats(InputParse())

def GenerateAndSaveStats(dataset):
    """

    :rtype: object
    """
    global StatsOutput
    StatsOutput = open("stats.txt", 'w')
    numchecked, p1wins, p2wins, count, count_given_p1win, count_given_p2win = genStats(dataset)
    StatsOutput.write(str(numchecked)+" "+str(p1wins)+" "+str(p2wins)+"\n*\n")
    for value in range(3):
        for row in range(4):
            StatsOutput.write((" ".join(list(map(str, count[value][row]))))+"\n")
        StatsOutput.write("$\n")
    StatsOutput.write("~\n")
    for value in range(3):
        for row in range(4):
            StatsOutput.write((" ".join(list(map(str, count_given_p1win[value][row]))))+"\n")
        StatsOutput.write("$\n")
    StatsOutput.write("~\n")
    for value in range(3):
        for row in range(4):
            StatsOutput.write((" ".join(list(map(str, count_given_p2win[value][row]))))+"\n")
        StatsOutput.write("$\n")

def ParseStats():
    global StatsRead
    statstr = StatsRead.read()
    statstr = statstr.split("\n*\n")
    statstr[0] = statstr[0].split(" ")
    numchecked = int(statstr[0][0])
    p1wins = int(statstr[0][1])
    p2wins = int(statstr[0][2])
    statstr[1] = statstr[1].split("~\n")
    for i in range(3):
        statstr[1][i] = statstr[1][i].split("\n$\n")[:-1]
        for j in range(3):
            statstr[1][i][j] = statstr[1][i][j].split("\n")
            for k in range(4):
                statstr[1][i][j][k] = statstr[1][i][j][k].split(" ")
                statstr[1][i][j][k] = list(map(int, statstr[1][i][j][k]))
    count = statstr[1][0]
    count_given_p1win = statstr[1][1]
    count_given_p2win = statstr[1][2]
    return numchecked, p1wins, p2wins, count, count_given_p1win, count_given_p2win

def main():
    #GenerateDataSet()
    #global mnexp, abexp
    #GenerateAndSaveStats(InputParse())
    #GenDataAndStats()
    numchecked, p1wins, p2wins, count, count_given_p1win, count_given_p2win = ParseStats()
    print("help me")

    #if len(b) == 4:
    #   for i in range(3):00
    #       tempstring = input()
    #       tempb = tempstring.split()
    #       b.extend(tempb[:])
    #for i in range(4):
    #   for j in range(4):
    #       arrr[i][j] = int( b[i*4 + j])
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

