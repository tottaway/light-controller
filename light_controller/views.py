from django.shortcuts import render, HttpResponse

import subprocess
import os, signal

# set up thread to handle 
def index(request):
    request.session['subprocess_pid'] = None
    return render(request, 'light_controller/index.html')

def set_lights(request):
    mode = request.GET.get("mode", "off")
    if request.session['subprocess_pid'] != None:
        os.kill(request.session['subprocess_pid'], signal.SIGINT)

    print("runnning lights")
    if mode == "flame":
        p = subprocess.Popen(['python', '/home/pi/rpi_ws281x/python/examples/custom_color.py', '--flame'])
        request.session['subprocess_pid'] = p.pid
    if mode == "gradient":
        p = subprocess.Popen(['python', '/home/pi/rpi_ws281x/python/examples/strandtest.py'])
        request.session['subprocess_pid'] = p.pid
    elif mode == "off":
        request.session['subprocess_pid'] = None


    return HttpResponse("Turned on lights")
