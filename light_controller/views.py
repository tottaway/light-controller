from django.shortcuts import render, HttpResponse

import subprocess
import os, signal

# set up thread to handle 
def index(request):
    request.session['subprocess_pid'] = None
    return render(request, 'light_controller/index.html')

def set_lights(request):
    # TODO spawn and kill processes appropriately
    if request.session['subprocess_pid'] != None:
        os.killpg(os.getpgid(request.session['subprocess_pid']), signal.SIGTERM)

    print("runnning lights")
    p = subprocess.Popen(['python', '/home/pi/rpi_ws281x/python/examples/custom_color.py', '--flame'])
    request.session['subprocess_pid'] = p.pid

    return HttpResponse("Turned on lights")
