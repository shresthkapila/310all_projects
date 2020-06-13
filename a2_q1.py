# a2_q1.py

import random

def rand_graph(p,n):
    new_dict = dict()

    for i in range(n):
        new_dict[i] =  []
    
    for j in range(n):
        for k in range(j+1, n):
            f_prob = random.random()
            if p > f_prob:
                new_dict[j].append(k)
                new_dict[k].append(j)
    
    return new_dict
