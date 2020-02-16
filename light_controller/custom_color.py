#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
import random
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT      = 45      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def warmWheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 128:
        return Color(0, 255, (pos * 2))
    else:
        pos -= 128
        return Color(0, 255, (255 - pos * 2))

def warmCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, warmWheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

flame_colors = []
flame_color_maxs = (5, 200, 35)
flame_color_mins = (0, 50, 0)
# Define functions which animate LEDs in various ways.
def flame(strip):
    """Wipe color across display a pixel at a time."""

    iter_brightness_change = random.randint(-3, 3)
    for i in range(strip.numPixels()):
        # for some pixels change their individual brightness and color as well
        if (random.uniform(0, 1) > 0.65):
            # amount to change color
            max_color_change = 2
            # amount to change brightness
            brightness_change = 2

            color_changes = (
                random.randint(-max_color_change, max_color_change),
                random.randint(-max_color_change, max_color_change),
                random.randint(-max_color_change, max_color_change)
            )
            brightness_change = random.randint(-brightness_change, brightness_change)

            for j in range(3):
                flame_colors[i][j] += (
                        color_changes[j] +
                        brightness_change
                    )

        # apply iteration brightness change to all pixels
        for j in range(3):
            flame_colors[i][j] += iter_brightness_change

            flame_colors[i][j] = max(
                    flame_colors[i][j],
                    flame_color_mins[j]
                )
            flame_colors[i][j] = min(
                    flame_colors[i][j],
                    flame_color_maxs[j]
                )

        color = Color(
            flame_colors[i][0],
            flame_colors[i][1],
            flame_colors[i][2]
        )
        strip.setPixelColor(i, color)
        strip.show()
        #time.sleep(3/1000.0)

def init_flame_arr():
    for i in range(strip.numPixels()):
        flame_colors.append([10, 200, 30])

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-nc', '--not-clear', action='store_true', help='clear the display on exit')
    parser.add_argument('--candle', action='store_true', help='Candle type light')
    parser.add_argument('--sodium', action='store_true', help='Candle type light')
    parser.add_argument('--tn40', action='store_true', help='Tungsten 40W light')
    parser.add_argument('--tn100', action='store_true', help='Tungsten 100W light')
    parser.add_argument('--flame', action='store_true', help='Flickering warm colors')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    try:
        while True:
            if args.candle:
                colorWipe(strip, Color(31, 255, 107))  # Candle
            elif args.tn40:
                colorWipe(strip, Color(143, 255, 197))  # Tungsten 40W
            elif args.tn100:
                colorWipe(strip, Color(217, 255, 214))  # Tungsten 100W
            elif args.sodium:
                colorWipe(strip, Color(10, 255, 63))  # Sodium
            elif args.flame:
                init_flame_arr()
                flame(strip)  # Flickering warm colors
            else: 
                warmCycle(strip, wait_ms=20)

    except KeyboardInterrupt:
        if not args.not_clear:
            colorWipe(strip, Color(0,0,0), 10)
