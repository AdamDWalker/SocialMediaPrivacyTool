import nltk

with open("Output_Log.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
tweets = [x.strip('\n') for x in content]


#sentence = "@ohhitsonlyalice I've been checking your twitter so much that it comes up before my uni timetable when I type "t" into my browser :')"
#sentence2 = "Also I won £6 on the lottery and managed to socialise too. What even is this day?!?"
#sentence3 = "RT @SuperMickyChow: #c4debate Sheila Hancock gets biggest round of applause for preaching unity and love for a better future."
#tokens = nltk.word_tokenize(sentence)

#tagged = nltk.pos_tag(tokens)

#entities = nltk.chunk.ne_chunk(sentence)
#print (tokens)
#print("\n")
#print(tagged)
for tweet in tweets:
    print(tweet + "\n")
