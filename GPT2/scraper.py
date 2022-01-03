import twint

user = "scba"

c = twint.Config()
c.Username = user
c.Lang = "en"

# Settings
c.Filter_retweets = True # remove retweets
c.Hide_output = True

# Save to results
c.Custom["tweet"] = ["tweet"]
c.Output = f"{user}_tweets.csv"
c.Store_csv = True

twint.run.Search(c)
