from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import requests
import json


def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=c6a543dcaf3df0a1956e82737f25ca3a'
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            form.save()
            if city_count == 0:
                r = requests.get(url.format(new_city)).json()


    form = CityForm()
    cities = City.objects.all()
    weather_info = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_info.append(weather)
    context = {'weather_info': weather_info, 'form': form}
    return render(request, 'clima/main.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')

def top3(request):
    sol = City.objects.order_by('count')[:3]
    context = {'sol': sol}
    return render(request, 'clima/top.html', context)


