import json
from csv import DictReader
import markovify
import re

user = "scba"

def clean_tweet(tweet):
    # Convert to ASCII
    tweet = tweet.encode("ascii", errors = "ignore").decode()
    
    # Do not add new line
    tweet = re.sub("\n", " ", tweet)

    # Ampersand escape (HTML)
    tweet = re.sub("&nbsp;", " ", tweet)
    tweet = re.sub("&lt;", "<", tweet)
    tweet = re.sub("&gt;", ">", tweet)
    tweet = re.sub("&amp;", "&", tweet)
    tweet = re.sub("&quot;", '"', tweet)
    tweet = re.sub("&apos;", "'", tweet)
    tweet = re.sub("&cent;", "¢", tweet)
    tweet = re.sub("&pound;", "£", tweet)
    tweet = re.sub("&yen;", "¥", tweet)
    tweet = re.sub("&euro;", "€", tweet)
    tweet = re.sub("&copy;", "©", tweet)
    tweet = re.sub("&reg;", "®", tweet)

    # Convert to list for deep cleaning
    tweet = tweet.split(" ")
    
    # Remove mentions if they are at start of the tweet (this would mean it is a reply)
    while tweet and tweet[0] and tweet[0][0] == "@":
        tweet.pop(0)

    # Remove . if they are at start of the tweet (most users use . to avoid making the tweet a reply)
    if tweet and tweet[0] and tweet[0][0] == ".":
        tweet[0] = tweet[0][1:]

    # Remove # if it is hashtag (ignore cashtags, since it could also be dollar sign)
    tweet = [re.sub("#", "", word) if len(word) > 1 and word[0] == "#" else word for word in tweet]

    # Remove @ if it is mention
    tweet = [re.sub("@", "", word) if len(word) > 1 and word[0] == "@" else word for word in tweet]
    
    # Remove empty word
    tweet = [word for word in tweet if word != ""]

    # Remove links (if link is in middle of tweet, we will not use this tweet for NLP, since sentences will be broken)
    while tweet and tweet[-1][:4] == "http":
        tweet.pop()
    
    for word in tweet:
        if word[:4] == "http":
            tweet = []
            break

    # Make first letter capitalised
    if tweet:
        tweet[0] = tweet[0][0].upper() + tweet[0][1:]

    # Convert back to string
    tweet = " ".join(tweet)
    
    return tweet

# Using a naive model
text_model = None
with open(f"{user}_tweets.csv", "r", encoding = "utf8") as f:
    result = list(DictReader(f))
    for item in result:
        tweet = clean_tweet(item["tweet"])
        if tweet:
            if text_model:
                text_model = markovify.combine(models = [text_model, markovify.Text(tweet, retain_original = False, well_formed = False)])
            else:
                text_model = markovify.Text(tweet, retain_original = False, well_formed = False)
    f.close()

with open(f"{user}_model.json", "w") as f:
    f.write(json.dumps(text_model.to_json()))
    f.close()
