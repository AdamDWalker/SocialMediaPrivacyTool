import nltk
import random

with open("Output_Log.txt") as f:
    tweets = f.read().split('~#~')
# you may also want to remove whitespace characters like `\n` at the end of each line
#tweets = [x.strip('\n') for x in content]
for tweet in tweets:
    tweet.strip('\n')

rand = random.randrange(0, len(tweets))
print(rand)
#tokens = nltk.word_tokenize(sentence)

#tagged = nltk.pos_tag(tokens)

#entities = nltk.chunk.ne_chunk(sentence)
#print (tokens)
#print("\n")
#print(tagged)
for tweet in tweets:
    print(tweets[rand] + "\n")
