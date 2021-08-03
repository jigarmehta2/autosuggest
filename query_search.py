from create_inv_index_search import *
from clean_text import *

with open('corpus.pickle', 'rb') as handle:
    documents= pickle.load(handle)
    handle.close()
    
with open('inverted_index.pickle', 'rb') as handle:
    inverted = pickle.load(handle)
    handle.close()
  
Q_words=["When","Are","How","Why","What","Which","Where","Who","Can","Is", "Am","do","does","I"]
Q_words=[x.lower() for x in Q_words]
    
def search_docs(queries):
    #input should be list
    
    out1=[]
    for query in queries:
        query=query.strip()
        result_docs = search(inverted, query)
        #print ("Search for '%s'\n" % (query))
        #print ("Search for '%s': %r" % (query, result_docs))
        out=[]
       
        for doc in result_docs:
            d=documents[doc]
            if( (len(d[0].split(" "))<13) & (query.lower() in d[0].lower())): 
            ### add logic for non-matching with hybrid solution!
                if (query.lower().split(" ")[0] not in Q_words):
                    out.append(d)
                    #print(d)
                elif(d[0].lower().startswith(query.lower())):
                    out.append(d)
                    #print(d)
        out1.append(out)
        
    #de-dup, rank, resleect
    out_final=pd.DataFrame()
    for i in range(len(out1)):
        if(len(out1[i])==0):
            continue
        a=pd.DataFrame(out1[i],columns=["suggested_docs","score"])
        a['query']= queries[i]
        a.sort_values(by='score',ascending=False,inplace=True)
        a.drop_duplicates(inplace=True)
        a=a.head(5)
        out_final=out_final.append(a,ignore_index=True)
        #print(a.shape)    
    return out_final[['query','suggested_docs','score']]