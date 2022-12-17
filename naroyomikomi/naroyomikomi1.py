#!/usr/bin/env python3
#coding: utf-8
""" 小説家になろうの読み込み """
""" 小説の一括ダウンロードを目指す """


import requests
from bs4 import BeautifulSoup
import re

URL = 'https://ncode.syosetu.com'       # 小説家になろうのURL
ID = 'zzzzzzz'                          # 小説のID 
HEADERS = {                             # HP読み込み時のヘッダー情報
    'User-Agent':'Mozilla/5.0'
}

def main():

    # 小説の目次HP読み込み
    # リクエストヘッダーが無いと読み込みエラーが出た(403)
    mokuzi_hp = requests.get(URL + '/' + ID, headers=HEADERS)

    # 読み込んだHTMLの解析？
    mokuzi_soup = BeautifulSoup(mokuzi_hp.text, "html.parser")

    # 小説のタイトルの取得
    syousetu_title = mokuzi_soup.find(class_=re.compile('novel_title'))
    print('')
    print('title:' + syousetu_title.text)


    # 小説へのリンク部分を取得
    mokuzi_elems = mokuzi_soup.find_all(href=re.compile('^/' + ID))

    # 取得した小説の見出しとリンクを表示（とりあえず3個）
    count = 1
    for elem in mokuzi_elems:

        print(str(count) + '.' + elem.contents[0])
        print(URL + elem.attrs['href'])

        if count < 3:
            count += 1
        else:
            break


    # 小説のページを読み込む(とりあえず1個)
    count = 1
    for elem in mokuzi_elems:

        # 小説の文章HP読み込み
        honbun_hp = requests.get(URL + elem.attrs['href'], headers=HEADERS)

        # 読み込んだHTMLの解析
        honbun_soup = BeautifulSoup(honbun_hp.text, "html.parser")

        # 小説の小タイトル取得
        honbun_title = honbun_soup.find(class_=re.compile('novel_subtitle'))
        print('subtitle:' + honbun_title.text)

        # 小説の本文の取得
        honbun_text = honbun_soup.find_all(id=re.compile('^L'))

        for line in honbun_text:
            print(line.text)


        if count < 1:
            count += 1
        else:
            break



if __name__ == '__main__':
    main()

