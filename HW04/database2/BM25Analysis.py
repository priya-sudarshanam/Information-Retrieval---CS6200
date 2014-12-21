import urllib, re, string, math
from collections import defaultdict
from string import punctuation

lemurlink0="http://fiji5.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=0&g=p&v="
lemurlink1="http://fiji5.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=1&g=p&v="
lemurlink2="http://fiji5.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=2&g=p&v="
lemurlink3="http://fiji5.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=3&g=p&v="
docidmapping="./intextdocid.txt"
BM250_result="./bm0.txt"
BM251_result="./bm1.txt"
BM252_result="./bm2.txt"
BM253_result="./bm3.txt"
queries_file="./queriestrial.txt"

#constants
AVE_DOCLEN0 = 493
NUM_DOCS0 = 84678

AVE_DOCLEN1 = 493
NUM_DOCS1 = 84678

AVE_DOCLEN2 = 288
NUM_DOCS2 = 84678

AVE_DOCLEN3 = 288
NUM_DOCS3 = 84678


MESG = "Results written successfully to file- BM0"
MESG = "Results written successfully to file- BM1"
MESG = "Results written successfully to file- BM2"
MESG = "Results written successfully to file- BM3"

def cleaned_queries():
  dictquery={}
  with open(queries_file, 'r') as f: 
          for line in f: 
            splitLine = line.split()
            dictquery[splitLine[0]] = splitLine[1:]
  return dictquery

# finding the length of the average query and returning the value
def avg_query():
  dict1=cleaned_queries()
  l=[]
  dict2 = {key: len(value) for (key, value) in dict1.iteritems()}
  len_query=(float(sum([v for v in dict2.values()])))
  len_dict=len([l.append(v) for v in dict2.values()])
  return len_query/len_dict

# calculating the term frequency of each term in the query
def term_freq():
  dict1=cleaned_queries()
  d1={}
  for v in dict1.values():
    for u in v:
      d1[u]=v.count(u)
  return d1

#calculate query_length for each term
def term_querylength():
  dict3={}
  dict1=cleaned_queries()
  qdict2=dict2 = {key: len(value) for (key, value) in dict1.iteritems()}
  for k,v in dict1.iteritems():
    for k1,v1 in qdict2.iteritems():
          if k1 == k:
             for i in v:
                dict3[i]=v1
  return dict3

# calculate the weight of each term in the query                
def query_term_weight():
   termdict3=term_freq()
   dict3=term_querylength()
   avgquerylen=avg_query()
   dict4={}
   dict4 = {k: ((termdict3[k])/(termdict3[k] + 0.5 + ((1.5*v)/avg_query()))) for (k,v) in dict3.iteritems()}
   return dict4

# creating an invertedlist - code given in the lemur details from the hw page
def inverted_list(llink,term):
    text = urllib.urlopen(llink+term).read()
    data = re.compile(r'.*?<BODY>(.*?)<HR>', re.DOTALL).match(text).group(1)
    numbers = re.compile(r'(\d+)',re.DOTALL).findall(data)
    ctf,df = float(numbers[0]), float(numbers[1])
    inverted_list = map(lambda i: (int(numbers[2 + 3*i]),
               		       float(numbers[3 + 3*i]),
	                       float(numbers[4 + 3*i]))
                    ,range(0, (len(numbers) - 2)/3))
    return ctf,df,inverted_list

#mapping of internal docid to external docid
def docid_mapping():
  docid_mapping_dict = {}
  with open(docidmapping, 'r') as f:
    docid_mapping_dict = {line.split()[0]: line.split()[1] for line in f}
  return docid_mapping_dict

def bm0(query_dictionary):
  f = open(BM250_result, "w")
  for qry_id, terms_list in query_dictionary.iteritems():
   docid_score_dict = defaultdict(lambda: 0)
   for term in terms_list:
        ctf,df,inv_list = inverted_list(lemurlink0,term)
        for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (math.log((NUM_DOCS0 - df + 0.5) / (df + 0.5)) * ((tf * (1.2 +1)) / (tf + (1.2 * (0.25 + (0.75 * doclen / AVE_DOCLEN0))))))
   print_models(docid_score_dict, qry_id, f)
  f.close()
  print MESG

def bm1(query_dictionary):
  f = open(BM251_result, "w")
  for qry_id, terms_list in query_dictionary.iteritems():
   docid_score_dict = defaultdict(lambda: 0)
   for term in terms_list:
        ctf,df,inv_list = inverted_list(lemurlink1,term)
        for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (math.log((NUM_DOCS1 - df + 0.5) / (df + 0.5)) * ((tf * (1.2 +1)) / (tf + (1.2 * (0.25 + (0.75 * doclen / AVE_DOCLEN1))))))
   print_models(docid_score_dict, qry_id, f)
  f.close()
  print MESG

def bm2(query_dictionary):
  f = open(BM252_result, "w")
  for qry_id, terms_list in query_dictionary.iteritems():
   docid_score_dict = defaultdict(lambda: 0)
   for term in terms_list:
        ctf,df,inv_list = inverted_list(lemurlink2,term)
        for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (math.log((NUM_DOCS2 - df + 0.5) / (df + 0.5)) * ((tf * (1.2 +1)) / (tf + (1.2 * (0.25 + (0.75 * doclen / AVE_DOCLEN2))))))
   print_models(docid_score_dict, qry_id, f)
  f.close()
  print MESG

def bm3(query_dictionary):
  f = open(BM253_result, "w")
  for qry_id, terms_list in query_dictionary.iteritems():
   docid_score_dict = defaultdict(lambda: 0)
   for term in terms_list:
        ctf,df,inv_list = inverted_list(lemurlink3,term)
        for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (math.log((NUM_DOCS3 - df + 0.5) / (df + 0.5)) * ((tf * (1.2 +1)) / (tf + (1.2 * (0.25 + (0.75 * doclen / AVE_DOCLEN3))))))
   print_models(docid_score_dict, qry_id, f)
  f.close()
  print MESG
   
   
#printing all models
def print_models(dict1, qry_id,f):
   docid_map_dict=docid_mapping()
   rank=1
   for (docid, score) in sorted(dict1.items(), key = lambda x: x[1], reverse=True):
       if rank <= 1000:
           line_of_text = str(qry_id) + "\t" + 'Q0' + "\t" + docid_map_dict[str(docid)] + "\t" + str(rank) + "\t" + str(score) + "\t" + 'Exp' + '\n'
           f.write(line_of_text)

           rank += 1

def main():
   query_dictionary = cleaned_queries()

   bm0(query_dictionary)
   bm1(query_dictionary)
   bm2(query_dictionary) 
   bm3(query_dictionary)
  
   
if __name__ == '__main__':
  main()

