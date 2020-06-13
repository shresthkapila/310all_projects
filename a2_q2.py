# a2_q2.py

def check_teams(graph, csp_sol):
    total_var = len(csp_sol)

    for i in range(total_var):
        for j in range(1,total_var):
            if csp_sol[i] == csp_sol[j]:
                if j in graph[i]:
                    return False

    return True

