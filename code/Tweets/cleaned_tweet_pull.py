import tweepy
import sys
import json
import os
from pathlib import Path

CONSUMER_KEY = 'N20SiHZ6nu4dphztRG1DRT2Wi'
CONSUMER_SECRET = 'j5wl8QDdOviwNd7qWiKEJN1Qi6VWIpf7CFnn5RHI5ykkqZeLMA'
ACCESS_TOKEN = '1264938804798017537-IzOlq69QRuBtH9ukNBJcAaSBCQgr4p'
ACCESS_TOKEN_SECRET = 'QeIxjAfdlIejQQkNciQmC13Y8ncBmayo4HQqT6YISblPV'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#[tweet_ID,date,time,lang,country_code ]
def load_tweet(tweetRow):
    if tweetRow[3] == "en" and tweetRow[4] == "US":
        print ("maybe")
        print (tweetRow)
        try:
            tweet = api.get_status(tweetRow[0], tweet_mode = "extended")
        except:
            return False
        if "mask" in tweet.full_text.lower():
            return tweet
        elif "masks" in tweet.full_text.lower():
            return tweet
        return False
    else:
        return False

def main(argv):
    if len(argv) < 2:
        print("no directory/file indicated")
        return
    try: 
        # os.makedirs(argv[1])
        entries = Path(argv[1])
        base = argv[1]
    except:
        return
    outfolder = "Loaded_Tweets/"
    
    startflag = False
    for entry in entries.iterdir():
        if ".tsv" in entry.name:
            fileName = base+"/"+entry.name

            writefolder = base + "/" + outfolder 

            if not os.path.exists(writefolder):
                os.makedirs(writefolder)
            print (fileName)
            with open(fileName,'r') as in_file:
                for line in in_file:
                    seperated = line.replace("\n","").split("\t")

                    if seperated[0] == "1275263067513925637": # << ID TO CONTINUE IF PULL IS INTERUPPTED MIDWAY
                        startflag = True
                    if startflag == False:
                        continue

                    l_tweet = load_tweet(seperated)
                    if l_tweet == False:
                        continue
                    outfile = writefolder + seperated[1] + ".json"
                    with open(outfile,'a') as writeFile:
                        outtext = json.dumps(l_tweet._json).replace("\n","") + "\n"
                        writeFile.write(outtext)
                    print("success")


                # with open(writefolder+"/"+day.name,'a') as out_file:
                #     for twit_id in in_file:
                #         newTweet = load_tweet(twit_id)
                #         if newTweet == False:
                #             print ("fail")
                #             continue
                #         print ("success")
                #         out_file.write(json.dumps(newTweet._json))
if __name__=="__main__":
    main(sys.argv)