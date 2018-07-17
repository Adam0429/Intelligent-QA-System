from gensim.models import word2vec
sentences = word2vec.Text8Corpus(u'分词后的爽肤水评论.txt')
model = word2vec.Word2Vec(sentences, size=50)

# y2 = model.similarity(u"好", u"还行")
# print(y2)

for i in model.most_similar(u"滋润"):
    print i[0], i[1]
