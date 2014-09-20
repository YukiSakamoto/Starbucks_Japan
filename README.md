Starbucks_Japan
===============

## これはなに？ ##
スターバックスの店舗情報を公式サイトからスクレイピングしてくるプログラムです。
以前はRubyで書いていましたが、この度、Pythonでlxmlというhtml, xmlをパースしてくれるライブラリを用いて書き直しました。


## 他に同じ事やってる人いるんじゃない？ ##
僕もそう思います。しかし、全店舗表っぽいものはネット上でもあったのですが、結構前に閉店した地元のスタバが載っていたりと、新しい情報のようには感じなかったので、それなら作ろうと思ってやった次第です。もしいいのがあれば教えて欲しいです。
　
## 結果は ##
outputsディレクトリに幾つかの県のお店リストを載せています。そこに無い県のリストが欲しい場合は、以下に示す方法で実行して自分で作ってください。
プルリクエストもらえると助かります。outputsディレクトリに追加して行きます。

## ありそうな質問 ##
##### プログラムを実行したい。 #####

Linux, Mac OS Xの方

ライブラリとして、lxmlが必要です。

	$> pip install lxml
	
でインストールしてください。もしこれしたときにpipがないっておこられたら

	$> easy_install pip
	
をした上で上記のpip install lxmlをもう一度。いずれもPermission deniedでおこられたらsudoをするのを忘れずに。

ライブラリのインストールが完了したら、スクレイピングの実行は

	$> python starbucks_scraping.py

と叩くだけでOKです。なお、Python2.7でしか確認していません。

スクレイピングする県の選択はスクリプトの下の方、

```PYTHON
pref_id_dict = {
        1: "Hokkaido",  2: "Aomori",    3: "Iwate",     4: "Miyagi",    5: "Akita", 6: "Yamagata",  7: "Fukushima",
        8: "Tokyo",     9: "Ibaraki",   10:"Gunnma",    11:"Saitama",   12:"Chiba", 13:"Tokyo",     14:"Kanagawa",
        15:"Niigata",   16:"Toyama",    17:"Ishikawa",  18:"Fukui",     19:"Yamanashi", 20: "Nagano",
        21:"Gifu",      22:"Sizuoka",   23:"Aichi",     24:"Mie",
        25:"Shiga",     26:"Kyoto",     27:"Osaka",     28:"Hyogo",     29:"Nara",  30:"Wakayama",
        31:"Tottori",   32:"Shimane",   33:"Okayama",   34:"Hiroshima", 35:"Yamaguchi",
        36:"Tokushima", 37:"Kagawa",    38:"Ehime",     39:"Kochi",
        40:"Fukuoka",   41:"Saga",      42:"Nagasaki",  43:"Kumamoto",  44:"Oita",  45:"Miyazaki",  46:"Kagoshima", 47:"Okinawa"
        }

#============================================================
prefid = 47	# <- _ここを変える_ 
filename = "%s.csv" % pref_id_dist[prefid]
print_header = True
#============================================================
```

pref_id_dictでハードコードされている番号と都道府県名の対応を元に、
prefidにわたす番号を変えてから実行してください。

Windowsの方はテストできてないので、実行の仕方はお任せします。

また、走らせ始めると、しばらくは終了しません。スターバックスのウェブサイトに何十（百）回もアクセスします。そうすると少なからずスターバックスのサーバーの捌けるトラフィックの一部を奪ってしまうことは容易に想像できます。とくに面白いプログラムではないので、むやみやたらな実行は極力避けましょう。

	 
##### 実行してみたんだけど、情報が取れない #####
スタバのサイトがこのスクリプトを書いた時(2014/09頃)のものとは変わったのかもしれません。
プログラムの性質上、公式サイトのHTML構造に依存するので、どうしようもないです。


##### 部分的に情報が取れてないよ #####

特に営業時間のパースって面倒くさいんですよ。。。

This Python script scrapes Japanese Starbucks website. So, I didn't prepare the document written in English, sorry.
