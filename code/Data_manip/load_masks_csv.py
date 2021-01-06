import sys
import json
import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as dts

def read_cleaned_masks(path):
    tweetlist = []
    with open(path,errors='ignore') as readFile:
        headers = readFile.readline().split(',')
        for line in readFile:
            unlabeled = line.split(',')
            temp_dict = {}
            for num in range(len(headers)):
                temp_dict[headers[num]] = unlabeled[num]
            tweetlist.append(temp_dict)
    return tweetlist

def by_date(tweets):
    list = []
    datelist = []
    accum = 0.0
    size = 1
    last = ""
    for tweet in tweets:
        if not last == tweet["Date"]:
            last = tweet["Date"]
            datelist.append(dts.datestr2num(last))
            list.append(accum/size)
            accum = 0
            size = 1
        else:
            if float(tweet["Sentiment"]) != 0:
                size += 1
            accum += float(tweet["Sentiment"])
    return list, datelist

def main(argv):
    mask_tweets = "cleaned_mask_tweets.csv"
    tweets = read_cleaned_masks(mask_tweets)
    feel_by_date,list_dates = by_date(tweets)

    plt.plot_date(list_dates,feel_by_date,xdate=True)
    plt.ylabel('overall sentiment')
    plt.xlabel('dates')
    plt.show()

    return

if __name__ == "__main__":
    main(sys.argv)