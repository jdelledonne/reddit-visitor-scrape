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

## Global variables

SUBREDDIT = "TruePenguins"

## Main execution

def main():
    url = parse_command_line()
    data = load_page_data(url)
    matches = parse_online_num(data)
    print("Subreddit: {}\nCurrent Visitors: {}".format(SUBREDDIT,matches[0]))

## Functions
def usage(status = 0):
    print('''Usage: {} [options] URL_OR_SUBREDDIT'''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)

def parse_command_line():
    args = sys.argv[1:]
    if not args:
        print(args)
        usage(1)

    while len(args) and args[0].startswith('-') and len(args[0]) > 1:
        arg = args.pop(0)
        if arg == '-h':
            usage(0)
        else:
            usage(1)

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

def parse_online_num(data):
    match = re.findall(">([0-9]+)<.*Online",data)
    return match

if __name__ == '__main__':
    main()

