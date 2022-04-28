from multiprocessing import Process # import to parallize comment and video download 
import description as desc
import deep_analyse as analyse

if __name__ == "__main__" :
	processor = [] # list that will contain all of our 8 process 
	for k in range(1,9):
		p = Process(target=desc.main,args=(k,))   
		processor.append(p) # add this process to the list 
		p.start() # start of the process 
	for elt in processor:
		elt.join() # to end all processes
	analyse.main()