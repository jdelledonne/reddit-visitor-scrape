#!/usr/bin/env python3

## visitorScrape.py
# Author: Joe Delle Donne
# Date: 07/04/2019

## import libraries
import requests
import os
import sys
import pprint
import re
import time
import matplotlib.pyplot as plt
import numpy

## Global variables

SUBREDDIT = "TruePenguins"      # Default Subreddit to be tracked
RATE      = 1                   # Rate in seconds at which the online user info will be tracked
DURATION  = 10                  # Duration in seconds that the subreddit will be tracked

## Main execution

def main():
    url = parse_command_line()
    users = track_users(url)
    print(users)
    plot_users(users)

## Functions
def usage(status = 0):
    print('''Usage: {} [options] URL_OR_SUBREDDIT
    
    -r      Change the rate (in seconds) at which user data will be extracted (default 1s)
    -d      Change the duration (in seconds) that the program will collect data (default 10s)
    '''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)

def parse_command_line():
    args = sys.argv[1:]
    if not args:
        print(args)
        usage(1)

    global RATE 
    global DURATION

    while len(args) and args[0].startswith('-') and len(args[0]) > 1:
        arg = args.pop(0)
        if arg == '-h':
            usage(0)
        elif arg == '-r':
            RATE = float(args.pop(0))
        elif arg == '-d':
            DURATION = int(args.pop(0))
        else:
            usage(1)

    global SUBREDDIT
    SUBREDDIT = args.pop(0)

    if SUBREDDIT.startswith('https://'):
        url = SUBREDDIT
    else:
        url = 'https://www.reddit.com/r/{}/'.format(SUBREDDIT)

    return url

def load_page_data(URL):
    headers  = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp19'))}
    response = requests.get(URL, headers=headers)
    return response.text

def parse_online_users(data):
    match = re.findall(">([0-9|.|k|m]+)<.*Online",data)
    return match

def track_users(url):
    total_time = 0
    users = []

    while total_time < DURATION:
        print('Total time: {}, Duration: {}'.format(total_time,DURATION))
        data = load_page_data(url)
        user_num = parse_online_users(data)[0]
        if user_num[-1] == 'k': # if the number is in the thousands, convert to a number
            user_num = float(user_num[0:len(user_num)-1])*1000
        users.append(float(user_num))
        total_time = total_time + RATE
        time.sleep(RATE)

    return users

def plot_users(users):
    plt.plot(numpy.linspace(1,DURATION,DURATION/RATE),users,'ro')
    plt.title("r/{} Users Graph".format(SUBREDDIT))
    plt.xlabel("Time (s)")
    plt.ylabel("Users")
    plt.show()
    pass

if __name__ == '__main__':
    main()

