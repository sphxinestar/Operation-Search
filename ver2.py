from pulp import *
import numpy as np
import math

f =  open('v2output.txt', 'w')
f2 = open('newArray.txt', 'w')

exp = np.zeros((360, 8, 8), dtype=float)
exp.fill(-10000)

for i in range(360) :  
    exp[i][0][0] = 107.0/11.0
    exp[i][0][1] = -11.0
    exp[i][0][2] = -10.0
    exp[i][0][3] = -19.0
    exp[i][0][4] = -5.0
    exp[i][0][5] = -18.0
    exp[i][0][6] = -9.0
    exp[i][1][1] = 107.0/9.0
    exp[i][1][0] = -11.0
    exp[i][1][2] = -20.0
    exp[i][1][3] = -8.0
    exp[i][1][4] = -15.0
    exp[i][1][5] = -6.0
    exp[i][1][6] = -11.0
    exp[i][2][2] = 180.0/16.0
    exp[i][2][0] = -10.0
    exp[i][2][1] = -20.0
    exp[i][2][3] = -28.0
    exp[i][2][4] = -6.0
    exp[i][2][5] = -26.0
    exp[i][2][6] = -19.0
    exp[i][3][3] = 152.0/13.0
    exp[i][3][0] = -19.0
    exp[i][3][1] = -8.0
    exp[i][3][2] = -28.0
    exp[i][3][4] = -22.0
    exp[i][3][5] = -4.0
    exp[i][3][6] = -17.0
    exp[i][4][4] = 129.0/13.0
    exp[i][4][0] = -5.0
    exp[i][4][1] = -15.0
    exp[i][4][2] = -6.0
    exp[i][4][3] = -22.0
    exp[i][4][5] = -21.0
    exp[i][4][6] = -13.0
    exp[i][5][5] = 129.0/13.0
    exp[i][5][0] = -18.0
    exp[i][5][1] = -6.0
    exp[i][5][2] = -26.0
    exp[i][5][3] = -4.0
    exp[i][5][4] = -21.0
    exp[i][5][6] = -16.0
    exp[i][6][6] = 161.0/6.0
    exp[i][6][0] = -9.0
    exp[i][6][1] = -11.0
    exp[i][6][2] = -19.0
    exp[i][6][3] = -17.0
    exp[i][6][4] = -13.0
    exp[i][6][5] = -16.0
    exp[i][7][7] = 0

