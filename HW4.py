
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
        self.h_symetry = self.__h_symmetry__()
        self.v_symetry = self.__v_symmetry__()
        self.min_h_intercepts, self.max_h_intercepts = self.__h_intercepts__()
        self.min_v_intercepts, self.max_v_intercepts = self.__v_intercepts__()

    def print(self):
        print(self.label, ":")
        for i in self.Array:
            print(i)
    def density(self):
        counter = 0
        total = 0
        for i in self.Array:
            for j in i:
                if(j == '1'):
                    counter += 1
                total += 1

        return counter/(self.rows * self.cols)

    def __h_symmetry__(self):
        temp = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if(self.Array[i][j] != self.Array[i][self.cols-(i+1)]):
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




if __name__ == "__main__":
    main()