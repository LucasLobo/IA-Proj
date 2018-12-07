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
        pass

    def computePostProb(self, evid):
        pass

        return 0


    def computeJointProb(self, evid):
        pass

        return 0
