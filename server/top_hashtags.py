from config import *
from twitter import *
from collections import Counter
import re

class TopHashtags:
    def __init__(self):
        self.master_counts = Counter()
        auth = OAuth(
                consumer_key=API_KEY,
                consumer_secret=API_SECRET,
                token=ACCESS_TOKEN,
                token_secret=ACCESS_TOKEN_SECRET)
        self.twitter_stream = TwitterStream(auth=auth)

    def extract_hashtags(self, sentence):
        return re.findall(r"#\w+", sentence)

    def word_freq(self, tweet):
        sentence = tweet.lower()
        words = self.extract_hashtags(sentence)
        freq = Counter()
        for word in words:
            freq[word] += 1
        return freq

    def get_top_n(self, n):
        return self.master_counts.most_common(n)

    def process(self, tweet):
        if tweet.has_key('lang') and tweet.has_key('text'):
            if tweet['lang'] == 'en':
                text = tweet['text']
                wf = self.word_freq(text)
                self.master_counts.update(wf)

    def start(self):
        iterator = self.twitter_stream.statuses.sample()
        for tweet in iterator:
            self.process(tweet)

def main():
    TopHashtags().start()

if __name__ == '__main__':
    main()
