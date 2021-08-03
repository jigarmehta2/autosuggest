import datefinder
import pandas as pd
import numpy as np
import argparse
import os
import warnings
import pickle
import logging
import argparse
import re
import warnings
warnings.filterwarnings("ignore")
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

pd.set_option("display.max.columns", None)
import json
import numpy as np
import spacy
import nltk
import re
brackets_re = re.compile(r"[\()[],.*[\]]")
replace_by_space_re = re.compile(r"[{}|@,;]")
non_alphanum_re = re.compile(r"[^0-9a-z#+_']")

import nltk # important
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
lemmatizer = nltk.stem.WordNetLemmatizer()
import string
printable = set(string.printable)

Q_words=["When","How","Why","What","Which","Where","Who","Can","Is", "Am"]
social=["hi","thx","thnx","yes","no","thanks","good", "thank you", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning", "morning", "good day", "oops","good afternoon", "good evening", "greetings", "greeting", "good to see you", "good night","its good seeing you", "how are you", "how're you", "how are you doing", "how ya doin'", "how ya doin", "how is everything", "how is everything going", "how's everything going", "how is you", "how's you", "how are things", "how're things", "how is it going", "how's it going", "how's it goin'", "how's it goin", "how is life been treating you", "how's life been treating you", "how have you been", "how've you been", "what is up", "what's up", "what is cracking", "what's cracking", "what is good", "what's good", "what is happening", "what's happening", "what is new", "what's new", "what is neww", "g’day", "howdy"]
 
nlp = spacy.load("en_core_web_sm")

def rm_stocks(text):
    text=text.replace("w2","W-2")
    text=text.replace("W2","W-2")
    text=text.replace("acct","account")
    text=text.replace("xfer","transfer")
    #s=pd.read_csv("/Users/a656526/Downloads/Yahoo Ticker Symbols.csv")
    #stock=s.Ticker.str.upper().tolist()
    #all=[]
    #for i in text.upper().split(" "):
    #eturn all
    return text

def ner(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["MONEY","ORG"]:
            return ""
    return text

def rm_date(text):
    text=text.replace(".","")
    document = nlp(text)
    text_no_namedentities = []
    pos=0
    ents = [e.text for e in document.ents if e.label_ == "DATE"]
    
    for i,item in enumerate(text.split(" ")):
        if item in ents:
            pos=i
            pass
        else:
            text_no_namedentities.append(item)
    if(pos>0 and len(text_no_namedentities)>=pos):
        text_no_namedentities.pop(pos-1)
    pos=0
    return " ".join(text_no_namedentities).strip()

def clean_text(text):
    text = str(text).lower().strip()  # lowercase text
    
    #expanded_words = []    
#     for word in text.split():
#   # using contractions.fix to expand the shotened words
#         expanded_words.append(contractions.fix(word))   
#     text = ' '.join(expanded_words)
    expanded_words = []  
    text = " ".join([w for w in text.split(" ") if w not in social])
   
    text=''.join(filter(lambda x: x in printable, text))
    text_encode=text.encode('ascii', 'ignore')
    text_decode = text_encode.decode()
    text=" ".join(text.split())
   
    # regex clean operations
    text = re.sub(brackets_re, "", text)  # remove [] & () brackets
    text = re.sub(replace_by_space_re, " ", text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(non_alphanum_re, " ", text)  # delete symbols which are not alphanumeric numbers from text
    text = re.sub(r"\s{2,}", " ", text)
   
    #lemmatization
    #text = " ".join([w for w in text.split(" ")])
    #text=text.replace("my","")
    text=text.replace("401 k","401k")
    text=text.replace("w2","W-2")
    text=text.replace("w 2","W-2")
    text=text.replace(" .",".")
    text=text.replace("?.","?")
    text=text.replace(".?",".")
    text=text.replace(" ?","?")
    text=text.replace("  "," ")
    text = " ".join([w for w in text.split(" ") if w !="my"])

    #print(text)
    text='. '.join(list(map(lambda x: x.strip().capitalize(), text.split('.'))))
 
    text=text.replace(" i "," I ")
    return text.strip()  # return cleaned text