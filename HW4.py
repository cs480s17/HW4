
Data = []
import sys
import copy
Epochs = 100
TrainingPortion = 0.9

class Perceptron:
    def __init__(self, num_inputs, Eta):
        self.weights = [1]*(num_inputs+1) #+1 is for W0, the threshold weight
        self.eta = Eta

    def copy(self):
        p = Perceptron(len(self.weights)-1,  self.eta)
        for i in range(len(self.weights)):
            p.weights[i] = self.weights[i]
        return p

    def learn(self, inputs, correct_output):
        prediction = self.predict(inputs)
        if prediction * correct_output <= 0: #if prediction and the correct output have a different sign:
            for i in range(len(self.weights)):
                new = self.weights[i] - (self.eta * (prediction - correct_output) * inputs[i])
                self.weights[i] = new
        else:
            return

    def test(self, inputs, correct_output):
        prediction = self.predict(inputs)
        return not(prediction * correct_output <= 0)  # if prediction and the correct output have a different sign, return false

    def predict(self, inputs):
        total = 0
        for i in range(len(self.weights)):
            total += self.weights[i] * inputs[i]
        return total

    def listWeights(self):
        for i in range(len(self.weights)):
            sys.stdout.write("w" + str(i) + " = " + str(self.weights[i]) + " ")
        sys.stdout.flush()
        return


class Numimg:
    def __init__(self, data = ""):
        self.label = data[0]
        temp = data[1:].split("\n") #like firewood
        self.Array = []
        for i in temp:
            self.Array.append(i.split(" ")[1:]) #because
        self.rows = len(self.Array)
        self.cols = len(self.Array[0])
        num_ones = self.num_ones()
        self.density = num_ones / (self.rows * self.cols)
        self.h_symmetry = self.__h_symmetry__() / num_ones
        self.v_symmetry = self.__v_symmetry__() / num_ones
        self.min_h_intercepts, self.max_h_intercepts = self.__h_intercepts__()
        self.min_v_intercepts, self.max_v_intercepts = self.__v_intercepts__()

    def print(self):
        print("Label:", self.label)
        print("density:", self.density)
        print("h_symmetry:", self.h_symmetry)
        print("v_symmetry:", self.v_symmetry)
        print("h intercepts(min,max):", self.min_h_intercepts, self.max_h_intercepts)
        print("v intercepts(min,max):", self.min_v_intercepts, self.max_v_intercepts)
        for i in self.Array:
            print(i)

    def num_ones(self):
        counter = 0
        for i in self.Array:
            for j in i:
                if(j == '1'):
                    counter += 1

        return counter

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

    def __h_intercepts__(self):
        min = sys.maxsize
        max = 0
        for i in range(self.rows):
            count = 0
            prev = '0'
            for j in range(self.cols): #following will count the number of 1 to 0 borders in current row
                curr = self.Array[i][j]
                if prev != curr:
                    if prev == '1':
                        count += 1
                    prev = curr
            if count < min:
                min = count
            if count > max:
                max = count
        return min, max

    def __v_intercepts__(self):
        min = sys.maxsize
        max = 0
        for i in range(self.cols):
            count = 0
            prev = '0'
            for j in range(self.rows): #following will count the number of 1 to 0 borders in current col
                curr = self.Array[j][i]
                if prev != curr:
                    if prev == '1':
                        count += 1
                    prev = curr
            if count < min:
                min = count
            if count > max:
                max = count
        return min, max

    def inputs(self):
        return [-1,
                self.density,
                self.h_symmetry,
                self.v_symmetry,
                self.min_h_intercepts,
                self.max_h_intercepts,
                self.min_v_intercepts,
                self.max_v_intercepts]





def parseData():
    global Data
    global cols, rows

    print("Opening Test Data File")
    f = open('testdata', 'r')
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
    global Epochs
    global TrainingPortion
    global Data
    ErrorArray = []
    PArray = []
    parseData()
    TrainingSize = int(len(Data) * TrainingPortion)
    BestP = None
    BestError = sys.maxsize
    CurrP = Perceptron(7, 0.05)
    CurrError = 0
    for i in range(TrainingSize, len(Data)):
        correct_out = (-1 if Data[i].label == '5' else 1)
        if not (CurrP.test(Data[i].inputs(), correct_out)):
            CurrError += 1
    ErrorArray.append(CurrError)
    PArray.append(CurrP.copy())
    if CurrError < BestError:
        BestError = CurrError
        BestP = CurrP.copy()
    for e in range(Epochs):
        CurrError = 0
        for i in range(TrainingSize):
            correct_out = (-1 if Data[i].label == '5' else 1)
            CurrP.learn(Data[i].inputs(), correct_out)

        for i in range(TrainingSize, len(Data)):
            correct_out = (-1 if Data[i].label == '5' else 1)
            if not(CurrP.test(Data[i].inputs(), correct_out)):
                CurrError += 1
        ErrorArray.append(CurrError)
        PArray.append(CurrP.copy())
        if CurrError < BestError:
            BestError = CurrError
            BestP = CurrP.copy()
    print("The best perceptron of", Epochs, "epochs has the following weights, where w0 is the threshold")
    BestP.listWeights()
    print()
    print("This results in", BestError, "Errors out of", len(Data) - TrainingSize, "Test Cases")
    return 0


if __name__ == "__main__":
    main()