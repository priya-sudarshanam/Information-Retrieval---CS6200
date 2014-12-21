import os, sys, math, urllib, re, linecache, timeit
from PorterStemmer import PorterStemmer
from collections import defaultdict
from string import punctuation

#global variables - filepaths

STOPWORDS_FILE = "/Users/Priya/Desktop/IR/HW05/stoplist.txt"
FILES_PATH = "/Users/Priya/Desktop/IR/HW05/created_files_without_stopping/"
CACM_PATH = "/Users/Priya/Desktop/IR/HW05/cacm/"
QUERY_TEXT_FILE = "/Users/Priya/Desktop/IR/HW05/cacm_query.txt"
RESULT_FILE_PATH = "/Users/Priya/Desktop/IR/HW05/removing_stopping/"

NUM_DOCS = 3204
NUM_TERMS = 246737
AVG_DOCLEN_1 = 77 
NUM_UNIQUE_TERMS_1 = 11418

MESG = "Results written successfully to file"

def stopwords(filename):
  stopwords_list = []
  with open(filename, 'r') as input_file:
    for line in input_file:
      [stopwords_list.append(word.lower()) for word in line.split()]
  input_file.close()  
  return stopwords_list


""" returns two dictionaries: 
    1. docid_words_dict: docid : processed content (stopping/stemming)
    2. docid_doclen_dict: docid : doclen """
def dicts_docid_words_docid_doclen():
  global STOPWORDS_FILE 
  p = PorterStemmer() 
  stopwords_list = stopwords(STOPWORDS_FILE)
  docid_words_dict = defaultdict(lambda: [])
  docid_doclen_dict = {}
  path = CACM_PATH
  """extract all the file names in the path and put them into a list"""
  dirs_list = os.listdir(path)
  for docname in dirs_list:
    docno = ''.join([s for s in docname if s.isdigit()])
    f = urllib.urlopen(path+docname).read()
    data = re.compile(r'.*?<pre>(.*?)([0-9]+\t[0-9]+\t[0-9]+)', re.DOTALL).match(f).group(1)
    data = re.findall(r"[\w]+", data)
    for word in data:
      word = word.lower()  
  #    if word not in stopwords_list:  
      word_stemmed = p.stem(word, 0,len(word)-1)
      docid_words_dict[docno].append(word_stemmed)
    """doclen is the length of doc after stopping and stemming"""
    docid_doclen_dict[docno]=len(data)  
  return docid_words_dict,docid_doclen_dict

 
""" returns three dictionaries:
    1. term_ctf_dict: term  : ctf 
    2. term_docids_dict: term : [docid-1, docid-2, ...]
    3. termdocid_tf_dict: (term, docid) : tf """
def dicts_term_ctf_term_docid_docid_tf(docid_words_dict):
  term_ctf_dict = defaultdict(lambda: 0)
  term_docids_dict = defaultdict(lambda: [])
  termdocid_tf_dict = defaultdict(lambda: 0)
  for docid, words_list in docid_words_dict.iteritems():
    for w in words_list:
      term_ctf_dict[w] += 1
      termdocid_tf_dict[(w,docid)] += 1
      if docid not in term_docids_dict[w]:
        term_docids_dict[w].append(docid)
  return term_ctf_dict, term_docids_dict, termdocid_tf_dict

def create_lemur_files(term_docids_dict, term_ctf_dict, docid_doclen_dict,termdocid_tf_dict):
  for term, docid_list in term_docids_dict.iteritems():
    try:
      f = open(FILES_PATH+term, "w+")
    except:
      continue
    f.write(str(term_ctf_dict[term])+'\t'+str(len(term_docids_dict[term]))+'\n')
    """write docid, doclen, tf in the file"""
    [f.write(docid + '\t' + str(docid_doclen_dict[docid]) + '\t' + str(termdocid_tf_dict[(term, docid)]) + '\n') for docid in docid_list]
  f.close()

""" fetch Lemur data from file by specifying term """
def fetch_lemur_data(term):
  global FILES_PATH
  with open(FILES_PATH + term, 'r') as f:
    data = f.read()
    numbers = re.compile(r'(\d+)',re.DOTALL).findall(data)
    ctf,df = float(numbers[0]), float(numbers[1])
    inverted_list = map(lambda i: (int(numbers[2 + 3*i]),
                         float(numbers[3 + 3*i]),
                         float(numbers[4 + 3*i]))
                    ,range(0, (len(numbers) - 2)/3))
  return ctf,df,inverted_list

""" get average doclen """
def get_avg_doclen(docid_doclen_dict):
  len_sum = 0
  num_of_docs = 0
  for doclen in docid_doclen_dict.values():
    len_sum += doclen
    num_of_docs += 1
  avg_doclen = len_sum / num_of_docs
  return avg_doclen


