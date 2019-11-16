from rpi_ws281x import PixelStrip, Color
from typing import Tuple

LED_COUNT = 50        # Number of LED pixels.
LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def show(led: int, color: Tuple[int, int, int]):
    strip.setPixelColor(led, Color(color[1], color[0], color[2])) # Values are GRB, so switch the first two
    strip.show()

def clear():
    for i in range(strip.numPixels()): # or LED_COUNT
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
