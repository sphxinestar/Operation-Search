from pulp import *
import numpy as np
import math

f =  open('v3output.txt', 'w')

x = np.zeros((9, 9), dtype=type(pulp.LpVariable))
exp = np.zeros((9, 9), dtype=int)
time = np.zeros((9, 9), dtype=int)

exp = [[0,0,0,0,0,0,0,0,-10000],
        [0,107,-11,-10,-19,-5,-18,-9,-10000],
        [0,-11,107,-20,-8,-15,-6,-11,-10000],
        [0,-10,-20,180,-28,-6,-26,-19,-10000],
        [0,-19,-8,-28,152,-22,-4,-17,-10000],
        [0,-5,-15,-6,-22,129,-21,-13,-10000],
        [0,-18,-6,-26,-4,-21,129,-16,-10000],
        [0,-9,-11,-19,-17,-13,-16,161,-10000],
        [-10000,-10000,-10000,-10000,-10000,-10000,-10000,-10000,-10000]]

time = [[0,0,0,0,0,0,0,0,0],
        [0,11,11,10,19,5,18,9,0],
        [0,11,9,20,8,15,6,11,0],
        [0,10,20,16,28,6,26,19,0],
        [0,19,8,28,13,22,4,17,0],
        [0,5,15,6,22,13,21,13,0],
        [0,18,6,26,4,21,13,16,0],
        [0,9,11,19,17,13,16,6,0],
        [0,0,0,0,0,0,0,0,0]]

if __name__ == "__main__":
    #print("YA")
    model = pulp.LpProblem("valuemax", pulp.LpMaximize)

    for i in range(9) : 
        for j in range(9) :
            index = 'x' + str(i) + str(j)
            #print(index)
            x[i][j] = pulp.LpVariable(index, lowBound=0, cat='Integer')

    # objective func
    model += (lpSum(x[i][j] * exp[i][j] for i in range(9) for j in range(9)))
    
    # restrict
    model += (lpSum(x[i][j] * time[i][j] for i in range(9) for j in range(9))) <= 360

    model += x[0][0] == 1
    model += x[1][1] <= 3
    model += x[2][2] <= 3
    model += x[3][3] <= 3
    model += x[4][4] <= 3
    model += x[5][5] <= 2
    model += x[6][6] <= 3
    model += x[7][7] <= 3
    
    for i in range(9) :
        model += x[i][i] == lpSum(x[i][j] for j in range(9)) - x[i][i]
        model += x[i][i] == lpSum(x[j][i] for j in range(9)) - x[i][i]        

    model.solve()

    for v in model.variables():
        print(v.name, "=", v.varValue)

    print("obj=", value(model.objective))

    for i in range(9):
        for j in range(9):
            f.write(str(int(x[i][j].varValue)))
        f.write("\n")
    f.close()

