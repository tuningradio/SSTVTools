sstvtool.py v1.0.1 2024.06.18: Windows11 +Python3.10.nで動作確認

Ver1.0.1変更点：
# Ver1.0.1変更点: 使えるSSTVモードを増やした。ストリーミング時、起動パラメーターで オーディオ出力デバイスを -d/--device {device_id}で数字を指定するとそこに出力する。
#

このプログラムは、pySSTVを応用したプログラムです。

基本的に画像ファイルをSSTV信号に変換します。
WIN11、Python 3.10.9で動作確認をしています。


付加機能：

・SSTVモードを指定できます。

・ストリーミング(即再生)とSSTV信号をファイルセーブのどちらかを選択できます。

・元画像のピクセルサイズに関係なく、必要なピクセルサイズに変更する機能。AI絵や監視カメラからの静止画像を指定したSSTVモードとピクセルサイズでSSTV信号を作成します。変更の際、元画像のアスペクト比は固定します。隙間は黒色で埋めます。

・テキストを画像にオーバーレイします。コールサインや監視カメラ番号を入れることが出来ます。
フォントの種類、サイズ、色、文字列、位置を指定できます(ソース内で変更してください)。文字列(text)を削除して ''だけにすると、テキストのオーバーレイ処理はしません。

使い方：

1)SSTV信号をoutput.wavにセーブしたい場合


python sstvtool.py -i aaaaa.png -p 320x240 -m Robot36 -o output.wav

-i SSTV信号に変換したい画像ファイル名を指定します。
-p 画像ファイルを横x縦ピクセルに大きさを変換します。基本的に次のSSTVモードに合わせてください。
-m SSTVモードを指定します。
-o [{output_filename}.wav] SSTV信号の出力方法を指定します。-oにファイル名を付けると、信号をファイルセーブします。SSTV信号のファイル出力はWAV形式なので、拡張子は.wavにしてください。
-d {device_ID} ストリーミング時、オーディオ出力デバイスのID番号を指定できます。指定しない場合は既定のオーディオに出力します。

2)SSTV信号をストリーミングしたい場合

python sstvtools.py -i aaaaa.png -p 320x240 -m Robot36 -s -d 6

-s この起動パラメータにより、直接音を出します。
-d device ID 6に音声を出力します。

なお、このバージョン(ver1.0.1)では文字列オーバーレイ機能の設定はソース内の数値・文字を変更してください。

変更する部分は63行の下記の部分です。

def generate_sstv_signal(image_path, mode='Robot36', stream=False, output_path=None, size=None, text='JA1XPM', font_path='arial.ttf', font_size=32, text_color='green', text_position=(5, 5), device_id=None)

そしてtext='' とすると文字列オーバーレイしません。

device_idは強制設定したい場合は数値を入れてください。 例:device_id=6




