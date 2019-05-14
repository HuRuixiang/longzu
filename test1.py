names = {}
if names.get("胡瑞祥") is None:			# 如果该人名在姓名字典中对应的权值为空（还没有这个键）
	names["胡瑞祥"] = 0					# 则创建该键值对
print(names)