# -*- coding: utf-8 -*-
"""Input text file of sentences

Output format: output term array.
"""

import jieba
import jieba.posseg as pseg

jieba.load_userdict('dictionary/dict.txt.big.txt')
jieba.load_userdict("dictionary/NameDict_Ch_v2")
def PosTokenizer(sentences, save=None, remove=None):
	def notInRemove(flag, List, action):
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
	
	for s in sentences:
		words = pseg.cut(s)
		for word, flag in words:
			if word != '\n':
				if remove != None and InActionList(flag, remove, 'remove') != False:
					result.append(word)
				elif save != None and InActionList(flag, save, 'save'):
					result.append(word)
	return result