from pulp import *

f =  open('output.txt', 'w')

exp = [[0]*8 for i in range(360)]
for i in range(360) :  
    exp[i][0] = 107/11
    exp[i][1] = 107/9
    exp[i][2] = 180/16
    exp[i][3] = 152/12
    exp[i][4] = 129/13
    exp[i][5] = 129/13
    exp[i][6] = 161/6
    exp[i][7] = 0

if __name__ == "__main__":
    #print("YA")
    model = pulp.LpProblem("valuemax", pulp.LpMaximize)
    x = [[0]*8 for i in range(360)]
    for i in range(360) : 
        for j in range(8) :
            index = 'x' + str(i) + str(j)
            #print(index)
            x[i][j] = pulp.LpVariable(index, lowBound=0, cat='Binary')
    '''
    model += 1*x111 + 2*x112 + 3*x113 + 4*x114 
    
    model += x111 + 2*x112 + 3*x113 <= 4
    model += x111 + x112 >= 1
    
    model.solve()
    for v in model.variables():
        print(v.name, "=", v.varValue)
    
    print('obj=', value(model.objective))
    '''
    
    model += lpSum(x[i][j] * exp[i][j] for i in range(360) for j in range(8))

    for i in range(25) :
        model += (x[i][4] == 1)

    for i in range(0,360) : # one movement per sec
        model += (x[i][0] + x[i][1] + x[i][2] + x[i][3] + x[i][4] + x[i][5] + x[i][6] + x[i][7] <= 1)
        model += (x[i][0] + x[i][1] + x[i][2] + x[i][3] + x[i][4] + x[i][5] + x[i][6] + x[i][7] > 0)

    for i in range(25,181) : # 6 birds reborn
        model += (lpSum(x[i+j][0] for j in range(120)) <= 22)
        model += (lpSum(x[i+j][0] for j in range(120)) > 21)

    for i in range(25,181) : # 3 wolves reborn
        model += (lpSum(x[i+j][1] for j in range(120)) <= 19)
        model += (lpSum(x[i+j][1] for j in range(120)) > 18)

    for i in range(25,181) : # 2 rocks reborn
        model += (lpSum(x[i+j][2] for j in range(120)) <= 32)
        model += (lpSum(x[i+j][2] for j in range(120)) > 31)
    
    for i in range(25,181) : # 1 froggy reborn
        model += (lpSum(x[i+j][3] for j in range(120)) <= 25)
        model += (lpSum(x[i+j][3] for j in range(120)) > 24)
    
    for i in range(25,61) : # 1 redbuff reborn
        model += (lpSum(x[i+j][4] for j in range(300)) <= 25)
        model += (lpSum(x[i+j][4] for j in range(300)) > 24)

    for i in range(25,61) : # 1 bluebuff reborn
        model += (lpSum(x[i+j][5] for j in range(300)) <= 24)
        model += (lpSum(x[i+j][5] for j in range(300)) > 23)

    for i in range(25,151) : # 1 crab reborn
        model += (lpSum(x[i+j][6] for j in range(150)) <= 19)
        model += (lpSum(x[i+j][6] for j in range(150)) > 18)

    model.solve()
    for v in model.variables():
        print(v.name, "=", v.varValue)

    print("obj=", value(model.objective))

    for i in range(8):
        for j in range(360):
            f.write(str(int(x[j][i].varValue)))
        f.write("\n")

    f.close()
