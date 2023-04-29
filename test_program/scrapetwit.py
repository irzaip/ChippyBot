import snscrape.modules.twitter as sntwitter

# Define the keyword you want to search for
keyword = "piring kfc"

# Define the maximum number of tweets you want to scrape
max_tweets = 100

# Define a list to hold the scraped tweets
tweets = []

# Use the SNScrape library to scrape tweets containing the keyword
for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:2010-01-01 until:2023-04-19').get_items()):
    if i >= max_tweets:
        break
    tweets.append(tweet)

# Print out the text of each scraped tweet
for tweet in tweets:
    print(tweet.content)