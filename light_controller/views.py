from django.shortcuts import render, HttpResponse
from light_controller.models import LightControllerProcess

import subprocess
import os, signal

# set up thread to handle 
def index(request):
    current_process = LightControllerProcess.objects.first()
    if current_process == None:
        current_process = LightControllerProcess()
        current_process.pid = None
        current_process.mode = "off"
        current_process.save()
    return render(request, 'light_controller/index.html', context = {"mode": current_process.mode})

def set_lights(request):
    mode = request.GET.get("mode", "off")
    current_process = LightControllerProcess.objects.select_for_update().first()

    if current_process.pid != None:
        os.kill(current_process.pid, signal.SIGINT)

    current_process.pid = None
    current_process.mode = "off"

    if mode == "flame":
        p = subprocess.Popen(['python', '/home/pi/rpi_ws281x/python/examples/custom_color.py', '--flame'])
        current_process.pid = p.pid
        current_process.mode = mode
    elif mode == "gradient":
        p = subprocess.Popen(['python', '/home/pi/rpi_ws281x/python/examples/strandtest.py'])
        current_process.pid = p.pid
        current_process.mode = mode

    current_process.save()



    return HttpResponse("Turned on lights")
