# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:39:04 2018

@author: Li Jiahao
"""

import jieba
import datetime
import time
import os


def cut(origin_file, cut_file, remove_stopwords=True):
    """
    Function to tokenize Chinese text and optionally remove stopwords
    Args:
    - origin_file (str): Path to the input file
    - cut_file (str): Path to the output file
    - remove_stopwords (bool): Flag to indicate whether to remove stopwords

    Returns:
    None
    """
    print('Tokenizing...\n')  # Displaying a message indicating tokenization
    fp = open(origin_file, 'r', encoding='utf-8')  # Open the input file
    raw_text = fp.read()  # Read the content without tokenization
    fp.close()  # Close the file
    words = jieba.cut(raw_text, cut_all=False)  # Tokenize the text using jieba
    # Join the tokens into a string, and replace certain punctuation and digits
    str_cut = ' '.join(words).replace('，', '').replace('。', '').replace('？', '').replace('！', '') \
        .replace('“', '').replace('”', '').replace('：', '').replace('…', '').replace('（', '').replace('）', '') \
        .replace('—', '').replace('《', '').replace('》', '').replace('、', '').replace('‘', '') \
        .replace('’', '').replace("0", '').replace("1", '').replace("2", '').replace("3", '').replace('；', '').replace(
        '.', '') \
        .replace("4", '').replace("5", '').replace("6", '').replace("7", '').replace("8", '').replace("9", '')

    if remove_stopwords:
        stop_words = []  # Create a list to store stopwords
        stop_f = open('C:\\Users\\Li Jiahao\\Desktop\\trial\\stop_words.txt', 'r')  # Open the stopwords file
        for line in stop_f.readlines():  # Read stopwords line by line
            line = line.strip()
            if not len(line):
                continue  # Skip empty lines
            stop_words.append(line)  # Add stopwords to the list
        stop_f.close()  # Close the stopwords file

        strlist_cut = str_cut.split(' ')  # Split the tokenized string into a list
        for string in strlist_cut:  # Iterate over each token in the list
            if not len(string):  # If the token has length 0, remove it
                strlist_cut.remove(string)
                continue
            if string in stop_words:  # If the token is a stopword, remove it
                strlist_cut.remove(string)
                continue
        str_cut = ' '.join(strlist_cut)  # Join the tokens back into a string

    fp = open(cut_file, 'w', encoding='utf-8')  # Open the output file for writing
    fp.writelines(str_cut)  # Write the tokenized content to the file
    fp.close()  # Close the file


prev_time = datetime.datetime.now()  # Record the current time

# List all files in the specified directory
file_list = os.listdir("C:\\Users\\Li Jiahao\\Desktop\\trial\\article\\xueqiu")

for file_name in file_list:
    original_file = "C:\\Users\\Li Jiahao\\Desktop\\trial\\article\\xueqiu\\" + file_name
    cut_file = "C:\\Users\\Li Jiahao\\Desktop\\trial\\cut\\" + "cut_" + file_name
    cut(original_file, cut_file, remove_stopwords=True)

cur_time = datetime.datetime.now()  # Record the time after tokenization
h1, remainder = divmod((cur_time - prev_time).seconds, 3600)
m1, s1 = divmod(remainder, 60)
print("Tokenization took %02d:%02d:%02d." % (h1, m1, s1))  # Print the time taken for tokenization
