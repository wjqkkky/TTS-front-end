#encoding=utf-8
import chinesetone2pinyin as cp
from ChineseRhythmPredictor import *
from ChineseRhythmPredictor.experiment import test_sentences,load_model
import chaifen
import time
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


def with_Rhythm(chinese,model,split=True):
    pinyin_input = test_sentences(model,[chinese])
    chinese_Normal, pinyin = cp.chinese2pinyin(pinyin_input)
    if split:
        pinyin = chaifen.split_sheng(pinyin)
    pinyin = pinyin.replace('#0', '').replace('#2', '#1')
    punctuation = [',', '.', '!', '?']
    if pinyin[-1] in punctuation:
        pinyin = pinyin[:-2] + '#2 ' + pinyin[-1]
    else:
        pinyin = pinyin + ' #2'
    pinyin = pinyin.replace(' r 5 ', ' er5 ')
    pinyin = pinyin.replace('  ', ' ')
    return chinese_Normal,pinyin
def without_Rhythm(chinese,split=True):
    chinese_Normal, pinyin = cp.chinese2pinyin(chinese)
    if split:
        pinyin = chaifen.split_sheng(pinyin)
    return chinese_Normal, pinyin
if __name__ == '__main__':
    chinese='时间~是下午2点36分。您想要什么啊，这个东西2983.07克或12345.60米。'
# pinyin_input = '今天是个好日子，心想的事儿都能成。儿子已经好了'
    model = load_model()

    # chinese_Normal, pinyin = with_Rhythm(chinese, model)
    chinese_Normal,pinyin = without_Rhythm(chinese)
    print(chinese_Normal)
    print(pinyin)
#time.sleep(5)
# pinyin_input = test_sentences(model,[pinyin_input])


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
# chinese_Normal,a=cp.chinese2pinyin(pinyin_input)
# print(chinese_Normal)
# a = chaifen.split_sheng(a)
# a = a.replace('#0','').replace('#2','#1')
# punctuation = [',','.','!','?']
# if a[-1] in punctuation:
#     a = a[:-2] +'#2 '+a[-1]
# else:
#     a = a+' #2'
# a = a.replace(' r 5 ', ' er5 ')
# a=a.replace('  ',' ')
#
# print(a)
