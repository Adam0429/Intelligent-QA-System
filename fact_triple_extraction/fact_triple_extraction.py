import codecs   
import re 
from pyltp import SentenceSplitter  
from pyltp import Segmentor  
from pyltp import Postagger  
from pyltp import NamedEntityRecognizer  
  
# news_files = codecs.open('input.txt','r',encoding='utf8')
# news_list = news_files.readlines()
news_list = []
news_list.append(input())
#type(news_list[1].encode('utf-8'))  
  
  
#分句  
''''' 
此函数参数输入的格式必须为str格式，所以直接获取的list里的参数值需要 
通过encode('utf-8')，从Unicode转换为str 
'''  
def sentence_splitter(sentence):  
    sents = SentenceSplitter.split(sentence)  
    # print('\n'.join(sents))  
    sents_list = list(sents)  
    return sents_list  
      
  
#分词     
def segmentor(sentence):  
    segmentor = Segmentor()  
    segmentor.load('/home/wangfeihong/桌面/ltp_data/cws.model')#加载模型  
    words = segmentor.segment(sentence) #分词  
    #默认可以这样输出  
    #print '\t'.join(words)  
    #可以转化成List输出  
    word_list = list(words)  
    segmentor.release()#释放模型  
    return word_list   
  
#词性标注  
def posttagger(words):  
    postagger = Postagger()  
    postagger.load('/home/wangfeihong/桌面/ltp_data/pos.model')  
    posttags=postagger.postag(words)  #词性标注  
    postags = list(posttags)  
    postagger.release() #释放模型  
    #print type(postags)  
    return postags  
  
#命名实体识别  
def ner(words,postags):  
    print('命名实体开始！')  
    recognizer = NamedEntityRecognizer()  
    recognizer.load('/home/wangfeihong/桌面/ltp_data/ner.model') #加载模型  
    netags = recognizer.recognize(words,postags) #命名实体识别  
    for word,ntag in zip(words,netags):  
        print(word+'/'+ ntag)  
    recognizer.release()   #释放模型  
    nerttags = list(netags)  
    return nerttags  
  
#新建一个txt文件保存命名实体识别的结果      
out_file = codecs.open('out_nerfile.txt','w',encoding='utf8')  
sents = sentence_splitter(news_list[0].encode('utf-8'))  
for sent in sents:  
    words=segmentor(sent)  
    tags = posttagger(words)  
    nertags = ner(words,tags)  
    for word,nertag in zip(words,nertags):  
        out_file.write(word+'/'+nertag+' ')  
out_file.close()  

file=codecs.open('out_nerfile.txt','r',encoding='utf8')  
file_content = file.read() 
file_list = file_content.split() 
#创建两个空列表，分别保存命名实体和构成命名实体短语词组的各个词   
ner_list=[]  
phrase_list=[]
word_list=[]
for word in file_list:  
    # if(re.search('Ni$',word)):  
    word_list=word.split('/')
    if re.search(r'^S',word_list[1]):  
        ner_list.append(word_list[0])
        print('提取出的命名实体为：',word_list)
    elif re.search(r'^B',word_list[1]):  
        phrase_list.append(word_list[0]) 
        print('提取出的命名实体为：',word_list)
    elif re.search(r'^I',word_list[1]):  
        phrase_list.append(word_list[0])
        print('提取出的命名实体为：',word_list)
    else:  
        phrase_list.append(word_list[0])  
        # print('提取出的命名实体为：',word_list[0])
        #把list转换为字符串.  
        ner_phrase=''.join(phrase_list)  
        ner_list.append(ner_phrase)   
        phrase_list=[]   
# for ner in ner_list:  
#     print(ner)  