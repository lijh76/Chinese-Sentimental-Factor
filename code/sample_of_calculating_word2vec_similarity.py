# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 13:21:04 2018

@author: Li Jiahao
"""

import re
import os
# import sys
import numpy as np
import codecs
import jieba
import gensim
import logging
from gensim.models import word2vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import datetime


def show_Word2Vec(save_model_name, s, k=1, mode='similarity'):
    """
    Parameters
        ----------
        save_model_name : str
            The name of the saved Word2Vec model file.
        s : str
            The input word.
        k : int/str
            If mode='similarity', it's a string.
            If mode='topk' (default), it's an integer, default value is 1.

        mode : str
            'similarity': Calculate the similarity between s and k, where k is a string.
            'topk': Find the top k similar words to s, where k is an integer.
            'vector': Display the vector representation of the word.
    Returns
        ----------
        float
            If mode='similarity', this is the similarity between s and k.
    """
    model = word2vec.Word2Vec.load(save_model_name)

    if mode == 'topk':
        # Find and print the top k similar words to s
        y = model.most_similar(s, topn=k)
        print('Words most similar to "%s":\n' % s)
        for item in y:
            print(item[0], item[1])

    elif mode == 'return_topk':
        # Return an iterator of the top k similar words to s
        return model.wv.most_similar(s, topn=k)

    elif mode == 'similarity':
        # Calculate and print the similarity between s and k
        y = model.similarity(s, k)
        print('Similarity between "%s" and "%s": %f%%' % (s, k, (y * 100)))
        return y

    elif mode == 'vector':
        # Display the vector representation of the word
        print(model[s])


# Example: Calculate and print the similarity between '同意' and '生效'
show_Word2Vec('C:\\Users\\Li Jiahao\\Desktop\\trial\\fake_model.model', '同意', '生效', mode='similarity')

# Example: Calculate and print the similarity between '上涨' and '下跌'
model = word2vec.Word2Vec.load(save_model_name)
model.similarity('上涨', '下跌')
