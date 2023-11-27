# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 09:42:56 2018

@author: HP

# Purpose: To annotate each section of the code for learning purposes.

"""

import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import datetime

# Define the working directory
work_space = r'D:\withoutchinese'

# Define a list of invalid characters in file names
invalid_char = ['|', '.', ':', ',', '*', '\\', '/', '/']


# Function to clean invalid characters in a string (used for article titles)
def clean_invalid(string):
    """
    Function to clean invalid characters in a string (used for article titles)
    Args:
    - string (str): Input string to be cleaned

    Returns:
    - tuple: A tuple containing the cleaned string and a flag indicating if any changes were made.
    """
    flag = 0  # Indicates if any changes were made
    for c in invalid_char:  # Check each invalid character
        if c in string:  # If the invalid character is present in the string
            string = string.replace(c, ' ')  # Replace it with a space
            flag = 1  # Set the flag to indicate changes
    return string, flag


def load(x, article_number):
    """
    Function to load articles on a webpage
    Args:
    - x: WebDriver object
    - article_number (int): Number of articles to load

    Returns:
    None
    """
    flag = 1  # Indicates if the bottom of the page has been reached
    L = 0
    while flag or L < article_number:
        L = len(x.find_elements_by_class_name('home__timeline__item'))  # Count the number of articles on the page
        try:
            x.find_element_by_class_name('home__timeline__more').click()  # Click the "Load More" button
            flag = 0  # Set the flag to 0 as the page has been scrolled
        except:
            x.find_elements_by_class_name('home__timeline__item')[-1].find_element_by_xpath('h3/a').send_keys(Keys.TAB)
            # If the "Load More" button is not found, use TAB to focus on the last article link (workaround)
    print(f'Loaded {L} articles.')


# Check if the 'article' directory exists, and create it if not
if not os.path.exists(work_space + '/article'):
    os.makedirs(work_space + '/article')

# Define the path for the log file
log_file = work_space + '/article/log.txt'


def download(x):
    """
    Function to download articles from a webpage
    Args:
    - x: WebDriver object

    Returns:
    None
    """
    count = 0  # Counter for downloaded articles
    article_links = x.find_elements_by_class_name('home__timeline__item')  # Find all article links
    log_fp = open(log_file, 'a')  # Open the log file for appending
    for link in article_links:
        try:
            link.find_element_by_xpath('h3/a').click()  # Click on the article link
            title = link.find_element_by_xpath('h3/a').text  # Get the title of the article
            title, flag = clean_invalid(title)  # Clean the title
            if flag:  # If changes were made to the title
                log_fp.writelines(title + '\n')  # Write the title to the log file
            windows = x.window_handles  # Get the handles of all open windows
            x.switch_to.window(windows[-1])  # Switch to the newly opened window
            text = x.find_element_by_xpath('//div[@class="article__bd__detail"]').text  # Get the text of the article

            # Check if the 'xueqiu' directory exists, and create it if not
            if not os.path.exists(work_space + '/article/xueqiu/'):
                os.makedirs(work_space + '/article/xueqiu/')

            txt_filename = work_space + '/article/xueqiu/' + title + '.txt'  # Define the path for the text file
            fp = open(txt_filename, 'w', encoding='utf-8')  # Open the text file for writing
            fp.writelines(text)  # Write the text to the file
            fp.close()  # Close the file
            x.close()  # Close the newly opened window
            count += 1  # Increment the article counter
            x.switch_to.window(windows[0])  # Switch back to the original window
        except:
            windows = x.window_handles  # If an exception occurs, get the window handles
            x.switch_to.window(windows[0])  # Switch back to the original window
            continue
    log_fp.close()  # Close the log file
    print(f'Downloaded {count} articles.')


prev_time = datetime.datetime.now()  # Record the current time
url_xueqiu = r'https://xueqiu.com/'  # URL of the website to be scraped
x = webdriver.Chrome()  # Initialize the Chrome WebDriver
x.get(url_xueqiu)  # Open the website in the browser
load(x, 1000)  # Load 1000 articles
download(x)  # Download the articles
x.quit()  # Close the browser
cur_time = datetime.datetime.now()  # Record the time after scraping
h, remainder = divmod((cur_time - prev_time).seconds, 3600)
m, s = divmod(remainder, 60)
print(f'It costs {h:02d}:{m:02d}:{s:02d}')  # Print the time taken for the process
