#-*-coding:utf8-*-

import os
import jieba
from wordcloud import WordCloud

file_path = input("请输入您需要生成词云的完整路径(右键->安全->复制完整路径):")
num = eval(input("请输入需要排序的词语数量:"))
cho = input("是否为中文(Y/N)?")
f = open(file_path, "r", encoding="utf-8")
txt = f.read()
f.close()
words = jieba.lcut(txt)
counts = {}
txt2 = " ".join(words)
for word in words:
    if len(word) == 1 or " " in word:
        continue
    else:
        counts[word] = counts.get(word,0) + 1
del words
ls = sorted(counts.items(), key=lambda x:x[1], reverse=True)
print("{0:一<10}{1:<}".format("词语", "数量"),end="\n")
for n,i in enumerate(ls):
    if n > num:
        break
    print("{0:一<10}{1:<}".format(i[0], i[1]),end="\n")
p = os.path.split(file_path)
p2 = os.path.splitext(p[1])
dist_path = p[0] + "\\" + p2[0] +".png"
print("正在生成词云到目录{}".format(dist_path))
if cho == "Y" or cho == "y":
    doc = txt2
else:
    doc = txt
wordcloud_get = WordCloud(min_word_length=2,font_path="C:\\Windows\\Fonts\\STFANGSO.TTF",\
    width=500,height=400,margin=5,font_step=1,max_words=num,min_font_size=5,\
        background_color="#CCCCFF").generate(txt2)
wordcloud_get.to_file(dist_path)
flag = 1
while flag!="exit":
    flag = input("请输入exit退出!")
    if flag == "exit":
        break
