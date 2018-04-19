import pymysql
import math
import pickle
from tqdm import tqdm
import re
import jieba.posseg as pseg
import codecs

allvectors = {}
vectors = {} # key is docid, value is dictionary (key is term, value is 1/0 weight)
lengths = {} # key is docid, value is vector length

def del_tag(strings):
    dr = re.compile(r'<[^>]+>',re.S)
    if type(strings) == type([]): 
        strs = []
        for string in strings:
            string = str(string)
            s = dr.sub('',string)
            strs.append(s)
        return strs
    else:
        strings= str(strings)
        s = dr.sub('',strings)
        return s

# db = pymysql.connect("localhost","root","970429","test",charset="utf8mb4")
# cursor = db.cursor()
# cursor.execute('select answer from QA')
# result = cursor.fetchall()

# stop_flag = ['x', 'c', 'u','d', 'p', 't', 'uj', 'm', 'f', 'r']
# def tokenization(text):
#     result = []
#     words = pseg.cut(text)
#     for word, flag in words:
#         if flag not in stop_flag:
#             result.append(word)
#     return result

# corpus = []

# for r in tqdm(result):
#     text = del_tag(r)
#     terms = tokenization(text)
#     corpus.append(terms)


# i = 0

# for sentence in corpus:
# 	i = i + 1
# 	docdict = {}
# 	length = 0 
# 	for word in sentence:
# 		if word not in allvectors.keys():
# 			allvectors[word] = 1
# 		else:
# 			allvectors[word] = allvectors[word] + 1
# 		if word not in docdict.keys():
# 			docdict[word] = 1
# 		else:
# 			docdict[word] = docdict[word] + 1
# 		length = length + 1
# 	vectors[i] = docdict
# 	lengths[i] = math.sqrt(length)



# model = []
# model.append(vectors)
# model.append(lengths)
# model.append(allvectors)

# output = open('VSM.model', 'wb')
# pickle.dump(model,output)

f = open("VSM.model","rb")
bin_data = f.read()
model = pickle.loads(bin_data)
vectors = model[0]
lengths = model[1]
allvectors = model[2]

query = ['开发者工具中心','大数据工具']
query_vector = {}
query_length = 0
for term in query:
	if term not in query_vector.keys():
		query_vector[term] = 1
	else:
		query_vector[term] = query_vector[term] + 1
	query_length = query_length + 1
query_length = math.sqrt(query_length)

sims = {} # key is docid, value is similarity to query
for idx,vector in vectors.items():
	sim = 0
	# numerator of cosine function
	for term in query_vector:
		if term in vector:
			tf_v = vector[term]/allvectors[term]
			idf_v = math.log10(allvectors[term]/vector[term])
			tf_q = query_vector[term]/allvectors[term]
			idf_q = math.log10(allvectors[term]/query_vector[term])
			sim += (tf_v-idf_v) * (tf_q-idf_q)
	if lengths[idx] == 0:
		# print(vectors[idx])
		sim = 0
	else:
		sim /= lengths[idx] * query_length # divide by product of vector lengths
	sims[idx] = sim # add similarity score

#之前用cmath 的时候，会出现科学计数法，导致不能排序，报错为TypeError: unorderable types: complex() < complex()
for did in sorted( sims, key=sims.get, reverse=True )[:10]:
	print( '{}: {}'.format( did, sims[did], ) )
