def split_sheng(words):
    '''
    :param words: 一段未拆分的拼音，拼音和标点和字符之间要用一个空格空起来
    :return: 拆分好的拼音。拆分为声母，韵母。
    '''
    list_sheng = ['b' ,'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k',  'j', 'q', 'x', 'zh',
                  'ch', 'sh','h', 'r', 'z', 'c', 's', 'w', 'y']
    words = words.replace('  ',' ')
    words =words.split(' ')
    word_split =[]
    list_special = ['y', 'j', 'q', 'x']
    for word in words:
        if word[0] in list_sheng:
            if word[:2] in list_sheng:
                word_split.append(word[:2])
                word_split.append(word[2:])
                continue
            else:
                if word[1] == 'u' and (word[0] in list_special):
                    word_temp = 'v' + word[2:]
                    word_split.append(word[0])
                    word_split.append(word_temp)
                else:
                    word_split.append(word[0])
                    word_split.append(word[1:])
        else:
            word_split.append(word)
    str_ = ' '.join(word_split)
    return str_
