import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=1000ee32828b278ef2cd2482446adc24'

    if request.method == 'POST':
        form = CityForm(request.POST)
        obj, created = City.objects.get_or_create(name= 'name')
        if created == 'True':
            obj.save()
            form.save()
        else:
            print("City already exists or added before")

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data,'form':form}
    return render(request, 'weather/weather.html', context)