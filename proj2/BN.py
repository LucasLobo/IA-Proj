#Grupo 87 | David Sousa Batista 86405 | Lucas Lobo Fell 86464
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""
class Node():
    def __init__(self, prob, parents = []):
        self.prob = prob
        self.parents = parents

    def computeProb(self, evid):
        prob = self.prob
        for parent in self.parents:
            prob = prob[evid[parent]]

        if not self.parents:
            prob = prob[0]
        return [1-prob,prob]

class BN():
    def __init__(self, gra, prob):
        self.gra = gra
        self.prob = prob

    def computePostProb(self, evid):
        knowns = {}
        for e_index in range(len(evid)):
            if (evid[e_index] == -1):
                goal = e_index
            elif (evid[e_index] != []):
                knowns[e_index] = evid[e_index]

        def enumerate_all(current, knowns):
            if current >= len(self.prob):
                return 1.0

            new_current = current + 1
            if current in knowns:
                return self.prob[current].computeProb(knowns)[knowns[current]] * enumerate_all(new_current, knowns)
            else:
                new_knowns = knowns.copy()
                sum = 0
                for yi in [0,1]:
                    new_knowns[current] = yi
                    sum += self.prob[current].computeProb(knowns)[yi] * enumerate_all(new_current, new_knowns)
                return sum

        Q = [None, None]

        for xi in [0,1]:
            knowns[goal] = xi
            Q[xi] = enumerate_all(0, knowns)

        return Q[1]/(Q[0] + Q[1])


    def computeJointProb(self, evid):
        prob = 1
        for node_index in range(len(self.prob)):
            prob *= self.prob[node_index].computeProb(evid)[evid[node_index]]
        return prob
