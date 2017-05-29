# -*- coding: utf-8 -*-
"""Input text file of sentences

Output format: output term array.
"""

import jieba
import jieba.posseg as pseg

stopwords = json.load(open('PTT_KCM_API/view/stopwords/stopwords.json'), 'r')
jieba.load_userdict('PTT_KCM_API/view/dictionary/dict.txt.big.txt')
jieba.load_userdict("PTT_KCM_API/view/dictionary/NameDict_Ch_v2")
jieba.load_userdict("PTT_KCM_API/view/dictionary/鄉民擴充辭典.txt")
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
		if word != '\n':
			if remove != None and InActionList(flag, remove, 'remove') != False:
				result.append(word)
			elif save != None and InActionList(flag, save, 'save'):
				result.append(word)
	return result

def CutAndrmStopWords(sentence):
    def condition(x):
        x = list(x)
        word, flag = x[0], x[1]
        if len(word) > 1 and flag!='eng' and flag != 'm' and flag !='mq' and word not in stopwords:
            return True
        return False

    result = filter(condition, pseg.cut(sentence))
    result = map(lambda x:list(x)[0], result)
    return list(result)