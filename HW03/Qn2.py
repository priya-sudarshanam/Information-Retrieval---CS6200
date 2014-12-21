from math import log, pow, floor
import timeit

start = timeit.default_timer()
#variables
counter = 0
p_rank = []
i = 0
d = 0.85
preplex = []
pageRank = {}

# calculate perplexity
def preplexity(pr):
    preplex = 0
    for page in pr:
        preplex += pr[page] * log(1.0/pr[page], 2)
    return pow(2, preplex)

#calculate difference in perplexity
def preplexfour(preplex):
    prep = map(lambda x: floor(x), preplex)
    prep0 = prep[0]
    prep = map(lambda x: x == prep0, prep)
    return len(prep) >= 4 and all(prep)

#create dictionary, calculate outpages and inlinks
def loadFile(path):
    inpages = {}
    outpages = {}
    #open file and return inlinks and outlinks
    with open(path) as f:
        for line in f:
            splits = line.split(' ')
            splits = filter(lambda x: x != '\n', splits)
            splits = map(lambda x: x.replace('\n',''), splits)
            page = splits[0]
            if page in inpages:
                inpages[page] += splits[1:]
            else:
                inpages[page] = splits[1:]
            if not page in outpages:
                outpages[page] = 0
            for inpage in splits[1:]:
                if inpage in outpages:
                    outpages[inpage] += 1
                else:
                    outpages[inpage] = 1
    return (inpages, outpages)

#calculate pagerank 
def pageRank(inpages, outpages):
    global i, preplex, d
    
    pageRank={}
    # filter sinknodes
    sinkpages = filter(lambda x: outpages[x] == 0, outpages)
    N = len(inpages)
    calc_d = (1.0-d)/N

    #calculate initial pagerank for each page
    for page in inpages:
        pageRank[page] = 1.0/N
    
    preplex += [preplexity(pageRank)]

    while not preplexfour(preplex[-4:]):
        newPR = {}
        sinkPR = 0
        for sink in sinkpages:
            sinkPR += pageRank[sink]
        for page in inpages:
            newPR[page] = calc_d + d*sinkPR/N
            for inlink in inpages[page]:
                newPR[page] += d* pageRank[inlink]/outpages[inlink]
        for page in newPR:
            pageRank[page] = newPR[page]

        i += 1
        preplex += [preplexity(pageRank)]

    print "#########################################\n Page Ranks\n"
    for prep in preplex:
        print prep
    return pageRank
   
def main():
    global counter, p_rank
    
    i,o = loadFile('C:/Users/Priya/Desktop/IR/HW03/wt2g_inlinks.txt')
    pr = pageRank(i,o)
   
    for page in pr:
        p_rank += [(page, pr[page])]
    sorted_pra = (sorted(p_rank, key=lambda x: x[1]))

    print "\n#########################################\n  Top 50 pages by page rank: \n"
    for p,r in list(reversed(sorted_pra[-50:])):
        print p, "\t", r
    
    print "\n#########################################\n Top 50 pages by in-link count:\n"
  
    for k in list(reversed(sorted(i, key=lambda k: len(i[k])))):
        if counter < 50:
            print k, "\t", len(i[k])
            counter += 1


    stop = timeit.default_timer()
    print '\n'
    print 'Running time is:', stop-start

if __name__ == '__main__':
    main()
