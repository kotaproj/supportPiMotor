# HTTPラズパイラジコン

**HTTPラズパイラジコン** は、ラズベリーパイモーターハットを使ったラジコンです。
HTTP通信を使って制御します。
Webフレームワークは、Bottleを使用しています。


- [HTTPラズパイラジコン](#httpラズパイラジコン)
- [Requirement](#requirement)
  - [フォントデータ](#フォントデータ)
  - [pip](#pip)



# Requirement

以下のモジュールのインストールが必要です。

## フォントデータ

表示機に表示するフォントは、IPAフォントを使用しています。

[IPAフォント](https://moji.or.jp/ipafont/)
より、フォントデータを以下に配置してください。

* /rc_http/ipaexg.ttf
* /rc_http/ipaexm.ttf


## pip

```bash
$ pip install bottle
```
