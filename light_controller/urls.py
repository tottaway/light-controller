from django.urls import path

from . import views

app_name = 'light_controller'
urlpatterns = [
    path('', views.index, name='index'),
    path('set_lights', views.set_lights, name='set_lights'),
]
