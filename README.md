# Intelligent-QA-System
the knowledge base management base on NLP

智能问答系统分为两部分，一是知识库的构建（建立问题到答案的关系），建议问题的生成以方便后台增删查改。二是推理机，知识推理运用建立在知识库所存储的知识的基础之上的,不同的知识表达方式在一定程度上决定了特定的知识运用方式。

### 直至比完赛

反思这比赛，我刚意识到比赛目的是从文本中生成问题。而我只写了一个爬虫，做了分割操作。将面包屑式的导航作为问题（自以为很对），但实际上是要从文本的陈述句中生成问题。一开始想法是对的，但逐步走偏。过于注重了推理机这部分，没有搞清赛题的主要目的。

赛题给了3个选择，规则，NLP，机器学习。

规则首先排除，肯定是列举不全。

选用NLP的话可以用哈工大的实体提取。

机器学习，主要是没有精力去做，没有数据，没有标注的时间。

等有了炼丹的经验再来完善这个项目

### 知识库

知识库传统的做法是三元组，但这个项目并不需要这样做，仅做笔记
知识字典 D 可用三元组表示如下:
D = ( O , T , E )
把三元组理解为 (实体entity,实体关系relation,实体entity)，把实体看作是结点，把实体关系（包括属性，类别等等）看作是一条边，那么包含了大量三元组的知识库就成为了一个庞大的知识图。

知识库涉及到的两大关键技术是

实体链指(Entity linking) ，即将文档中的实体名字链接到知识库中特定的实体上。它主要涉及自然语言处理领域的两个经典问题实体识别 (Entity Recognition) 与实体消歧 (Entity Disambiguation)，简单地来说，就是要从文档中识别出人名、地名、机构名、电影等命名实体。并且，在不同环境下同一实体名称可能存在歧义，如苹果，我们需要根据上下文环境进行消歧。
关系抽取 (Relation extraction)，即将文档中的实体关系抽取出来，主要涉及到的技术有词性标注 (Part-of-Speech tagging, POS)，语法分析，依存关系树 (dependency tree) 以及构建SVM、最大熵模型等分类器进行关系分类等。

理想的联合学习应该如下图：输入一个句子，通过实体识别和关系抽取联合模型，直接得到有关系的实体三元组。这种可以克服上面流水线方法的缺点，但是可能会有更复杂的结构。参考:https://zhuanlan.zhihu.com/p/31672529

实体提取用哈工大的库pyltp(可以用CTB模型重新做分词模型)，导入官方模型即可，也可以导入自己的

关系提取转换为分类问题，这个我在推理机里已经做了



文档结构树：做法不同于传统的文档结构树，由于数据集是网页，层次结构分明而答案并不需要经过NLP分析得到，只需要得到某一段落的文字。这样按标签提取即可，如h标签的通常是标题重要信息。原想用h标签做问题，答案用它的兄弟节点，可是网页层次不统一，情况复杂。并不适合用这种算法。所以自行做了创新：得到所有h标签，取两两中间的部分作为答案，准确率高
利用文档结构树从问题映射到答案。

数据库：

标准问题：通过规则组合关键词生成（基于文档结构树技术）

答案：带网页标签的答案

描述词：此数据的描述，由网页中提取出

问题词组：通过分词（全模式分词算法）和去除停用词等步骤得到的词组。用于计算文本相似度。

答案词组：通过分词（全模式分词算法）和去除停用词等步骤得到的词组。用于计算文本相似度。

感觉标准答案只是给评委看，并不是作为问题检索的最重要的方式。暂时先这样做，准确度和效率不行就只用结构。因为问句很难匹配，而结构只需词对上即可



### QA对自动生成

### 目前仅实现对大标题的问题生成，由于每个每个页面不止有一个问题，所以要结合问题标签生成

