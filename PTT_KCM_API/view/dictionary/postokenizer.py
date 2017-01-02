# -*- coding: utf-8 -*-
"""Input text file of sentences

Output format: output term array.
"""

import jieba
import jieba.posseg as pseg

jieba.load_userdict('dict.txt.big.txt')
jieba.load_userdict("NameDict_Ch_v2")
def PosTokenizer(sentences, save=None, remove=None):
	def InActionList(flag, List, action):
		determine = True
		if action == 'remove':
			determine != determine
		for i in List:
			if i in flag:
				return determine
		return not determine

	result = []
	if save != None and remove != None:
		raise ("cannot use save and remove at once.")
	
	words = pseg.cut(sentences)
	for word, flag in words:
		print(word)
		if word != '\n':
			if remove != None and InActionList(flag, remove, 'remove') != False:
				result.append(word)
			elif save != None and InActionList(flag, save, 'save'):
				result.append(word)
	return result