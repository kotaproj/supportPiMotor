

import time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import board
import digitalio

# OLED設定
DISP_WIDTH = 128
DISP_HEIGHT = 64
DEVICE_ADDR = 0x3C

# フォントファイル
PATH_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def main():
    # 初期化

    RESET_PIN = digitalio.DigitalInOut(board.D4)
    i2c = board.I2C()
    oled = adafruit_ssd1306.SSD1306_I2C(
        DISP_WIDTH, DISP_HEIGHT, i2c, addr=DEVICE_ADDR, reset=RESET_PIN)
    font14 = ImageFont.truetype(PATH_FONT, 14)

    # 表示クリア
    oled.fill(0)
    oled.show()

    # モノクロイメージの作成
    image = Image.new("1", (DISP_WIDTH, DISP_HEIGHT))
    draw = ImageDraw.Draw(image)

    # 1行目に"Line - 0"
    # 2行目に"Line - 1"
    # 3行目に"Lien - 2"
    # 4行目に"Lien - 3"
    for line_no in range(4):
        line = "Line - " + str(line_no)
        draw.text((0, line_no*16), line, font=font14, fill=255)

    # 描画
    oled.image(image)
    oled.show()

    # 3秒待ち
    time.sleep(3)

    # 表示クリア
    oled.fill(0)
    oled.show()


if __name__ == "__main__":
    main()