目前打算先使用基本的NLP和规则来自动生成问题。[PYLTP](https://github.com/HIT-SCIR/pyltp)是哈工大的一个开源中文文本处理python库，我们目前需要用到其中的中文分词和中文词性标注功能。我们目前只对页面进行问题自动生成处理，使用华为云帮助中心每个页面顶部的结构说明（多个标签）为每个页面生成单个问题。

处理方法为：

#### 分标签

这一步可能在spider.py中已经处理了。

#### 筛除对问题生成无用的标签

有些标签对问题生成美元意义，例如第一个永远是“帮助中心”。

另外如“概览”，“FAQ”这样的文字不太可能出现在问题中。

#### 使用PYLTP的分词和词性标注

需要引用PYLTP库和下载模型。

```python
#分词
def segmentor(sentence=''):
    segmentor = Segmentor()  # 初始化实例
    segmentor.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/cws.model')  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    # 可以转换成List 输出
    words_list = list(words)
    segmentor.release()  # 释放模型
    return words_list

#获取分词后词性
def posttagger(words):
    postagger = Postagger() # 初始化实例
    postagger.load('/Users/zhangqinyuan/Downloads/ltp_data_v3.4.0/pos.model')  # 加载模型
    postags = postagger.postag(words)  # 词性标注
#   for word,tag in zip(words,postags):
#       print (word+'/'+tag)
    postags_list = list(postags)
    postagger.release()  # 释放模型
    return postags_list
```

#### 生成问题

这一步最为重要，基于规则我们目前考虑了以下几种情况：

一、假如只有一个有用标签或最后一个标签包含“简介”，则直接使用“什么是… …？”来生成问题。如：“帮助中心 > 机器学习服务”。

二、假如最后一个标签的开头是疑问词，则不需要生成问题。如：“帮助中心 > 机器学习服务 > 什么是机器学习服务”。

三、假如最后一个标签是“概述”或者“产品概述”，则用第一个标签和倒数第二个标签生成问题。如：“帮助中心 > 机器学习服务 > 产品介绍 > 产品概述”。

四、假如最后一个标签在例外情况（动词做定语开头）之中，则用“… …有哪些？”生成问题。如：“帮助中心 > 机器学习服务 > 使用限制”。

五、假如最后一个标签的最后一个词为管理，则用“怎么管理… …?”生成问题。如：“帮助中心 > 云容器引擎 > 用户指南 > 操作指南 > 存储管理”。

六、假如最后一个标签以动词开头，使用“怎么… …”来生成问题。如：“帮助中心 > 镜像服务 > 用户指南 > 管理 > 共享镜像”。

七、假如最后一个标签为"与... ..."，使用第一个标签和最后一个标签形成问句。如：“帮助中心 > 镜像服务 > 用户指南 > 管理 > 与容器的关系”

八、假如最后一个标签以动词、形容词开头，使用“… …有哪些”来生成。如：“帮助中心 > 镜像服务 > 用户指南 > 管理”。

目前存在这几种问题有待解决：

一、仍然有些动词做定语开头的标签没有添加进情况四中。

二、有些标签以名词、形容词开头但是不能用“… ...有哪些”来问。如“可视化”，“场景说明”。解决方法有待研究。

三、某些标签以其他词开头，如英文。解决方法有待研究。



### 推理机

关键词+关键字匹配
如果不能通过用户问题的关键词找到描述词，就用关键词中的字取匹配描述词

推理机针对当前问题的条件或已知信息，反复匹配知识库中的规则，获得新的结论，以得到问题求解结果。

创新在于:我会个每条问题对加上一个权重值，用来处理难以选择的情况，高权重值的答案更容易被选择。使用次数越多，知识库越准确。暂时不知道这个值应该在什么情况下增加？？？？


       	   	=== 问题分类
       		|           
     问题分析  ---    === 主题提取
    		|
    		=== 关键词提取
            
首先要做的就是理解用户的问题，首先就要分词，对每个词进行分析
词库需要自己用大量相关文档构建，文档越多，相关度越大，分词正确率越高，但仍不能保证100%的正确率。
做完分词和词性标注后。对问题进行分析。
分词是最重要的一步。词库应该尽可能贴合知识库的方向。
比如“云服务器是什么？”
用普通词库分出的关键词是 云 和 服务器 
而我们想要的是“云服务器”这整个词，分错会影响后来的匹配，所以应采用相关的词库
现在的想法是直接从每个网页中提出描述，将描述的词加进词库，并把词频设为3，因为过大的次频会影响TF-IDF算法提取关键词，过小的词频又不能被分出。

问题分类是问句理解的必须步骤。

问题分类分为两种
1.基于规则的：
根据词性标注的结果，判断各种词序的顺序，句法
2.基于统计的：
用机器学习训练模型
暂时不知道两种效果如何，计划都做

在这里，最重要的是关键词提取，需要用来匹配知识库
问句分类也是用来匹配知识库。但知识库的问题暂时没做分类处理，后期做



### 前端
由于我数据库的答案是带标签存的，前端返回答案时可以直接呈现网页原本的效果，包括li,table...

关键词提取:
1.可以用jieba库：
https://www.cnblogs.com/zhbzz2007/p/6177832.html
1) 基于TF-IDF算法进行关键词抽取：
TF-IDF的主要思想就是：如果某个词在一篇文档中出现的频率高，也即TF高；并且在语料库中其他文档中很少出现，即DF的低，也即IDF高，则认为这个词具有很好的类别区分能力。TF-IDF在实际中主要是将二者相乘
2) 基于TextRank算法进行关键词抽取

