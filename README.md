Starbucks_Japan
===============

## これはなに？ ##
スターバックスが好きでよく利用しています。東京都や神奈川県はスターバックスの店舗も多く、夜遅くの時間まで営業している店舗も多くて便利なのですが、営業時間で店舗を検索できないなど、スターバックスの店舗検索には若干の使いづらさを感じていました。

そこで、なんとか自分で好きなように店を探すいい方法はないか？と、ある日スタバでウダウダと考えている途中で、とにかくまずはデータベースを拾い上げてくるしかない、ということでこのスクリプトを書きました。

スターバックスの店舗検索で表示されるリストをすべて巡回し、日本全国のスタバの店舗の基本情報を收集するプログラムです。これでスタバでお勉強したり、MacBook Airを開いてのコーディングが捗りますね。


## 他に同じ事やってる人いるんじゃない？ ##
僕もそう思います。しかし、全店舗表っぽいものはネット上でもあったのですが、結構前に閉店した地元のスタバが載っていたりと、新しい情報のようには感じなかったので、それなら作ろうと思ってやった次第です。もしいいのがあれば教えて欲しいです。
　
## 能書きはいいから、結果を早く ##
添付しているCSVファイルがそれです。エンコーディングはUTF-8です。また、僕はCSVが好きですが、CSVファイルがわからない人のために、Excel形式に変換したものも(.xlsxのファイル)添付しています。それぞれ東京都版、神奈川県版、全国版の３種類があります。


こちらからもDLできます。

* [全国版](http://www19.atpages.jp/~dashboard/starbucks/Starbucks_All.xlsx "全国版")
* [東京都](http://www19.atpages.jp/~dashboard/starbucks/Starbucks_Tokyo.xlsx "東京都")
* [神奈川県](http://www19.atpages.jp/~dashboard/starbucks/Starbucks_Kanagawa.xlsx "神奈川県")

## ありそうな質問 ##
##### プログラムを実行したい。 #####
Linux, Mac OS Xの方は、コマンドラインをたちあげて

	$> ruby all_Starbucks.rb

と叩くだけでOKです。Rubyと標準添付のモジュールさえあれば特にそれ以外の依存ライブラリはないと思います。Windowsの人はRubyの実行の仕方はお任せします。

また、走らせ始めると、しばらくは終了しません。スターバックスのウェブサイトに何十回もアクセスします。そうすると少なからずスターバックスのサーバーの捌けるトラフィックの一部を奪ってしまうことは容易に想像できます。とくに面白いプログラムではないので、改変目的以外での実行は極力避けましょう。

デフォルトでは全国版がStarBucks_All.csvというファイル名で出力されます。コマンドラインとかカレントディレクトリなどの概念の分からない人は本を読むか、誰かに聞くか、諦めてください。
	 
##### 実行してみたんだけど、情報が取れない #####
スタバのサイトがこのスクリプトを書いた時(2012/08頃)のものとは変わったのかもしれません。
このプログラム自体はただ正規表現を並べただけのもので、賢いやり方では全くもってないので、サイトのリニューアルなどに耐えうるロバスト性は持っていません。必要だと思ったらその時にはまた書き直します。

##### スタバのウェブサイトに出てくるリストにある検索結果の件数と一致しないんだけど #####
例えば、東京都だと、262件位あると表示され、Webページでリストページを辿って行くと、確かにそれと同数出てくるようです。しかし、プログラムでスクレイピングしてみると、どうしても重複がでる、ということを確認しています。したがって、収集の過程でもし同じテンポの情報を再度収集しているようであれば、それは登録しないようにしています。その先のつじつま合わせは、いつかするかもしれませんが期待しないでください。



This Ruby-script scrapes Japanese Starbucks websites. So, I didn't prepare the document written in English, sorry.
