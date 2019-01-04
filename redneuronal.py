import math

class RedN:
    def __init__(self, layers:list):
        self.red = layers
        self.outputs = []
        for layer in layers:
            aux = []
            for neuron in layer:
                aux.append(0)
            self.outputs.append(aux)
        print(self.outputs)

    def getbias(self, neuron:list):
        return neuron[-1]

    def getneuron(self, layer, neuron):
        return self.red[layer][neuron]

    def getw(self, neuron:list):
        return neuron[0:len(neuron)-2]

    def getinput(self, currentlayer:int):
        return self.outputs[currentlayer-1]

    def calc(self, input:list):
        for i, layer in enumerate(self.red):
            if i == 0:
                data = input
            else:
                data = self.getinput(i)
            for j, neuron in enumerate(layer):
                val = self.calcneuron(neuron, data)
                self.outputs[i][j] = val
        return self.outputs[-1]

    def calcneuron(self, neuron:list, data:list):
        r = 0
        r+= self.getbias(neuron)
        for i, xi in enumerate(data):
            v = self.normalize(xi)
            r+=v * neuron[i]
        return self.f(r)

    def f(self, z):
        return 1 / (1 + math.exp(-z))

    def normalize(self, x):
        return (x+10)/20






