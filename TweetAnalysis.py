import nltk
import random
from nltk.sentiment.vader import SentimentIntensityAnalyzer as vaderSentiment

with open("Output_Log.txt") as f:
    tweets = f.read().split('~#~')
# you may also want to remove whitespace characters like `\n` at the end of each line
#tweets = [x.strip('\n') for x in content]
for tweet in tweets:
    tweet.strip('\n')

# Generate a random value so as to print a random tweet as a test sentence
rand = random.randrange(0, len(tweets))

sentence = str(tweets[rand])
# tokens = nltk.word_tokenize(sentence)
# tagged = nltk.pos_tag(tokens)
# entities = nltk.chunk.ne_chunk(tagged)

vs = vaderSentiment()
vsVal = vs.polarity_scores(sentence)

print(sentence + "\n")
print("\t" + str(vsVal))
# print(tokens)
# print("\n")
# print(tagged)
# print("\n")
# print(entities)
