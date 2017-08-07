#importing dependencies

from textblob import TextBlob
import sys,tweepy


# function to calculate percentage
def percentage(part, whole):
  return 100 * float(part)/float(whole)



#BMP mapping
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


#authenticating
consumerKey = ''
consumerSecret = ''
accessToken = ''
accessTokenSecret = '' 
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


#input for term to be searched and how many tweets to search
searchTerm = input("Enter Keyword/Tag to search about: ")
NoOfTerms = int(input("Enter how many tweets to search: "))


#searching for tweets
tweets = tweepy.Cursor(api.search, q=searchTerm).items(NoOfTerms)


#creating some variables to store info
polarity = 0
positive = 0
wpositive = 0
spositive = 0
negative = 0
wnegative = 0
snegative = 0
neutral = 0


#iterating through tweets
for tweet in tweets:
   #print (tweet.text.translate(non_bmp_map))    #print tweet's text
   analysis = TextBlob(tweet.text)
   #print(analysis.sentiment)    #print tweet's polarity
   polarity+=analysis.sentiment.polarity    #adding up polarities to find the average later
        
   if (analysis.sentiment.polarity==0):     #adding reaction of how people are reacting to find average later
       neutral+=1
   elif (analysis.sentiment.polarity>0 and analysis.sentiment.polarity<=0.3):
       wpositive+=1
   elif (analysis.sentiment.polarity>0.3 and analysis.sentiment.polarity<=0.6):
       positive+=1
   elif (analysis.sentiment.polarity>0.6 and analysis.sentiment.polarity<=1):
       spositive+=1
   elif (analysis.sentiment.polarity>-0.3 and analysis.sentiment.polarity<=0):
       wnegative+=1
   elif (analysis.sentiment.polarity>-0.6 and analysis.sentiment.polarity<=-0.3):
       negative+=1
   elif (analysis.sentiment.polarity>-1 and analysis.sentiment.polarity<=-0.6):
       snegative+=1    



#finding average of how people are reacting
positive = percentage(positive, NoOfTerms)
wpositive = percentage(wpositive, NoOfTerms)
spositive = percentage(spositive, NoOfTerms)
negative = percentage(negative, NoOfTerms)
wnegative = percentage(wnegative, NoOfTerms)
snegative = percentage(snegative, NoOfTerms)
neutral = percentage(neutral, NoOfTerms)


#finding average reaction
polarity = polarity/NoOfTerms


#printing out data
print("How people are reacting on "+searchTerm+" by analyzing "+str(NoOfTerms)+" tweets.")
print()
print("General Report: ")

if (polarity==0):
    print("Neutral")
elif (polarity>0 and polarity<=0.3):
    print("Weakly Positive")
elif (polarity>0.3 and polarity<=0.6):
    print("Positive")
elif (polarity>0.6 and polarity<=1):
    print("Strongly Positive")
elif (polarity>-0.3 and polarity<=0):
    print("Weakly Negative")
elif (polarity>-0.6 and polarity<=-0.3):
    print("Negative")
elif (polarity>-1 and polarity<=-0.6):
    print("Strongly Negative")    


print()
print("Detailed Report: ")
print( str(positive) + "% people thought it was positive")
print( str(wpositive) + "% people thought it was weakly positive")
print( str(spositive) + "% people thought it was strongly positive")
print( str(negative) + "% people thought it was negative")
print( str(wnegative) + "% people thought it was weakly negative")
print( str(snegative) + "% people thought it was strongly negative")
print( str(neutral) + "% people thought it was neutral")

    
