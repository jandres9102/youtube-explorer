import comment as c # import function to download comments
import script as sc # import function to download meta-data
from multiprocessing import Process # import to parallize comment and video download 


if __name__ == "__main__":

	# main()
	processor = [] # list that will contain all of our 8 process 
	for k in range(1,9):
		p = Process(target=sc.main,args=())   
		p.start() # start of the process 
		processor.append(p) # add this process to the list 
	
	for elt in processor:
		elt.join() # to end all processes
	