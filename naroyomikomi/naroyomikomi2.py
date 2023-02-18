#!/usr/bin/env python3
#coding: utf-8
""" 小説家になろうの読み込み """
""" 小説をダウンロードしテキストファイルに書き出す """
""" 小説はIDを指定する """
""" 何話(START_EPISODE)〜何話(END_EPISODE)を読み込むか指定する """


import requests
from bs4 import BeautifulSoup
import re
import time

URL = 'https://ncode.syosetu.com'       # 小説家になろうのURL
HEADERS = {                             # HP読み込み時のヘッダー情報
    'User-Agent':'Mozilla/5.0'
}

ID = 'n9669bk'                          # 小説のID

START_EPISODE = 1                       # 第何話から読み込むか
END_EPISODE = 3                        # 第何話で終了するか

def main():

    # 小説の目次HP読み込み
    # リクエストヘッダーが無いと読み込みエラーが出た(403)
    mokuzi_hp = requests.get(URL + '/' + ID, headers=HEADERS)

    # 読み込んだHTMLの解析？
    mokuzi_soup = BeautifulSoup(mokuzi_hp.text, "html.parser")

    # 小説のタイトルの取得
    syousetu_title = mokuzi_soup.find(class_=re.compile('novel_title'))

    # 出力するファイルのオープン
    # ubuntuの時とPATHの指定が違う。絶対PATHで指定した方がよいかも？
    # encoding='UTF-8'を入れないとUnicodeEncodeError: 'cp932' codec can't encode～エラーが出た
    with open('practices/naroyomikomi/download/' + syousetu_title.text\
        + str(START_EPISODE) + '-' + str(END_EPISODE) + '.txt', 'w', encoding='UTF-8') as outfile:

        print(syousetu_title.text + str(START_EPISODE) + '-' + str(END_EPISODE) +  '.txt 書き込み開始')
        
        # タイトルを出力
        print('Ti    :' + syousetu_title.text, file=outfile)
    
        # 小説へのリンク部分を取得
        mokuzi_elems = mokuzi_soup.find_all(href=re.compile('^/' + ID))

        # 小説のページを読み込む
        count = 1
        for elem in mokuzi_elems:

            if START_EPISODE <= count <= END_EPISODE:

                #処理の進行度を表示
                wariai = int((count - START_EPISODE) / (END_EPISODE - START_EPISODE) * 100)
                senn = ('#' * (wariai // 5)) + ('-' * (20 - wariai // 5))
                print('\r' + senn + str(wariai) + '% 書き込み完了', end='')

                # 小説の文章HP読み込み
                honbun_hp = requests.get(URL + elem.attrs['href'], headers=HEADERS)

                # 読み込んだHTMLの解析
                honbun_soup = BeautifulSoup(honbun_hp.text, "html.parser")

                # サブタイトルを出力
                print('St' + str(count).zfill(4) + ':' + elem.contents[0], file=outfile)

                # 小説の本文の取得
                honbun_text = honbun_soup.find_all(id=re.compile('^L[0-9]'))

                licount = 1

                for line in honbun_text:

                    # 空白の行は飛ばす（全半角スペースのみの行も飛ばす）
                    if re.sub('[\u3000 ]', '', line.text) != '':
                        # 行を出力
                        print('Li' + str(licount).zfill(4) + ':' + line.text, file=outfile)

                        licount += 1

                #1秒停止
                time.sleep(1)

            elif count > END_EPISODE:
                break
                
            count += 1

    print('')
    

if __name__ == '__main__':
    main()

