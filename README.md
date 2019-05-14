写在前面：本文是学习实验楼《Python 基于共现提取<釜山行>人物关系》这一课后的总结，博主仅做了一些微小的改动，大家可以点击[这里](https://www.shiyanlou.com/courses/677)跳转学习。
***
开门见山，先亮结果。我用这种方法制作了《龙族3·黑月之潮(下)》的人物关系网络图，如下图所示：
<div align=center><img src="https://github.com/HuRuixiang/longzu/blob/master/result/result.png?raw=true" width = 40%/></div>

这个图是用Gephi生成的，关于Gephi使用的教程有很多，大家去[这里](https://www.udemy.com/gephi/)学习。
图形可以由软件自动生成，但是数据得需要我们自己准备。要画出这种关系图，我们需要给Gephi输入两种格式的文件，即节点文件和边文件。
+ 节点文件（node.txt），有Id, Label, Weight（节点出现的次数）三个变量，如图所示：
<div align=center><img src="https://github.com/HuRuixiang/longzu/blob/master/resource/node.jpg?raw=true" width = 40%/></div>

+ 边文件（edge.txt），有Source（起点），Target（终端），Weight（该起点-终点的出现次数）三个变量，如图所示：
<div align=center><img src="https://github.com/HuRuixiang/longzu/blob/master/resource/edge.jpg?raw=true" width = 40%></div>
下面我将和大家分享怎么样用Python对文本中的关系进行提取，生成这两个格式的文件。

### 准备
1、安装jieba库，可以在命令行输入以下命令：
```Python
pip install jieba
```
2、安装Gephi，可以点击[这里](https://github.com/HuRuixiang/longzu/blob/master/gephi-0.9.1-windows.exe)下载Gephi-0.9.1-windows。
3、准备待处理的文本，这里以《龙族3·黑月之潮(下)》为例，[点击下载](https://github.com/HuRuixiang/longzu/blob/master/resource/%E9%BE%99%E6%97%8F3%C2%B7%E9%BB%91%E6%9C%88%E4%B9%8B%E6%BD%AE(%E4%B8%8B).txt)。
4、准备姓名字典，可以直接从百度百科上复制粘贴，以下是《龙族》主要角色的姓名字典：
<div align=center><img src="https://github.com/HuRuixiang/longzu/blob/master/resource/dict.jpg?raw=true" width = 40%/></div>

### 导入相关库
```python
import jieba, codecs
```
为什么要用codecs打开文件，而不直接用open打开文件，请看[这里](https://www.cnblogs.com/buptldf/p/4805879.html)。
### 创建字典
+ 使用字典类型names保存人物，该字典的键为人物名称，值为该人物在全文中出现的次数；
+ 使用字典类型relationships保存人物关系的有向边，该字典的键为有向边的起点，值为一个字典edge，edge的键是有向边的终点，值是有向边的权值，代表两个人物之间联系的紧密程度。
+ lineNames是一个缓存变量，保存对每一段分词得到当前段中出现的人物名称，lineName[i]是一个列表，列表中存储第i段中出现过的人物。

```python
names = {}			# 姓名字典
relationships = {}	        # 关系字典
lineNames = []		        # 每段内人物关系
```

### 生成节点文件（node.txt）
```python
jieba.load_userdict("resource\\dict.txt")	        # 加载字典
with open("resource\\dict.txt","r",encoding="utf8") as f:
	nameList = f.readlines()		        # 将角色姓名存入列表nameList
with codecs.open("resource\\龙族3·黑月之潮·下.txt", "r", "utf8") as f:
	for line in f.readlines():
		wordList = jieba.lcut(line)             # 分词并返回一个列表
		lineNames.append([])		        # 为新读入的一段添加该段的人物名称列表
		for w in wordList:	                # 遍历列表
			if w+"\r\n" not in nameList:
				continue	            # 当分词不在姓名列表nameList时认为该词不是人名
			lineNames[-1].append(w)	            # 为当前段的环境增加一个人物
			if names.get(w) is None:            # 如果该人名在姓名字典中对应的权值为空（还没有这个键值对）
				names[w] = 0                # 则创建该键值对，参考实例test1.py
				relationships[w] = {}
			names[w] += 1	                    # 该人物出现次数加 1
```

### 生成边文件（edge.txt）
```python
for line in lineNames:	                    # 对于每一段
	for name1 in line:					
		for name2 in line:	    # 每段中的任意两个人
			if name1 == name2:
				continue
			if relationships[name1].get(name2) is None:	  # 若两人尚未同时出现则新建项
				relationships[name1][name2]= 1
			else:                                             # 两人共同出现次数加 1
				relationships[name1][name2] = relationships[name1][name2]+ 1		
```

### 存储节点文件（node.txt）
```python
with codecs.open("longzu_node.txt", "w", "utf8") as f:
	f.write("Id Label Weight\r\n")
	for name, times in names.items():
		f.write(name + " " + name + " " + str(times) + "\r\n")
```

### 存储边文件（edge.txt）
```python
with codecs.open("longzu_edge.txt", "w", "utf8") as f:
	f.write("Source Target Weight\r\n")
	for name, edges in relationships.items():
		for v, w in edges.items():
			if w > 3:
				f.write(name + " " + v + " " + str(w) + "\r\n")
```