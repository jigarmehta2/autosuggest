from clean_text import *
from create_inv_index_search import *
import argparse
import pickle
import warnings
warnings.filterwarnings("ignore")

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    # Sagemaker specific arguments. Defaults are set in the environment variables.
    parser.add_argument('--data_dir', type=str)
    parser.add_argument('--train_file', type=str)
    parser.add_argument('--test_file', type=str )
    parser.add_argument('--model_dir', type=str)
    #parser.add_argument('--train_eval_predict', type=str, default='train')
    parser.add_argument('--raw_or_clean', type=str)
    parser.add_argument('--clean_filename', type=str)
    
    args = parser.parse_args()
    
    colnames=['Sentence','Intent']
    input_file1 =  os.path.join(args.data_dir, args.train_file) 
    input_file2 =  os.path.join(args.data_dir, args.test_file)
    
    if(args.raw_or_clean=="raw"):
  
        print("\nReading raw training and test files")
        f1 = pd.read_csv( input_file1,error_bad_lines=False, warn_bad_lines=False,header=0)[colnames]
        f2 = pd.read_csv( input_file2,error_bad_lines=False, warn_bad_lines=False,header=0)

        f1.columns=colnames
        f2.columns=colnames
        f=pd.concat([f1,f2],ignore_index=True)
        #f=f1
        print("size of raw dataset =", f.shape[0])
        #f=f.sample(frac=0.1)
       
        #print(colnames)

        f=f[f.Sentence.notnull()]
        f['len']=f.Sentence.str.split(" ").apply(len)
        f=f[f.len>3]
        f["new_sent"]=f.Sentence.apply(ner).apply(rm_date).apply(clean_text)  
        f["flag"]=f.new_sent.apply(lambda x: str(x.split(" ")[0]) in Q_words)*1
        f.loc[f.flag==1 ,"new_sent"]=f['new_sent']+"?"
        f.loc[f.flag==0 ,"new_sent"]=f['new_sent']+"."
        #text=text.replace(".?","?")
        f.drop(columns=["flag"],inplace=True)
        #f.Intent.value_counts()[:5]

        f.reset_index(inplace=True,drop=True)
        f['doc1']=np.arange(f.shape[0])
        #f.drop(columns="doc",inplace=True)
        f["doc"]="doc"+f["doc1"].astype(str)
        f.drop(columns="doc1",inplace=True)
        documents =dict(zip(f.doc,f.new_sent))
        with open('corpus', 'wb') as handle:
            pickle.dump(documents, handle)
    else:
        print("\nReading pre-processed clean file as input ..")
        with open(args.clean_filename, 'rb') as handle:
            documents = pickle.load(handle)
    #documents=dict(zip(corpus.doc,zip(corpus.Sentence,corpus.wgt)))
    print("\nBuilding inverted index")
    # Build Inverted-Index for documents
    inverted = {}
    #documents = {'doc1':doc1, 'doc2':doc2}
    for doc_id, text in documents.items():
        doc_index = inverted_index(text[0])
        inverted_index_add(inverted, doc_id, doc_index)
   
    
    print("\nSaving the inverted index as pickle")
    with open('inverted_index.pickle', 'wb') as handle:
        pickle.dump(inverted, handle)
        handle.close()
    print("Process Done, success!")
    # Print Inverted-Index
#     for word, doc_locations in inverted.items():
#        print (word, doc_locations)