经过实验发现jieba库的词库不满足大部分的关键词提取，因为词库中没有收录相关的词

### 这是已经做完的事情，但是帮助不大

1.词库进一步细分,是否有必要统计词频?

2.数据库改进（去重）是否有必要每个页面全部存进一条数据用于不精确的查询（done）

3.推理机多条结果处理（返回最短，词条最少）=》》改为返回三条最高分

4.人工标注（训练问题实现）

5.前端+实现点击链接查询（done）

6.后端（done）

7.如果用户输入过少自动加上是什么。

8.最先用数据库搜索，得到数据集。再用bm25搜标题，相似度匹配过低再用bm25搜答案（相似度过低需探索）
答案相似度还是很低该怎么办》。。

9.测试（生成各种问法的问题去改）最后用召回率和准确度

10.每次分析问句先返回疑	问词，返回的步骤是：先有个中文疑问词表直接判断这句话里面是否存在疑问词（多少钱这类的），如果没有可能是以另一种方式问（服务器的价格）

这样就需要用到句法分析，比如主谓宾的句法，就提取宾语作为疑问词，还有其他句法需要总结。判断完以后得到疑问词近义词数组。每个近义词在数据库中搜一遍。搜到了数量
最多的证明作者是用这种问法（疑问词）去问这类的问题。再将疑问词返回给到关键词词组去检索。

11.bm25模型对问题和答案同时进行检索，赋予问题和答案不同的权重组合给分。（必做）

12.去除无用词 如服务 影响搜索 初审测试时就因为 服务这个词 干扰了正确选项（必做）

13.bm25里参数应当有所改变,比如idf就没有必要了, 如: 云硬盘虽然出现的次数过多,但是作为索引词很重要.答案里出现的次数也不该影响到打分.
知识库不像常规的文档,td-idf并不能影响这些打分	

14.改词典,不用最大分词法了,因为会影响我corpus里的分词,这样用户输半个词就没法加上分.改完全模式分词,把所有能分的全分出来

有关机器学习:

第一次想法是:每次分析问句先返回疑问词，返回的步骤是：先有个中文疑问词表直接判断这句话里面是否存在疑问词（多少钱这类的），如果没有可能是以另一种方式问（服务器的价格）

这样就需要用到句法分析，比如主谓宾的句法，就提取宾语作为疑问词，还有其他句法需要总结。判断完以后得到疑问词近义词数组。每个近义词在数据库中搜一遍。搜到了数量

最多的证明作者是用这种问法（疑问词）去问这类的问题。再将疑问词返回给到关键词词组去检索。

后来觉得首先需要枚举各类疑问词实在太low也不够科学,进而更新第二次想法:

用训练好的模型去标注数据库里各条答案.在用户输入时提出关键词,鉴别这条问句的类型,从检索检索结果中匹配类型相同的数据,进行返回.

(这样做的缺点是我数据库里存的问题并不是完整的问句 for exm:帮助中心-Anti-DDoS流量清洗-接口参考-告警提醒API接口-查询告警配置信息-功能介绍

如果拿这样的数据去训练模型,我不确定能做出有用的模型

帮助中心-云专线-常见问题-云专线使用方式有几种?-云专线使用方式有几种?

对于这类问法,既可以属于定义又可以属于数量的标为数量

对于先判断问句类型的做法,如果用户问云专线的使用方式,先归类就变为定义,从而找不到这个答案

解决办法是先拿关键词去搜,搜出多少个以上再用归类归,少数部分就不用归类了



