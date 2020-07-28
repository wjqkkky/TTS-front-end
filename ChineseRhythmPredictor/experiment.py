import pickle
import time
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from tqdm import tqdm
from jieba import posseg
from ChineseRhythmPredictor.model import RhythmPredictor

# import sys
# import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# sys.stdout.write("Your content....")

def score(y: list, pred: list):
    tag2idx = {'#0': 0, '#2': 1}
    res = [[0 for _ in range(2)] for _ in range(2)]
    for yi, predi in zip(y, pred):
        print(yi,predi)
        res[tag2idx[yi]][tag2idx[predi]] += 1
    print(res)
    for i in range(2):
        tot = sum(res[i])
        res[i] = [res[i][j] / tot for j in range(2)]
        print('#{}:'.format(i+1), res[i])


def make_data():
    words_batch, labels_batch = [], []
    with open('data.txt', 'r',encoding='utf-8') as f:
        for line in f.readlines():
            left, _, right = line[:-1].partition('|')
            labels_batch.append(right.split(' ')[:-1])
            words_batch.append(left.split(' '))
    feat_as_sentence, label_as_sentence = [], []
    feat_all, label_all = [], []
    bar = tqdm(total=len(words_batch))
    for i in range(len(words_batch)):
        words, labels = words_batch[i], labels_batch[i]
        # Extract features from a sentence
        sentence_feats = RhythmPredictor.extract_features(words)
        # Features and labels as a sentence
        feat_as_sentence.append(sentence_feats)
        label_as_sentence.append(labels)
        # All features and labels
        feat_all.extend(sentence_feats)
        label_all.extend(labels)
        bar.update(1)
    bar.close()
    with open('dataset.pkl', 'wb') as f:
        data = {
            'feat_as_sentence': feat_as_sentence,
            'label_as_sentence': label_as_sentence,
            'feat_all': feat_all,
            'label_all': label_all
        }
        pickle.dump(data, f)


def make_model():
    model = RhythmPredictor(max_depth=50, n_estimators=20, n_jobs=-1)
    with open('dataset.pkl', 'rb') as f:
        data = pickle.load(f)
    feat_all = pd.DataFrame(data['feat_all'],
                            columns=RhythmPredictor.ALL_COLUMNS)
    label_all = data['label_all']
    # Fit tree using all data at one time
    train_x, train_y = feat_all[:-1000], label_all[:-1000]
    model.fit(train_x, train_y)
    # Fit CRF using data from one sentence at a time
    feat_as_sentence = data['feat_as_sentence'][:-1000]
    label_as_sentence = data['label_as_sentence'][:-1000]
    model.fit_crf(feat_as_sentence[:], label_as_sentence[:])
    model.PREDICT_WITH_CRF = True
    #print(feat_all[-10:])
    pred = model.predict(feat_all[-1000:])
    score(label_all[-1000:], pred)
    model.dump(tree_path='tree.pkl',crf_path='crf.pt')


def test_data():
    model = RhythmPredictor()
    model.load(tree_path='tree.pkl',crf_path='crf.pt')
    model.PREDICT_WITH_CRF = True
    with open('dataset.pkl', 'rb') as f:
        data = pickle.load(f)
    count = {label: [0, 0] for label in model.RHYTHM_TAGS}
    total = [0, 0]
    feat_as_sentence = data['feat_as_sentence'][-1000:]
    label_as_sentence = data['label_as_sentence'][-1000:]
    progress_bar = tqdm(total=len(feat_as_sentence))

    true_labels=[]
    pre_labels=[]
    for feats, labels in zip(feat_as_sentence, label_as_sentence):
        if len(feats) > 0:
            true_labels.extend(labels)
            pred = model.predict(feats)
            pre_labels.extend(pred)
            for i in range(len(labels)):
                count[labels[i]][pred[i] == labels[i]] += 1
                total[pred[i] == labels[i]] += 1
        progress_bar.update(1)
    #print(true_labels)
    #print(pre_labels)
    progress_bar.close()
    # Show prediction result
    score(true_labels,pre_labels)
    print('Total acc: ', total[1] / sum(total))
    for label, count_pair in count.items():
        print('Label: {}, acc: {}'.format(label,
                                          count_pair[1] / sum(count_pair)))


def cross_validate_test():
    with open('dataset.pkl', 'rb') as f:
        dataset = pickle.load(f)
    cv = KFold(n_splits=10, shuffle=True)
    x, y = np.array(dataset['feat_all']), np.array(dataset['label_all'])
    for train_index, valid_index in cv.split(x):
        train_x, train_y = x[train_index], y[train_index]
        valid_x, valid_y = x[valid_index], y[valid_index]
        model = RhythmPredictor()
        model.PREDICT_WITH_CRF = True
        model.fit(train_x, train_y, max_depth=30)
        # Cross validation
        progress_bar = tqdm(total=len(valid_x))
        count = {label: [0, 0] for label in model.RHYTHM_TAGS}
        total = [0, 0]
        
        for feats, labels in zip(valid_x, valid_y):
            if len(feats) > 0:
                pred = model.predict(feats)
                for i in range(len(labels)):
                    count[labels[i]][pred[i] == labels[i]] += 1
                    total[pred[i] == labels[i]] += 1
            progress_bar.update(1)
        progress_bar.close()
        # Show prediction result
        print('Total acc: ', total[1] / sum(total))
        for label, count_pair in count.items():
            print('Label: {}, acc: {}'.format(label,
                                              count_pair[1] / sum(count_pair)))

def load_model():
    model = RhythmPredictor()
    model.load(tree_path='./ChineseRhythmPredictor/tree.pkl',crf_path='./ChineseRhythmPredictor/crf.pt')
    model.PREDICT_WITH_CRF = True
    return model

def test_sentences(model,sentences):

    # sentences = ['交易中心负责办抵押登记，抵押科抽出一半人手天天来这儿。',
    #     '这时候，居委会一张罗，事情就摆平了。',
    #     '决不允许有一点儿特殊化。',
    #     '访问期间，我们曾到现代公司所属的蔚山工厂参观。',
    #     '奔驰公司加快在华投资。',
    #     '于是第一季度，前来投资的外商更多。',
    #     '往往是毛衣外面套棉裤。',
    #     '法四军人将赴北极探险。',
    #     '雪越来越厚，车已经不能再前行。',
    #
    # ]
    result = []
    for sentence in sentences:
        pairs = [tuple(pair) for pair in posseg.cut(sentence)]
        words = [pair[0] for pair in pairs]
        poses = [pair[1] for pair in pairs]
        start = time.time()
        #print(words)
        #print(poses)
        labels = model.predict_words(words, poses)
        print('Time: ', time.time() - start)
        str_=''
        for i in range(len(words)):
            if i <len(labels):
                str_ = str_ + words[i]+labels[i]
            else:
                str_ = str_+words[i]
          #      if labels[i] =='#1':
               #     str = str + words[i]
              #  elif labels[i]=='#4':
             #       str = str + words[i] +'#2'
            #    else:
           #         str = str + words[i] + '#1'
          #  else:
         #       str = str + words[i]
        # print(str_)
        result.append(str_)
    return str_

if __name__ == '__main__':
    make_data()
    make_model()
    # test_data()
    # cross_validate_test()
    # test_sentences()
