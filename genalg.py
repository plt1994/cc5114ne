import redneuronal

import random
import time
import statistics


class RedNeuronalGA:
    def __init__(self, size, config:list, inputsize, mut_rate = 0.01, lastbest_rate = 0.5, tour_size = 10):
        '''

        :param size:
        :param n_genes:
        :param config: lista que indica [numero de layers, [numero de neuronas por layer]]
        :param mut_rate:
        :param lastbest_rate:
        :param tour_size:
        '''
        self.totalfitness = []
        self.inputsize = inputsize
        self.lastbest_rate = lastbest_rate
        self.pop_size = size
        self.mutation_rate = mut_rate
        self.tournament_size = tour_size
        self.current_generation = [] #lista de redes
        self.current_fitness = [] #valores de fitness encontrados despues de jugar
        self.final_ind = None
        self.config = config

    def set_tournamentsize(self, size):
        self.tournament_size = size

    def set_mutationrate(self, rate):
        self.mutation_rate = rate

    def set_survivalrate(self, rate):
        self.lastbest_rate = rate

    def initialize(self):
        for i in range(self.pop_size):
            red = []
            n_layers = self.config[0]
            for j in range(n_layers): #numero de layers
                layer = []
                n_neuronasj = self.config[1][j]
                for k in range(n_neuronasj):
                    neuron = []
                    if j == 0:
                        for p in range(self.inputsize):
                            neuron.append(random.random()*2)
                    else:
                        for p in range(self.config[1][j-1]):
                            neuron.append(random.random()*2)
                    neuron.append(random.randint(-2,2))
                    layer.append(neuron)
                red.append(layer)
            self.current_generation.append(redneuronal.RedN(red))

    def tournament_selection(self, population: list, k):
        ''' Randomly select the best individual after k iterations'''
        N = len(population)
        best = None
        for i in range(k):
            ind = population[random.randint(0, N - 1)]
            if best == None or self.fitness(ind) > self.fitness(best):
                best = ind
        return best


    def reproduce(self, red1:redneuronal.RedN, red2:redneuronal.RedN):
        nlayers = len(red1.red)
        new = []
        for i in range(nlayers):
            layer1 = red1.red[i]
            layer2 = red2.red[i]
            l = len(layer1)
            r = random.randint(1, l - 1)
            rep = layer1[0:r] + layer2[r:l]
            baby = []
            for i in range(l):
                if random.random() < self.mutation_rate:
                    baby.append(self.mutneuron(rep[i]))
                else:
                    baby.append(rep[i])
            new.append(baby)
        return redneuronal.RedN(new)


    def find(self):
        # best individuals of last generation
        best = []
        size = self.pop_size
        # selecciono a los posibles mejores
        while (len(best) < size*self.lastbest_rate):
            sel = self.tournament_selection(self.current_generation, self.tournament_size)
            if sel not in best:
                best.append(sel)
                self.current_generation.remove(sel)
        # crear nueva generacion a partir de los mejores anteriores
        gen = []
        while (len(gen) < size):
            ind1, ind2 = random.sample(best, 2)
            baby = self.reproduce(ind1, ind2)
            gen.append(baby)
        self.current_generation = gen
        self.savefitness()
        self.current_fitness = []


    def fitness(self, ind):
        for i in range(self.pop_size):
            if ind is self.current_generation[i]:
                return self.current_fitness[i]

    def savefitness(self):
        self.totalfitness.append(statistics.mean(self.current_fitness))

    def mutneuron(self, neuron:list):
        new = []
        for i in neuron:
            new.append(random.random()*2)
        return new


