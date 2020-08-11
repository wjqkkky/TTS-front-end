# encoding=utf-8
import argparse

import chinesetone2pinyin as cp
from ChineseRhythmPredictor import *
from ChineseRhythmPredictor.experiment import test_sentences, load_model
import chaifen
import time
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import sys
import codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def with_Rhythm(chinese, model, split=True):
	pinyin_input = test_sentences(model, [chinese])
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
	return chinese_Normal, pinyin


def without_Rhythm(chinese, split=True):
	chinese_Normal, pinyin = cp.chinese2pinyin(chinese)
	if split:
		pinyin = chaifen.split_sheng(pinyin)
	return chinese_Normal, pinyin


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--cn_file', default='')
	parser.add_argument('--pinyin_file', default='pinyin.txt')
	args = parser.parse_args()
	cn_file = args.cn_file
	pinyin_file = args.pinyin_file
	model = load_model()
	#     chinese='时间~是下午2点36分。您想要什么啊，这个东西2983.07克或12345.60米。'
	# # pinyin_input = '今天是个好日子，心想的事儿都能成。儿子已经好了'
	# chinese_Normal, pinyin = with_Rhythm(chinese, model)
	# chinese_Normal, pinyin = without_Rhythm(chinese)
	f_out = open(pinyin_file, "w")
	with open(cn_file, "r", encoding="utf-8") as f:
		while 1:
			line = f.readline().strip()
			print(line)
			if not line:
				break
			chinese_Normal, pinyin = with_Rhythm(line, model)
			print(pinyin)
			f_out.writelines(pinyin)
	f.close()
