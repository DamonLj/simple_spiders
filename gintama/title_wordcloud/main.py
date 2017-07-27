# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
# matplotlib.use('qt4agg')
from wordcloud import WordCloud
import jieba


class WordCloud_CN(object):
    '''
    use package wordcloud and jieba
    generating wordcloud for chinese character
    '''

    def __init__(self, stopwords_file):
        self.stopwords_file = stopwords_file
        self.text_file = text_file

    @property
    def get_stopwords(self):
        self.stopwords = {}
        f = open(self.stopwords_file, 'r', encoding='utf-8')
        line = f.readline().rstrip()
        while line:
            self.stopwords.setdefault(line, 0)
            self.stopwords[line] = 1
            line = f.readline().rstrip()
        f.close()
        return self.stopwords

    @property
    def seg_text(self):
        with open(self.text_file, 'r', encoding='utf-8') as f:
            text = f.readlines()
            text = r' '.join(text)

            seg_generator = jieba.cut(text)
            self.seg_list = [
                i for i in seg_generator if i not in self.get_stopwords]
            self.seg_list = [i for i in self.seg_list if i != u' ']
            self.seg_list = r' '.join(self.seg_list)
        return self.seg_list

    def show(self):
        # wordcloud = WordCloud(max_font_size=40, relative_scaling=.5)
        gintama_mask = np.array(Image.open(pic_file))
        wordcloud = WordCloud(font_path=os.path.join(dirpath, 'static\simheittf\simhei.ttf'),
                              mask=gintama_mask)
        # background_color = "black", margin = 5, width = 1800, height = 800,
        self.wordcloud = wordcloud.generate(self.seg_text)

        plt.figure()
        plt.imshow(self.wordcloud)
        plt.axis("off")
        plt.show()

    def save(self):
        self.wordcloud.to_file(os.path.join(dirpath, "gintama_title.png"))


if __name__ == '__main__':
    dirpath = os.getcwd()
    stopwords_file = os.path.join(dirpath, 'static\stopwords.txt')
    text_file = os.path.join(dirpath, 'gintamatitle.txt')
    pic_file = os.path.join(dirpath, 'gintama.png')

    generater = WordCloud_CN(stopwords_file)
    generater.show()
    generater.save()