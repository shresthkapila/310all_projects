# a2_q4.py

from csp import *
from a2_q1 import *
from a2_q2 import * 
import time 
import random

#------------------------------------------------------------------------------------------------------------
# Changes in the CSP class (added unassigns variable)
class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases (for example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(n^4) for the
    explicit representation). In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints, unassigns):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        # super().__init__(())
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.initial = ()
        self.nassigns = 0
        self.unassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]
            self.unassigns = self.unassigns + 1

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""

        # Subclasses may implement this more efficiently
        def conflict(var2):
            return var2 in assignment and not self.constraints(var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP:', self, 'with assignment:', assignment)

    # These methods are for the tree and graph-search interface:

    def actions(self, state):
        """Return a list of applicable actions: non conflicting
        assignments to an unassigned variable."""
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        """Perform an action and return the new state."""
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

# END OF CLASS
#----------------------------------------------------------------------------------------------------------------------

# Modified version
def MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""
    if isinstance(neighbors, str):
        neighbors = parse_neighbors(neighbors)
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint, 0)

# Helper function for counting the teams 
def countTeams(solution):
    teams = []
    for x in range(len(solution)):
        if solution[x] not in teams:
            teams.append(solution[x])
    return len(teams)

# Additional feature - returns the number of people in team with largest number of people
def maxPeople(solution):
    teams = {}
    maxPeople = 0
    for i in range(len(solution)):
        if solution[i] not in teams:
            teams[solution[i]] = 0
    for i in range(len(teams)):
        for j in range(len(solution)):
            if i == solution[j]:
                teams[i] += 1
    for i in range(len(teams)):
        if teams[i] > maxPeople:
            maxPeople = teams[i]
    return maxPeople	


#---------------------------------------------------------------------------------------------------------------------------

