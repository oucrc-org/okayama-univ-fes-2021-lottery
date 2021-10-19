# okayama-univ-fes-2021-lottery

## 環境構築
`pip install PyMySQL`で必要なパッケージをインストール  
環境を汚したくない場合はvenvを使用

## ファイル
- .gitignore: Gitに上げたくないファイルやディレクトリ名を記載したファイル
- lottery.py: メインプログラム
  - DBに接続
  - DBから情報を受信する
  - 固有キーとユーザ名を格納
  - 乱数で任意の人数弾き出す
  - DBから切断
- config.py: 環境変数の読み込みプログラム