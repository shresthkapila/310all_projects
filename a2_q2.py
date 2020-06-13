# a2_q2.py

# from a2_q1 import *

def check_teams(graph, csp_sol):
    total_var = len(csp_sol)

    for i in range(total_var):
        for j in range(1,total_var):
            if csp_sol[i] == csp_sol[j]:
                if j in graph[i]:
                    return False

    return True

# g = {0:[1,2], 1:[0], 2: [0], 3:[]}

# x = {0:1, 1:0, 2:0, 3:1}

# y = check_teams(g,x)
# print(y)
