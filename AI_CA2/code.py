# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 23:32:56 2020

@author: Mahta
"""

import numpy as np
import pandas as pd
import random
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

AND = 0
OR = 1
XOR = 2
NAND = 3
NOR = 4
XNOR =5

truth_table =pd.read_csv('truth_table.csv')
num_rows = len(truth_table)
columns = len(truth_table.columns)
num_inputs = columns-1    
OUT = truth_table['Output'].to_numpy()
Inputs ={}
for i in range(num_inputs):
    Inputs[i] = truth_table.iloc[:,i].to_numpy()


def gate_result(chromosome,input1,size):
    if size ==1:
        return input1
    gate = chromosome[num_inputs-size]
    input2 = Inputs[num_inputs-size+1]
    if gate==AND :
        return gate_result(chromosome,np.bitwise_and(input1,input2),size-1)
    elif gate ==OR:
        return gate_result(chromosome,np.bitwise_or(input1,input2),size-1)
    elif gate ==XOR:
        return gate_result(chromosome,np.bitwise_xor(input1,input2),size-1)
    elif gate == NAND:
        return gate_result(chromosome,np.bitwise_not(np.bitwise_and(input1, input2)),size-1)
    elif gate == NOR:
        return gate_result(chromosome,np.bitwise_not(np.bitwise_or(input1, input2)),size-1)
    elif gate == XNOR:
        return gate_result(chromosome,np.bitwise_not(np.bitwise_xor(input1, input2)),size-1)
    else:
        print(gate)
        raise ValueError('NOT DEFINED!')
        
        
def population_initialization(size):
    population =[]
    for i in range(size):
        chromosome = np.random.randint(low=0, high=6, size=num_inputs-1)
        population.append(chromosome)
    return population

def fitness(population):
    scores = []
    for chromosome in population:
        G9 = gate_result(chromosome,Inputs[0],num_inputs)        
        f = sum(np.bitwise_not(np.bitwise_xor(G9, OUT)))
        scores.append(f)
    scores,population = np.array(scores),np.array(population)
    inds = np.argsort(scores)
    return list(scores[inds][::-1]), list(population[inds,:][::-1])
    
def selection(population,n_parents):
    next_generation = []
    for i in range(n_parents):
        next_generation.append(population[i])
    return next_generation

def crossover(population):
    n=(num_inputs -1)//2
    next_generation = population
    for i in range(len(next_generation)):
        child = population[i]
        child[n-1:n+1] = population[(i+1)%len(population)][n-1:n+1]
        next_generation.append(child)
    return next_generation

def mutation(pop_after_cross,mutation_rate):
    population_nextgen = []
    for i in range(0,len(pop_after_cross)):
        chromosome = pop_after_cross[i]
        for j in range(len(chromosome)):
            if random.random() < mutation_rate:
                chromosome[j]= random.randint(0,5)
        population_nextgen.append(chromosome)
    return population_nextgen

def generations(size,n_parents,mutation_rate):
    best_chromo= []
    best_score= []
    population_nextgen=population_initialization(size)
    while num_rows not in best_score:
        scores, pop_after_fit = fitness(population_nextgen)
        print(scores[:2])
        pop_after_sel = selection(pop_after_fit,n_parents)
        pop_after_cross = crossover(pop_after_sel)
        population_nextgen = mutation(pop_after_cross,mutation_rate)
        best_chromo.append(pop_after_fit[0])
        best_score.append(scores[0])
    print(best_chromo.pop())
    return best_chromo,best_score


chromo,score=generations(size=200,n_parents=100,mutation_rate=0.10)