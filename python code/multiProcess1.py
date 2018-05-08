
import os
from multiprocessing import Process

def doubler(number):
	result = number * 2
	proc = os.getpid()
	print('{0} doubled to {1} by process id : {2}'.format(number, result, proc))

if __name__=="__main__":
	number = [3,6,9,12,15,21,35,11,11,11,11,11]
	procs = []
	for index, numver in enumerate(number):
		proc = Process(target= doubler, args=(number,))
		procs.append(proc)
		proc.start()

	for proc in procs: # 기다렸다가 끝내라
		proc.join()














"""
import multiprocessing
import threading
import os
import time

class MyThread(threading.Thread):
    def __init__(self, threadid,start, end,result):
        threading.Thread.__init__(self)
        self.threadid = threadid
        self.start1 = start
        self.end = end
        self.daemon = True

    def run(self):
        sum = 0
        for i in range(self.start1, self.end):
            sum += i
        result[self.threadid] = sum
     
def sum(end1):
	sum =0
	for i in range(1,end1+1):
		sum += i
	print(os.getpid())
	return sum

if __name__=="__main__":
	pool = multiprocessing.Pool(4)
	tstart = time.time()
	print(pool.map(sum,range(100001,1000100)))
	print(time.time()-tstart)"""