# TTS-front-end-processing
需要的环境：
numpy==1.14
jieba==0.39
pandas
pypinyin==0.36.0
scikit_learn==0.21.3
torch==1.0.1.post2
tqdm==4.36.1



1.下载git clone https://github.com/ysujiang/TTS-front-end.git

2.安装环境：
pip install -r  requirements.txt

3.应用模型
说明：本模型训练的为二级韵律+TN处理+ChineseTone拼音转文本处理
运行：python TTS-front-end-main.py
备注：主函数里，（1）with_Rhythm(chinese,model)为带韵律的模型，默认参数split=True进行切分声韵母，当split为false的时候，不进行声韵母切分
（2）without_Rhythm(chinese)为不带韵律预测的模型，默认参数split=True进行切分声韵母，当split为false的时候，不进行声韵母切分

4.模型训练
数据格式为data.txt所示（二级标签）
训练运行：python experiment.py
备注：如需要更改韵律标签重新训练（多级标签），则需要注意一下几点：
（1）注意修改experiment.py中的score函数tag2idx,以及range(*)，以及model.py中29行RHYTHM_TAGS
（2）使用时注意修改TTS-front-end-main.py中的with_Rhythm()第18、21、23行
