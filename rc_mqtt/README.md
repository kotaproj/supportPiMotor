# MQTTラズパイラジコン

**MQTTラズパイラジコン** は、ラズベリーパイモーターハットを使ったラジコンです。
MQTT通信を使って制御します。



- [MQTTラズパイラジコン](#mqttラズパイラジコン)
- [Requirement](#requirement)
  - [MQTT](#mqtt)
    - [MQTT Broker(サーバ)](#mqtt-brokerサーバ)
    - [MQTT Subscribe(リスナー)](#mqtt-subscribeリスナー)
    - [MQTT Publisher(クライアント)](#mqtt-publisherクライアント)
  - [フォントデータ](#フォントデータ)
  - [pip](#pip)



# Requirement

以下のモジュールのインストールが必要です。

## MQTT

### MQTT Broker(サーバ)

MQTTブローカーは、mosquittoを使用しています。
インストールおよび起動は以下です。

- インストール

```bash
$ sudo apt install mosquitto
```

- サービス起動

```bash
$ sudo systemctl start mosquitto
```

### MQTT Subscribe(リスナー)

本プログラム自身となります

### MQTT Publisher(クライアント)

MQTTブローカーは、mosquittoを使用しています。
インストールおよび起動は以下です。

- インストール

```bash
$ sudo apt install mosquitto-clients
```

- LED1を点灯させる

```bash
$ mosquitto_pub -d -t orz -m "pim:led_no1_on" -h 127.0.0.1 --topic topic_1
```


## フォントデータ

表示機に表示するフォントは、IPAフォントを使用しています。

[IPAフォント](https://moji.or.jp/ipafont/)
より、フォントデータを以下に配置してください。

* /rc_mqtt/ipaexg.ttf
* /rc_mqtt/ipaexm.ttf


## pip

```bash
$ pip install icecream
$ pip install paho.mqtt
```