if __name__ == "__main__":
    #print("YA")
    model = pulp.LpProblem("valuemax", pulp.LpMaximize)
    
    x = np.zeros((360, 8, 8), dtype=type(pulp.LpVariable))
    y = np.zeros((359, 8, 8), dtype=type(pulp.LpAffineExpression))
    yp = np.zeros((359, 8, 8), dtype=type(pulp.LpVariable))
    ym = np.zeros((359, 8, 8), dtype=type(pulp.LpVariable))

    for i in range(359) :
        for j in range(8) : 
            for k in range(8) :
                    index = 'yp' + str(i) + str(j) + str(k)
                    yp[i][j][k] = pulp.LpVariable(index, lowBound=0, cat='Binary')
                    index = 'ym' + str(i) + str(j) + str(k)
                    ym[i][j][k] = pulp.LpVariable(index, lowBound=0, cat='Binary')

    for i in range(360) : 
        for j in range(8) :
            for k in range(8) :
                index = 'x' + str(i) + str(j) + str(k)
                #print(index)
                x[i][j][k] = pulp.LpVariable(index, lowBound=0, cat='Binary')

    for i in range(359) :
        for j in range(8) :
            for k in range(8) :
                y[i][j][k] = (x[i][j][k] - x[i+1][j][k])
                if (y[i][j][k] <= 0) :
                    yp[i][j][k] = 0
                else :
                    yp[i][j][k] = y[i][j][k]
                if (y[i][j][k] >= 0) :
                    ym[i][j][k] = 0
                else :
                    ym[i][j][k] = -y[i][j][k]

    model += (lpSum(x[i][j][k] * exp[i][j][k] for i in range(360) for j in range(8) for k in range(8)) + (-100000*lpSum(yp[k][i][j] + ym[k][i][j] for i in range(8) for j in range(8) for k in range(359))))
    
    for i in range(360) : # One movement per sec
        model += (lpSum(x[i][j][k] for j in range(8) for k in range(8)) == 1)
    
    for i in range(13) : # Start from redbuff
        model += (x[i][4][4] == 1)
    
    for i in range(300) :
        model += (x[13+i][4][4] == 0)
    
    model += (lpSum(x[i][4][4] for i in range(313, 360)) <= 13) # 1 redbuff

    model += (lpSum(x[i][0][0] for i in range(360)) <= 33) # 6 birds
    model += (lpSum(x[i][1][1] for i in range(360)) <= 27) # 3 wolves
    model += (lpSum(x[i][2][2] for i in range(360)) <= 48) # 2 rocks
    model += (lpSum(x[i][3][3] for i in range(360)) <= 26) # 1 froggy
    model += (lpSum(x[i][5][5] for i in range(360)) <= 26) # 1 blue buff
    model += (lpSum(x[i][6][6] for i in range(360)) <= 18) # 1 crab
    
    for i in range(230) :
        model += (lpSum(x[i+j][0][0] for j in range(131)) <= 11)
    for i in range(232) :
        model += (lpSum(x[i+j][1][1] for j in range(129)) <= 9)
    for i in range(225) :
        model += (lpSum(x[i+j][2][2] for j in range(136)) <= 16)
    for i in range(228) :
        model += (lpSum(x[i+j][3][3] for j in range(133)) <= 13)
    for i in range(48) :
        model += (lpSum(x[i+j][4][4] for j in range(313)) <= 13)
    for i in range(48) :
        model += (lpSum(x[i+j][5][5] for j in range(313)) <= 13)
    for i in range(205) :
        model += (lpSum(x[i+j][6][6] for j in range(156)) <= 6)
    '''
    for i in range(360) :
        for j in range(8) :
            for k in range(8) :
                model += (x[i][j][k] >= 0)
                model += (x[i][j][k] <= 1)
    '''
    '''
    for i in range(350) :
        temp0 = 11*((lpSum(x[i+k][0][0] for k in range(11)))/11)
        model += (lpSum(x[i+j][0][0] for j in range(11)) == temp0) 
    for i in range(352) :
        temp1 = 9*((lpSum(x[i+k][1][1] for k in range(9)))/9)
        model += (lpSum(x[i+j][1][1] for j in range(9)) == temp1)
    for i in range(345) :
        temp2 = 16*((lpSum(x[i+k][2][2] for k in range(16)))/16)
        model += (lpSum(x[i+j][2][2] for j in range(16)) == temp2)    
    for i in range(348) :
        temp3 = 13*((lpSum(x[i+k][3][3] for k in range(13)))/13)
        model += (lpSum(x[i+j][3][3] for j in range(13)) == temp3)    
    for i in range(348) :
        temp4 = 13*((lpSum(x[i+k][4][4] for k in range(13)))/13)
        model += (lpSum(x[i+j][4][4] for j in range(13)) == temp4)  
    for i in range(348) :
        temp5 = 13*((lpSum(x[i+k][5][5] for k in range(13)))/13)
        model += (lpSum(x[i+j][5][5] for j in range(13)) == temp5)  
    for i in range(355) :
        temp6 = 6*((lpSum(x[i+k][6][6] for k in range(6)))/6)
        model += (lpSum(x[i+j][6][6] for j in range(6)) == temp6)        

    for i in range(230) :
        model += (lpSum(x[i+j][0][1] for j in range(131)) <= 11)
        model += (lpSum(x[i+j][0][2] for j in range(131)) <= 10)
        model += (lpSum(x[i+j][0][3] for j in range(131)) <= 19)
        model += (lpSum(x[i+j][0][4] for j in range(131)) <= 5)
        model += (lpSum(x[i+j][0][5] for j in range(131)) <= 18)
        model += (lpSum(x[i+j][0][6] for j in range(131)) <= 9)
    for i in range(232) :
        model += (lpSum(x[i+j][1][0] for j in range(129)) <= 11)
        model += (lpSum(x[i+j][1][2] for j in range(129)) <= 20)
        model += (lpSum(x[i+j][1][3] for j in range(129)) <= 8)
        model += (lpSum(x[i+j][1][4] for j in range(129)) <= 15)
        model += (lpSum(x[i+j][1][5] for j in range(129)) <= 6)
        model += (lpSum(x[i+j][1][6] for j in range(129)) <= 11)
    for i in range(225) :
        model += (lpSum(x[i+j][2][0] for j in range(136)) <= 10)
        model += (lpSum(x[i+j][2][1] for j in range(136)) <= 20)
        model += (lpSum(x[i+j][2][3] for j in range(136)) <= 28)
        model += (lpSum(x[i+j][2][4] for j in range(136)) <= 6)
        model += (lpSum(x[i+j][2][5] for j in range(136)) <= 26)
        model += (lpSum(x[i+j][2][6] for j in range(136)) <= 19)
    for i in range(228) :
        model += (lpSum(x[i+j][3][0] for j in range(133)) <= 19)
        model += (lpSum(x[i+j][3][1] for j in range(133)) <= 8)
        model += (lpSum(x[i+j][3][2] for j in range(133)) <= 28)
        model += (lpSum(x[i+j][3][4] for j in range(133)) <= 22)
        model += (lpSum(x[i+j][3][5] for j in range(133)) <= 4)
        model += (lpSum(x[i+j][3][6] for j in range(133)) <= 17)
    for i in range(48) :
        model += (lpSum(x[i+j][4][0] for j in range(313)) <= 5)
        model += (lpSum(x[i+j][4][1] for j in range(313)) <= 15)
        model += (lpSum(x[i+j][4][2] for j in range(313)) <= 6)
        model += (lpSum(x[i+j][4][3] for j in range(313)) <= 22)
        model += (lpSum(x[i+j][4][5] for j in range(313)) <= 21)
        model += (lpSum(x[i+j][4][6] for j in range(313)) <= 13)
    for i in range(48) :
        model += (lpSum(x[i+j][5][0] for j in range(313)) <= 18)
        model += (lpSum(x[i+j][5][1] for j in range(313)) <= 6)
        model += (lpSum(x[i+j][5][2] for j in range(313)) <= 26)
        model += (lpSum(x[i+j][5][3] for j in range(313)) <= 4)
        model += (lpSum(x[i+j][5][4] for j in range(313)) <= 21)
        model += (lpSum(x[i+j][5][6] for j in range(313)) <= 16)
    for i in range(205) :
        model += (lpSum(x[i+j][6][0] for j in range(156)) <= 9)
        model += (lpSum(x[i+j][6][1] for j in range(156)) <= 11)
        model += (lpSum(x[i+j][6][2] for j in range(156)) <= 19)
        model += (lpSum(x[i+j][6][3] for j in range(156)) <= 17)
        model += (lpSum(x[i+j][6][4] for j in range(156)) <= 13)
        model += (lpSum(x[i+j][6][5] for j in range(156)) <= 16)
    ###########################################################
    for i in range(230) :
        model += ((lpSum(x[i+j][0][1] for j in range(131)))
                +(lpSum(x[i+j][0][2] for j in range(131)))
                +(lpSum(x[i+j][0][3] for j in range(131)))
                +(lpSum(x[i+j][0][4] for j in range(131)))
                +(lpSum(x[i+j][0][5] for j in range(131)))
                +(lpSum(x[i+j][0][6] for j in range(131)))
                ) >= (lpSum(x[i+j][0][0] for j in range(131))/11)*1
                
    for i in range(232) :
        model += ((lpSum(x[i+j][1][0] for j in range(129)))
                +(lpSum(x[i+j][1][2] for j in range(129)))
                +(lpSum(x[i+j][1][3] for j in range(129)))
                +(lpSum(x[i+j][1][4] for j in range(129)))
                +(lpSum(x[i+j][1][5] for j in range(129)))
                +(lpSum(x[i+j][1][6] for j in range(129)))
                ) >= (lpSum(x[i+j][1][1] for j in range(129))/9)*1

    for i in range(225) :
        model += ((lpSum(x[i+j][2][0] for j in range(136)))
                +(lpSum(x[i+j][2][1] for j in range(136)))
                +(lpSum(x[i+j][2][3] for j in range(136)))
                +(lpSum(x[i+j][2][4] for j in range(136)))
                +(lpSum(x[i+j][2][5] for j in range(136)))
                +(lpSum(x[i+j][2][6] for j in range(136)))
                ) >= (lpSum(x[i+j][2][2] for j in range(136))/16)*1

    for i in range(228) :
        model += ((lpSum(x[i+j][3][0] for j in range(133)))
                +(lpSum(x[i+j][3][1] for j in range(133)))
                +(lpSum(x[i+j][3][2] for j in range(133)))
                +(lpSum(x[i+j][3][4] for j in range(133)))
                +(lpSum(x[i+j][3][5] for j in range(133)))
                +(lpSum(x[i+j][3][6] for j in range(133)))
                ) >= (lpSum(x[i+j][3][3] for j in range(133))/13)*1

    for i in range(48) :
        model += ((lpSum(x[i+j][4][0] for j in range(313)))
                +(lpSum(x[i+j][4][1] for j in range(313)))
                +(lpSum(x[i+j][4][2] for j in range(313)))
                +(lpSum(x[i+j][4][3] for j in range(313)))
                +(lpSum(x[i+j][4][5] for j in range(313)))
                +(lpSum(x[i+j][4][6] for j in range(313)))
                ) >= (lpSum(x[i+j][4][4] for j in range(313))/13)*1

    for i in range(48) :
        model += ((lpSum(x[i+j][5][0] for j in range(313)))
                +(lpSum(x[i+j][5][1] for j in range(313)))
                +(lpSum(x[i+j][5][2] for j in range(313)))
                +(lpSum(x[i+j][5][3] for j in range(313)))
                +(lpSum(x[i+j][5][4] for j in range(313)))
                +(lpSum(x[i+j][5][6] for j in range(313)))
                ) >= (lpSum(x[i+j][5][5] for j in range(313))/13)*1

    for i in range(205) :
        model += ((lpSum(x[i+j][6][0] for j in range(156)))
                +(lpSum(x[i+j][6][1] for j in range(156)))
                +(lpSum(x[i+j][6][2] for j in range(156)))
                +(lpSum(x[i+j][6][3] for j in range(156)))
                +(lpSum(x[i+j][6][4] for j in range(156)))
                +(lpSum(x[i+j][6][5] for j in range(156)))
                ) >= (lpSum(x[i+j][6][6] for j in range(156))/6)*1

    '''
    # Route

    model.solve()
    for v in model.variables():
        print(v.name, "=", v.varValue)

    print("obj=", value(model.objective))

    for i in range(8):
        for j in range(8):
            for k in range(360):
                f.write(str(int(x[k][i][j].varValue)))
            f.write("\n")

    f.close()

    f2.close()

    #print(type(y[0][0]))