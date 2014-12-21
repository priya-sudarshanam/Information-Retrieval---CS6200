import sys 
from compiler.ast import flatten

# define variables
P=[]
sinkNodes=[]
d = 0.85
filename = "C:/Users/Priya/Desktop/IR/HW03/GraphNodes.txt"
initPR ={}
newPR ={}
dictionary ={}
outlinks = {}
i=0

# create dictionary 
def node_dictionary(filename): 
   global P, initPR, newPR, dictionary
   with open(filename, 'r') as f: 
          for line in f: 
            splitLine = line.split() 
            dictionary[splitLine[0]] =splitLine[1:]

   #create a list of sinknodes
   for k in dictionary.keys(): 
        if k not in flatten(dictionary.values()): 
            sinknodes.append(k)
   
   #create a list of keys of the dictionary
   for key in dictionary.keys(): 
      P.append(key) 

   #create initial page rank for each nodes
   for p in dictionary: 
      initPR[p] = (float("{0:.3f}".format(float(1)/len(P)))) 

   #create total outlinks for each nodes
   for k in dictionary.keys(): 
      ctr=flatten(dictionary.values()).count(k) 
      outlinks[k]=ctr 

   #call pagerank function with dictionary, and other details
   calc_page_rank(dictionary, initPR, sinkNodes) 
  
     
# calculate pagerank for nodes
def calc_page_rank(dictionary, initPR, sinkNodes): 
   global i, P
   
   while i < 100: 
         sinkPR = 0
         for p in sinkNodes: 
            sinkPR += initPR[p] 
              
         for p in P: 
            newPR[p] = (1-d)/len(P) + (d*sinkPR)/len(P)
            for q in dictionary[p]: 
                 newPR[p] += (d*initPR[q])/(outlinks[q]) 

         for p in P: 
             initPR[p] = newPR[p] 
  
         i += 1
         dict1=sorted(initPR.iteritems(), key=lambda key_value: key_value[0])
           
         #print page rank for iteration 1
         if i == 1: 
             print "Iteration 1"
             for k, v in dict1: 
                print k, (float("{0:.5f}".format(v))) 
             print "\n"

         #print page rank for iteration 10
         if i == 9: 
             print "Iteration 10"
             for k, v in dict1: 
                print k, (float("{0:.5f}".format(v))) 
             print "\n"

         #print page rank for iteration 100
         if i == 99: 
             print "Iteration 100"
             for k, v in dict1: 
                print k, (float("{0:.5f}".format(v))) 
             print "\n"
  

# call function
if __name__ == "__main__":
   node_dictionary(filename) 
