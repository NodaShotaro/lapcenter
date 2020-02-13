
# LapCenterのデータ分析プログラム

## 概要

オリエンテーリングのラップタイム公開サイト[LapCenter](https://mulka2.com/lapcenter/)からスクレイピングしたデータを分析するためのプログラム集とその記録をここに残します．

## 使い方

- settings/raceList.csvへレース結果のURLを追加
- python3 make_csv.pyの実行
- python3 preprocess.pyの実行
- 出てきた./csv/join.csvを読み込んで分析

## 作成したプログラム

### make_csv.py

./raceList.csvにエンコード「utf-8」で記録されたレース一覧のURLを読み込み，各ページからラップを抽出してCSV形式へ変換するプログラム．./settings/processedRaceList.csvと./settings/raceList.csvから差分を読み取ってデータセットへ追加する．
抽出されたCSVファイルはcsv/runner_tmp.csv，csv/leg_tmp.csvへ格納される．
前者はラップを記録したデータ，後者はレッグを記録したデータを格納する．
なお，これらの2つのCSVファイルのデータは，プログラム実行以前に記録していたものに差分を追加する形で実装されている．

### preprocess.py

機能
- ラップタイム，ミスタイム，合計タイムを秒に変換
- 6人以下のレース結果の削除
- スタート位置の計算
- runner / legの2テーブルのJOIN
- 結果をcsv/join.csvに出力

### predict.py



### mylib.py

- データセットの操作関数
  - def filter_little_race(df,min_sample)
    - min_sampleより少ない出走人数のレースを削除する関数．
  - convertLapTime(df,dimName)  
    - 文字列で記録されているラップタイムを秒に変換するプログラム．
  - def join_with_leginfo(df)
    - dfと./csv/leg.csvの2つのテーブルを結合するプログラム
  - def makeStartPosition(df)
    - dfに各選手が何番目の出走だったかを記録するプログラム．
  - def completeMissValue(df)
    - runnerテーブルの欠損値を補完するプログラム．
  - def delete_little_runner(df,min_sample,leginfo=True)
    - 出走回数がmin_sample以下の選手の情報を削除するプログラム．
  - makeLegLabel(df)
    - ラップのミスタイムの量でカテゴリ分けを行うプログラム．

- データセットの問合せ関数
  - def load()
    - join.csvを読み込んでくれる関数
  - def extractTargetRunner(df,filename)
    - 謎
  - def extractByDate(df,year,month)
    - year年month月以降のデータを抽出する関数．
