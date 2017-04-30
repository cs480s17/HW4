
Data = []

class Numimg:
    def __init__(self, data = ""):
        self.label = data[0]
        temp = data[1:].split("\n") #like firewood
        self.Array = []
        for i in temp:
            self.Array.append(i.split(" ")[1:]) #because
        self.rows = len(self.Array)
        self.cols = len(self.Array[0])
        self.density = self.density()
        self.h_symmetry = self.__h_symmetry__()
        self.v_symmetry = self.__v_symmetry__()
        #self.min_h_intercepts, self.max_h_intercepts = self.__h_intercepts__()
        #self.min_v_intercepts, self.max_v_intercepts = self.__v_intercepts__()

    def print(self):
        print("Label: ", self.label)
        print("density: ", self.density)
        print("h_symmetry: ", self.h_symmetry)
        print("v_symmetry: ", self.v_symmetry)
        for i in self.Array:
            print(i)

    def density(self):
        counter = 0
        for i in self.Array:
            for j in i:
                if(j == '1'):
                    counter += 1

        return counter/(self.rows * self.cols)

    def __h_symmetry__(self):
        temp = 0
        for i in range(self.rows//2):
            for j in range(self.cols//2):
                if(self.Array[i][j] != self.Array[i][self.cols-(j+1)]):
                    temp += 1
        return temp

    def __v_symmetry__(self):
        temp = 0
        for i in range(self.rows//2):
            for j in range(self.cols//2):
                if(self.Array[i][j] != self.Array[self.rows-(i+1)][j]):
                    temp += 1
        return temp



def parseData():
    global Data
    global cols, rows

    print("Opening Test Data File")
    f = open('Smalltest.txt', 'r')
    print("Reading File to String")
    tempdata = f.read()
    print("Splitting into Samples")
    dataarray = tempdata.split("\n\n\n") #yep
    dataarray.pop()
    for i in dataarray:
        Data.append(Numimg(i)) #you know it

def printData():
    global Data
    for i in Data:
        i.print()

def main():
    parseData()
    printData()
    return 0


if __name__ == "__main__":
    main()