####--------------------------------------------------------------------------------------------------
""" Merging with project 2 """
####--------------------------------------------------------------------------------------------------


""" Create a dictionary: query_id : term list (term have been lowered, stemmed and maybe stopped)
    The parameter is_stopping is a boolean: true => stopping; false => not stopping"""
def dict_qryid_terms(is_stopping):
  global STOPWORDS_FILE 
  stopwords_list = stopwords(STOPWORDS_FILE)  ## create stopwords list
  p = PorterStemmer() ##create an Porter Stemmer instance 
  dictquery = defaultdict(lambda: [])  ## create the target dictionary
  with open(QUERY_TEXT_FILE, 'r') as f: 
    for line in f: 
      data_list = re.findall(r"[\w]+", line)
      query_id = data_list[0]
      for term in data_list[1:]:
        term = term.lower()
        if is_stopping:
          if term not in stopwords_list:
            dictquery[query_id].append(p.stem(term, 0,len(term)-1))
        else: 
            dictquery[query_id].append(p.stem(term, 0,len(term)-1))
  return dictquery

## Returns the average query length
def avg_query_len(qryid_terms_dict):
  l=[]
  temp_dict = {key: len(value) for (key, value) in qryid_terms_dict.iteritems()}
  len_query = (float(sum([v for v in temp_dict.values()])))
  len_dict = len([l.append(v) for v in temp_dict.values()])
  return len_query/len_dict

## Returns a term_freq_dictionary {term : term frequency}:
def dict_term_freq(dict_qryid_terms):
  term_freq_dict={}
  for v in dict_qryid_terms.values():
    for u in v:
      term_freq_dict[u]=v.count(u)
  return term_freq_dict

## Returns a term_qrylen_dict {term : length of the query}:
def dict_term_qrylen(qryid_terms_dict):
  term_qrylen_dict = {}
  #qryid_terms_dict = dict_qryid_terms()
  temp_dict = {key: len(value) for (key, value) in qryid_terms_dict.iteritems()}
  for k,v in qryid_terms_dict.iteritems():
    for k1,v1 in temp_dict.iteritems():
      if k1 == k:
         for i in v:
            term_qrylen_dict[i]=v1
  return term_qrylen_dict

## Returns a qryterm_wgt_dict {term : weight of term in that query}:
def dict_qryterm_wgt(qryid_terms_dict):
   term_freq_dict = dict_term_freq(qryid_terms_dict)
   term_qrylen_dict = dict_term_qrylen(qryid_terms_dict)
   avgquerylen=avg_query_len(qryid_terms_dict)
   qryterm_wgt_dict = {}
   qryterm_wgt_dict = {k: ((term_freq_dict[k])/(term_freq_dict[k] + 0.5 + ((1.5*v)/avgquerylen))) for (k,v) in term_qrylen_dict.iteritems()}
   return qryterm_wgt_dict

## model 1 : vector space model - okapitf
def run_model_1(qryid_terms_dict):
  f = open(RESULT_FILE_PATH+"results_model-1.txt", "w")
  query_term_wgt_dict = dict_qryterm_wgt(qryid_terms_dict)
  for qry_id, terms in qryid_terms_dict.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    for term in terms:
      try:
        ctf,df,inv_list = fetch_lemur_data(term)
      except:
        ctf = 0
        df = 0
        inv_list = []
      for (docid,doclen,tf) in inv_list:
        docid_score_dict[docid] += (query_term_wgt_dict[term] * (tf / (tf + 0.5 + ((1.5 * doclen)/AVG_DOCLEN_1)))) 

    print_models(docid_score_dict, qry_id,f)
  f.close()
  print MESG+"   model- 1"

## model 2 : vector space model - okapitf * idf
def run_model_2(qryid_terms_dict):
  f = open(RESULT_FILE_PATH+"results_model-2.txt", "w")
  query_term_wgt_dict = dict_qryterm_wgt(qryid_terms_dict)
  for qry_id, terms in qryid_terms_dict.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    for term in terms:
      try:
        ctf,df,inv_list = fetch_lemur_data(term)
      except:
        ctf = 0
        df = 0
        inv_list = []
      for (docid,doclen,tf) in inv_list:
        docid_score_dict[docid] += ((query_term_wgt_dict[term] * (tf / (tf + 0.5 + ((1.5 * doclen)/AVG_DOCLEN_1)))) * math.log(float(NUM_DOCS/1 + df)))

    print_models(docid_score_dict, qry_id,f)
  f.close()
  print MESG+"   model- 2"

