
Data = []

class Numimg:
    def __init__(self, data = ""):
        self.label = data[0]
        temp = data[1:].split("\n") #like firewood
        self.Array = []
        for i in temp:
            self.Array.append(i.split(" ")[1:]) #because
        self.density = self.density()
        self.h_symetry = self.__h_symetry__()
        self.v_symetry = self.__v_symetry__()
        self.min_h_intercepts, self.max_h_intercepts =__h_intercepts__()
        self.min_v_intercepts, self.max_v_intercepts =__v_intercepts__()
    def print(self):
        print(self.label, ":")
        for i in self.Array:
            print(i)




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