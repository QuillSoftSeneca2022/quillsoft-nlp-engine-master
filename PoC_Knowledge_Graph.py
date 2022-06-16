#source: https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/
import re
import pandas as pd
from pandas import DataFrame
import bs4
import requests
import spacy
from spacy import displacy
from DataClasses.Document import Document
from DataExtraction.DocumentExtraction import DocumentExtraction
import time

nlp = spacy.load('en_core_web_md')

from spacy.matcher import Matcher 
from spacy.tokens import Span 

import networkx as nx

import matplotlib.pyplot as plt
from tqdm import tqdm

def draw_graph_kg(file_path, relation):
    #pd.set_option('display.max_colwidth', 200)
    text = DocumentExtraction.GetDocumentSentences(file_path)

    #create Pandas DataFrame
    candidate_sentences = DataFrame(text,columns=[0])
    candidate_sentences.shape

    def get_entities(sent):
        
        # ent1 = ""
        # ent2 = ""

        # prv_tok_dep = ""    # dependency tag of previous token in the sentence
        # prv_tok_text = ""   # previous token in the sentence

        # prefix = ""
        # modifier = ""

        ent1, ent2, prv_tok_dep, prv_tok_text, prefix, modifier = "", "", "", "", "", ""
        #############################################################
    
        for tok in nlp(sent):
            # if token is a punctuation mark then move on to the next token
            if tok.dep_ != "punct":
                # check: token is a compound word or not
                if tok.dep_ == "compound":
                    prefix = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        # prefix = prv_tok_text + " "+ tok.text
                        prefix = " ".join([prv_tok_text, tok.text])

            
                # check: token is a modifier or not
                if tok.dep_.endswith("mod") == True:
                    modifier = tok.text
                    # if the previous word was also a 'compound' then add the current word to it
                    if prv_tok_dep == "compound":
                        #modifier = prv_tok_text + " "+ tok.text
                        modifier = " ".join([prv_tok_text, tok.text])
            
                if tok.dep_.find("subj") == True:
                    #ent1 = modifier +" "+ prefix + " "+ tok.text
                    ent1 = " ".join([modifier, prefix, tok.text])
                    # prefix = ""
                    # modifier = ""
                    # prv_tok_dep = ""
                    # prv_tok_text = ""      
                    prefix, modifier, prv_tok_dep, prv_tok_text = "","","","" 

                if tok.dep_.find("obj") == True:
                    #ent2 = modifier +" "+ prefix +" "+ tok.text
                    ent2 = " ".join([modifier, prefix, tok.text])

                
                # update variables
                prv_tok_dep, prv_tok_text = tok.dep_, tok.text
                #prv_tok_text = tok.text
        #############################################################

        return [ent1.strip(), ent2.strip()]

    entity_pairs = []
    print('printing test-----------------2')
    start_time = time.time()
    for i in tqdm(candidate_sentences[0]):
        entity_pairs.append(get_entities(i))
    end_time = time.time()
    print('processing time : ', end_time - start_time)

    def get_relation(sent):
        doc = nlp(sent)

        # Matcher class object 
        matcher = Matcher(nlp.vocab)

        #define the pattern 
        pattern = [{'DEP':'ROOT'}, 
                    {'DEP':'prep','OP':"?"},
                    {'DEP':'agent','OP':"?"},  
                    {'POS':'ADJ','OP':"?"}] 
        
        matcher.add("matching_1", [pattern]) 

        matches = matcher(doc)
        k = len(matches) - 1

        span = doc[matches[k][1]:matches[k][2]] 

        return(span.text)

    relations = [get_relation(i) for i in tqdm(candidate_sentences[0])]

    # extract subject
    source = [i[0] for i in entity_pairs]
    # extract object
    target = [i[1] for i in entity_pairs]

    #remove incomplete relations
    clean_source = []
    clean_target = []
    clean_relations = []

  
    for i in range(len(source)):
        if source[i].strip() != '' and target[i].strip() != '':
            clean_source.append(source[i])
            clean_target.append(target[i])
            clean_relations.append(relations[i])
 

    # print('printing test-----------------2')
    # start_time = time.time()
    # clean_source = [source[i] for i in range(len(source)) if source[i].strip() != '' and target[i].strip() != '']
    # clean_target = [target[i] for i in range(len(source)) if source[i].strip() != '' and target[i].strip() != '']
    # clean_relations = [relations[i] for i in range(len(source)) if source[i].strip() != '' and target[i].strip() != '']
    # end_time = time.time()
    # print('processing time : ', end_time - start_time)

    #print raw relations
    raw_relations = []
    [raw_relations.append(x) for x in clean_relations if x not in raw_relations]
    print("Relations")

   
    for i in range(len(raw_relations)):
        print("{}\t{}".format(raw_relations[i], pd.Series(relations).value_counts()[i]))

    kg_df = pd.DataFrame({'source':clean_source, 'target':clean_target, 'edge':clean_relations})

    if relation == '':
        #All relations
        G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12,12))
        pos = nx.spring_layout(G)
        nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
        plt.show(block=False)
    else:
        #Single relation
        G=nx.from_pandas_edgelist(kg_df[kg_df['edge'] == relation], "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())
        plt.figure(figsize=(12,12))
        pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
        nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
        plt.show(block=False)