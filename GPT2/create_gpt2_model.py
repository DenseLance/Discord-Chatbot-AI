import re
import os
from csv import DictReader
import gpt_2_simple as gpt2

# Generating file
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

with open(f"{user}_tweets.csv", "r", encoding = "utf8") as f:
    result = list(DictReader(f))
    f.close()

with open(f"{user}_gpt2.txt", "w", encoding = "utf8") as f:
    for item in result:
        tweet = clean_tweet(item["tweet"])
        if tweet:
            f.write("<|startoftext|>" + tweet + "<|endoftext|>")
            f.write("\n")
    f.close()

# Download model
model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
    gpt2.download_gpt2(model_name = model_name)

# Finetune model
sess = gpt2.start_tf_sess()
gpt2.finetune(sess, f"{user}_gpt2.txt", model_name = model_name, restore_from = "fresh", steps = 100) # steps is max number of training steps
