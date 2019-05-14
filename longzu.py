import jieba, codecs
#为什么要用codecs打开文件，看这里：https://www.cnblogs.com/buptldf/p/4805879.html

names = {}					# 姓名字典
relationships = {}			# 关系字典
lineNames = []				# 每段内人物关系

# count names
jieba.load_userdict("resource\\dict.txt")		# 加载字典
with codecs.open("resource\\dict.txt","r",encoding="utf8") as f:
	nameList = f.readlines()					# 将角色姓名存入列表nameList
with codecs.open("resource\\龙族3·黑月之潮·下.txt", "r", "utf8") as f:
	for line in f.readlines():
		wordList = jieba.lcut(line)				# 分词并返回一个列表
		lineNames.append([])					# 为新读入的一段添加该段的人物名称列表
		for w in wordList:						# 遍历列表
			if w+"\r\n" not in nameList:
				continue						# 当分词不在姓名列表nameList时认为该词不是人名
			lineNames[-1].append(w)				# 为当前段的环境增加一个人物
			if names.get(w) is None:			# 如果该人名在姓名字典中对应的权值为空（还没有这个键值对）
				names[w] = 0					# 则创建该键值对，参考实例test1.py
				relationships[w] = {}
			names[w] += 1						# 该人物出现次数加 1

# explore relationships
for line in lineNames:							# 对于每一段
	for name1 in line:					
		for name2 in line:						# 每段中的任意两个人
			if name1 == name2:
				continue
			if relationships[name1].get(name2) is None:		# 若两人尚未同时出现则新建项
				relationships[name1][name2]= 1
			else:
				relationships[name1][name2] = relationships[name1][name2]+ 1		# 两人共同出现次数加 1

# # output
with codecs.open("longzu_node.txt", "w", "utf8") as f:
	f.write("Id Label Weight\r\n")
	for name, times in names.items():
		f.write(name + " " + name + " " + str(times) + "\r\n")

with codecs.open("longzu_edge.txt", "w", "utf8") as f:
	f.write("Source Target Weight\r\n")
	for name, edges in relationships.items():
		for v, w in edges.items():
			if w > 3:
				f.write(name + " " + v + " " + str(w) + "\r\n")