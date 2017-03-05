import nltk

sentence = "This is the test sentence that I have written to try out various things that nltk can do."

tokens = nltk.word_tokenize(sentence)

tagged = nltk.pos_tag(tokens)

#entities = nltk.chunk.ne_chunk(sentence)
print (tokens)
print("\n")
print(tagged)
