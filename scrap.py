#-*-coding:utf8-*-

import re
import requests
import urllib
import os,time
from bs4 import BeautifulSoup

def get_web(key_word,page_num,COOKIE):
    """
    定义获取一个指定页源码的函数
    """
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Referer': 'https://list.tmall.com/search_product.htm?q=%C4%DA%D2%C2&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton',
               'Cookie':'{}'.format(COOKIE)}
    key_word = urllib.parse.quote(key_word)
    url = 'https://list.tmall.com/search_product.htm?&s={}&q={}'.format((page_num-1)*60,key_word)
    i=1
    while i<5:
        res = requests.get(url,headers=headers,timeout=5)
        if res.status_code == 200:
            m = re.findall('亲，小二正忙，滑动一下马上回来', res.text)
            if m == [] :
                return res.text
            else:
                return 0
        i += 1

ls = [] #定义接收所有解析到的url链接的列表
def get_oneurl_imgs(res):
    """
    定义获取一个页面所有图片url的函数
    """
    soup = BeautifulSoup(res,'lxml')
    for dic in soup.find_all('p',class_="ks-switchable-content"): # 查找p标签(可选),p标签结果更多
    # for dic in soup.find_all('a',class_="productImg"): #查找a标签
        for item in dic.find_all('img'): # 查找a标签下的img标签
            if item != (None or []):
                a = str(item.attrs.get("data-ks-lazyload-custom")) # 取得p标签解析出的字典值
                # a = str(item.attrs.get("src")) # 取得a标签解析出的字典值
                url_res = ''.join(re.findall(r'img.alicdn.com/.*?jpg', a))
                if url_res != '':
                    ls.append('http://'+url_res+'_430x430q90.jpg')
                    # print('{}'.format('*'*30))

def main():
    # 打开外部文件，获取cookiec参数
    with open("paras.txt","r",encoding="utf-8") as f1:
        COOKIE = re.findall(r'".*"',f1.read())[0].strip("\"")
    # 设计循环
    while True:
        # 创建文件目录
        dirname = os.getcwd()
        key_word = input("请输入查询关键字：")
        page_name = eval(input("请输入总共爬取页数:"))
        if not os.path.exists(dirname+"/图片抓取/{}".format(key_word)):
            os.makedirs(dirname+"/图片抓取/{}".format(key_word))
        flag = 1
        print("程序初始化....")
        # 循环获取所有页面的img图片链接
        while True:
            for i in range(1,page_name+1):
                result = get_web(key_word,i,COOKIE)
                if not result:
                    flag = 0
                    break
                get = get_oneurl_imgs(result)
                print("\r正在初始化第{}个页面，待处理{}个页面，请稍等...".format(i,page_name-i),end="")
                time.sleep(2)
            if flag == 0: # 判断cookie是否失效
                COOKIE = input("\ncookie失效，需要滑动验证，请重新输入cookie:")
                # 将新传入的cookie值写入文件替换
                with open("paras.txt", "r+", encoding="utf-8") as fi:
                    s = fi.read()
                    s = re.sub(pattern=r'^cookie_para=".*"', repl='cookie_para=\"{}\"'.format(COOKIE), string=s)
                    fi.seek(0)
                    fi.truncate()
                    fi.write(s)
                flag = 1
                continue
            break
        print("\r 图片链接获取完毕，开始缓存...")
        # 保存图片
        for i,j in enumerate(ls):
            x = len(ls)
            fo = open("图片抓取/{0}/{0}-{1}.png".format(key_word,i+1), 'bw+')
            res = requests.get(j)
            print("\r 当前进度{0:.2%}，写入第{1}张图片...".format((i+1)/x,i+1),end='')
            fo.write(res.content)
            fo.close()
        inp = input("爬取完毕!\n是否退出(y|Y)：")
        if inp == ("y" or "Y"):
            break

if __name__ == '__main__':
    main()
