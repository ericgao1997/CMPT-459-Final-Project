import sys
import json
import os
from pathlib import Path
from spacy.lang.en import English

nlp = English()

def load_Sentiments(file_path):
    word_dict = {}
    with open(file_path) as f:
        for line in f:
            attrs = line.split()
            dict = {}
            for val in attrs:
                temp = val.split('=')
                if len(temp) == 2:
                    dict[temp[0]] = temp[1]

            # Check the strength of the word
            if dict["type"] == "strongsubj":
                strength = 1
            else:
                strength = 0.5

            # Check the polarity (sentiment) of the word
            if dict["priorpolarity"] == "negative":
                strength = strength * -1
            elif dict["priorpolarity"] == "neutral":
                continue

            # put them together
            word_dict[dict["word1"]] = strength
    return word_dict
            
def readTweetJsons(file_path):
    json_list = []
    with open(file_path) as f:
        for line in f:
            json_list.append(json.loads(line))
    return json_list

def compute_sentiment(text, lexicon):
    score = 0
    words = nlp(text)
    for word in words:
        if word.lemma_ in lexicon.keys():
            score += lexicon[word.lemma_]
    return score

def main(argv):
    
    #Load in sentiment dictionary
    sentiment_lexicon = "subjclueslen1-HLTEMNLP05.tff"
    dict = load_Sentiments(sentiment_lexicon)
    #Set up path to loaded tweets
    basePath = "tweet_IDs/Loaded_Tweets/"
    entries = Path(basePath)
    #Deletes old csv to create a new one
    out_file = "cleaned_mask_data.csv"
    if os.path.exists(out_file):
        os.remove(out_file)

    with open(out_file,'a',encoding='utf-8',errors='ignore') as writeFile:
        fileheader = "Date,Sentiment,City,State\n"
        writeFile.write(fileheader)
        for entry in entries.iterdir():
            date = entry.name.split('.')[0]
            print (date)
            readFileName = basePath + entry.name
            raw_tweets = readTweetJsons(readFileName)
            for val in raw_tweets:
                val["score"] = compute_sentiment(val["full_text"],dict)
                try:
                    location = val["place"]['full_name'].split(',')
                    city = location[0]
                    state = location[1]
                except:
                    print (val["place"])
                    continue
                out_line = date + "," + str(val["score"]) + "," + city + "," + state + "\n"
                writeFile.write(out_line)

    # Previous test to load and display info from one day's jsons.
    # test_file = "2020-03-21.json"
    # data = readTweetJsons(test_file)
    # print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # for val in data:
    #     val["score"] = compute_sentiment(val["full_text"],dict)
    #     print (val["full_text"])
    #     print ("score is: ", val["score"])
    #     print (val["place"]['full_name'])
    #     print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return

if __name__ == "__main__":
    main(sys.argv)