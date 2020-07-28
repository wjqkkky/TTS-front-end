#encoding=utf-8
import chinesetone2pinyin as cp
from ChineseRhythmPredictor import *
from ChineseRhythmPredictor.experiment import test_sentences,load_model
import chaifen
import time
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
#pinyin_input='时间~是下午2:36，63.4元。2983.07克或12345.60米。'
pinyin_input = '今天是个好日子，心想的事儿都能成。儿子已经好了'
model = load_model()
#time.sleep(5)
pinyin_input = test_sentences(model,[pinyin_input])


#with open('sentences-6.7.txt','r',encoding="utf-8") as f:
#	data=f.readlines()
     # print(data[0])
#	with open('sentences-0708_pinyin_yunlv.txt','w',encoding="utf-8") as fw:
#		for text in data:
		#	#print(text)
#			text = ex.test_sentences([text])
#			print(text)
#			a=cp.chinese2pinyin(text)
#			print(a)
			#fw.write(a)
#	fw.close()
#f.close()
a=cp.chinese2pinyin(pinyin_input)
a = chaifen.split_sheng(a)
a = a.replace('#0','').replace('#2','#1')
punctuation = [',','.','!','?']
if a[-1] in punctuation:
    a = a[:-2] +'#2 '+a[-1]
else:
    a = a+' #2'
a = a.replace('r 5 ', ' er5 ')
a=a.replace('  ',' ')

print(a)
