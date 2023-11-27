# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:04:58 2018

@author: Li Jiahao
"""
# Two sets of labels
positive_words = ['提升', '改善', '猛增', '激增', '增高', '增长', '增进',
                  '增益', '增大', '增多', '增加', '增值', '剧增', '倍增',
                  '收购', '优势']

negative_words = ['下滑', '下降', '拖累', '下跌', '暴跌',
                  '跌落', '急降', '直线滑降', '突降', '降价', '降低',
                  '降落', '亏损', '亏本', '亏欠', '违规', '处罚']

# Code for calculating WordNet similarity
import codecs
import numpy as np
import nltk
from nltk.corpus import wordnet as wn


def loadWordNet():
    """
    Load the WordNet dataset from the "cow-not-full" file and integrate it into a set.
    Each entry in the set is a tuple containing a synset code and its corresponding lemma in Chinese.
    """
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
        if status in ['Y', 'O']:
            if not (synset.strip(), lemma.strip()) in known:
                known.add((synset.strip(), lemma.strip()))
    return known


def findWordNet(known, key):
    """
    Find WordNet synset codes for a given target word in Chinese.
    """
    ll = []
    for kk in known:
        if (kk[1] == key):
            ll.append(kk[0])
    return ll


def id2ss(ID):
    """
    Convert WordNet ID to Synset object.
    """
    return wn.synset_from_pos_and_offset(str(ID[-1:]), int(ID[:8]))


def get_wnsimilarity(s0, s1, known):
    """
    Calculate the WordNet similarity between two words using their synset codes.
    """
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
                if (sim != None):
                    similarity += desc0.path_similarity(desc1)
                else:
                    count += 1
        try:
            similarity /= (len(l0) * len(l1) - count)
        except:
            similarity = 0
    return similarity


# Load WordNet dataset
known = loadWordNet()

# Import the synonyms library
import synonyms

# Handling a single word case
target_word = '获益'

# Calculate and print WordNet and synonyms similarity for positive and negative labels
for l in positive_words:
    print('WordNet similarity for positive labels', target_word, '-', l, get_wnsimilarity(target_word, l, known))

for l in negative_words:
    print('WordNet similarity for negative labels', target_word, '-', l, get_wnsimilarity(target_word, l, known))

for l in positive_words:
    print('Synonyms similarity for positive labels', target_word, '-', l, synonyms.compare(target_word, l))

for l in negative_words:
    print('Synonyms similarity for negative labels', target_word, '-', l, synonyms.compare(target_word, l))

# For a list of words
m = ['效益', '爱情', '安装', '昂然', '讨还', '融和']
x = []
for target_word in m:
    # Calculate WordNet and synonyms similarity with each word in the label set
    a = [target_word, get_wnsimilarity(target_word, '处罚', known), get_wnsimilarity(target_word, '违规', known),
         get_wnsimilarity(target_word, '亏欠', known), get_wnsimilarity(target_word, '亏本', known),
         get_wnsimilarity(target_word, '亏损', known), get_wnsimilarity(target_word, '降落', known),
         get_wnsimilarity(target_word, '降低', known), get_wnsimilarity(target_word, '降价', known),
         get_wnsimilarity(target_word, '突降', known), get_wnsimilarity(target_word, '直线滑降', known),
         get_wnsimilarity(target_word, '急降', known), get_wnsimilarity(target_word, '跌落', known),
         get_wnsimilarity(target_word, '暴跌', known), get_wnsimilarity(target_word, '下跌', known),
         get_wnsimilarity(target_word, '拖累', known), get_wnsimilarity(target_word, '下降', known),
         get_wnsimilarity(target_word, '下滑', known), get_wnsimilarity(target_word, '优势', known),
         get_wnsimilarity(target_word, '收购', known), get_wnsimilarity(target_word, '倍增', known),
         get_wnsimilarity(target_word, '剧增', known), get_wnsimilarity(target_word, '增值', known),
         get_wnsimilarity(target_word, '增加', known), get_wnsimilarity(target_word, '增多', known),
         get_wnsimilarity(target_word, '增大', known), get_wnsimilarity(target_word, '增益', known),
         get_wnsimilarity(target_word, '增进', known), get_wnsimilarity(target_word, '增长', known),
         get_wnsimilarity(target_word, '增高', known), get_wnsimilarity(target_word, '激增', known),
         get_wnsimilarity(target_word, '猛增', known), get_
