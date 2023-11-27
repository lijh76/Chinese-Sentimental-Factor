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
    sentences = []  # Initialize a list
    fp = open(filename, 'r', encoding='utf-8')  # Open the file in UTF-8 format
    lines = fp.readlines()  # Read the file line by line
    for line in lines:
        line = line.strip()
        if len(line) <= 1:
            continue  # Skip lines with length less than or equal to 1
        line = line.replace('\n', '').replace('\r', '').split(' ')
        sentences.append(line)  # Append each word to the list
    return sentences

def train_Word2Vec(cut_file, save_model_name, Size=100, Min_count=5):
    # Train Word2Vec using content from cut_file, save the model as save_model_name, with a default vector size of 100 and minimum word count of 5
    print('Start training...')  # Display training start
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = txt2sentence(cut_file)
    model = gensim.models.Word2Vec(sentences, size=Size, min_count=Min_count)
    model.save(save_model_name)  # Save the trained model
    # model.wv.save_word2vec_format(save_model_name+".bin", binary=True)

def cut(origin_file, cut_file, remove_stopwords=True):
    # Perform text segmentation on origin_file and save the result in cut_file
    print('Cutting...\n')  # Display cutting message
    fp = open(origin_file, 'r', encoding='utf-8')
    raw_text = fp.read()  # Text without cutting
    fp.close()
    words = jieba.cut(raw_text, cut_all=False)
    str_cut = ' '.join(words).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
        .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
        .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
        .replace('’', '').replace("0", '').replace("1", '').replace("2", '').replace("3", '').replace('；', '') \
        .replace('.', '').replace("4", '').replace("5", '').replace("6", '').replace("7", '').replace("8", '') \
        .replace("9", '')
    # Remove punctuation, numbers, and other characters
    if remove_stopwords:
        stop_words = list()
        stop_f = open(stopwords_txt, 'r', encoding='utf-8')
        for line in stop_f.readlines():
            line = line.strip()
            if not len(line):
                continue
            stop_words.append(line)
        stop_f.close()
        strlist_cut = str_cut.split(' ')
        for string in strlist_cut:
            if not len(string):
                strlist_cut.remove(string)
                continue
            if string in stop_words:
                strlist_cut.remove(string)
                continue
        str_cut = ' '.join(strlist_cut)
    fp = open(cut_file, 'w', encoding='utf-8')
    fp.writelines(str_cut)
    fp.close()

save_model_name = 'C:\\Users\\Li Jiahao\\Desktop\\trial\\fake_model.model'
# Naming the generated model and saving it in the specified directory

origin_file = 'D:\\withoutchinese\\article\\xueqiu\\“不可抗辩”条款是“挡箭牌”？.txt'
cut_file = 'C:\\Users\\Li Jiahao\\Desktop\\trial\\cut_“不可抗辩”条款是“挡箭牌”？.txt'

prev_time = datetime.datetime.now()  # Current time
cut(origin_file, cut_file, remove_stopwords=False)
# Perform segmentation on the specified file, without removing stopwords
cur_time = datetime.datetime.now()  # Time after segmentation
h1, remainder = divmod((cur_time - prev_time).seconds, 3600)
m1, s1 = divmod(remainder, 60)

prev_time = datetime.datetime.now()  # Current time
train_Word2Vec(cut_file, save_model_name, Size=200, Min_count=2)
# Train Word2Vec with the specified parameters
cur_time = datetime.datetime.now()  # Time after training
h2, remainder = divmod((cur_time - prev_time).seconds, 3600)
m2, s2 = divmod(remainder, 60)
print("It takes %02d:%02d:%02d to perform segmentation." % (h1, m1, s1))
print("It takes %02d:%02d:%02d to train the Word2Vec model." % (h2, m2, s2))
