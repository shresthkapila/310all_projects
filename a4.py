# a4.py
# Author - Shresth Kapila
# CMPT310 Assignment 4  
# ...

#-----------------------------------------------------------------------------------------------------------
# Global variables
validCommands = ["load","tell","infer_all"]
all_files = []
global currentKB
KB = []
infered = []


#-----------------------------------------------------------------------------------------------------------
# Helping functions

# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"


#-----------------------------------------------------------------------------------------------------------
# load command
def load(fileName):
    try:
        f = open(fileName, "r")
        line = f.readlines()

        while '\n' in line:
            line.remove('\n')

        for i in range(len(line)):
            oline = line[i]
            newLine = ""
            for j in range(len(oline)):
                if oline[j] != '\n':
                    newLine += oline[j]

            line[i] = newLine    

        if loadCheck(line):
            for l in line:
                print('\t' + l)
            print('\n', f'{len(line)} new rules(s) added')
        else:
            print(f'Error: {fileName} is not a valid knowledge base load')
    except FileNotFoundError:
        print(f'Error: {fileName} is not a valid knowledge base')


def loadCheck(line):
    for l in line:
        variables = l.split(' <-- ')
        if (len(variables) != 2):
            return False
        head = variables[0]
        atoms = variables[1].split(' & ')
        for a in atoms:
            if is_atom(a) is False:
                return False
        data = [head, atoms] 
        all_files.append(data) 
    return True


#-----------------------------------------------------------------------------------------------------------
# tell command
def tell(atoms):
    tempKB = []
    repKB = []
    atoms.pop(0)
    if tellCheck(atoms) == False:
        return
    # print(atoms)
    # print(all_files)
    for af in all_files:
        for a in atoms: 
            if a in af[0] or a in af[1]:
                if a in KB:
                    if a not in tempKB and a not in repKB:
                        print(f'\tatom "{a}" already known to be true')
                        repKB.append(a)
                else:
                    KB.append(a)
                    tempKB.append(a)
                    print(f'\t"{a}" added to KB')
            else:
                if a in KB:
                    if a not in tempKB and a not in repKB:
                        print(f'\tatom "{a}" already known to be true')
                        repKB.append(a)
                else: 
                    KB.append(a)
                    tempKB.append(a)
                    print(f'\t"{a}" added to KB')
            # print(KB)
            # print(tempKB)

def tellCheck(atoms):
    for a in atoms:
        if is_atom(a) is False:
            print(f'Error: "{a}" is not a valid atom')
            return False
    return True
    


#-----------------------------------------------------------------------------------------------------------
# infer_all command
def infer_all():
    infered = []
    for al in all_files:
        tempInfer = [] 
        for atoms in al[1]:
            if al[0] not in KB and al[0] not in infered:
                if atoms in KB:
                    tempInfer.append(atoms)
        if tempInfer == al[1]:
            infered.append(al[0])
    return infered


#-----------------------------------------------------------------------------------------------------------
# main program (interactive interpreter)
def run_interpreter():
    while (True):
        Input = []
        userInput = input("kb> ")
        command = userInput.split()
        for w in command:
            Input.append(w)
        
        if (len(Input) == 0):
            continue

        if (Input[0] in validCommands):
            if (Input[0] == "load"):
                if (len(Input) == 1):
                    print(f'Error: No file to load')
                    print("Try to enter 'load a4_q2_kb.txt'")
                else: #(Input[1] == "a4_q2_kb.txt"):
                    currentKB = Input[1]
                    all_files.clear()
                    load(Input[1])
                    # print(all_files)
            elif (Input[0] == "tell"):
                if (len(Input) == 1):
                    print(f'Error: tell needs atleast one atom')
                elif (len(Input) > 1):
                    tell(Input)
                else:
                    print(f'Error: {Input[1]} is not a valid knowledge base')
            elif (Input[0] == "infer_all"):
                if (len(Input) > 1):
                    print(f'Error: unknown command {userInput}')
                else:
                    itemp = infer_all()
                    for atoms in itemp:
                        KB.append(atoms)
                    while True:
                        temp = infer_all() 
                        if len(temp) == 0:
                            break
                        else:
                            for t in temp:
                                itemp.append(t)
                                KB.append(t)
                    infered = itemp
                    print(f'\tNewly inferred atoms:')
                    if len(infered) == 0:
                        print("\t   <none>")
                    else:
                        print("\t", end="   ")
                        for i in range(len(infered)):
                            if i == len(infered) - 1:
                                print(f'{infered[i]}')
                            else:
                                print(f'{infered[i]}', end=", ")

                    print(f'\tAtoms already known to be true:')
                    if len(KB) == 0:
                        print("\t   <none>")
                    else:
                        for j in range(len(KB)):
                            if KB[j] not in infered:
                                if j == 0:
                                    print(f'\t   {KB[j]}', end="")
                                else:
                                    print(f', {KB[j]}', end="")
                        print("")

        else:
            print(f'Error: unknown command {userInput}')
            

run_interpreter()

