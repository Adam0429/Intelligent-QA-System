from gensim.models import word2vec
sentences = word2vec.Text8Corpus(u'corpusSegDone.txt')
model = word2vec.Word2Vec(sentences, min_count=5, size=50)

# y2 = model.similarity(u"好", u"还行")
# print(y2)
print("费用 similarity:")
for i in model.most_similar(u"费用"):
    print(i[0], i[1])
model.save('wordvec.model')