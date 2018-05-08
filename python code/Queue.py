from multiprocessing import Queue, Process
import time
def sender(data,q):
	for item in data:
		q.put(item)
		time.sleep(1)

def receiver(q):
	while True:
		x = q.get()
		if x == False:
			return
		print(x*x)


if __name__=="__main__":
	q = Queue()
	data = [2,3,6,7,9,11,-1]
	proc1 = Process(target = sender, args=(data,q))
	proc2 = Process(target = receiver, args=(q,))
	proc1.start()
	proc2.start()
	proc1.join()
	proc2.join()
	q.close()
