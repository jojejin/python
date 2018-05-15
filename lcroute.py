import random
import multiprocessing, os, time, random
Sbox = (0xE, 0x3, 0x0, 0x7, 0x2, 0xC, 0xF, 0xB, 0x5, 0xA, 0x6, 0x9, 0x8, 0x1, 0x4, 0xD)

def LCxor(a, b):
    return (a & 8) >> 3 ^ (a & 4) >> 2 ^ (a & 2) >> 1 ^ (a & 1) ^ (b & 8) >> 3 ^ (b & 4) >> 2 ^ (b & 2) >> 1 ^ (b & 1)

def permutation(p):
    p = (p[0] << 12) + (p[1] << 8) + (p[2] << 4) + p[3]
    c = [((p >> 15 & 1) << 3) | ((p >> 11 & 1) << 2) | ((p >> 7 & 1) << 1) | ((p >> 3 & 1)),
         ((p >> 14 & 1) << 3) | ((p >> 10 & 1) << 2) | ((p >> 6 & 1) << 1) | ((p >> 2 & 1)),
         ((p >> 13 & 1) << 3) | ((p >> 9 & 1) << 2) | ((p >> 5 & 1) << 1) | ((p >> 1 & 1)),
         ((p >> 12 & 1) << 3) | ((p >> 8 & 1) << 2) | ((p >> 4 & 1) << 1) | ((p & 1))]
    return c

def substitution(p):
    p = (p[0] << 12) + (p[1] << 8) + (p[2] << 4) + p[3]
    c = [(Sbox[(p >> 12 & 0xf)]), (Sbox[(p >> 8 & 0xf)]), (Sbox[(p >> 4 & 0xf)]), (Sbox[(p & 0xf)])]
    return c

def generationLCtable():
	LCtable = []

	for table in range(16):
	    LCtable.append([-8 for i in range(16)])

	for i in range(16):  # input masking
	    for j in range(16):  # output masking
	        for x in range(16):
	            if 0 == LCxor(i & x, j & Sbox[x]):
	                LCtable[i][j] += 1
	return LCtable


def selectRoute(LCtable):
	LCroute = []
	for route in range(16):
	    LCroute.append([])

	for i in range(16):
	    for j in range(16):
	    	if (LCtable[i][j] != 0):
	    		LCroute[i].append(j)
	return LCroute

def findRoute(LCtable,LCroute,Round,Prob,fileName,count):
	routine = []

	while count:
	    count -= 1
	    for a in range(1, 16):
	        table = []
	        t = [0,0,0,0]
	        t[count&3] = a

	        table.append(t[:])
	        prob = 1 / 2

	        for j in range(Round):
	            for i in range(4):
	                if t[i] != 0:
	                	temp = t[i]
	                	t[i] = LCroute[t[i]][ random.randint(0, len(LCroute[t[i]])-1)]
	                	prob *= abs(LCtable[temp][t[i]] / 8)            	
	            table.append(t[:])
	            t = permutation(t)
	            table.append(t[:])

	        if prob >= Prob:
	        	if [table[0],table[-1],prob] not in routine:
	        		routine.append([table[0],table[-1],prob])
	        		routineLast = routine[-1]
	        		if routineLast[1].count(0) >= 2:
		        		f = open(fileName,'a')
		        		A = str(hex((routineLast[0][0]<<12) +(routineLast[0][1]<<8) +(routineLast[0][2]<<4) +(routineLast[0][3])))
		        		B = str(hex((routineLast[1][0]<<12) +(routineLast[1][1]<<8) +(routineLast[1][2]<<4) +(routineLast[1][3])))
		        		C = str(routineLast[2])
		        		data = "%s\t%s\t%s\n"%(A,B,C)
		        		f.write(data)
		        		f.close()
		        		print ("i'm find!",count)


def Route(RouteInfo):
	_round, Prob, fileName, count= RouteInfo

	table = generationLCtable()
	route = selectRoute(table)
	findRoute(table,route,_round,Prob,fileName,count)

#Route([4,0.02,"routine_round_1.txt",1000000])
if __name__=="__main__":

	RouteInfo = [[4,0.02,"routine_round_1.txt",1000000],
	[3,0.05,"routine_round_2.txt",1000000],
	[2,0.1,"routine_round_3.txt",1000000],
	[1,0.2,"routine_round_4.txt",1000000],
	[0,0.5,"routine_round_5.txt",1000000]]

	pool = multiprocessing.Pool(5)
	tstart = time.time()
	pool.map(Route,RouteInfo)
	print(time.time()-tstart)

"""
table = generationLCtable()
print("   ",end = "")
for j in range(0,16):
	print("%3d"%j,end = "")
print()
j = 0

for subtable in table:
	print ("%3d"%j,end = "")
	for i in subtable:
		print("%3d"%i,end = "")
	print()
	j+=1

route = selectRoute(table)
for subroute in route:
	print(subroute)	
"""
