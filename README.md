# ラズベリーパイモーターハット [![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

**ラズベリーパイモーターハット** は、ラズパイでラジコンをつくるためのハットです。

![pim_camrobo1](https://user-images.githubusercontent.com/59393206/106386194-256f2b00-6417-11eb-80bb-3b87ea92dddb.jpg)


ラジコンの土台となるのは、タミヤ工作シリーズの

- カムプログラムロボット工作セット
- アームクローラー工作セット

を使用します。

詳細は、[Wiki](https://github.com/kotaproj/supportPiMotor/wiki)を見てください。

## Requirement

以下のモジュールのインストールが必要です。

Pythonは3.7以上が必要。

### apt

```bash
$ sudo apt install pigpio
$ sudo service pigpiod start
$ sudo systemctl enable pigpiod.service
```
## Pythonの環境を用意する
* env名は好きな名前を用意してください

```bash
$ python3 -m venv env_torpc
$ source env_torpc/bin/activate
```

### pip

```bash
$ pip install pigpio
$ pip install smbus
$ pip install smbus2
$ pip install adafruit-circuitpython-ssd1306
$ pip install pillow==8.1.0
$ git clone https://github.com/adafruit/Adafruit_CircuitPython_SSD1306
```
