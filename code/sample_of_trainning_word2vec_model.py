# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 13:39:31 2018

@author: Li Jiahao
"""

import re
import os
#import sys
import numpy as np
import codecs
import jieba
import gensim
import logging
from gensim.models import word2vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import datetime

def txt2sentence(filename):    
    # Function to convert a text file into a list of sentences
    sentences = []  # Create a list
    fp = open(filename, 'r', encoding='utf-8')  # Open the file in utf-8 format
    lines = fp.readlines()  # Read the file line by line
    for line in lines:  # Process each line
        line = line.strip()
        if len(line) <= 1:  # Skip if the line has a length less than or equal to 1
            continue
        line = line.replace('\n', '').replace('\r', '').split(' ')  # Replace line breaks, split words using spaces
        sentences.append(line)  # Add each word to the list
    return sentences

def train_Word2Vec(cut_file, save_model_name, Size=100, Min_count=5):
    # Train Word2Vec using cut_file, save the model as save_model_name, generate 100-dimensional word vectors
    print('start training...')  # Display start of training
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)  # Configuration for logging
    sentences = txt2sentence(cut_file)  # Convert cut_file to sentences
    model = gensim.models.Word2Vec(sentences, size=Size, min_count=Min_count)  # Train Word2Vec model
    model.save(save_model_name)  # Save the model locally
    # model.wv.save_word2vec_format(save_model_name+".bin",binary=True)

def cut(origin_file, cut_file, remove_stopwords=True):
    # Function to perform text segmentation and optionally remove stopwords
    print('cutting...\n')  # Display 'cutting' message
    fp = open(origin_file, 'r', encoding='utf-8')  # Open the origin_file in utf-8 format
    raw_text = fp.read()  # Read the file without cutting
    fp.close()  # Close the file
    words = jieba.cut(raw_text, cut_all=False)  # Tokenize the text using jieba
    str_cut = ' '.join(words).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
        .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
        .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
        .replace('’', '').replace("0", '').replace("1", '').replace("2", '').replace("3", '').replace('；', '').replace('.', '') \
        .replace("4", '').replace("5", '').replace("6", '').replace("7", '').replace("8", '').replace("9", '')
    # Remove punctuation and numbers
    if remove_stopwords:
        stop_words = list()  # Create a list to store stopwords
        stop_f = open('C:\\Users\\Li Jiahao\\Desktop\\trial\\stop_words.txt', 'r', encoding='utf-8')  # Open stopwords file
        for line in stop_f.readlines():  # Read stopwords line by line
            line = line.strip()
            if not len(line):
                continue
            stop_words.append(line)  # Add each stopword to the list
        stop_f.close()  # Close stopwords file

        strlist_cut = str_cut.split(' ')  # Split words in str_cut
        for string in strlist_cut:
            if not len(string):
                strlist_cut.remove(string)
                continue
            if string in stop_words:
                strlist_cut.remove(string)
                continue
        str_cut = ' '.join(strlist_cut)  # Join words back into str_cut
    fp = open(cut_file, 'w', encoding='utf-8')
    fp.writelines(str_cut)
    fp.close()  # Write segmented text into cut_file

save_model_name = 'C:\\Users\\Li Jiahao\\Desktop\\trial\\model'
# Name the generated model
origin_file = 'C:\\Users\\Li Jiahao\\Desktop\\trial\\std_zh_wiki_00'
cut_file = 'C:\\Users\\Li Jiahao\\Desktop\\trial\\cut_std_zh_wiki_00'

prev_time = datetime.datetime.now()  # Record the current time
cut(origin_file, cut_file, remove_stopwords=True)
# Perform text segmentation on origin_file, save the result in cut_file, and optionally remove stopwords
cur_time = datetime.datetime.now()  # Record the time after segmentation
h1, remainder = divmod((cur_time - prev_time).seconds, 3600)
m1, s1 = divmod(remainder, 60)

prev_time = datetime.datetime.now()  # Record the current time
train_Word2Vec(data_place + cut_file, data_place + save_model_name, Size=200, Min_count=2)
# Train Word2Vec model using cut_file, save the model, generate 200-dimensional word vectors, and set the minimum count to 2
cur_time = datetime.datetime.now()  # Record the time after training
h2, remainder = divmod((cur_time - prev_time).seconds, 3600)
m2, s2 = divmod(remainder, 60)
print("It costs %02d:%02d:%02d to cut." % (h1, m1, s1))  # Display time taken for text segmentation
print("It costs %02d:%02d:%02d to train word2vec model." % (h2, m2, s2))  # Display time taken for model training