# running.. question 4 
# instead of running in one loop, running all the graphs separately makes the process faster (LOOP UNROLLING) from CMPT295
def run_q4():
        
    for i in range(5):
        print("Set of graphs:  ", i+1)

        graphs = [rand_graph(0.1,105), rand_graph(0.2,105), rand_graph(0.3,105), 
                    rand_graph(0.4,105), rand_graph(0.5,105), rand_graph(0.6,105)]
        

        print("Graph: ", 1)
        start_time = time.time()
        for j in range(105):
            newdomain={w:[] for w in range(j+1)}
            for x in range(len(newdomain)):
                for y in range(len(newdomain)):    
                    newdomain[y].append(x)
            problem = MapColoringCSP(newdomain,graphs[0])
            AC3(problem)
            solution = min_conflicts(problem)
            if solution is None:
                continue
            else:
                break

        elapsed_time = time.time() - start_time
        
        print(f'IceBreaker problem for n=105; p=0.1', file = open("a2_q4terminal.txt","a"))
        print(f'==> checkTeams true(if solution is correct): {check_teams(graphs[0],solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of teams: {countTeams(solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> total time (in seconds): {elapsed_time}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of assigned variable: {problem.nassigns}', file = open("a2_q4terminal.txt","a") )
        print(f'==> no of unassigned variable: {problem.unassigns}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of friends in largest team: {maxPeople(solution)} ', file = open("a2_q4terminal.txt","a"))
        print(f'==> solution (teams be like): {solution}', file = open("a2_q4terminal.txt","a"))
        print('\n', file = open("a2_q4terminal.txt","a"))


        #----------------------------------------------------------------------------------------------------------------------------


        print("Graph: ", 2)
        start_time = time.time()
        for j in range(105):
            newdomain={w:[] for w in range(j+1)}
            for x in range(len(newdomain)):
                for y in range(len(newdomain)):    
                    newdomain[y].append(x)
            problem = MapColoringCSP(newdomain,graphs[1])
            AC3(problem)
            solution = min_conflicts(problem)
            if solution is None:
                continue
            else:
                break

        elapsed_time = time.time() - start_time
        
        print(f'IceBreaker problem for n=105; p=0.2', file = open("a2_q4terminal.txt","a"))
        print(f'==> checkTeams true(if solution is correct): {check_teams(graphs[1],solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of teams: {countTeams(solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> total time (in seconds): {elapsed_time}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of assigned variable: {problem.nassigns}', file = open("a2_q4terminal.txt","a") )
        print(f'==> no of unassigned variable: {problem.unassigns}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of friends in largest team: {maxPeople(solution)} ', file = open("a2_q4terminal.txt","a"))
        print(f'==> solution (teams be like): {solution}', file = open("a2_q4terminal.txt","a"))
        print('\n', file = open("a2_q4terminal.txt","a"))


        #----------------------------------------------------------------------------------------------------------------------------


        print("Graph: ", 3)
        start_time = time.time()
        for j in range(105):
            newdomain={w:[] for w in range(j+1)}
            for x in range(len(newdomain)):
                for y in range(len(newdomain)):    
                    newdomain[y].append(x)
            problem = MapColoringCSP(newdomain,graphs[2])
            AC3(problem)
            solution = min_conflicts(problem)
            if solution is None:
                continue
            else:
                break

        elapsed_time = time.time() - start_time
        
        print(f'IceBreaker problem for n=105; p=0.3', file = open("a2_q4terminal.txt","a"))
        print(f'==> checkTeams true(if solution is correct): {check_teams(graphs[2],solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of teams: {countTeams(solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> total time (in seconds): {elapsed_time}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of assigned variable: {problem.nassigns}', file = open("a2_q4terminal.txt","a") )
        print(f'==> no of unassigned variable: {problem.unassigns}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of friends in largest team: {maxPeople(solution)} ', file = open("a2_q4terminal.txt","a"))
        print(f'==> solution (teams be like): {solution}', file = open("a2_q4terminal.txt","a"))
        print('\n', file = open("a2_q4terminal.txt","a"))


        #----------------------------------------------------------------------------------------------------------------------------


        print("Graph: ", 4)
        start_time = time.time()
        for j in range(105):
            newdomain={w:[] for w in range(j+1)}
            for x in range(len(newdomain)):
                for y in range(len(newdomain)):    
                    newdomain[y].append(x)
            problem = MapColoringCSP(newdomain,graphs[3])
            AC3(problem)
            solution = min_conflicts(problem)
            if solution is None:
                continue
            else:
                break

        elapsed_time = time.time() - start_time
        
        print(f'IceBreaker problem for n=105; p=0.4', file = open("a2_q4terminal.txt","a"))
        print(f'==> checkTeams true(if solution is correct): {check_teams(graphs[3],solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of teams: {countTeams(solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> total time (in seconds): {elapsed_time}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of assigned variable: {problem.nassigns}', file = open("a2_q4terminal.txt","a") )
        print(f'==> no of unassigned variable: {problem.unassigns}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of friends in largest team: {maxPeople(solution)} ', file = open("a2_q4terminal.txt","a"))
        print(f'==> solution (teams be like): {solution}', file = open("a2_q4terminal.txt","a"))
        print('\n', file = open("a2_q4terminal.txt","a"))


        #----------------------------------------------------------------------------------------------------------------------------



        print("Graph: ", 5)
        start_time = time.time()
        for j in range(105):
            newdomain={w:[] for w in range(j+1)}
            for x in range(len(newdomain)):
                for y in range(len(newdomain)):    
                    newdomain[y].append(x)
            problem = MapColoringCSP(newdomain,graphs[4])
            AC3(problem)
            solution = min_conflicts(problem)
            if solution is None:
                continue
            else:
                break

        elapsed_time = time.time() - start_time
        
        print(f'IceBreaker problem for n=105; p=0.5', file = open("a2_q4terminal.txt","a"))
        print(f'==> checkTeams true(if solution is correct): {check_teams(graphs[4],solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of teams: {countTeams(solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> total time (in seconds): {elapsed_time}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of assigned variable: {problem.nassigns}', file = open("a2_q4terminal.txt","a") )
        print(f'==> no of unassigned variable: {problem.unassigns}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of friends in largest team: {maxPeople(solution)} ', file = open("a2_q4terminal.txt","a"))
        print(f'==> solution (teams be like): {solution}', file = open("a2_q4terminal.txt","a"))
        print('\n', file = open("a2_q4terminal.txt","a"))


        #----------------------------------------------------------------------------------------------------------------------------


        print("Graph: ", 6)
        start_time = time.time()
        for j in range(105):
            newdomain={w:[] for w in range(j+1)}
            print(newdomain)
            for x in range(len(newdomain)):
                for y in range(len(newdomain)):    
                    newdomain[y].append(x)
            problem = MapColoringCSP(newdomain,graphs[5])
            AC3(problem)
            solution = min_conflicts(problem)
            if solution is None:
                continue
            else:
                break

        elapsed_time = time.time() - start_time
        
        print(f'IceBreaker problem for n=105; p=0.6', file = open("a2_q4terminal.txt","a"))
        print(f'==> checkTeams true(if solution is correct): {check_teams(graphs[5],solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of teams: {countTeams(solution)}', file = open("a2_q4terminal.txt","a"))
        print(f'==> total time (in seconds): {elapsed_time}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of assigned variable: {problem.nassigns}', file = open("a2_q4terminal.txt","a") )
        print(f'==> no of unassigned variable: {problem.unassigns}', file = open("a2_q4terminal.txt","a"))
        print(f'==> no of friends in largest team: {maxPeople(solution)} ', file = open("a2_q4terminal.txt","a"))
        print(f'==> solution (teams be like): {solution}', file = open("a2_q4terminal.txt","a"))
        print('//////////////////////////////////\n', file = open("a2_q4terminal.txt","a"))

# comment to not run
run_q4()



        

