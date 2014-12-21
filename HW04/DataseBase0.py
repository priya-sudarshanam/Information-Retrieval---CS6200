import urllib, re, string, math
from collections import defaultdict
from string import punctuation

#files and lemur link
docidmapping="./intextdocid.txt"
model1_result="./pjtokpi1.txt"
model2_result="./pjtokpi2.txt"
model3_result="./pjtokpi3.txt"
model4_result="./pjtokpi4.txt"
model5_result="./pjtokpi5.txt"
queries_file="./25cleanedqueries.txt"
lemurlink="http://fiji5.ccs.neu.edu/~zerg/lemurcgi/lemur.cgi?d=0&g=p&v="

#constants
NUM_DOCS = 84678 
NUM_TERMS = 41802513
NUM_UNIQUE_TERMS = 207615 
AVE_DOCLEN = 493 
MESG = "Results written successfully to file- Database0"

#cleaned up the query by removing stop words and returning the dictionary
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
def inverted_list(term):
    text = urllib.urlopen(lemurlink+term).read()
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
    for line in f:
      splitLine = line.split()
      docid_mapping_dict[splitLine[0]]=splitLine[1]
  return docid_mapping_dict

#OKAPITF - MODEL 1
#calculate the score for each term and rank in the reverse order of the score
def okapimodel1(query_dictionary, query_term_wgt_dict):
  f = open(model1_result, "w")
  for qry_id, terms in query_dictionary.iteritems():
     docid_score_dict = defaultdict(lambda: 0)
     for term in terms:
          ctf,df,inv_list = inverted_list(term)
          for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (query_term_wgt_dict[term] * (tf / (tf + 0.5 + ((1.5 * doclen)/288))))
     print_models(docid_score_dict, qry_id, f) 
  f.close()
  print MESG

#OKAPITF*IDF - MODEL 2
#calculate the score for each term and rank in the reverse order of the score
def okapimodel2(query_dictionary, query_term_wgt_dict):
  f = open(model2_result, "w")

  for qry_id, terms_list in query_dictionary.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    for term in terms_list:
        ctf,df,inv_list = inverted_list(term)
        for (docid,doclen,tf) in inv_list:
           docid_score_dict[docid] += ((query_term_wgt_dict[term] * (tf / (tf + 0.5 + ((1.5 * doclen)/288)))) * math.log(float(84678/1 + df)))
    print_models(docid_score_dict, qry_id, f) 
  f.close()
  print MESG

#LAPLACE SMOOTHING - MODEL 3
#calculate the score for each term and rank in the reverse order of the score
def okapimodel3(query_dictionary):
  f = open(model3_result, "w")

  for qry_id, terms_list in query_dictionary.iteritems():
   docid_score_dict = defaultdict(lambda: 0)
   seen_dict = defaultdict(lambda: ()) 
   docid_qryterms_dict = defaultdict(lambda: [])  
   term_ctfdf_dict = defaultdict(lambda: ()) 
   for term in terms_list:
        ctf,df,inv_list = inverted_list(term)
        for (docid,doclen,tf) in inv_list:
          seen_dict[(docid,term)] = (doclen, tf)
          term_ctfdf_dict[term] = (ctf, df)
          docid_qryterms_dict[docid] = terms_list

   for docid, terms in docid_qryterms_dict.iteritems():
      for term in terms:
        if seen_dict.has_key((docid,term)):
          doclen = seen_dict[(docid,term)][0]
          tf = seen_dict[docid,term][1]
          ctf = term_ctfdf_dict[term][0]
          docid_score_dict[docid] += math.log((tf + 1)/(doclen + NUM_UNIQUE_TERMS),10)
        else:
          ctf = term_ctfdf_dict[term][0]
          docid_score_dict[docid] += math.log((1/(doclen + NUM_UNIQUE_TERMS) ), 10)

          
   print_models(docid_score_dict, qry_id, f) 
  f.close()
  print MESG

#JELINEK-MERCER SMOOTHING - MODEL 4
#calculate the score for each term and rank in the reverse order of the score
def okapimodel4(query_dictionary):
  f = open(model4_result, "w")
  for qry_id, terms_list in query_dictionary.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    seen_dict = defaultdict(lambda: ())
    docid_qryterms_dict = defaultdict(lambda: [])  
    term_ctfdf_dict = defaultdict(lambda: ())  
    for term in terms_list:
        ctf,df,inv_list = inverted_list(term)
        for (docid,doclen,tf) in inv_list:
          seen_dict[(docid,term)] = (doclen, tf)
          term_ctfdf_dict[term] = (ctf, df)
          docid_qryterms_dict[docid] = terms_list

    for docid, terms in docid_qryterms_dict.iteritems():
      for term in terms:
        if seen_dict.has_key((docid,term)):
          doclen = seen_dict[(docid,term)][0]
          tf = seen_dict[docid,term][1]
          ctf = term_ctfdf_dict[term][0]
          docid_score_dict[docid] += math.log( (0.8 * tf/doclen) + (0.2 * ctf / NUM_TERMS), 10 )
        else:
          ctf = term_ctfdf_dict[term][0]
          docid_score_dict[docid] += math.log( (0.2 * ctf / NUM_TERMS), 10)
    print_models(docid_score_dict, qry_id, f) 
  f.close()
  print MESG

#BM25 - MODEL 5
#calculate the score for each term and rank in the reverse order of the score
def okapimodel5(query_dictionary):
  f = open(model5_result, "w")
  for qry_id, terms_list in query_dictionary.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    for term in terms_list:
        ctf,df,inv_list = inverted_list(term)
        for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (math.log((84678 - df + 0.5) / (df + 0.5)) * ((tf * (1.2 +1)) / (tf + (1.2 * (0.25 + (0.75 * doclen / 288))))))

    print_models(docid_score_dict, qry_id, f) 
  f.close()
  print MESG

# print all models
def print_models(dict1, qry_id,f):
   docid_map_dict=docid_mapping()
   rank=1
   for (docid, score) in sorted(dict1.items(), key = lambda x: x[1], reverse=True):
       if rank <= 1000:
           line_of_text = str(qry_id) + "\t" + 'Q0' + "\t" + docid_map_dict[str(docid)] + "\t" + str(rank) + "\t" + str(score) + "\t" + 'Exp' + '\n'
           f.write(line_of_text)

           rank += 1

# main calls other functions
def main():
   query_dictionary = cleaned_queries()
   query_term_wgt_dict = query_term_weight()
   
   okapimodel1(query_dictionary, query_term_wgt_dict)
   okapimodel2(query_dictionary, query_term_wgt_dict)
   okapimodel3(query_dictionary)
   okapimodel4(query_dictionary)
   okapimodel5(query_dictionary)
   
if __name__ == '__main__':
  main()




