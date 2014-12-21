from __future__ import division
import os

#variables
unique_words=[]
words_seen = 0	
uniq_seen = 0
seen=[]
xy_pairs =[]
total_x = 0
numerator = 0
denominator=0
total_y=0
x_avg=0
y_avg=0

file2="C:/Users/Priya/Desktop/IR/HW02/LeastSquaresInput.txt"

#######################################################################
# open file and read content
with open(file2) as f:
	words = f.readlines()  
	words = map(lambda s: s.strip(), words) 
	f.close

###############################################################
# process unique words

for w in words:
	words_seen += 1  
	if w not in seen:
		uniq_seen += 1 
		seen.append(w)  
		xy_pairs.append([words_seen,uniq_seen])
		
#######################################################################
## compute the K and beta, using least square method

xy_length = len(xy_pairs)

for x in xy_pairs:
  total_x += x[0]
  total_y += x[1]


for p in xy_pairs:
	numerator += (p[0] - x_avg) * (p[1] - y_avg)
	denominator += (p[0] - x_avg)**2

x_avg = float(total_x) / xy_length
y_avg= float(total_y) / xy_length
slope = float(numerator) / denominator
y_intercept = (y_avg - slope * x_avg)

print "Total number of words: ", total_x, "\nUnique words seen: ", uniq_seen ,"\n"
print "Beta: {0:.5f}".format(slope), "\nk: {0:.5f}".format(y_intercept)


if "__name__" == "__main__":
   print_words(file2)
  
