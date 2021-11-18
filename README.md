# okayama-univ-fes-2021-lottery

## 環境構築
`pip install PyMySQL`，`pip install python-dotenv`，`pip install cryptography`で必要なパッケージをインストール  
環境を汚したくない場合はvenvを使用

## ファイル
- .env.example: 環境変数のサンプルファイル
- .gitignore: Gitに上げたくないファイルやディレクトリ名を記載したファイル
- lottery.py: メインプログラム
- config.py: 環境変数の読み込みプログラム

## 使い方
抽選モード選択（1:自動抽選モード，3:スタンプ8つ獲得している人のみの自動抽選モード）

### 1. 自動抽選モード
全ての景品に対して自動抽選を行う．
出力体裁は次のとおりである．
```
Lotterying present_id = 6 # 抽選中のプレゼントID
Stock = 1                 # プレゼント残数
[10]                      # user_id
Remained stock = 0        # 抽選後プレゼント残数（余り）
```

### 3. スタンプ8つ獲得している人のみの自動抽選モード
プログラム開始時，プレゼント残数（余り）を入力する必要があります．
```
Select lottery mode(Auto:1, Manual:2, Auto8:3).
3
Please input remained_stock.
1
[10]
Remained stock = 0
```
