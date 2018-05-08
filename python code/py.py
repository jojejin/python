import multiprocessing, os, time, random

loop = 10000000

def pi(count):
	result = 0
	i = 0
	while i < count :
		x = random.uniform(0,1)
		y = random.uniform(0,1)
		if (x**2 + y**2) <= 1: result += 1
		i += 1
	return result

if __name__=="__main__":
    pool = multiprocessing.Pool(8)

    _sum = 0

    tstart = time.time()
    
    for a in pool.map(pi,[loop/8 for i in range(8) ]):
    	_sum += a

    print (_sum/loop * 4)
    print(time.time()-tstart)