import tweepy
import csv
import re
from collections import Counter
from textblob import TextBlob
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
load_dotenv()


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        
        # Importing keys from .env file
        CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


        # authenticating
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter Keyword/Tag to search about: ")
        NoOfTerms = int(input("Enter how many tweets to search: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang="en").items(NoOfTerms)

        # Open/create a file to append data to
        with open('result.csv', 'a') as csvFile:
            # Use csv writer
            csvWriter = csv.writer(csvFile)

            # iterating through tweets fetched
            for tweet in self.tweets:
                #Append to temp so that we can store in csv later. I use encode UTF-8
                self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
                # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                analysis = TextBlob(tweet.text)
                # print(analysis.sentiment)  # print tweet's polarity
                self.sentiments.append(analysis.sentiment.polarity)

            # Write to csv
            csvWriter.writerow(self.tweetText)

        # calculate sentiment percentages
        sentiment_counts = Counter(
            'strongly positive' if s > 0.6 and s <= 1 else
            'strongly negative' if s >= -1 and s <= -0.6 else
            'positive' if s > 0.3 and s <= 0.6 else
            'weakly positive' if 0.3 >= s > 0 else
            'neutral' if s==0 else
            'weakly negative' if 1 >= s > -0.3 else
            'negative' if 0.6 >= s > -1 else 'other'
            for s in self.sentiments)
        positive = self.percentage(sentiment_counts['positive'], NoOfTerms)
        wpositive = self.percentage(sentiment_counts['weakly positive'], NoOfTerms)
        negative = self.percentage(sentiment_counts['negative'], NoOfTerms)
        wnegative = self.percentage(sentiment_counts['weakly negative'], NoOfTerms)
        spositive = self.percentage(sentiment_counts['strongly positive'], NoOfTerms)
        snegative = self.percentage(sentiment_counts['strongly negative'], NoOfTerms)
        neutral = self.percentage(sentiment_counts['neutral'], NoOfTerms)
        # finding average reaction
        polarity = sum(self.sentiments) / NoOfTerms

        # printing out data
        print(f"How people are reacting on {searchTerm} by analyzing {NoOfTerms} tweets.")
        print()
        print("General Report: ")

        if polarity == 0:
            print("Neutral")
        elif polarity > 0 and polarity <= 0.3:
            print("Weakly Positive")
        elif polarity > 0.3 and polarity <= 0.6:
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()
