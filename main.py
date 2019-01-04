from redneuronal import *

layer1 = [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]] # 4 inputs
layer2 = [[1,2,3,4,5],[1,2,3,8,5]]
layer3 = [[1,2,3], [0,.1,.2]]
layers = [layer1, layer2, layer3]
red = RedN(layers)
input = [1,2,3,4]

print(red.outputs)
print(red.calc(input))
print(red.red)
print(red.outputs[-1])