## model 3 - Laplace smoothing
def run_model_3(qryid_terms_dict):
  f = open(RESULT_FILE_PATH+"results_model-3.txt", "w")
  query_term_wgt_dict = dict_qryterm_wgt(qryid_terms_dict)

  for qry_id, terms_list in qryid_terms_dict.iteritems():
    docid_score_dict = defaultdict(lambda: 0)

    seen_dict = defaultdict(lambda: ()) 
    docid_qryterms_dict = defaultdict(lambda: [])  
    term_ctfdf_dict = defaultdict(lambda: ())  
    for term in terms_list:
      try:
        ctf,df,inv_list = fetch_lemur_data(term)
      except:
        ctf = 0
        df = 0
        inv_list = []
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
            docid_score_dict[docid] += math.log((tf + 1)/(doclen + NUM_UNIQUE_TERMS_1))

          else:
            try:
              ctf = term_ctfdf_dict[term][0]
            except:
              ctf = 0
            docid_score_dict[docid] += math.log(1/(doclen + NUM_UNIQUE_TERMS_1))
          
    print_models(docid_score_dict, qry_id,f)
  f.close()
  print MESG+"   model- 3" 

## model 4 - Jelinek-Mercer smoothing
def run_model_4(qryid_terms_dict):
  f = open(RESULT_FILE_PATH+"results_model-4.txt", "w")
  query_term_wgt_dict = dict_qryterm_wgt(qryid_terms_dict)

  for qry_id, terms_list in qryid_terms_dict.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    seen_dict = defaultdict(lambda: ()) 
    docid_qryterms_dict = defaultdict(lambda: [])  
    term_ctfdf_dict = defaultdict(lambda: ())  
    for term in terms_list:
      try:
        ctf,df,inv_list = fetch_lemur_data(term)
      except:
        ctf = 0
        df = 0
        inv_list = []
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
            docid_score_dict[docid] += math.log(0.8 * tf/doclen) + (0.2 * ctf / NUM_TERMS)
          else:
            try:
              ctf = term_ctfdf_dict[term][0]
            except:
              ctf = 0.000001
            docid_score_dict[docid] += math.log(0.2 * ctf / NUM_TERMS)
          
    print_models(docid_score_dict, qry_id,f)
  f.close()
  print MESG+"   model- 4"   

## model 5 -BM25
def run_model_5(qryid_terms_dict):
  f = open(RESULT_FILE_PATH+"results_model-5.txt", "w")
  query_term_wgt_dict = dict_qryterm_wgt(qryid_terms_dict)

  for qry_id, terms in qryid_terms_dict.iteritems():
    docid_score_dict = defaultdict(lambda: 0)
    for term in terms:
        try:
          ctf,df,inv_list = fetch_lemur_data(term)
        except:
          ctf = 0
          df = 0
          inv_list = []
        for (docid,doclen,tf) in inv_list:
            docid_score_dict[docid] += (math.log((NUM_DOCS - df + 0.5) / (df + 0.5)) * ((tf * (1.2 +1)) / (tf + (1.2 * (0.25 + (0.75 * doclen / AVG_DOCLEN_1))))))
            
    print_models(docid_score_dict, qry_id,f)
  f.close()
  print MESG+"   model- 5"

def print_models(docid_score_dict, qry_id, f):
    rank=1
    for (docid, score) in sorted(docid_score_dict.items(), key = lambda x: x[1], reverse=True):
      if rank <= 1000:
        line_of_text = str(qry_id) + "\t" + 'Q0' + "\t" + ('CACM-' + str(docid)) + "\t" + str(rank) + "\t" + str(score) + "\t" + 'Exp' + '\n'
        f.write(line_of_text)
        rank += 1
        
####--------------------------------------------------------------------------------------------------
""" Main function """
####--------------------------------------------------------------------------------------------------


if __name__ == '__main__':

  start = timeit.default_timer()
  #create two dictionaries:
  #docid_words_dict,docid_doclen_dict = dicts_docid_words_docid_doclen()

  #create three dictionaries:
  #term_ctf_dict, term_docids_dict, termdocid_tf_dict = dicts_term_ctf_term_docid_docid_tf(docid_words_dict)
  
  #create_lemur_files() to create a lemur statistics file for each unique term"""
  #create_lemur_files(term_docids_dict, term_ctf_dict, docid_doclen_dict,termdocid_tf_dict)

  qryid_terms_dict = dict_qryid_terms(True)
  
  # run 5 models
  run_model_1(qryid_terms_dict)
  run_model_2(qryid_terms_dict)
  run_model_3(qryid_terms_dict)
  run_model_4(qryid_terms_dict)
  run_model_5(qryid_terms_dict)
##
  stop = timeit.default_timer()
  print '\n'
  print 'running time is:', stop - start

       
