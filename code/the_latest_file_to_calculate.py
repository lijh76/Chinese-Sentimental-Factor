# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:40:10 2018

@author: Li Jiahao
"""
# Preparation Section
import synonyms
import sys
import codecs
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import wordnet as wn

def loadWordNet():
    # Load the WordNet dataset from the cow-not-full file and integrate it into a set
    f = codecs.open("D:/withoutchinese/cow-not-full.txt", "rb", "utf-8")
    known = set()
    for l in f:
        if l.startswith('#') or not l.strip():
            continue
        row = l.strip().split("\t")
        if len(row) == 3:
            (synset, lemma, status) = row
        elif len(row) == 2:
            (synset, lemma) = row
            status = 'Y'
        else:
            print("illformed line: ", l.strip())
        if status in ['Y', 'O' ]:
            if not (synset.strip(), lemma.strip()) in known:
                known.add((synset.strip(), lemma.strip()))
    return known

def findWordNet(known, key):
    # Find the WordNet codes for a given target word
    ll = []
    for kk in known:
        if (kk[1] == key):
            ll.append(kk[0])
    return ll

def id2ss(ID):
    # Convert WordNet ID to WordNet Synset
    return wn.synset_from_pos_and_offset(str(ID[-1:]), int(ID[:8]))

def get_wnsimilarity(s0, s1, known):
    # Calculate WordNet similarity between two synsets
    l0 = findWordNet(known, s0)
    l1 = findWordNet(known, s1)
    if (len(l1) == 0) or (len(l0) == 0):
        return 0
    else:
        similarity = 0
        count = 0
        for wid0 in l0:
            desc0 = id2ss(wid0)
            for wid1 in l1:
                desc1 = id2ss(wid1)
                sim = desc0.path_similarity(desc1)
                if(sim != None):
                    similarity += desc0.path_similarity(desc1)
                else:
                    count += 1
        try:
            similarity /= (len(l0) * len(l1) - count)
        except:
            similarity = 0
    return similarity

known = loadWordNet()

# Read in the words for similarity calculation
m = []
with open('C:\\Users\\Li Jiahao\\Desktop\\trial\\word_classification.txt') as f:
    for line in f:
        m.append(line.strip('\n'))

# Calculation Section
x = []
for target_word in m:
    # Calculate WordNet and Synonyms similarity for each word in the list
    a = [target_word, get_wnsimilarity(target_word,'处罚', known),
         get_wnsimilarity(target_word,'违规', known),get_wnsimilarity(target_word,'亏欠', known),
         get_wnsimilarity(target_word,'亏本', known),get_wnsimilarity(target_word,'亏损', known),
         get_wnsimilarity(target_word,'降落', known),get_wnsimilarity(target_word,'降低', known),
         get_wnsimilarity(target_word,'降价', known),get_wnsimilarity(target_word,'突降', known),
         get_wnsimilarity(target_word,'直线滑降', known),get_wnsimilarity(target_word,'急降', known),
         get_wnsimilarity(target_word,'跌落', known),get_wnsimilarity(target_word,'暴跌', known),
         get_wnsimilarity(target_word,'下跌', known),get_wnsimilarity(target_word,'拖累', known),
         get_wnsimilarity(target_word,'下降', known),get_wnsimilarity(target_word,'下滑', known),
         get_wnsimilarity(target_word,'优势', known),get_wnsimilarity(target_word,'收购', known),
         get_wnsimilarity(target_word,'倍增', known),get_wnsimilarity(target_word,'剧增', known),
         get_wnsimilarity(target_word,'增值', known),get_wnsimilarity(target_word,'增加', known),
         get_wnsimilarity(target_word,'增多', known),get_wnsimilarity(target_word,'增大', known),
         get_wnsimilarity(target_word,'增益', known),get_wnsimilarity(target_word,'增进', known),
         get_wnsimilarity(target_word,'增长', known),get_wnsimilarity(target_word,'增高', known),
         get_wnsimilarity(target_word,'激增', known),get_wnsimilarity(target_word,'猛增', known),
         get_wnsimilarity(target_word,'改善', known),get_wnsimilarity(target_word,'提升', known),
         synonyms.compare(target_word,'处罚'), synonyms.compare(target_word,'违规'),
         synonyms.compare(target_word,'亏欠'), synonyms.compare(target_word,'亏本'),
         synonyms.compare(target_word,'亏损'), synonyms.compare(target_word,'降落'),
         synonyms.compare(target_word,'降低'), synonyms.compare(target_word,'降价'),
         synonyms.compare(target_word,'突降'), synonyms.compare(target_word,'直线滑降'),
         synonyms.compare(target_word,'急降'), synonyms.compare(target_word,'跌落'),
         synonyms.compare(target_word,'暴跌'), synonyms.compare(target_word,'下跌'),
         synonyms.compare(target_word,'拖累'), synonyms.compare(target_word,'下降'),
         synonyms.compare(target_word,'下滑'), synonyms.compare(target_word,'优势'),
         synonyms.compare(target_word,'收购'), synonyms.compare(target_word,'倍增'),
         synonyms.compare(target_word,'剧增'), synonyms.compare(target_word,'增值'),
         synonyms.compare(target_word,'增加'), synonyms.compare(target_word,'增多'),
         synonyms.compare(target_word,'增大'), synonyms.compare(target_word,'增益'),
         synonyms.compare(target_word,'增进'), synonyms.compare(target_word,'增长'),
         synonyms.compare(target_word,'增高'), synonyms.compare(target_word,'激增'),
         synonyms.compare(target_word,'猛增'), synonyms.compare(target_word,'改善'),
         synonyms.compare(target_word,'提升')]
    x.append(a)

# Output Data
name = ['word',"wn处罚","wn违规","wn亏欠","wn亏本","wn亏损","wn降落","wn降低",
        "wn降价","wn突降","wn直线滑降","wn急降","wn跌落","wn暴跌","wn下跌","wn拖累",
        "wn下降","wn下滑","wn优势","wn收购","wn倍增","wn剧增","wn增值","wn增加",
        "wn增多","wn增大","wn增益","wn增进","wn增长","wn增高","wn激增","wn猛增",
        "wn改善","wn提升", "syn处罚","syn违规","syn亏欠","syn亏本","syn亏损",
        "syn降落","syn降低","syn降价","syn突降","syn直线滑降","syn急降","syn跌落",
        "syn暴跌","syn下跌","syn拖累","syn下降","syn下滑","syn优势","syn收购","syn倍增",
        "syn剧增","syn增值","syn增加","syn增多","syn增大","syn增益","syn增进","syn增长",
        "syn增高","syn激增","syn猛增","syn改善","syn提升"]
text = pd.DataFrame(columns=name, data=x)
text.to_csv('C:\\Users\\Li Jiahao\\Desktop\\trial\\word_classification.csv')
