import comment as c # import function to download comments
import script as sc # import function to download meta-data
from multiprocessing import Process # import to parallize comment and video download 

def main(file_value = 10):
	c.main(file_value) #function to  download comment
	sc.main() #function to download meta-data 


if __name__ == "__main__":

	# main()
	processor = [] # list that will contain all of our 8 process 
	for k in range(1,9):
		p = Process(target=main,args=(k,))  
		p.start() # start of the process 
		processor.append(p) # add this process to the list 
	
	for elt in processor:
		elt.join() # to end all processes
	