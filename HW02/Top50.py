from collections import Counter

#variables:
total = 0
uniq_total = 0
words_seen = [] # using seen to collect the words have been seen
seen = []
rank = 0
line1 =  "\r *** Most frequent 25 words: *** \n WORD   FREQUENCY      RANK    PROBABILITY    RANK * PROB    "
line2 =  "\n\n\r *** Most frequent words starting with letter f:  \nWORD  \
         FREQUENCY        RANK   PROBABILITY   RANK * PROB "
counter = 0
FList = []
file2="C:/Users/Priya/Desktop/IR/HW02/Top50.txt"

######################################################################
## Returns: the number of total count of the words.
def countTotal(words):
        total = 0
        for w in words:
          total += 1 
        return total
######################################################################
## Returns: the total count of unique words.
def unique_words(words):
     global seen, uniq_total
     for w in words:
         if w not in words_seen:
               uniq_total += 1
               words_seen.append(w)
     return uniq_total

######################################################################
## Returns: the word's starting with f
def top_fwords(words, n, seen):
     global rank, FList
     for w in words:
          if w.startswith('f') and w not in seen: 
               FList.append(w)  
     top_words = Counter(FList).most_common(n)  
     
     for w in top_words:
          rank += 1
          print w[0],'   ','\t', w[1], '\t\t' , rank, '\t' , probability(w[1],countTotal(words)), '\t\t' \
              , rank * probability(w[1],countTotal(words)), '\t\t' 

######################################################################

## Returns: the word's probability of occurrence
def probability(occurs, total):
     return round(float(occurs)/total,4)


######################################################################
## Returns: the top n most frequent words 
def top_words(words, n):
     global rank  
     cnt = Counter(words)  
     common_words = cnt.most_common(n) 
     for w in common_words:
          rank += 1
         
          print w[0],'\t' , w[1], '\t\t', rank, '\t' \
              , probability(w[1],countTotal(words)), '\t\t' \
              , rank * probability(w[1],countTotal(words)), '\t\t' 
              
######################################################################
def print_words():
     global seen, counter
     with open(file2) as f:
          words = f.readlines()  
          words = map(lambda s: s.strip(), words) 
          f.closed
    
     print line1
     top_words(words, 25)  
     print line2
     
     for w in Counter(words).most_common(25): 
          seen.append(w[0])   

     top_fwords(words, 25, seen)  
     print "\n Total words:", countTotal(words), "\nTotal unique words:", unique_words(words)
 
######################################################################
print_words()
     







