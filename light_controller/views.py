from django.shortcuts import render

from neopixel import *
import light_utils

# set up thread to handle 
import threading
mtx = threading.Lock()
mode = "off"

def index(request):
    # start  up all of the async stuff now if its not already
    if 'light_thread' in request.session:
        request.session['light_thread'] = threading.Thread(target=light_controller)
        request.session['light_thread'].start()

    return render(request, 'light_controller/index.html')

def set_lights(request):
    with mtx:
        global mode
        mode = request.POST.get("mode")
    
# this process runs in the background on handles the lights
def light_controller(mtx):
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    # init stuff for flame setting
    flame_colors = light_utils.init_flame_arr
    flame_color_maxs = (5, 200, 35)
    flame_color_mins = (0, 50, 0)
    while True:
        current_mode = "off"
        # bool flag to stop from constantly wiping darkness on lights
        on = False
        with mtx:
            # copy mtx protected string (not sure if this is the cleanest way
            # to do this)
            current_mode = ''.join(mode)
            
        if current_mode == "off" and on:
            light_utils.colorWipe(strip, Color(0, 0, 0), 10)
        elif current_mode == "flame":
            # Flickering warm colors
            light_utils.flame(strip, flame_colors, flame_color_maxs, flame_color_mins

