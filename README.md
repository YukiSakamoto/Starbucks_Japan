Starbucks_Japan
===============

## これはなに？ ##
スターバックスの店舗情報を公式サイトからスクレイピングしてくるプログラムです。
以前はRubyで書いていましたが、この度、Pythonでlxmlというhtml, xmlをパースしてくれるライブラリを用いて書き直しました。
　
## いいから店舗のリストを ##
このディレクトリにあるcsvファイルを見てください。

## ありそうな質問 ##
##### プログラムを実行したい。 #####

Linux, Mac OS Xの方

処理系としてPython2.7, ライブラリとして、lxmlが必要です。lxmlは、

	$> pip install lxml
	
でインストールしてください。もしpipがないとエラーが出た場合は、

	$> easy_install pip
	
をした上で上記のpip install lxmlをもう一度。いずれもPermission deniedとなった場合は、sudoをするのを忘れずに。

ライブラリのインストールが完了したら、スクレイピングの実行は

	$> python starbucks_scraping.py

と叩くだけでOKです。Python2.7でしか確認していません。

パラメータに関して述べます。
プログラムの上部に以下のような記述があります。ここがパラメータの設定部分です。

```PYTHON
pref_id_dict = { 
        1: "Hokkaido",  2: "Aomori",    3: "Iwate",     4: "Miyagi",    5: "Akita", 6: "Yamagata",  7: "Fukushima",
        8: "Tochigi",   9: "Ibaraki",   10:"Gumma",    11:"Saitama",    12:"Chiba", 13:"Tokyo",     14:"Kanagawa",
        15:"Niigata",   16:"Toyama",    17:"Ishikawa",  18:"Fukui",     19:"Yamanashi", 20: "Nagano",  
        21:"Gifu",      22:"Sizuoka",   23:"Aichi",     24:"Mie",   
        25:"Shiga",     26:"Kyoto",     27:"Osaka",     28:"Hyogo",     29:"Nara",  30:"Wakayama",
        31:"Tottori",   32:"Shimane",   33:"Okayama",   34:"Hiroshima", 35:"Yamaguchi",
        36:"Tokushima", 37:"Kagawa",    38:"Ehime",     39:"Kochi",     
        40:"Fukuoka",   41:"Saga",      42:"Nagasaki",  43:"Kumamoto",  44:"Oita",  45:"Miyazaki",  46:"Kagoshima", 47:"Okinawa"
        }

#============================================================
# Parameters

#cache
load_list_cache = False
save_list_cache = False
load_storedetail_cache = True
save_storedetail_cache = True
savedir = "starbucks"

# list that contains the numbers of prefectures to survey
region  = range(1, 48)

# output filename
filename = "20150928.csv"

# Progress Output
verbose = False
#============================================================
```

pref_id_dictでハードコードされている番号と都道府県名の対応を元に、
regionには、探索を実行する都道府県の番号をlist形式で渡してください。

cache関係のパラメータは、各都道府県の店舗リストに関してはキャッシュせずに、各店舗頁のみキャッシュすることをお勧めします。
なお、全店舗キャッシュすると40MB弱の容量になりました。

filenameが、出力するcsvファイルの名前です。

走らせ始めると、しばらくは終了しません。スターバックスのウェブサイトに何百回もアクセスします。そうすると少なからずスターバックスのサーバーの捌けるトラフィックの一部を奪ってしまうことは容易に想像できます。とくに面白いプログラムではないので、むやみやたらな実行は極力避けましょう。
また利用する場合は先にも書いた通り、キャッシュを利用してください。
	 
##### 実行してみたんだけど、情報が取れない #####
スタバのサイトがこのスクリプトを書いた時(2015/09頃)のものとは変わったのかもしれません。
プログラムの性質上、公式サイトのHTML構造に依存するので、どうしようもないです。


##### 部分的に情報が取れてないよ #####

特に営業時間のパースって面倒くさいんですよ。。。

This Python script scrapes Japanese Starbucks website. So, I didn't prepare the document written in English, sorry.
